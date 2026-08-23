# INTAKE — what we need before we measure anything

Accuracy is the product. The fastest way to destroy it is to start measuring a plan set
that cannot support a measurement. So every job passes an intake gate first, and the gate
is automated (`takeoff.py` runs it before any analysis).

Every job gets one of three verdicts:

- **PASS → we measure everything.**
- **PARTIAL → we measure the floors and skirting now.** The set has dimensioned floor
  plans but no internal wet-area elevations — the most common shape a real set arrives in
  (5 of the 9 stress-test sets). The takeoff delivered is floors + tile skirting, and its
  walls section reads: *"Walls: not measured — this set has no internal wet-area
  elevations. Send the internal elevations and we'll add every wall."* A `PARTIAL_<job>.md`
  letter goes with it saying exactly which sheets unlock the walls.
- **FAIL → we send back `REJECTED_<job>.md`** telling the tradie exactly what is missing
  and exactly what to send instead. **We never guess off bad inputs.**

A rejection is not a lost job. It is a 60-second email that saves both sides a wrong quote.
And a PARTIAL is not a rejection at all — it is a smaller job delivered the same day, with
a standing offer to finish it.

---

## A. Base requirements — the file

### A1. Vector PDF with a selectable text layer — REQUIRED

The dimensions must be *machine-readable text* in the PDF, not pixels.

- ✅ A PDF exported from Revit / ArchiCAD / AutoCAD / SketchUp Layout.
- ❌ A photo of a plan. A phone scan. A screenshot. A flattened raster PDF.

**Why:** we read the printed dimension strings directly. If the numbers are pixels, the
only way to get a measurement is OCR (which misreads 3 as 8, and 1605 as 1005) or scaling
off the drawing (which we never do). Neither is good enough to quote off.

**How to check yourself:** open the PDF, try to select a dimension number with your mouse
and copy it. If it highlights, you're fine.

### A2. Printed dimensions in mm covering the surfaces being quoted — REQUIRED

We measure from **stated dimensions only. We never scale off the drawing.**

- Every room being quoted needs its overall extents dimensioned.
- Dimension chains should be present and should sum to their stated totals.
- Millimetres, not metres or feet. Australian architectural convention.

**Why:** a drawing printed to a different paper size, or with "fit to page" ticked, is no
longer at its stated scale. Scaling off it produces numbers that look right and are wrong
by 3–8%. On a $9,000 tiling job that is $500 of your margin, and you will not find out
until the tiles run out.

### A3. Elevations included, if you want wall areas — REQUIRED FOR WALL QUOTES

A floor plan alone gives us floor area and nothing else.

- Wall tile area needs the elevation sheets, because the **true tiling height** lives
  there, not on the plan.
- Elevations tell us what is actually tiled: full height, a 450 splashback, a 1200 nib,
  a 300 skirting, or nothing at all.
- Without elevations we can give you floor m² and we will say plainly that walls were
  not quoted.

### A4. All notes / legend / general-arrangement pages included — REQUIRED

Send the whole set, not the two pages you think matter.

**Why:** the notes page is where "All dimensions are frame to frame" lives, and that
single line changes whether your measurement is to the stud or to the finished tile face.
It is also where finishes schedules, mitred-corner requirements and tile types live —
all of which change your rate.

### A5. Sheet titles, scale and revision visible — REQUIRED

Each sheet must carry its title block: sheet number, scale, revision, date. We quote
against a revision. If a sheet is untitled we cannot tell you which drawing your number
came from, and you cannot defend the quote on site.

---

## B. Three answers from you — REQUIRED

We ask three questions on every job. They take a minute and they change the whole output.

### B1. What's your trade?

`tiler` / `painter` / `waterproofer` / `other`

Sets what we measure. A tiler and a painter want almost opposite numbers off the same
wall — the tiler wants the tiled band, the painter wants everything above it.

### B2. Which rooms, and which surfaces?

e.g. *"Main bath and master ensuite only — floors and walls. Skip the laundry."*
e.g. *"All wet areas, floors only."*

Sets scope. Stops you paying for a takeoff of a room you're not quoting, and stops us
handing you a number for a room you didn't want.

### B3. Wastage preference?

`none` / `10%` (default) / `15%` / *your own number*

We always report the measured quantity **and** the adjusted quantity side by side. This
just tells us which one to headline.

On a customer with a stored profile this is normally answered already — it comes from their
lay pattern (see `PROFILE_QUESTIONS.md` Q1). Ask it here only to override for this job.

---

## B-extra. Three more per-job questions — the order, not the measurement

These change how we convert measured area into an order. They **cannot** change a measured
area. Ask them per job, because the answer changes job to job.

### B4. Lay pattern for **this** job, if it's different from your usual

`straight` / `brick bond` / `diagonal` / `herringbone` — or "same as usual".

Most jobs are the customer's default and this takes one word. But a client who's specified
herringbone in the ensuite and straight everywhere else changes the order materially, and
it's the sort of thing that gets mentioned on site and never written down.

The cut allowance follows the pattern, using the percentages in their profile:

| Pattern | Their profile says | Applied to |
|---|---|---|
| straight | e.g. 10% | this job, unless overridden |
| brick bond | e.g. 10% | |
| diagonal | e.g. 15% | |
| herringbone | e.g. 15% | |

Per-room patterns are fine — tell us which room. We'll apply the right percentage to each
and show them separately.

### B5. Tile size / format

e.g. *"600 × 600 porcelain"*, *"300 × 100 subway"*, *"1200 × 600 large format"*.

Two reasons we ask:

- Large format (anything over 600) generally justifies a higher cut allowance than the
  pattern alone suggests, and we'll say so rather than quietly bumping it.
- It tells us whether a stated pattern is even sensible — herringbone in 1200 × 600 is a
  different conversation from herringbone in 600 × 100.

If the tile isn't chosen yet, say so. We'll deliver on the profile default and flag that the
allowance may move once it is.

### B6. m² per box  *(optional — but it's the number you buy in)*

If you give it to us, the **ORDER THIS** box gains a **"boxes to buy"** line, rounded **up**
to whole boxes:

```
boxes = ceiling( order m² ÷ m² per box )
```

Rounded up, never to nearest — you cannot buy 0.4 of a box, and rounding down puts you short
on site.

We show the boxes, and the coverage those boxes actually give you, so the gap is visible:

```
  Floor tiles ....  36.4 m²
  Boxes to buy ...  31 boxes  (1.44 m²/box = 44.6 m² — 8.2 m² over)
```

That 8.2 m² is not waste we invented; it's the granularity of the supplier's packaging. Seen
plainly, it's often the moment a tradie decides to drop to a smaller allowance, or to keep
the spare deliberately.

Different tile per room? Give us the m² per box for each and we'll do them separately.

---

## C. The automated gate — what `takeoff.py` actually checks

Run before any analysis. Machine-checkable subset of the above. Twelve checks, in the order
the gate runs them:

| # | Check | Rule | Fails when |
|---|---|---|---|
| 1 | **Readable file** | The PDF opens at all | Corrupt file, or not a PDF |
| 2 | **Encryption** | Not password-locked against extraction | Locked file |
| 3 | **Page count** | ≥ 1, ≤ 300 | Empty or absurd file |
| 4 | **Text layer** | ≥ 200 extractable characters across the document | Scanned / raster / image-only PDF |
| 5 | **Text density** | ≥ 20 characters per page on average | Mostly-image PDF with a title block only |
| 6 | **Text quality** | ≥ 90% of characters belong on a drawing sheet | Text is present but is OCR spray, not a real text layer |
| 7 | **mm dimension tokens** | ≥ 30 integer tokens in the range 20–20000 | No printed dimensions, or dimensions are in the image |
| 8 | **Dimension chains** | ≥ 5 chains that sum to a printed total (±5 mm), ≥ 0.4/page | Numbers exist but never add up — the OCR signature. The one check noise can't fake |
| 9 | **Dimensioned pages** | ≥ 1 page carrying ≥ 8 dimension tokens | Cover sheets and 3Ds only |
| 10 | **Plan pages** | ≥ 1 sheet whose *title-block* name reads as a floor plan | No floor plan → no floor area. When no sheet can be named at all, the letter says *that* — never "you have no floor plan" |
| 11 | **Elevation pages** | ≥ 1 sheet whose title-block name reads as an elevation | Warning only, unless walls are in scope → then a fail |
| 12 | **Wet-area elevations** | ≥ 1 elevation sheet carrying ≥ 4 distinct wet-area terms incl. a fitting, and ≥ 5 dimension tokens | The elevations are external only — floors are measurable, walls are not. Conditional, like #11 |

**How the checks become a verdict:**

- Any failure among checks **1–10** → **FAIL.** `REJECTED_<job>.md` is written and
  nothing is measured.
- Checks **11–12** are the *wall-evidence* checks. When they are the **only** failures
  (walls were asked for, floor plans are dimensioned and readable) → **PARTIAL.**
  Floors + skirting are measured now; `PARTIAL_<job>.md` says what unlocks the walls.
  Under `--no-walls` they are warnings and the verdict is PASS.
- Nothing failed → **PASS.**

Sheet naming (checks 10–12) is scored from the title block — line size, position at a page
edge, a sheet number nearby — with boilerplate excluded and wrapped names joined. Every
failure message states only what was actually established: what we *did* find, before what
we didn't.

Three more things are recorded at intake but **never block the run**:

| Recorded | Rule | When missing / low |
|---|---|---|
| **Word-hit score** *(advisory)* | ≥ 15% of alphabetic tokens are recognised words | Warned and recorded for the reviewer. Demoted from a hard gate: on the test corpus it could not separate OCR spray (0.315) from a clean set (0.307) — the chain check (#8) is what actually catches a scan |
| **Intake answers** | trade / rooms / wastage supplied | Carried into the takeoff as questions |
| **Customer profile** | `customers/<name>.md` exists and is `CONFIRMED` | Trade-standard defaults, stated on the order box |

> **Threshold status:** every numeric threshold above was tuned on the nine-set backtest
> corpus (`backtest/SOURCES.md`) and evaluated on those same nine files. There is no
> held-out set yet. The separations are wide (`STRESS_REPORT.md`), but the values are
> **tuned-on-corpus, pending validation on live jobs** — expect them to move.

---

## D. What a rejection looks like

Polite, specific, actionable. It names what failed, what it means, and what to send.
It never lectures and never blames the tradie for what the architect exported.

```
Hi — thanks for sending through 5 Ellalong Rd.

I can't measure this set accurately yet, and I'd rather tell you that than send you
numbers you can't trust. Here's what's blocking it:

  ✗ No selectable text layer
      What this means: the file is a scan/photo, so the dimensions are pixels rather
      than numbers I can read.
      What to send: ask your designer to re-export the PDF straight from their drawing
      software (not printed and scanned).

  ✗ No elevation sheets found — and you asked for wall tile areas
      What this means: wall tiling heights only appear on elevations.
      What to send: the elevation sheets for each room you want walls quoted on.

Everything else in the set is fine. Send those two things through and I'll have your
numbers back same day.
```

---

## E. Why this gate exists (the one-paragraph version)

We are competing on accuracy, and accuracy is decided before the first measurement, at
the point where we choose whether to accept the input. A takeoff produced from a phone
photo of a plan is not a cheaper takeoff — it is a different, worthless product that
happens to look identical. Rejecting bad inputs is the cheapest quality control that
exists, and being the only supplier who says *"I can't measure this yet, here's what I
need"* is a large part of why a tradie trusts the numbers when we do send them.
