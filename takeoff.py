#!/usr/bin/env python3
"""
TAKEOFF v1 - AI plan-measurement for tradies.

Pipeline
--------
    1. INTAKE GATE   deterministic checks on the PDF, run BEFORE any analysis.
                     FAIL -> write REJECTED_<job>.md and stop. We never guess off
                     bad inputs.
    2. EXTRACT       render every page to PNG + pull the text layer with coordinates
                     (PyMuPDF). Deterministic. No model involved.
    3. ANALYSE       invoke the `claude` CLI headless inside the job folder, against
                     TAKEOFF_METHOD.md, to produce TAKEOFF_<job>.md.

Requires: PyMuPDF (pip install pymupdf) and, for step 3, Claude Code on PATH.

Usage
-----
    python takeoff.py plans.pdf
    python takeoff.py plans.pdf --job smith-reno --trade tiler \
        --rooms "main bath, ensuite" --wastage 10
    python takeoff.py plans.pdf --intake-only
    python takeoff.py plans.pdf --no-analyse
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    sys.exit("PyMuPDF is required.  pip install pymupdf")


# --------------------------------------------------------------------------
# Intake gate  (see INTAKE.md section C)
# --------------------------------------------------------------------------

MIN_TOTAL_CHARS = 200      # check 1  text layer exists at all
MIN_CHARS_PER_PAGE = 20    # check 2  text density
MIN_DIM_TOKENS = 30        # check 3  printed mm dimensions
MIN_TOKENS_FOR_DIM_PAGE = 8
MIN_DIM_PAGES = 1          # check 4  at least one properly dimensioned sheet
MAX_PAGES = 300            # check 7

DIM_RE = re.compile(r"\b(\d{2,5})\b")
PLAN_RE = re.compile(r"\bPLAN\b", re.I)
ELEV_RE = re.compile(r"\bELEVATION", re.I)


class Check:
    """One intake check: a verdict plus the plain-English fix."""

    def __init__(self, key, ok, hard, detail, means="", send=""):
        self.key, self.ok, self.hard = key, ok, hard
        self.detail, self.means, self.send = detail, means, send

    @property
    def status(self):
        return "PASS" if self.ok else ("FAIL" if self.hard else "WARN")


def _dimension_tokens(text: str) -> list[int]:
    """Integers that look like millimetre dimensions on an architectural sheet."""
    out = []
    for tok in DIM_RE.findall(text):
        val = int(tok)
        if 20 <= val <= 20000:
            out.append(val)
    return out


# Ordered most- to least-diagnostic of a sheet name. A sheet is named for the
# drawing it holds, so those keywords beat words that merely appear in annotations.
TITLE_PATTERNS = [
    re.compile(p, re.I) for p in (
        r"(FLOOR|CEILING|SETOUT|TILE)\s+PLAN\b",
        r"\bELEVATIONS?\b",
        r"\bSECTIONS?\b",
        r"\b3D\b",
        r"\bRCP\b",
        r"\bSCHEDULE\b",
    )
]
TITLE_HINT = re.compile("|".join(p.pattern for p in TITLE_PATTERNS), re.I)


def _sheet_title(text: str) -> str:
    """Sheet title from the title block.

    Architectural title blocks put the sheet name on its own line, so prefer the
    shortest all-caps line that carries a drawing-type keyword (FLOOR PLAN,
    ELEVATIONS, 3D...). Falls back to the longest all-caps line only if nothing
    matches, which keeps busy annotation text out of the register.
    """
    caps = [ln.strip() for ln in text.split("\n")
            if 3 <= len(ln.strip()) <= 60
            and ln.strip() == ln.strip().upper()
            and any(c.isalpha() for c in ln)]
    for pat in TITLE_PATTERNS:
        hits = [ln for ln in caps if pat.search(ln)]
        if hits:
            # shortest hit == the bare sheet name, not a sentence that mentions it
            return min(hits, key=len)
    return max(caps, key=len) if caps else ""


def run_intake(pdf_path: Path, want_walls: bool = True) -> tuple[list[Check], dict]:
    """Deterministic gate. Returns (checks, facts). Runs before any analysis."""
    checks: list[Check] = []
    facts: dict = {}

    try:
        doc = fitz.open(pdf_path)
    except Exception as exc:
        checks.append(Check(
            "readable", False, True, f"PDF could not be opened: {exc}",
            "The file is corrupt, or isn't a PDF.",
            "Re-export the drawing set as a PDF and send it again."))
        return checks, facts

    # check 8 - encryption
    encrypted = bool(doc.is_encrypted and doc.needs_pass)
    checks.append(Check(
        "encryption", not encrypted, True,
        "PDF is password-protected against extraction" if encrypted
        else "PDF is not locked",
        "A locked PDF blocks us from reading the dimension text.",
        "Send an unlocked copy, or the password."))

    # check 7 - page count
    n = doc.page_count
    facts["pages"] = n
    checks.append(Check(
        "page_count", 1 <= n <= MAX_PAGES, True,
        f"{n} page(s)",
        "The file is empty or implausibly large.",
        "Send the drawing set as a single PDF of the relevant sheets."))

    per_page = []
    for i, page in enumerate(doc):
        text = page.get_text() or ""
        toks = _dimension_tokens(text)
        title = _sheet_title(text)
        per_page.append({
            "page": i + 1, "chars": len(text.strip()),
            "dims": len(toks), "title": title,
        })

    facts["per_page"] = per_page
    total_chars = sum(p["chars"] for p in per_page)
    total_dims = sum(p["dims"] for p in per_page)
    dim_pages = [p for p in per_page if p["dims"] >= MIN_TOKENS_FOR_DIM_PAGE]
    plan_pages = [p for p in per_page if PLAN_RE.search(p["title"])]
    elev_pages = [p for p in per_page if ELEV_RE.search(p["title"])]

    facts.update(total_chars=total_chars, total_dims=total_dims,
                 dim_pages=len(dim_pages), plan_pages=len(plan_pages),
                 elev_pages=len(elev_pages))

    # check 1 - text layer
    checks.append(Check(
        "text_layer", total_chars >= MIN_TOTAL_CHARS, True,
        f"{total_chars} extractable characters (need {MIN_TOTAL_CHARS})",
        "The file is a scan or photo, so the dimensions are pixels rather than "
        "numbers we can read. We won't OCR them and we won't scale off the drawing.",
        "Ask your designer to re-export the PDF straight out of their drawing "
        "software - not printed and scanned."))

    # check 2 - density
    density = total_chars / max(n, 1)
    checks.append(Check(
        "text_density", density >= MIN_CHARS_PER_PAGE, True,
        f"{density:.0f} characters per page (need {MIN_CHARS_PER_PAGE})",
        "Most pages carry no readable text - likely images with a text title block.",
        "Re-export the full set as vector PDF from the drawing software."))

    # check 3 - dimension tokens
    checks.append(Check(
        "dimension_tokens", total_dims >= MIN_DIM_TOKENS, True,
        f"{total_dims} mm dimension tokens found (need {MIN_DIM_TOKENS})",
        "We can read text but can't find printed millimetre dimensions. We measure "
        "from stated dimensions only - we never scale off the drawing.",
        "Send drawings with the dimension strings printed on them, in mm."))

    # check 4 - properly dimensioned sheets
    checks.append(Check(
        "dimensioned_pages", len(dim_pages) >= MIN_DIM_PAGES, True,
        f"{len(dim_pages)} sheet(s) carry a real dimension chain",
        "The set looks like cover sheets, 3D views or renders only.",
        "Include the dimensioned floor plans and elevations."))

    # check 5 - plan sheets
    checks.append(Check(
        "plan_pages", len(plan_pages) >= 1, True,
        f"{len(plan_pages)} floor plan sheet(s) detected",
        "Without a floor plan we cannot measure floor area.",
        "Include the floor plan sheet for every room you want quoted."))

    # check 6 - elevations (hard only if walls are in scope)
    checks.append(Check(
        "elevation_pages", len(elev_pages) >= 1, want_walls,
        f"{len(elev_pages)} elevation sheet(s) detected",
        "Wall tiling heights only appear on elevations. Without them we can give you "
        "floor area only.",
        "Include the elevation sheets for each room you want wall areas on."))

    doc.close()
    return checks, facts


def write_rejection(job_dir: Path, job: str, pdf: Path,
                    checks: list[Check], facts: dict, answers: dict) -> Path:
    """Polite, specific rejection: what's missing and what to send instead."""
    failed = [c for c in checks if not c.ok and c.hard]
    warned = [c for c in checks if not c.ok and not c.hard]
    passed = [c for c in checks if c.ok]
    out = job_dir / f"REJECTED_{job}.md"
    today = _dt.date.today().isoformat()

    L = [f"# Can't measure this set yet - {job}", "",
         f"**File:** `{pdf.name}`  |  **Checked:** {today}  |  "
         f"**Pages:** {facts.get('pages', '?')}", "",
         "Thanks for sending this through. I can't measure it accurately yet, and I'd "
         "rather tell you that than send you numbers you can't trust.", "",
         "Here's exactly what's blocking it, and what to send instead.", "",
         "---", "", "## What's blocking it", ""]

    for c in failed:
        L += [f"### ✗ {c.detail}", "",
              f"**What this means:** {c.means}", "",
              f"**What to send:** {c.send}", ""]

    if warned:
        L += ["## Worth knowing (not blocking)", ""]
        for c in warned:
            L += [f"- **{c.detail}** — {c.means} {c.send}", ""]

    if passed:
        L += ["## What's already fine", ""]
        L += [f"- {c.detail}" for c in passed]
        L += [""]

    L += ["---", "", "## The short version", "",
          "Send those items through and I'll have your numbers back same day.",
          "",
          "Everything I need is listed in `INTAKE.md`, but the two that matter most:",
          "",
          "1. A **vector PDF** exported from the drawing software (not a scan or photo) —",
          "   you can check by trying to select a dimension number with your mouse.",
          "2. **Printed dimensions in mm**, plus the **elevation sheets** if you want wall",
          "   areas as well as floors.", ""]

    if any(v in (None, "") for v in answers.values()):
        L += ["## And three quick questions", ""]
        if not answers.get("trade"):
            L.append("- What's your trade? (tiler / painter / waterproofer / other)")
        if not answers.get("rooms"):
            L.append("- Which rooms and which surfaces do you want quoted?")
        if not answers.get("wastage"):
            L.append("- Wastage preference? (none / 10% / 15% / your own number)")
        L.append("")

    L += ["---", "", "*We measure from stated dimensions only. We never scale off the "
          "drawing, and we never guess off a bad input — that's the whole point.*", ""]

    out.write_text("\n".join(L), encoding="utf-8")
    return out


# --------------------------------------------------------------------------
# Extraction  (deterministic - no model involved)
# --------------------------------------------------------------------------

def extract(pdf_path: Path, job_dir: Path, dpi: int = 150) -> dict:
    """Render pages to PNG and dump the text layer, plain and with coordinates."""
    pages_dir = job_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    mat = fitz.Matrix(dpi / 72, dpi / 72)

    plain, coords, register = [], [], []
    for i, page in enumerate(doc):
        num = i + 1
        page.get_pixmap(matrix=mat).save(pages_dir / f"page_{num:02d}.png")

        text = page.get_text() or ""
        plain.append(f"===== PAGE {num} =====\n{text}")

        coords.append(f"===== PAGE {num} =====")
        for blk in page.get_text("dict")["blocks"]:
            for line in blk.get("lines", []):
                d = line.get("dir", (1, 0))
                s = "".join(sp["text"] for sp in line.get("spans", [])).strip()
                if s:
                    x, y = line["bbox"][0], line["bbox"][1]
                    coords.append(f"{x:7.1f} {y:7.1f}  dir=({d[0]:.0f},{d[1]:.0f})  {s}")

        register.append({
            "page": num,
            "title": _sheet_title(text),
            "scale": (re.search(r"1\s*:\s*\d+\s*@?\s*A\d", text) or [None])
                     and (re.search(r"1\s*:\s*\d+\s*@?\s*A\d", text).group(0)
                          if re.search(r"1\s*:\s*\d+\s*@?\s*A\d", text) else ""),
            "dims": len(_dimension_tokens(text)),
        })

    (job_dir / "all_text.txt").write_text("\n".join(plain), encoding="utf-8")
    (job_dir / "text_coords.txt").write_text("\n".join(coords), encoding="utf-8")

    reg = ["# Sheet register", "", "| Page | Sheet title | Scale | Dim tokens |",
           "|---|---|---|---|"]
    for r in register:
        reg.append(f"| {r['page']} | {r['title']} | {r['scale'] or ''} | {r['dims']} |")
    (job_dir / "sheet_register.md").write_text("\n".join(reg), encoding="utf-8")

    doc.close()
    return {"pages": len(register), "register": register}


# --------------------------------------------------------------------------
# Analysis  (claude CLI, headless)
# --------------------------------------------------------------------------

def resolve_claude() -> str | None:
    """Find the claude binary. Honours CLAUDE_CLI if set."""
    return os.environ.get("CLAUDE_CLI") or shutil.which("claude")


def build_command(binary: str, prompt: str) -> list[str]:
    """Wrap .cmd/.bat shims through cmd.exe on Windows; otherwise invoke directly."""
    args = ["-p", prompt, "--dangerously-skip-permissions"]
    if os.name == "nt" and binary.lower().endswith((".cmd", ".bat")):
        return ["cmd.exe", "/c", binary, *args]
    return [binary, *args]


INSTRUCTION = """\
You are performing a professional quantity takeoff for a tradie. Accuracy is the product.

Read METHOD.md in this folder and follow it exactly, in order. It is the protocol; do not
improvise around it.

Inputs in this folder:
  - METHOD.md          the analysis protocol you must follow
  - SPEC.md            what the output must contain
  - INTAKE.md          the intake requirements (already passed) and the answers given
  - intake_report.md   the intake result and the tradie's answers
  - sheet_register.md  page -> sheet title -> scale
  - all_text.txt       full text layer, per page
  - text_coords.txt    every text run with x/y coordinates and rotation
  - pages/*.png        one rendered image per page - LOOK AT THESE

Job details:
  Job name : {job}
  Trade    : {trade}
  Rooms    : {rooms}
  Wastage  : {wastage}

Method reminders that matter most:
  - Measure from STATED dimensions only. Never scale off the drawing.
  - Rooms are rarely rectangles. Decompose the floor into bands. Never use
    overall_width x overall_depth unless you have proved the room is rectangular.
  - Use TRUE tiling heights from the elevations, never an assumed ceiling height.
  - Run every check in METHOD.md section 5 and print the pass/fail log.
  - Give every room a confidence rating (HIGH / MED / LOW) per METHOD.md section 6.
  - Never silently assume. Every inferred number becomes a numbered question.
  - Lead the document with QUESTIONS FOR YOU. Always.

Write your result to TAKEOFF_{job}.md in this folder, in the order given by SPEC.md
section 3, and end with the CONFIRM BEFORE QUOTING checklist.
"""


def analyse(job_dir: Path, job: str, answers: dict, timeout: int = 3600) -> Path | None:
    binary = resolve_claude()
    if not binary:
        print("  ! claude CLI not found on PATH - skipping analysis.")
        print("    Install Claude Code, or set CLAUDE_CLI to the binary path.")
        return None

    prompt = INSTRUCTION.format(
        job=job,
        trade=answers.get("trade") or "not supplied - ask in QUESTIONS FOR YOU",
        rooms=answers.get("rooms") or "not supplied - ask in QUESTIONS FOR YOU",
        wastage=answers.get("wastage") or "not supplied - show measured, +10% and +15%",
    )
    cmd = build_command(binary, prompt)
    print(f"  > {binary} -p <instruction> --dangerously-skip-permissions")
    print(f"    cwd = {job_dir}")

    try:
        proc = subprocess.run(cmd, cwd=str(job_dir), timeout=timeout,
                              capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        print(f"  ! analysis timed out after {timeout}s")
        return None
    except OSError as exc:
        print(f"  ! could not launch claude: {exc}")
        return None

    if proc.returncode != 0:
        print(f"  ! claude exited {proc.returncode}")
        if proc.stderr:
            print("   ", proc.stderr.strip()[:2000])
        return None

    (job_dir / "claude_stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    out = job_dir / f"TAKEOFF_{job}.md"
    if out.exists():
        return out
    # The model answered on stdout instead of writing the file - keep it anyway.
    if proc.stdout and proc.stdout.strip():
        out.write_text(proc.stdout, encoding="utf-8")
        return out
    return None


# --------------------------------------------------------------------------

def write_intake_report(job_dir: Path, job: str, pdf: Path,
                        checks: list[Check], facts: dict, answers: dict) -> Path:
    out = job_dir / "intake_report.md"
    L = [f"# Intake report - {job}", "",
         f"**File:** `{pdf.name}`  |  **Pages:** {facts.get('pages','?')}  |  "
         f"**Checked:** {_dt.date.today().isoformat()}", "",
         "| Check | Result | Detail |", "|---|---|---|"]
    for c in checks:
        L.append(f"| {c.key} | {c.status} | {c.detail} |")
    L += ["", "## Answers from the tradie", "",
          f"- **Trade:** {answers.get('trade') or '_not supplied - ask_'}",
          f"- **Rooms / surfaces:** {answers.get('rooms') or '_not supplied - ask_'}",
          f"- **Wastage:** {answers.get('wastage') or '_not supplied - show all_'}", ""]
    out.write_text("\n".join(L), encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="TAKEOFF v1 - AI plan measurement")
    ap.add_argument("pdf", type=Path, help="path to the plan set PDF")
    ap.add_argument("--job", help="job name (default: PDF stem)")
    ap.add_argument("--outdir", type=Path, default=Path("jobs"))
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--trade", help="tiler / painter / waterproofer / other")
    ap.add_argument("--rooms", help="which rooms and surfaces to quote")
    ap.add_argument("--wastage", help="none / 10 / 15 / your own number")
    ap.add_argument("--no-walls", action="store_true",
                    help="floors only - elevations become a warning, not a failure")
    ap.add_argument("--intake-only", action="store_true", help="run the gate and stop")
    ap.add_argument("--no-analyse", action="store_true", help="extract but don't call claude")
    ap.add_argument("--timeout", type=int, default=3600)
    a = ap.parse_args(argv)

    if not a.pdf.exists():
        print(f"error: {a.pdf} not found")
        return 2

    job = a.job or re.sub(r"[^A-Za-z0-9_-]+", "_", a.pdf.stem)
    job_dir = (a.outdir / job).resolve()
    job_dir.mkdir(parents=True, exist_ok=True)
    answers = {"trade": a.trade, "rooms": a.rooms, "wastage": a.wastage}

    print(f"TAKEOFF v1  |  job '{job}'  |  {job_dir}")

    # ---- 1. INTAKE GATE - always first, before any analysis -----------------
    print("[1/3] intake gate")
    checks, facts = run_intake(a.pdf, want_walls=not a.no_walls)
    for c in checks:
        print(f"      {c.status:4}  {c.key:20} {c.detail}")

    write_intake_report(job_dir, job, a.pdf, checks, facts, answers)

    if any(not c.ok and c.hard for c in checks):
        path = write_rejection(job_dir, job, a.pdf, checks, facts, answers)
        print(f"\nINTAKE FAILED - no analysis run.\nWrote {path}")
        print("We never guess off bad inputs.")
        return 1

    print("      -> PASS")
    if a.intake_only:
        return 0

    # ---- 2. EXTRACT ---------------------------------------------------------
    print("[2/3] extracting pages + dimension text")
    info = extract(a.pdf, job_dir, dpi=a.dpi)
    print(f"      {info['pages']} pages rendered @ {a.dpi} dpi")

    for name in ("TAKEOFF_METHOD.md", "SPEC.md", "INTAKE.md"):
        src = Path(__file__).resolve().parent / name
        if src.exists():
            dst = job_dir / ("METHOD.md" if name == "TAKEOFF_METHOD.md" else name)
            shutil.copyfile(src, dst)

    if a.no_analyse:
        print("      (--no-analyse) stopping after extraction")
        return 0

    # ---- 3. ANALYSE ---------------------------------------------------------
    print("[3/3] analysis via claude CLI")
    out = analyse(job_dir, job, answers, timeout=a.timeout)
    if out:
        print(f"\nDone. {out}")
        return 0
    print("\nExtraction complete, analysis did not produce a file.")
    print(f"Everything the analysis needs is in {job_dir}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
