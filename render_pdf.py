#!/usr/bin/env python3
"""Render a markdown document to PDF.

Uses `markdown` for md -> HTML and PyMuPDF's Story engine for HTML -> PDF, so the
only dependencies are the two libraries takeoff.py already needs plus `markdown`.

    pip install pymupdf markdown
    python3 render_pdf.py BUSINESS_PLAN.md BUSINESS_PLAN.pdf "TAKEOFF - Business Plan"
"""

from __future__ import annotations

import sys
from pathlib import Path

import fitz
import markdown

CSS = """
body      { font-family: sans-serif; font-size: 9.5pt; line-height: 1.45; color: #1a1a1a; }
h1        { font-size: 20pt; margin: 18pt 0 8pt 0; color: #111; }
h2        { font-size: 14pt; margin: 16pt 0 6pt 0; color: #111; }
h3        { font-size: 11pt; margin: 12pt 0 4pt 0; color: #222; }
h4        { font-size: 10pt; margin: 10pt 0 3pt 0; color: #333; }
p         { margin: 0 0 6pt 0; }
ul, ol    { margin: 0 0 6pt 0; }
li        { margin: 0 0 3pt 0; }
blockquote{ margin: 6pt 0 6pt 10pt; padding-left: 8pt; color: #444; }
code      { font-family: monospace; font-size: 8.5pt; color: #7a2020; }
pre       { font-family: monospace; font-size: 8pt; background: #f4f4f4;
            padding: 6pt; margin: 6pt 0; line-height: 1.3; }
pre code  { color: #1a1a1a; }
table     { width: 100%; margin: 6pt 0 8pt 0; }
th        { font-size: 8.5pt; text-align: left; background: #ececec;
            padding: 3pt; border: 1px solid #c8c8c8; }
td        { font-size: 8.5pt; padding: 3pt; border: 1px solid #d8d8d8;
            vertical-align: top; }
hr        { margin: 10pt 0; }
em        { color: #333; }
"""


def render(src: Path, dst: Path, title: str = "") -> Path:
    html_body = markdown.markdown(
        src.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    html = f"<html><head><title>{title}</title></head><body>{html_body}</body></html>"

    story = fitz.Story(html=html, user_css=CSS)
    writer = fitz.DocumentWriter(str(dst))
    page = fitz.paper_rect("a4")
    frame = page + (54, 54, -54, -60)  # ~19mm margins

    pages = 0
    more = True
    while more:
        dev = writer.begin_page(page)
        more, _ = story.place(frame)
        story.draw(dev)
        writer.end_page()
        pages += 1
        if pages > 400:  # runaway guard
            break
    writer.close()

    # stamp page numbers
    doc = fitz.open(dst)
    for i, pg in enumerate(doc):
        pg.insert_text(
            fitz.Point(page.width / 2 - 12, page.height - 32),
            f"{i + 1} / {doc.page_count}", fontsize=8, color=(0.45, 0.45, 0.45),
        )
    doc.saveIncr()
    n = doc.page_count
    doc.close()
    print(f"{dst}  ({n} pages)")
    return dst


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    render(Path(sys.argv[1]), Path(sys.argv[2]),
           sys.argv[3] if len(sys.argv) > 3 else "")
