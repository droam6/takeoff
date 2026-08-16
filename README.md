# TAKEOFF

**AI plan measurement for tradies.** Send a plan set, get a room-by-room m² breakdown back
the same day, with every number showing its working.

Not software they have to learn — a service they send plans to.

```bash
pip install pymupdf
python3 takeoff.py sample_plans.pdf --trade tiler --rooms "all wet areas" --wastage 10
```

---

## The rule everything else serves

> **We measure from stated dimensions only. We never scale off the drawing, and we never
> silently assume.**

Anything the drawings don't say becomes a numbered question at the top of the delivered
document — not a guess buried in a footnote.

---

## Documents

| File | What it is |
|---|---|
| [`INTAKE.md`](INTAKE.md) | What a plan set must have before we'll measure it, and the three questions we ask every tradie |
| [`SPEC.md`](SPEC.md) | What we output — for tilers and for painters |
| [`TAKEOFF_METHOD.md`](TAKEOFF_METHOD.md) | The analysis protocol, including the six-check verification layer and the confidence rating |
| [`QUICKSTART.md`](QUICKSTART.md) | Exact usage, macOS and Windows PowerShell |
| [`TAKEOFF_sample.md`](TAKEOFF_sample.md) | A worked takeoff of the sample set — 5 wet areas, full working, 15 questions |
| [`BUSINESS_PLAN.md`](BUSINESS_PLAN.md) · [`.pdf`](BUSINESS_PLAN.pdf) | The business: problem, moat, pricing, go-to-market, kill criteria |

## Code

| File | What it does |
|---|---|
| `takeoff.py` | Intake gate → extraction → analysis via the `claude` CLI |
| `render_pdf.py` | Markdown → PDF (used for the business plan; works for takeoffs too) |

## Pipeline

```
1. INTAKE GATE   deterministic checks, run BEFORE any analysis
                 PASS → continue     FAIL → REJECTED_<job>.md, and stop
2. EXTRACT       PyMuPDF: page images + text layer with coordinates. Deterministic.
3. ANALYSE       claude CLI, headless, against TAKEOFF_METHOD.md → TAKEOFF_<job>.md
```

The model is used for one thing: associating a printed dimension with the element it
describes. Extraction and arithmetic are deterministic.

## Sample set

`sample_plans.pdf` is a real architectural joinery set (Harper Lane Design, project 24107 —
5 Ellalong Road, Cremorne NSW) covering a powder room, laundry, main bathroom, guest ensuite
and master ensuite. 25 sheets, mm dimensions, 1:20 @ A3 throughout except sheet 12.01 which
is 1:25.

Worked result: [`TAKEOFF_sample.md`](TAKEOFF_sample.md).
