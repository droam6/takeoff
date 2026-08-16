#!/usr/bin/env python3
"""
TAKEOFF backtest harness - QA only.

Runs every PDF in backtest/inbox/ through the real pipeline and scores the result.
Nothing here is customer-facing; it exists to find out where the gate and the
method break on plans we didn't choose.

    backtest/
      inbox/            drop plan PDFs here
      results/<name>/   per-plan output (rejection letter, or extraction + takeoff)
      RESULTS.md        the scoreboard
      SOURCES.md        where each PDF came from

Two depths:

  structure probe (default)   gate -> extract -> deterministic read of the sheet
                              register. Fast, free, no model. Answers "is this
                              measurable, and what rooms are in it".

  --analyse                   the above plus the real headless `claude` takeoff
                              for every set that passes the gate. Slow and
                              costed; gives real headline areas.

Usage
-----
    python3 backtest/backtest.py
    python3 backtest/backtest.py --analyse
    python3 backtest/backtest.py --analyse --only wollahra-da
    python3 backtest/backtest.py --customer angus
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import fitz  # noqa: E402
from takeoff import (  # noqa: E402
    run_intake, write_rejection, write_intake_report, extract, analyse,
    load_profile, resolve_order_settings, write_profile_report,
    _dimension_tokens, _sheet_title,
)

HERE = Path(__file__).resolve().parent
INBOX = HERE / "inbox"
RESULTS = HERE / "results"

ROOM_WORDS = [
    "bath", "ensuite", "powder", "laundry", "kitchen", "wc", "toilet",
    "shower", "butler", "pantry", "mudroom", "wet area",
]
PLAN_RE = re.compile(r"(FLOOR|CEILING|SETOUT|TILE)\s+PLAN\b", re.I)
ELEV_RE = re.compile(r"\bELEVATIONS?\b", re.I)
SECT_RE = re.compile(r"\bSECTIONS?\b", re.I)
SCALE_RE = re.compile(r"1\s*:\s*(\d+)")


# --------------------------------------------------------------------------
# Deterministic structure probe - no model involved
# --------------------------------------------------------------------------

def probe(pdf: Path) -> dict:
    """Read the set's structure: rooms, sheet mix, scales, dimension density.

    This is the cheap question the gate can't answer on its own: the gate says
    "there are plans and there are elevations"; the probe says "are they for the
    SAME room", which is what decides whether a wall area can be measured at all.
    """
    doc = fitz.open(pdf)
    sheets, scales = [], set()
    for i, page in enumerate(doc):
        text = page.get_text() or ""
        title = _sheet_title(text)
        sheets.append({
            "page": i + 1,
            "title": title,
            "dims": len(_dimension_tokens(text)),
            "is_plan": bool(PLAN_RE.search(title)),
            "is_elev": bool(ELEV_RE.search(title)),
            "is_sect": bool(SECT_RE.search(title)),
        })
        for m in SCALE_RE.finditer(text):
            scales.add(f"1:{m.group(1)}")
    doc.close()

    def room_of(title: str) -> str | None:
        t = title.lower()
        for w in ROOM_WORDS:
            if w in t:
                return re.sub(r"\s+(floor plan|elevations?|3d|sections?)\s*$", "",
                              title, flags=re.I).strip().title()
        return None

    rooms: dict[str, dict] = {}
    for sh in sheets:
        r = room_of(sh["title"])
        if not r:
            continue
        e = rooms.setdefault(r, {"plan": 0, "elev": 0, "dims": 0})
        e["plan"] += sh["is_plan"]
        e["elev"] += sh["is_elev"]
        e["dims"] += sh["dims"]

    measurable = {r: v for r, v in rooms.items() if v["plan"] and v["elev"]}
    floors_only = {r: v for r, v in rooms.items() if v["plan"] and not v["elev"]}

    return {
        "pages": len(sheets),
        "sheets": sheets,
        "scales": sorted(scales),
        "plan_sheets": sum(s["is_plan"] for s in sheets),
        "elev_sheets": sum(s["is_elev"] for s in sheets),
        "sect_sheets": sum(s["is_sect"] for s in sheets),
        "total_dims": sum(s["dims"] for s in sheets),
        "wet_rooms": rooms,
        "measurable_rooms": measurable,
        "floors_only_rooms": floors_only,
    }


def probe_flags(pr: dict, checks) -> list[str]:
    """Things a human reviewer should look at. Not failures - suspicions."""
    f = []
    if len(pr["scales"]) > 1:
        f.append(f"mixed scales in one set ({', '.join(pr['scales'])}) - scaling risk")
    if not pr["scales"]:
        f.append("no scale printed on any sheet")
    if pr["plan_sheets"] and not pr["elev_sheets"]:
        f.append("plans but no elevations - floors only, no wall areas")
    if pr["elev_sheets"] and not pr["plan_sheets"]:
        f.append("elevations but no floor plan - no floor areas")
    if pr["floors_only_rooms"]:
        f.append("wet rooms with a plan but no elevations: "
                 + ", ".join(sorted(pr["floors_only_rooms"])))
    if not pr["wet_rooms"]:
        f.append("no wet areas identified by sheet title")
    if pr["pages"] and pr["total_dims"] / pr["pages"] < 10:
        f.append(f"thin dimensioning ({pr['total_dims'] / pr['pages']:.0f} tokens/page)")
    if pr["sect_sheets"] == 0:
        f.append("no sections - raked ceilings could not be resolved")
    warn = [c for c in checks if not c.ok and not c.hard]
    for c in warn:
        f.append(f"gate warning: {c.detail}")
    return f


# --------------------------------------------------------------------------

def headline_areas(takeoff_md: Path | None) -> str:
    """Pull the ORDER THIS figures out of a produced takeoff, if there is one."""
    if not takeoff_md or not takeoff_md.exists():
        return "—"
    txt = takeoff_md.read_text(encoding="utf-8", errors="replace")
    out = []
    for label in ("Floor tiles", "Wall tiles"):
        m = re.search(rf"{label}\s*[.\s]*([\d,]+\.?\d*)\s*m", txt)
        if m:
            out.append(f"{label.split()[0].lower()} {m.group(1)} m²")
    return " / ".join(out) if out else "produced, not parsed"


def run_one(pdf: Path, args) -> dict:
    name = re.sub(r"[^A-Za-z0-9_-]+", "_", pdf.stem)[:60]
    out_dir = RESULTS / name
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    row = {"file": pdf.name, "name": name, "size_mb": round(pdf.stat().st_size / 1e6, 1)}
    t0 = time.time()

    try:
        checks, facts = run_intake(pdf, want_walls=True)
    except Exception as exc:  # a PDF so broken the gate itself throws
        row.update(intake="ERROR", why=f"gate crashed: {exc}", pages="?",
                   rooms="—", areas="—", flags=["harness caught an exception"],
                   runtime=round(time.time() - t0, 1))
        (out_dir / "ERROR.txt").write_text(traceback.format_exc())
        return row

    row["pages"] = facts.get("pages", "?")
    write_intake_report(out_dir, name, pdf, checks, facts,
                        {"trade": "tiler", "rooms": "all wet areas", "wastage": "10"})

    hard_fails = [c for c in checks if not c.ok and c.hard]
    if hard_fails:
        # Fail politely, and keep the letter we would actually send.
        write_rejection(out_dir, name, pdf, checks, facts,
                        {"trade": "tiler", "rooms": None, "wastage": None})
        row.update(
            intake="FAIL",
            why="; ".join(c.detail for c in hard_fails),
            rooms="—", areas="—",
            flags=[f"rejected: {c.key}" for c in hard_fails],
            runtime=round(time.time() - t0, 1),
        )
        return row

    pr = probe(pdf)
    (out_dir / "probe.json").write_text(json.dumps(pr, indent=2))

    extract(pdf, out_dir, dpi=args.dpi)
    prof = load_profile(args.customer, ROOT)
    settings = resolve_order_settings(prof, {"trade": "tiler"})
    write_profile_report(out_dir, prof, {"trade": "tiler"}, settings)

    takeoff_md = None
    if args.analyse:
        for src, dst in (("TAKEOFF_METHOD.md", "METHOD.md"), ("SPEC.md", "SPEC.md"),
                         ("INTAKE.md", "INTAKE.md"),
                         ("PROFILE_QUESTIONS.md", "PROFILE_QUESTIONS.md")):
            if (ROOT / src).exists():
                shutil.copyfile(ROOT / src, out_dir / dst)
        takeoff_md = analyse(out_dir, name,
                             {"trade": "tiler", "rooms": "all wet areas",
                              "wastage": None, "tile_size": None,
                              "m2_per_box": None, "lay_pattern": None},
                             prof, settings, timeout=args.timeout)

    rooms = sorted(pr["measurable_rooms"]) or sorted(pr["wet_rooms"])
    row.update(
        intake="PASS",
        why=f"{pr['plan_sheets']} plan / {pr['elev_sheets']} elev sheets, "
            f"{pr['total_dims']} dim tokens",
        rooms=", ".join(rooms) if rooms else "none identified",
        n_measurable=len(pr["measurable_rooms"]),
        areas=headline_areas(takeoff_md),
        flags=probe_flags(pr, checks),
        scales=pr["scales"],
        runtime=round(time.time() - t0, 1),
    )
    return row


# --------------------------------------------------------------------------

def write_scoreboard(rows: list[dict], args) -> Path:
    out = HERE / "RESULTS.md"
    passed = [r for r in rows if r["intake"] == "PASS"]
    failed = [r for r in rows if r["intake"] == "FAIL"]
    errored = [r for r in rows if r["intake"] == "ERROR"]

    L = ["# Backtest scoreboard", "",
         f"**Run:** {_dt.date.today().isoformat()} · "
         f"**Depth:** {'full pipeline (gate + extract + model takeoff)' if args.analyse else 'structure probe (gate + extract, no model)'} · "
         f"**Plans:** {len(rows)}", "",
         f"**{len(passed)} passed the gate · {len(failed)} rejected · {len(errored)} errored**", "",
         "| File | Pages | Intake | Why | Rooms found | Headline areas | Flags | Runtime |",
         "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        flags = r.get("flags") or []
        fl = "<br>".join(f"⚠️ {x}" for x in flags) if flags else "—"
        mark = {"PASS": "✅ PASS", "FAIL": "🛑 FAIL", "ERROR": "💥 ERROR"}[r["intake"]]
        L.append(f"| `{r['file']}` | {r.get('pages','?')} | {mark} | {r.get('why','')} | "
                 f"{r.get('rooms','—')} | {r.get('areas','—')} | {fl} | {r.get('runtime','?')}s |")

    L += ["", "---", "", "## Rejections in full", ""]
    if not failed:
        L.append("_None._")
    for r in failed:
        letter = RESULTS / r["name"] / f"REJECTED_{r['name']}.md"
        L += [f"### `{r['file']}`", "",
              f"**Gate said:** {r['why']}", ""]
        if letter.exists():
            body = letter.read_text(encoding="utf-8")
            blocking = body.split("## What's blocking it")[-1].split("## What's already fine")[0]
            L += ["The letter we would actually send:", "",
                  "```", blocking.strip()[:1800], "```", ""]

    L += ["", "## Per-plan detail", ""]
    for r in passed:
        L += [f"### `{r['file']}`", "",
              f"- Sheets: {r.get('why')}",
              f"- Scales: {', '.join(r.get('scales') or []) or 'none printed'}",
              f"- Wet rooms with plan **and** elevations: **{r.get('n_measurable', 0)}**",
              f"- Rooms: {r.get('rooms')}",
              f"- Headline: {r.get('areas')}"]
        for x in (r.get("flags") or []):
            L.append(f"- ⚠️ {x}")
        L.append("")

    out.write_text("\n".join(L), encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="TAKEOFF backtest harness (QA only)")
    ap.add_argument("--analyse", action="store_true",
                    help="also run the real headless takeoff on every set that passes")
    ap.add_argument("--only", help="substring filter on the filename")
    ap.add_argument("--customer", default="angus")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--timeout", type=int, default=5400)
    a = ap.parse_args(argv)

    INBOX.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(p for p in INBOX.glob("*.pdf"))
    if a.only:
        pdfs = [p for p in pdfs if a.only.lower() in p.name.lower()]
    if not pdfs:
        print(f"No PDFs in {INBOX}")
        return 2

    print(f"BACKTEST  |  {len(pdfs)} plan set(s)  |  "
          f"{'full pipeline' if a.analyse else 'structure probe'}\n")
    rows = []
    for pdf in pdfs:
        print(f"── {pdf.name}")
        row = run_one(pdf, a)
        rows.append(row)
        print(f"   {row['intake']}  {row.get('why','')[:90]}")
        for x in (row.get("flags") or [])[:4]:
            print(f"   ⚠️  {x}")
        print(f"   {row.get('runtime')}s\n")

    out = write_scoreboard(rows, a)
    ok = sum(r["intake"] == "PASS" for r in rows)
    print(f"{ok}/{len(rows)} passed the gate.  Scoreboard: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
