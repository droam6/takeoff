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

The customer profile (--customer) affects the ORDER only. Measured areas are the
plans' truth and are identical for every customer - see TAKEOFF_METHOD.md 7.7.

Requires: PyMuPDF (pip install pymupdf) and, for step 3, Claude Code on PATH.

Usage
-----
    python takeoff.py plans.pdf
    python takeoff.py plans.pdf --job smith-reno --trade tiler \
        --rooms "main bath, ensuite" --wastage 10
    python takeoff.py plans.pdf --customer angus \
        --lay-pattern herringbone --tile-size "600x600 porcelain" --m2-per-box 1.44
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

class Check:
    """One intake check: a verdict, and the plain-English fix."""

    def __init__(self, key, ok, hard, detail, means="", send=""):
        self.key, self.ok, self.hard = key, ok, hard
        self.detail, self.means, self.send = detail, means, send

    @property
    def status(self):
        return "PASS" if self.ok else ("FAIL" if self.hard else "WARN")


DIM_RE = re.compile(r"\b(\d{2,5})\b")
PLAN_RE = re.compile(r"\bPLAN\b", re.I)
ELEV_RE = re.compile(r"\bELEVATION", re.I)

# --------------------------------------------------------------------------
# Readability - is this a text layer, or OCR spray dressed up as one?
#
# The gate used to ask "is there text" and "are there integers". An OCR'd scan
# satisfies both with noise. These checks ask whether the text can actually be
# READ, which is the premise everything downstream stands on.
# --------------------------------------------------------------------------

# Words that appear on real architectural sheets, plus enough plain English to
# score a notes block. Deliberately small and embedded: a system dictionary
# would make the gate's verdict depend on which machine it ran on.
VOCAB = set("""
plan plans elevation elevations section sections detail details drawing drawings sheet
floor ground first upper lower roof site slab setout ceiling wall walls door doors window
windows schedule legend notes note scale rev revision date drawn checked project client
address lot number title north level levels existing proposed demolition new area areas
bathroom bath ensuite powder laundry kitchen pantry living dining bedroom robe garage
porch deck balcony stair stairs hall entry study office toilet shower vanity basin sink
bench tiles tile tiled tiling render rendered paint painted finish finishes
timber steel concrete brick brickwork glass glazing frame framed frames stud studs
insulation waterproof waterproofing membrane fall falls waste screed hob niche
skirting joinery cabinet cabinets cupboard drawer drawers shelf shelves splashback
mirror tapware taps spout rail hooks holder seat screen alcove surround
all any and are for from has have its may must not the this that with use used using
unless otherwise dimensions dimension high wide deep long height width depth length
overall internal external face faces centre center line lines above below between
construction building builder architect designer copyright property permission
verify verified confirm confirmed works work prior commencing commencement
""".split())

CLEAN_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                  " .,-:;/()&%'\"#@+=\n\t")
WORD_RE = re.compile(r"[A-Za-z]{3,}")


def text_quality(text: str) -> tuple[float, float]:
    """(clean_ratio, word_hit_rate).

    clean_ratio - share of characters that belong on a drawing sheet at all.
                  OCR of line-work sprays glyphs the sheet never contained.
    word_hit    - share of alphabetic tokens that are real words.
    """
    if not text.strip():
        return 0.0, 0.0
    body = text.strip()
    clean = sum(1 for c in body if c in CLEAN_CHARS) / len(body)
    words = WORD_RE.findall(body)
    hit = (sum(1 for w in words if w.lower() in VOCAB) / len(words)) if words else 0.0
    return clean, hit


def _dimension_tokens(text: str) -> list:
    """Millimetre-looking integers in a block of text."""
    return [int(t) for t in DIM_RE.findall(text) if 20 <= int(t) <= 20000]


def _dim_tokens_xy(page):
    """Dimension tokens with position and orientation. (value, x, y, vertical)"""
    out = []
    for blk in page.get_text("dict")["blocks"]:
        for line in blk.get("lines", []):
            d = line.get("dir", (1, 0))
            vertical = abs(d[1]) > abs(d[0])
            s = "".join(sp["text"] for sp in line.get("spans", [])).strip()
            x, y = line["bbox"][0], line["bbox"][1]
            for tok in DIM_RE.findall(s):
                v = int(tok)
                if 20 <= v <= 20000:
                    out.append((v, x, y, vertical))
    return out


def verify_chains(tokens, tol: int = 5, min_total: int = 400) -> int:
    """Count dimension chains that actually check out.

    A chain is a run of two or more labels lying along one line whose values sum
    to another printed value within `tol` mm - "100 + 840 + 790 = 1730". Real
    drawings are full of these, because that is how a chain is dimensioned.
    OCR noise is not: random integers do not sum to other random integers on the
    same axis within 5 mm except by accident.

    This is the one check OCR cannot fake, so it is the one that decides whether
    the text layer is trustworthy.
    """
    if len(tokens) < 3:
        return 0
    totals = {v for v, _, _, _ in tokens}
    verified, seen = 0, set()

    for vertical in (False, True):
        group = [t for t in tokens if t[3] == vertical]
        buckets = {}
        for v, x, y, _ in group:
            key = round((x if vertical else y) / 6.0)
            buckets.setdefault(key, []).append((v, y if vertical else x))
        for key, members in buckets.items():
            if len(members) < 2:
                continue
            members.sort(key=lambda m: m[1])
            vals = [m[0] for m in members]
            n = len(vals)
            for i in range(n):
                run = 0
                for j in range(i, min(n, i + 8)):
                    run += vals[j]
                    if j == i or run < min_total:
                        continue
                    for t in totals:
                        if abs(t - run) <= tol and t not in vals[i:j + 1]:
                            sig = (vertical, key, i, j)
                            if sig not in seen:
                                seen.add(sig)
                                verified += 1
                            break
    return verified


# --------------------------------------------------------------------------
# Sheet titles - from the title block, with a sheet number beside them
# --------------------------------------------------------------------------

TITLE_KW = re.compile(
    r"(floor\s*plan|ceiling\s*plan|setout\s*plan|tile\s*plan|site\s*plan|roof\s*plan"
    r"|elevations?\b|elev\.|sections?\b|\b3d\b|\brcp\b|demolition\s*plan"
    r"|landscape\s*plan|schedule|cover\s*sheet)", re.I)

# Mentions drawing words but is never a sheet name.
BOILER_RE = re.compile(
    r"(copyright|property of|no liability|accepts no|permission|must not be|may not be"
    r"|shall be|should be|in accordance|australian standard|\bAS ?\d{3,}|do not scale"
    r"|verify all|notify|subject to|drawings are|this drawing|refer to)", re.I)

SHEETNO_RE = re.compile(r"\b([A-Z]{0,3}-?\d{1,3}[./]\d{1,3}|[A-Z]{1,3}-?\d{2,3})\b")


def sheet_title(page):
    """Best sheet title for a page, and how confident we are (0-1).

    Scored, not guessed, on three signals a real title block always has: the
    line is big relative to the page, it hugs an edge where title blocks live,
    and a sheet number sits next to it. Case-insensitive, because plenty of
    practices set sheet names in mixed case.

    Returns ("", 0.0) when nothing scores. Callers must then say "couldn't
    confidently identify", never invent a count from a guess.
    """
    lines = []
    for blk in page.get_text("dict")["blocks"]:
        prev = None
        for ln in blk.get("lines", []):
            s = "".join(sp["text"] for sp in ln.get("spans", [])).strip()
            if not s:
                continue
            size = max((sp["size"] for sp in ln.get("spans", [])), default=0.0)
            bb = ln["bbox"]
            lines.append((s, size, bb))
            # Sheet names wrap. Offer the joined pair as a candidate too, so
            # "PLAN DET. & INT. ELEV -" / "BATH & BED 3" is read as one title.
            if prev and 0 <= bb[1] - prev[2][3] < 8 and abs(bb[0] - prev[2][0]) < 40:
                lines.append((f"{prev[0]} {s}".strip(),
                              max(size, prev[1]), prev[2]))
            prev = (s, size, bb)
    if not lines:
        return "", 0.0

    mb = page.mediabox
    maxsize = max(l[1] for l in lines) or 1.0
    numbers = []
    for s, _, bb in lines:
        m = SHEETNO_RE.search(s)
        if m:
            numbers.append(bb)

    best, best_score = "", 0.0
    for s, size, bb in lines:
        if not (3 <= len(s) <= 60) or not TITLE_KW.search(s) or BOILER_RE.search(s):
            continue
        if s.rstrip().endswith(".") and len(s.split()) > 3:
            continue                      # a sentence that mentions a drawing word
        x0, y0 = bb[0], bb[1]
        edge = min(x0, y0, abs(mb.width - x0), abs(mb.height - y0))
        score = 0.55 * (size / maxsize) + 0.25 * (1.0 - min(edge, 260) / 260.0)
        if any(abs(nb[0] - x0) < 220 and abs(nb[1] - y0) < 60 for nb in numbers):
            score += 0.20
        if score > best_score:
            best, best_score = s, score
    return best, round(best_score, 3)


def _sheet_title(text: str) -> str:
    """Text-only fallback, used by the extractor's sheet register."""
    cands = [ln.strip() for ln in text.split("\n")
             if 3 <= len(ln.strip()) <= 60 and not BOILER_RE.search(ln)]
    hits = [ln for ln in cands if TITLE_KW.search(ln)]
    return min(hits, key=len) if hits else ""


WET_RE = re.compile(
    r"\b(bath|bathroom|ensuite|ens|shower|vanity|basin|laundry|powder|wc|toilet|tile|"
    r"tiled|tiling|splashback|niche|tapware|mixer|waterproof|hob|screen)\b", re.I)
FITTING_RE = re.compile(
    r"\b(basin|vanity|shower|mixer|tapware|splashback|niche|hob|waterproof|screen)\b",
    re.I)
SHEET_PLAN_RE = re.compile(
    r"(floor|ground|first|second|upper|lower|roof|site|demolition|setout|tile|ceiling)"
    r"\s*plan", re.I)
SHEET_ELEV_RE = re.compile(r"(elevations?\b|elev\.)", re.I)
# A scale only counts as a scale when it is written like one.
SCALE_RE = re.compile(r"(1\s*:\s*\d{1,4}\s*@?\s*A\d|scale[^\n]{0,18}?1\s*:\s*\d{1,4})", re.I)

TITLE_CONF = 0.30       # below this we say we couldn't identify it, not that it's absent
MIN_CHAINS = 5          # total verified chains across the document
MIN_CHAINS_PER_PAGE = 0.4
MIN_CLEAN_RATIO = 0.90
MIN_WORD_HIT = 0.15
MIN_WET_KEYWORDS = 4    # on one elevation sheet, incl. at least one fitting


def classify_pages(doc):
    """Per-page: title, confidence, class, dimension tokens, wet-area evidence."""
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text() or ""
        title, conf = sheet_title(page)
        toks = _dim_tokens_xy(page)
        kws = {m.group(0).lower() for m in WET_RE.finditer(text)}
        pages.append({
            "page": i + 1,
            "title": title,
            "conf": conf,
            "named": conf >= TITLE_CONF,
            "is_plan": conf >= TITLE_CONF and bool(SHEET_PLAN_RE.search(title)),
            "is_elev": conf >= TITLE_CONF and bool(SHEET_ELEV_RE.search(title)),
            "chars": len(text.strip()),
            "dims": len(toks),
            "chains": verify_chains(toks),
            "wet_kw": len(kws),
            "has_fitting": bool(FITTING_RE.search(text)),
            "scales": sorted({m.group(0) for m in SCALE_RE.finditer(text)}),
        })
    return pages


def run_intake(pdf_path: Path, want_walls: bool = True):
    """Deterministic gate. Returns (checks, facts). Runs before any analysis.

    Every failure message states only what was actually established. Where a
    signal is merely absent, the wording says we could not identify it - never
    a count asserting the customer's drawings lack something they contain.
    """
    checks, facts = [], {}

    try:
        doc = fitz.open(pdf_path)
    except Exception as exc:
        checks.append(Check(
            "readable", False, True, f"PDF could not be opened: {exc}",
            "The file is corrupt, or isn't a PDF.",
            "Re-export the drawing set as a PDF and send it again."))
        return checks, facts

    encrypted = bool(doc.is_encrypted and doc.needs_pass)
    checks.append(Check(
        "encryption", not encrypted, True,
        "PDF is password-protected against extraction" if encrypted
        else "PDF is not locked",
        "A locked PDF blocks us from reading the dimension text.",
        "Send an unlocked copy, or the password."))

    n = doc.page_count
    facts["pages"] = n
    checks.append(Check(
        "page_count", 1 <= n <= MAX_PAGES, True, f"{n} page(s)",
        "The file is empty or implausibly large.",
        "Send the drawing set as a single PDF of the relevant sheets."))

    pages = classify_pages(doc)
    all_text = "\n".join((p.get_text() or "") for p in doc)
    clean, word_hit = text_quality(all_text)

    total_chars = sum(p["chars"] for p in pages)
    total_dims = sum(p["dims"] for p in pages)
    total_chains = sum(p["chains"] for p in pages)
    chains_pp = total_chains / max(n, 1)
    dim_pages = [p for p in pages if p["dims"] >= MIN_TOKENS_FOR_DIM_PAGE]
    plan_pages = [p for p in pages if p["is_plan"]]
    elev_pages = [p for p in pages if p["is_elev"]]
    named = [p for p in pages if p["named"]]
    wet_elev = [p for p in elev_pages
                if p["wet_kw"] >= MIN_WET_KEYWORDS and p["has_fitting"] and p["dims"] >= 5]
    scales = sorted({s for p in pages for s in p["scales"]})

    facts.update(per_page=pages, total_chars=total_chars, total_dims=total_dims,
                 total_chains=total_chains, chains_per_page=round(chains_pp, 2),
                 clean_ratio=round(clean, 3), word_hit=round(word_hit, 3),
                 dim_pages=len(dim_pages), plan_pages=len(plan_pages),
                 elev_pages=len(elev_pages), named_pages=len(named),
                 wet_elev_pages=len(wet_elev), scales=scales)

    checks.append(Check(
        "text_layer", total_chars >= MIN_TOTAL_CHARS, True,
        f"{total_chars} extractable characters (need {MIN_TOTAL_CHARS})",
        "The file is a scan or photo, so the dimensions are pixels rather than "
        "numbers we can read. We won't OCR them and we won't scale off the drawing.",
        "Ask your designer to re-export the PDF straight out of their drawing "
        "software - not printed and scanned."))

    density = total_chars / max(n, 1)
    checks.append(Check(
        "text_density", density >= MIN_CHARS_PER_PAGE, True,
        f"{density:.0f} characters per page (need {MIN_CHARS_PER_PAGE})",
        "Most pages carry no readable text - likely images with a text title block.",
        "Re-export the full set as vector PDF from the drawing software."))

    # ---- readability, not existence -------------------------------------
    quality_ok = clean >= MIN_CLEAN_RATIO and word_hit >= MIN_WORD_HIT
    checks.append(Check(
        "text_quality", quality_ok, True,
        f"text quality: {clean:.1%} of characters usable, {word_hit:.0%} of words "
        f"recognised (need {MIN_CLEAN_RATIO:.0%} / {MIN_WORD_HIT:.0%})",
        "There is text in this file, but it doesn't read like a drawing sheet - "
        "which is what a scan looks like after OCR has been run over it.",
        "Send the original PDF exported from the drawing software, not a scan."))

    checks.append(Check(
        "dimension_tokens", total_dims >= MIN_DIM_TOKENS, True,
        f"{total_dims} mm dimension tokens found (need {MIN_DIM_TOKENS})",
        "We can read text but can't find printed millimetre dimensions. We measure "
        "from stated dimensions only - we never scale off the drawing.",
        "Send drawings with the dimension strings printed on them, in mm."))

    chains_ok = total_chains >= MIN_CHAINS and chains_pp >= MIN_CHAINS_PER_PAGE
    checks.append(Check(
        "dimension_chains", chains_ok, True,
        f"{total_chains} dimension chains check out ({chains_pp:.2f} per page, "
        f"need {MIN_CHAINS} and {MIN_CHAINS_PER_PAGE}/page)",
        "Text is present but not reliably readable. On a real drawing the numbers "
        "in a chain add up to the total printed beside them - 100 + 840 + 790 = "
        "1730. We can't find enough of those here, which is what OCR'd scans look "
        "like: numbers that are individually plausible and never add up.",
        "Send the original vector PDF from the drawing software. If this is already "
        "the original, let us know and we'll look at it by hand."))

    checks.append(Check(
        "dimensioned_pages", len(dim_pages) >= MIN_DIM_PAGES, True,
        f"{len(dim_pages)} sheet(s) carry a real dimension chain",
        "The set looks like cover sheets, 3D views or renders only.",
        "Include the dimensioned floor plans and elevations."))

    # ---- sheet identification: never assert absence from a failed guess --
    if named:
        plan_detail = (f"{len(plan_pages)} floor plan sheet(s) identified"
                       if plan_pages else
                       f"no floor plan among the {len(named)} sheet(s) we could name")
        plan_means = ("Without a floor plan we cannot measure floor area."
                      if plan_pages else
                      f"We read sheet names on {len(named)} of {n} sheets and none of "
                      "them is a floor plan.")
    else:
        plan_detail = f"couldn't confidently identify any sheet names across {n} sheets"
        plan_means = ("We couldn't read the title blocks, so we can't tell which sheet "
                      "is which. That may be our end, not yours.")
    checks.append(Check(
        "plan_pages", len(plan_pages) >= 1, True, plan_detail, plan_means,
        "Send the floor plan sheet for every room you want quoted, or tell us which "
        "sheet number it is and we'll work from that."))

    elev_detail = (f"{len(elev_pages)} elevation sheet(s) identified" if elev_pages
                   else (f"no elevation sheet among the {len(named)} sheet(s) we could "
                         f"name" if named else "couldn't confidently identify sheet names"))
    checks.append(Check(
        "elevation_pages", len(elev_pages) >= 1, want_walls, elev_detail,
        "Wall tiling heights only appear on elevations. Without them we can give you "
        "floor area only.",
        "Include the elevation sheets for each room you want wall areas on."))

    # ---- the check that legitimately rejects a DA set --------------------
    wet_detail = (f"{len(wet_elev)} internal elevation sheet(s) of wet areas"
                  if wet_elev else
                  (f"{len(plan_pages)} floor plan(s) and {len(elev_pages)} elevation "
                   f"sheet(s) found, but none of the elevations is a dimensioned "
                   f"internal elevation of a wet area"))
    checks.append(Check(
        "wet_area_elevations", len(wet_elev) >= 1, want_walls, wet_detail,
        "The elevations in this set look like external elevations - the outside of "
        "the building. Wall tile quantities come from internal elevations: the wall "
        "drawings of each bathroom, ensuite and laundry, with tiling heights on them.",
        "Ask for the internal elevations / joinery sheets for each wet area. If they "
        "don't exist, we can still do floor areas - just say the word."))

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
# Customer profile  (see PROFILE_QUESTIONS.md)
#
# The profile changes the ORDER only. It can never change a measured area -
# measured areas are the plans' truth and are the same for every customer.
# --------------------------------------------------------------------------

TRADE_STANDARD = {
    "default_lay_pattern": "straight",
    "wastage_straight": "10",
    "wastage_brick_bond": "10",
    "wastage_diagonal": "15",
    "wastage_herringbone": "15",
    "skirting_in_order_box": "yes",
    "want_box_counts": "yes",
    "rounding": "0.1",
    "include_painting": "no",
    "batch_variation_buffer": "0",
    "reorder_lead_time_buffer": "0",
    "always_flag": "waterproofing zones, trims in lineal metres",
}

KV_RE = re.compile(r"^\s*([a-z_]+)\s*:\s*(.+?)\s*$")


def load_profile(name: str | None, root: Path) -> dict:
    """Load customers/<name>.md. Missing or unconfirmed -> trade-standard defaults.

    A missing profile never blocks a job. It means the order is built on trade
    standards, which the takeoff then states plainly rather than passing off as
    the customer's own settings.
    """
    prof = dict(TRADE_STANDARD)
    prof["customer"] = name or ""
    prof["status"] = "DEFAULTS - not yet confirmed"
    prof["_source"] = "trade-standard defaults (no profile loaded)"

    if not name:
        return prof

    path = root / "customers" / f"{name}.md"
    if not path.exists():
        prof["_source"] = f"trade-standard defaults (no {path.name} found)"
        prof["_missing"] = str(path)
        return prof

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("#"):
            continue
        m = KV_RE.match(line)
        if m and (m.group(1) in TRADE_STANDARD or m.group(1) in ("customer", "trade", "status")):
            prof[m.group(1)] = m.group(2)

    prof["_source"] = str(path)
    return prof


def profile_is_confirmed(prof: dict) -> bool:
    return prof.get("status", "").strip().upper().startswith("CONFIRMED")


def resolve_order_settings(prof: dict, job: dict) -> dict:
    """Work out the cut allowance for this job.

    Precedence, highest first:
        explicit --wastage  ->  --lay-pattern  ->  profile default pattern  ->  10%
    """
    pattern = (job.get("lay_pattern") or prof.get("default_lay_pattern") or "straight")
    key = "wastage_" + pattern.strip().lower().replace(" ", "_").replace("-", "_")
    try:
        pct = float(prof.get(key, TRADE_STANDARD.get(key, "10")))
    except ValueError:
        pct = 10.0

    source = "this job's lay pattern" if job.get("lay_pattern") else "profile default pattern"
    if job.get("wastage"):
        try:
            pct = float(str(job["wastage"]).rstrip("%"))
            source = "explicit --wastage for this job"
        except ValueError:
            pass

    def _f(k):
        try:
            return float(prof.get(k, "0"))
        except ValueError:
            return 0.0

    batch, lead = _f("batch_variation_buffer"), _f("reorder_lead_time_buffer")
    return {
        "pattern": pattern, "cut_pct": pct, "cut_source": source,
        "batch_pct": batch, "lead_pct": lead,
        "total_pct": pct + batch + lead,          # added points, never compounded
        "rounding": prof.get("rounding", "0.1"),
        "skirting_in_box": prof.get("skirting_in_order_box", "yes"),
        "want_boxes": prof.get("want_box_counts", "yes"),
        "include_painting": prof.get("include_painting", "no"),
        "always_flag": prof.get("always_flag", ""),
        "confirmed": profile_is_confirmed(prof),
    }


def write_profile_report(job_dir: Path, prof: dict, job: dict, s: dict) -> Path:
    """Job-level order settings. Named order_settings.md, not profile.md, so it can't
    collide with the copied PROFILE_QUESTIONS.md on a case-insensitive filesystem."""
    out = job_dir / "order_settings.md"
    L = ["# Order settings for this job", "",
         f"**Customer:** {prof.get('customer') or '_none given_'}",
         f"**Profile:** `{prof.get('_source')}`",
         f"**Status:** {prof.get('status')}", "",
         "> These settings change the **order** only. They cannot change a measured area.",
         "> Measured areas are the plans' truth and are the same for every customer.", "",
         "| Setting | Value | From |", "|---|---|---|",
         f"| Lay pattern | {s['pattern']} | {'this job' if job.get('lay_pattern') else 'profile default'} |",
         f"| Extra for cuts | {s['cut_pct']:g}% | {s['cut_source']} |",
         f"| Batch variation buffer | {s['batch_pct']:g}% | profile |",
         f"| Reorder lead-time buffer | {s['lead_pct']:g}% | profile |",
         f"| **Total added** | **{s['total_pct']:g}%** | added points, not compounded |",
         f"| Rounding | {s['rounding']} | profile |",
         f"| Skirting in the order box | {s['skirting_in_box']} | profile |",
         f"| Box counts wanted | {s['want_boxes']} | profile |",
         f"| Painter quantities shown | {s['include_painting']} | profile |",
         f"| Always flag | {s['always_flag']} | profile |", "",
         "## This job", "",
         f"- **Tile size / format:** {job.get('tile_size') or '_not given - ask_'}",
         f"- **m² per box:** {job.get('m2_per_box') or '_not given - no boxes line_'}",
         f"- **Lay pattern override:** {job.get('lay_pattern') or '_none - using the profile default_'}",
         ""]
    if not s["confirmed"]:
        L += ["## ⚠️ Not confirmed by the customer", "",
              "This profile has not been confirmed. The order box must say so in plain words,",
              "and the profile questions must be repeated at the bottom of the takeoff.", ""]
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
  - PROFILE_QUESTIONS.md  how customer profiles work, and what they may not change
  - intake_report.md   the intake result and the tradie's answers
  - order_settings.md  THE ORDER SETTINGS FOR THIS JOB - read this before you convert
                       any measured area into an order quantity
  - sheet_register.md  page -> sheet title -> scale
  - all_text.txt       full text layer, per page
  - text_coords.txt    every text run with x/y coordinates and rotation
  - pages/*.png        one rendered image per page - LOOK AT THESE

Job details:
  Job name : {job}
  Trade    : {trade}
  Rooms    : {rooms}
  Wastage  : {wastage}

Order settings (from order_settings.md - these change the ORDER only):
  Customer      : {customer}
  Profile status: {profile_status}
  Lay pattern   : {pattern}
  Extra for cuts: {cut_pct}%  ({cut_source})
  Extra buffers : batch {batch_pct}%, lead time {lead_pct}%  -> {total_pct}% added in total
  Rounding      : {rounding}
  Skirting in the order box: {skirting_in_box}
  Show painter quantities  : {include_painting}
  Tile size     : {tile_size}
  m2 per box    : {m2_per_box}
  Always flag   : {always_flag}

GETTING THE NUMBERS RIGHT - the reminders that matter most:
  - Measure from STATED dimensions only. Never scale off the drawing.
  - Rooms are rarely rectangles. Decompose the floor into bands. Never use
    overall_width x overall_depth unless you have proved the room is rectangular.
  - Use TRUE tiling heights from the elevations, never an assumed ceiling height.
  - Run every check in METHOD.md section 5.
  - Rate every room HIGH / MED / LOW per METHOD.md section 6 - as working vocabulary
    only. Those words must NOT appear in the document you write.
  - Never silently assume. Every inferred number becomes a question.

MEASURED vs ORDER - a hard boundary (METHOD.md 7.7). Do not blur it.
  - A MEASURED area is what the plans say. It is the same for every customer alive.
    NOTHING in the profile may change it. If a preference could move a measured
    number, that number was a guess, not a measurement.
  - An ORDER quantity is a measured area with this customer's settings applied.
  - Apply the conversion in visible steps, never folded into one percentage:
    measured -> + cut allowance -> + any buffers (ADDED points, not compounded)
    -> rounding -> boxes. Show each step.
  - The ORDER box and the room lines carry ORDER quantities. The measured areas go
    below, under HOW WE GOT THESE NUMBERS, at full precision, with the conversion
    shown and a plain line saying the measured column never changes with anyone's
    settings and the order column always does.
  - The ORDER box MUST carry a one-line settings sentence saying what was applied,
    where it came from, and inviting a change - see METHOD.md 10.1 for the wording
    for each case. If the profile status is not CONFIRMED, that line must say the
    settings are trade standard and not this customer's yet, and the profile
    questions must be repeated near the bottom of the document.
  - If m2 per box was given, add a "boxes to buy" line under the m2 line for that
    material, rounded UP to whole boxes, showing the coverage those boxes give.

WRITING IT SO IT GETS READ - just as important. Follow METHOD.md sections 9, 10 and 11
to the letter. The tradie reads this on a phone, one-handed, in a ute. A number he
misreads is exactly as wrong as one you miscalculated.

  - THE ANSWER COMES FIRST. Section 1 is an "ORDER THIS" box with the quantities to
    order, with the extra for cuts ALREADY ADDED and a line saying so. Nothing above it.
  - Then "CHECK THESE n THINGS BEFORE YOU QUOTE" - three to five plain tick-box
    questions, only the ones that move a number materially. Smaller items go to the
    bottom with a one-line pointer, never promoted up.
  - Then ROOM BY ROOM: one number per line, rounded to 0.1 m2, plain English, and NOT
    ONE piece of arithmetic. No "x", no sums, no formulas in this section.
  - Round each room to 0.1 first, then make each total the sum of the rounded room
    figures, so the rooms visibly add up to the total.
  - Anything not safe to order (a LOW room) is EXCLUDED from the order box and listed
    underneath as "NOT IN THAT TOTAL", with the question number that unblocks it.
  - ALL working, checks, formulas and method detail go BELOW, under
    "HOW WE GOT THESE NUMBERS". There for whoever wants it, invisible to whoever doesn't.
  - NO JARGON above that divider. Say "sloped ceiling wall" not trapezoid,
    "double-checked against the plan totals" not reconciliation/cross-check,
    "extra for cuts" not wastage, "taken off" not deduction, "door hole" not opening,
    "wall drawings" not elevations, "off the floor" not AFF, "measured in strips" not
    polygon decomposition. Keep words a tradie owns: niche, splashback, skirting, nib
    wall, hob, screen, m2.
  - Use exactly two marks and nothing else: (tick) ready to order, (warning) confirm
    this first. NEVER a confidence rating, a percentage, a score or a star. Every
    warning mark must have a matching tick-box question.
  - End with the plain-language "Before you quote" checklist from METHOD.md section 11.

Write your result to TAKEOFF_{job}.md in this folder.
"""


def analyse(job_dir: Path, job: str, answers: dict, prof: dict, s: dict,
            timeout: int = 3600) -> Path | None:
    binary = resolve_claude()
    if not binary:
        print("  ! claude CLI not found on PATH - skipping analysis.")
        print("    Install Claude Code, or set CLAUDE_CLI to the binary path.")
        return None

    prompt = INSTRUCTION.format(
        job=job,
        trade=answers.get("trade") or "not supplied - ask in QUESTIONS FOR YOU",
        rooms=answers.get("rooms") or "not supplied - ask in QUESTIONS FOR YOU",
        wastage=answers.get("wastage") or "from the lay pattern below",
        customer=prof.get("customer") or "none given",
        profile_status=prof.get("status", ""),
        pattern=s["pattern"], cut_pct=f"{s['cut_pct']:g}", cut_source=s["cut_source"],
        batch_pct=f"{s['batch_pct']:g}", lead_pct=f"{s['lead_pct']:g}",
        total_pct=f"{s['total_pct']:g}", rounding=s["rounding"],
        skirting_in_box=s["skirting_in_box"],
        include_painting=s["include_painting"],
        tile_size=answers.get("tile_size") or "not given - ask",
        m2_per_box=answers.get("m2_per_box") or "not given - no boxes line",
        always_flag=s["always_flag"],
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
    ap.add_argument("--wastage", help="explicit override; normally comes from the lay pattern")
    ap.add_argument("--customer", help="load customers/<name>.md (see PROFILE_QUESTIONS.md)")
    ap.add_argument("--lay-pattern",
                    help="straight / brick bond / diagonal / herringbone - this job only")
    ap.add_argument("--tile-size", help='e.g. "600x600 porcelain"')
    ap.add_argument("--m2-per-box", type=float,
                    help="if given, the order box gains a boxes-to-buy line, rounded up")
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
    answers = {"trade": a.trade, "rooms": a.rooms, "wastage": a.wastage,
               "tile_size": a.tile_size,
               "m2_per_box": a.m2_per_box, "lay_pattern": a.lay_pattern}

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

    # ---- 1b. CUSTOMER PROFILE - the order settings, never the measurement ----
    root = Path(__file__).resolve().parent
    prof = load_profile(a.customer, root)
    settings = resolve_order_settings(prof, answers)
    write_profile_report(job_dir, prof, answers, settings)
    mark = "confirmed" if settings["confirmed"] else "NOT CONFIRMED - trade standard"
    print(f"      profile: {prof.get('_source')}  [{mark}]")
    print(f"      order:   {settings['pattern']} lay, "
          f"{settings['total_pct']:g}% added, rounding {settings['rounding']}")
    if a.m2_per_box:
        print(f"               boxes at {a.m2_per_box} m2/box, rounded up")
    print("               (order settings only - measured areas are unaffected)")

    if a.intake_only:
        return 0

    # ---- 2. EXTRACT ---------------------------------------------------------
    print("[2/3] extracting pages + dimension text")
    info = extract(a.pdf, job_dir, dpi=a.dpi)
    print(f"      {info['pages']} pages rendered @ {a.dpi} dpi")

    copies = {"TAKEOFF_METHOD.md": "METHOD.md", "SPEC.md": "SPEC.md",
              "INTAKE.md": "INTAKE.md", "PROFILE_QUESTIONS.md": "PROFILE_QUESTIONS.md"}
    for name, as_name in copies.items():
        src = root / name
        if src.exists():
            shutil.copyfile(src, job_dir / as_name)

    if a.no_analyse:
        print("      (--no-analyse) stopping after extraction")
        return 0

    # ---- 3. ANALYSE ---------------------------------------------------------
    print("[3/3] analysis via claude CLI")
    out = analyse(job_dir, job, answers, prof, settings, timeout=a.timeout)
    if out:
        print(f"\nDone. {out}")
        return 0
    print("\nExtraction complete, analysis did not produce a file.")
    print(f"Everything the analysis needs is in {job_dir}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
