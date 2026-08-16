#!/usr/bin/env python3
"""Render a markdown document to a branded CHALKLINE PDF.

Markdown -> HTML (`markdown`) -> PDF (PyMuPDF's Story engine), so the only
dependencies are the two libraries takeoff.py already needs plus `markdown`.

Brand system per BRAND.md: typographic wordmark, one accent (Chalk Blue
#1462A0), header strip with the document control block, footer strip carrying
the re-issue promise once, and ASCII boxes left in monospace so the ORDER THIS
dotted leaders line up.

Page control
------------
A line containing only `<!--newpage-->` starts a new page. Used to hold the
ANSWER PACK to its three pages.

    pip install pymupdf markdown

    python3 render_pdf.py TAKEOFF_sample.md TAKEOFF_sample.pdf \
        --title "TAKEOFF - 5 Ellalong Road" --job TKF-001 --rev A \
        --drawings "Rev L, 01/09/25" --supersedes none --date "16 Aug 2026"
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import fitz
import markdown

ACCENT = (0.078, 0.384, 0.627)     # #1462A0  Chalk Blue
INK = (0.102, 0.102, 0.102)        # #1A1A1A
GREY = (0.40, 0.40, 0.40)          # #666666
RULE = (0.847, 0.847, 0.847)       # #D8D8D8

PAGEBREAK = "<!--newpage-->"

CSS = """
body      { font-family: sans-serif; font-size: 9.5pt; line-height: 1.45; color: #1a1a1a; }
h1        { font-size: 17pt; margin: 4pt 0 7pt 0; color: #111; }
h2        { font-size: 13pt; margin: 15pt 0 6pt 0; color: #1462A0; }
h3        { font-size: 10.5pt; margin: 11pt 0 4pt 0; color: #111; }
h4        { font-size: 9.5pt; margin: 9pt 0 3pt 0; color: #333; }
p         { margin: 0 0 6pt 0; }
ul, ol    { margin: 0 0 6pt 0; }
li        { margin: 0 0 3pt 0; }
blockquote{ margin: 6pt 0 6pt 10pt; padding-left: 8pt; color: #444; }
code      { font-family: monospace; font-size: 8.5pt; color: #1462A0; }
pre       { font-family: monospace; font-size: 7.6pt; background: #f5f7f9;
            padding: 5pt; margin: 5pt 0; line-height: 1.22; }
pre code  { color: #1a1a1a; }
table     { width: 100%; margin: 6pt 0 8pt 0; }
th        { font-size: 8.5pt; text-align: left; background: #e7eef4;
            padding: 3pt; border: 1px solid #c8d4de; }
td        { font-size: 8.5pt; padding: 3pt; border: 1px solid #d8d8d8;
            vertical-align: top; }
hr        { margin: 9pt 0; }
em        { color: #333; }
"""

PROMISE = "Answer the questions — we re-issue free within 24 hours."

BRAND_FILE = Path(__file__).resolve().parent / "BRAND.md"


def read_brand(path: Path = BRAND_FILE) -> tuple[str, str]:
    """Company name and tagline, read from BRAND.md.

    BRAND.md is the single source of truth for the name. Nothing here hardcodes
    it, so a rename is one edit in one file rather than a grep across the repo.
    """
    name, tagline = "", ""
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\*\*Name:\*\*\s*(.+?)\s*$", line)
            if m and not name:
                name = m.group(1).strip()
            m = re.match(r"\*\*Tagline:\*\*\s*\*?(.+?)\*?\s*$", line)
            if m and not tagline:
                tagline = m.group(1).strip()
            if name and tagline:
                break
    except OSError:
        pass
    return name or "CHALKLINE", tagline or "Measured, not guessed."


def spaced(name: str) -> str:
    """Wordmark letter-spacing, per BRAND.md."""
    return " ".join(name.upper())


def _text(page, x, y, s, size=8, color=INK, font="helv"):
    page.insert_text(fitz.Point(x, y), s, fontsize=size, color=color, fontname=font)


def draw_header(page, meta, first: bool, pw: float):
    """Header strip. Full control block on page 1, slim bar after that."""
    L, R, top = 54, pw - 54, 40
    if first:
        _text(page, L, top, spaced(meta.get("name", "")), 15, INK, "hebo")
        page.draw_line(fitz.Point(L, top + 6), fitz.Point(L + 168, top + 6),
                       color=ACCENT, width=2)
        _text(page, L, top + 17, meta.get("tagline", "Measured, not guessed."), 8, GREY, "heit")
        rows = [("Job ref", meta.get("job", "")), ("Takeoff", meta.get("rev", "")),
                ("Drawings", meta.get("drawings", "")),
                ("Supersedes", meta.get("supersedes", "")), ("Date", meta.get("date", ""))]
        rows = [(k, v) for k, v in rows if v]
        y = top - 4
        for k, v in rows:
            _text(page, R - 168, y, k, 7.5, GREY)
            _text(page, R - 96, y, str(v), 7.5, INK, "hebo")
            y += 9.5
        base = max(top + 26, y)
        page.draw_line(fitz.Point(L, base), fitz.Point(R, base), color=ACCENT, width=1.4)
        return base + 16
    _text(page, L, top, spaced(meta.get("name", "")), 8.5, INK, "hebo")
    tail = "   ·   ".join(x for x in (meta.get("job"), f"Takeoff {meta.get('rev')}"
                                      if meta.get("rev") else None) if x)
    if tail:
        _text(page, R - fitz.get_text_length(tail, fontname="helv", fontsize=7.5),
              top, tail, 7.5, GREY)
    page.draw_line(fitz.Point(L, top + 5), fitz.Point(R, top + 5), color=RULE, width=0.8)
    return top + 20


def draw_footer(page, meta, n, total, pw, ph):
    L, R, y = 54, pw - 54, ph - 42
    page.draw_line(fitz.Point(L, y), fitz.Point(R, y), color=RULE, width=0.8)
    _text(page, L, y + 12, PROMISE, 7.5, ACCENT, "hebo")
    contact = meta.get("contact", "hello@chalkline.example  ·  04XX XXX XXX")
    _text(page, L, y + 22, contact, 7, GREY)
    pn = f"{n} / {total}"
    _text(page, R - fitz.get_text_length(pn, fontname="helv", fontsize=7.5),
          y + 12, pn, 7.5, GREY)


def render(src: Path, dst: Path, meta: dict) -> Path:
    raw = src.read_text(encoding="utf-8")
    chunks = [c for c in raw.split(PAGEBREAK)]

    page_rect = fitz.paper_rect("a4")
    pw, ph = page_rect.width, page_rect.height
    writer = fitz.DocumentWriter(str(dst))

    pages_meta = []          # (first_page?) per emitted page
    first_chunk = True
    for chunk in chunks:
        html_body = markdown.markdown(
            chunk, extensions=["tables", "fenced_code", "sane_lists"])
        story = fitz.Story(html=f"<html><body>{html_body}</body></html>", user_css=CSS)
        more, guard = True, 0
        chunk_first = True
        while more:
            is_first = first_chunk and chunk_first
            top = 108 if is_first else 62
            frame = fitz.Rect(54, top, pw - 54, ph - 52)
            dev = writer.begin_page(page_rect)
            more, _ = story.place(frame)
            story.draw(dev)
            writer.end_page()
            pages_meta.append(is_first)
            chunk_first = False
            guard += 1
            if guard > 300:
                break
        first_chunk = False
    writer.close()

    doc = fitz.open(dst)
    total = doc.page_count
    for i, page in enumerate(doc):
        draw_header(page, meta, pages_meta[i] if i < len(pages_meta) else False, pw)
        draw_footer(page, meta, i + 1, total, pw, ph)
    doc.saveIncr()
    doc.close()
    print(f"{dst}  ({total} pages)")
    return dst


def main() -> None:
    ap = argparse.ArgumentParser(description="Render markdown to a branded CHALKLINE PDF")
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--title", default="")
    ap.add_argument("--name", default=None, help="defaults to BRAND.md")
    ap.add_argument("--tagline", default=None, help="defaults to BRAND.md")
    ap.add_argument("--job", default="")
    ap.add_argument("--rev", default="")
    ap.add_argument("--drawings", default="")
    ap.add_argument("--supersedes", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--contact", default="hello@chalkline.example  ·  04XX XXX XXX")
    a = ap.parse_args()
    brand_name, brand_tagline = read_brand()
    render(a.src, a.dst, {
        "title": a.title, "name": a.name or brand_name,
        "tagline": a.tagline or brand_tagline, "job": a.job, "rev": a.rev,
        "drawings": a.drawings, "supersedes": a.supersedes, "date": a.date,
        "contact": a.contact,
    })


if __name__ == "__main__":
    main()
