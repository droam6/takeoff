# TAKEOFF_METHOD — the analysis protocol

This is the procedure. Follow it in order. Do not skip the verification layer, and do not
resolve an ambiguity by choosing a number — resolve it by asking a question.

**The one rule everything else serves:** *we measure from stated dimensions only. We never
scale off the drawing, and we never silently assume.*

---

## 0. Before anything — the intake gate

Run the checks in `INTAKE.md` §C. If any hard check fails, write `REJECTED_<job>.md` and
stop. Do not produce a partial takeoff off a failed set.

---

## 1. Build the sheet register

For every page, record: page number, sheet number, sheet title, scale, revision, date.

Classify each sheet:

| Class | Match on title | Use |
|---|---|---|
| PLAN | `…FLOOR PLAN` | floor polygon, wall runs, opening positions |
| ELEVATION | `…ELEVATIONS` | tiling heights, feature zones, niches, openings |
| 3D / RENDER | `…3D` | context only — **never** a source of dimensions |
| NOTES / LEGEND | notes, schedule, legend | measurement conventions, finishes |

Then group sheets by **room**. Announce the grouping in the output. If a room has
elevations but no plan (or vice versa), that is a finding, not a gap to paper over.

> Sample set: the Powder Room has sheets 3.02–3.04 (elevations + 3D) but **no 3.01 floor
> plan**. Its floor area therefore cannot be measured from the set. That goes in QUESTIONS,
> and the room is rated LOW.

## 2. Read the notes page first

Find the measurement convention before measuring. In the sample set the notes state:

- *"All dimensions are as indicated, Use written dimensions"* → confirms rule zero.
- *"All dimensions are frame to frame"* → dimensions run to the stud frame, so the
  finished tiled face sits ~30–40 mm inside each printed line. Record this; it is a
  systematic bias, and it makes printed-dimension takeoffs marginally **generous** (safe)
  rather than short.
- *"All wall tiles & niches to be mitred at corner junctions… No trims"* → a labour item,
  reported in linear metres.

## 3. Identify each room and its extents

For each room, from the PLAN sheet:

1. Read every dimension chain — overall, and each sub-chain.
2. Establish the **internal floor polygon** as a rectilinear band decomposition:

   ```
   area = Σ (band_width × band_depth)
   ```

   Never `overall_width × overall_depth` unless the room is provably a rectangle with no
   step, nib or alcove. Prove it from the chains, don't assume it from the look of it.

3. Record fixture footprints from the plan (bath surround, vanity, joinery, shower seat)
   with their printed dimensions.

## 4. Pair printed dimensions to plan extents and elevation runs

Every printed number must be assigned to a physical thing before it is used:

- A number on a chain with plain tick marks locates a **wall face**.
- A number with a ℄ symbol locates a **fixture centreline** — it is not a wall dimension
  and must never be summed into a wall chain.
- A number in **red** is typically a setout/services dimension (tap centreline, waste,
  niche position). Useful context; not a room extent.
- A number inside a **revision cloud** has changed. Flag it — you may be looking at a
  superseded neighbour.

Match each elevation to a plan wall by its overall run length. Elevations in these sets
are **developed** — a stepped wall is drawn flattened, so the elevation run equals the
sum of its plan segments, not the straight-line distance.

## 5. VERIFICATION LAYER — run all six, log every result

No takeoff is released without this log. Each check is PASS / FAIL / N/A, with the
arithmetic shown.

### 5.1 Chains sum to stated totals

Every sub-chain must equal the overall it sits under.

```
Main Bath, north wall:      550 + 1000 + 1020  =  2570   vs stated 2570   PASS
Main Bath, south wall:      685 + 820 + 245 + 20 + 1000 = 2770 vs 2770    PASS
Powder Room, elevation 04:  100 + 840 + 790    =  1730   vs stated 1730   PASS
```

Tolerance: **±5 mm PASS silently, 6–25 mm PASS with note, >25 mm FAIL → question.**
Rounding in CAD routinely produces 5 mm; 150 mm is a drawing error and must be asked about.

### 5.2 Opposite elevations of the same room agree

Wall 1 and wall 3 are the same length. Wall 2 and wall 4 are the same length. If they
are not, either the room is not rectangular (check the plan) or a sheet is wrong.

```
Guest Ensuite:  E01 4000 vs E03 4000   PASS
                E02 2110 vs E04 2110   PASS
Powder Room:    E01 1605 vs E03 1615   PASS-with-note (10 mm)
```

### 5.3 Wall runs reconcile with the floor perimeter

The sum of the elevation run lengths must equal the perimeter of the floor polygon. This
is the single strongest check available, because it ties two independent sheets together.

```
Main Bath   elevations: 3895 + 2770 + 3895 + 2770                = 13330
            plan polygon: 2570 + 2112 + 200 + 1783 + 2770 + 3895 = 13330   PASS (0 mm)

Master Ens. elevations: 3820 + 5215 + 3820 + 5215                = 18070
            plan polygon (12 sides, summed)                      = 18079   PASS (9 mm)
```

A failure here means the plan and the elevations disagree about the shape of the room.
Stop and ask; do not average them.

### 5.4 Heights reconcile within each elevation

Every vertical chain must sum to the stated wall height.

```
Main Bath E01:  300 + 540 + 60 + 250 + 1000 + 550          = 2700   PASS
Laundry  E01:   135 + 725 + 40 + 700 + 900 + 200           = 2700   PASS
Powder   E02:   300 + 40 + 310 + 250 + 200 + 1350 + 250    = 2700   PASS
```

If no chain sums to a stated wall height, **the wall height is not dimensioned.** Say so.
Do not import 2700 from the room next door.

### 5.5 Fixture dimensions agree between plan and elevation

The bath is the same bath on both sheets.

```
Main Bath bath alcove:  plan 1020 wide × 2000 deep;  elevation 02 shows 1020   PASS
Master vanity:          plan 580 × 2000;  elevation 03 chain 20+750+465+750+35 = 2020  PASS-with-note
```

### 5.6 Sanity ranges

Totals are checked against ranges that a real wet area falls in. Anything outside is a
loud flag, not a quiet number.

| Quantity | Sane range | Action outside |
|---|---|---|
| Bathroom / ensuite floor | 2 – 25 m² | re-derive the polygon |
| Wall tile : floor area ratio | 2.0 – 5.5 × | usually means a height was assumed |
| Ceiling height | 2100 – 3600 mm | check it was read, not assumed |
| Wall tile per room | 5 – 60 m² | check for a missed opening deduction |
| Any single wall | 1 – 20 m² | check run × height pairing |
| Niche | 0.1 – 1.5 m² | check w/h/d were not swapped |

---

## 6. Confidence rating — internal, expressed as a tick or a flag

Every room gets a rating, assigned mechanically from the checks in §5.

| Rating | Criteria |
|---|---|
| **HIGH** | Plan **and** elevations present. §5.1–5.4 all PASS (≤25 mm). All tiling heights printed. No undimensioned opening in scope. Sanity ranges clear. |
| **MED** | Plan and elevations present, but one of: a chain discrepancy 26–200 mm; ≤2 undimensioned openings; a niche depth missing; a fixture dimension conflict. Numbers are usable after the questions are answered. |
| **LOW** | A required sheet is missing; a wall height is undimensioned; a chain discrepancy >200 mm; a raked ceiling with no section; §5.3 FAIL. **Numbers are provisional and must not be quoted from until the questions are answered.** |

### The rating is never printed as HIGH / MED / LOW

The words HIGH, MED and LOW are working vocabulary. They do not appear in the delivered
document, and neither does any confidence percentage or score. A tradie reading a number on
a phone needs to know one thing: *can I use this or not?* A three-band score makes him do
arithmetic on our uncertainty, which is our job, not his.

It is expressed customer-facing as exactly two marks, and nothing else:

| Mark | Means | Comes from |
|---|---|---|
| ✅ | **Ready to order.** Use this number. | HIGH |
| ⚠️ | **Confirm this first.** | MED and LOW |

A ⚠️ always sits next to a matching tick-box question in §10.2 — never on its own. If we
flag something, we say what to do about it in the same breath.

Where a LOW room cannot produce a usable number at all (missing sheet, undimensioned
ceiling), its quantity is **kept out of the order total** and shown separately as "not in
that total" — see §10.1. A number a tradie must not order from does not belong in the
number he orders from.

---

## 7. Compute the quantities

### 7.1 Floor

```
gross floor  = Σ (band_width × band_depth)          [rectilinear decomposition]
net floor    = gross − Σ (floor-occupying fixtures)
```

Deduct: built-in bath surrounds and hobs, floor-standing joinery, shower seats/benches.
Do **not** deduct: wall-hung vanities (tiles run under), WC pans, floor wastes.
List every deduction as its own line so it can be added back.

### 7.2 Walls

```
wall area = run_length × true_tiling_height
```

The tiling height comes from the elevation, and it is whatever the elevation says:

| Case | Height used |
|---|---|
| Full-height tiling | floor to ceiling, as dimensioned |
| Tiling above a bath | ceiling − bath rim height (e.g. 2700 − 550 = 2150) |
| Splashback | the stated splashback height only (e.g. 450) |
| Nib / half wall | the stated nib height (e.g. 1200) |
| Tile skirting | the stated skirting height (e.g. 300) |
| Not stated | **it becomes a question. No default.** |

### 7.3 Raked ceilings — trapezoids

```
wall area = run × (h_low + h_high) / 2
```

For a gable/hip within a run, split the run at the rake break and sum the pieces:

```
area = Σ [ segment_run × (h_start + h_end) / 2 ]
```

Both `h_low` and `h_high` must be **printed**. If the rake is drawn but not dimensioned,
the room drops to LOW and the wall is reported as provisional against an explicit assumed
height, flagged in QUESTIONS.

### 7.4 Feature-tile zones

Measured separately, reported on their own line, subtracted from the standard-tile line
for that wall so the two do not double-count.

### 7.5 Niches

```
niche area = (w × h) + 2(d × h) + 2(w × d)
```

Reported as both a count and an area. Missing depth → question, not a default.

### 7.6 Openings

Deducted from the wall they sit in. Undimensioned opening heights get a clearly-labelled
provisional value (AU standard door leaf 2040 mm) **and** a question. Never a silent one.

### 7.7 Wastage

```
+10%  = measured × 1.10          [default: straight lay, rectangular rooms]
+15%  = measured × 1.15          [raked ceilings, diagonal/herringbone, large format]
```

Presented as columns beside the measured figure. The measured figure is always the
headline; the adjusted figures never replace it.

---

## 8. Show all working

Every number in the output carries its arithmetic inline:

```
Floor (gross)   2570 × 3895                = 10.010 m²
                + step 200 × 1635          =  0.327 m²
                                             10.337 m²
Less bath surround 1020 × (2000 + 90)      =  2.132 m²
Floor (net tiled)                            8.205 m²
```

A number a tradie cannot re-derive on the back of a docket is a number they cannot
defend on site.

---

---

## 9. Write it for a phone screen in a ute

Everything up to here is how we get the numbers right. This section is how we stop that
work being wasted.

**A correct number the tradie can't find, can't read, or doesn't trust is worth nothing.**
He is reading this on a phone, one-handed, in a ute, between jobs — or at the kitchen table
at 9pm with the answer needed tonight. Readability is not presentation polish sitting on
top of the accuracy work. It is part of the accuracy work, because a number that gets
misread is exactly as wrong as a number that was miscalculated.

Three rules, applied to every word that faces a customer:

### 9.1 The answer comes first. The working comes last.

He opens the document and sees what to order. Not a summary, not a sheet register, not a
methodology note — the quantity, in a box, at the top.

Everything that explains, proves or qualifies that number lives **below**, under
**HOW WE GOT THESE NUMBERS**. It is there in full for whoever wants it, and invisible to
whoever doesn't. Nobody is made to scroll past our workings to reach their answer.

### 9.2 No jargon, anywhere customer-facing

If a word exists to make the writer sound like an estimator, it goes. Use the word the
tradie would use standing in the room.

| Never write | Write |
|---|---|
| trapezoid / raked plane | **sloped ceiling wall** |
| reconciliation / cross-check passed | **double-checked against the plan totals** |
| wastage factor / wastage allowance | **extra for cuts** (or *extra for cuts and breakage*) |
| deduction / deduct | **taken off** |
| opening | **door hole / window hole** |
| perimeter | **all the walls added up** |
| rectilinear decomposition / polygon | **measured in strips** |
| net of fixtures | **after taking off the bath and the cupboards** |
| elevation | **wall drawing** (say *wall drawings (elevations)* once, then drop it) |
| AFF / above finished floor | **off the floor** |
| provisional / indicative | **we've guessed this — please confirm** |
| confidence: MED | **⚠️ confirm this** |
| nominal / notional | **about** |

Keep the words a tradie already owns: *niche, splashback, skirting, hob, nib wall, screen,
m², linear metres, setout*. Stripping those is its own kind of talking down.

Sentence rules: short. One idea per line. Numbers rounded to **0.1 m²** everywhere
customer-facing — three decimal places on a phone screen is noise pretending to be rigour.
The full-precision figures live in the working section.

### 9.3 Two marks, no scores

The only status marks in the whole document are **✅** and **⚠️** (see §6). No HIGH/MED/LOW,
no percentages, no confidence scores, no star ratings, no colour coding that dies in
greyscale. A tradie should never have to interpret our uncertainty — he should be told
either *use this* or *check this first*.

Every ⚠️ has a matching tick-box question. Nothing is flagged without being asked.

---

## 10. The output template

Every `TAKEOFF_<job>.md` follows this exact order. Do not reorder it, and do not let any
part of §10.5 leak upward.

### 10.1 — ORDER THIS  *(the totals box, first thing on the page)*

A single box with the order quantities. **Extra for cuts is already added**, and the box
says so in words.

```
==================================================
  ORDER THIS
==================================================
  Floor tiles ................  36.4 m²
  Wall tiles .................  58.6 m²
  Feature tiles ..............  12.0 m²
  Tile skirting ..............   7.3 m
==================================================
  Includes 10% extra for cuts and breakage.
```

Rules:

- **Round to 0.1.** Round each room first, then make the total the sum of the rounded room
  figures — so the rooms visibly add up to the total. A total that doesn't match the lines
  above it destroys trust in every other number on the page.
- **One material per line.** Different tile = different line, because it's a different
  order.
- Anything that is not safe to order (a LOW room, per §6) is **excluded from the box** and
  listed immediately underneath:

```
  NOT IN THAT TOTAL — 2 things we can't finish yet
  • Master ensuite walls — about 50.8 m² more. We need the ceiling
    height first (question 1).
  • Powder room floor — about 3.1 m². The floor plan sheet isn't in
    the set (question 2).
```

### 10.2 — CHECK THESE *n* THINGS BEFORE YOU QUOTE

Immediately below the box. Tick-boxes, plain questions, no numbering scheme beyond 1, 2, 3.

```
⚠️ CHECK THESE 4 THINGS BEFORE YOU QUOTE

[ ] 1. How high are the master ensuite walls, and is the ceiling sloped?
       Every other room says 2700. The master ensuite drawings don't say,
       anywhere. Until you tell us we can't give you a wall number for
       that room. The floor is fine.
```

Rules:

- **Only what changes a number materially.** Aim for three to five. If everything is
  urgent, nothing is.
- Each one: the question in bold as a single line, then two or three plain lines saying
  what's missing and what it moves. Never more.
- State the size of the exposure in m² where you can — that's how he decides what to chase.
- Smaller items do **not** get promoted here. They go in §10.5 under *What we had to fill
  in*, with a one-line pointer from this section so nothing is hidden:
  *"There are 8 smaller things we filled in — they're listed at the bottom."*

### 10.3 — ROOM BY ROOM

One block per room. **Order quantities** (extra for cuts already in), one number per line,
rounded to 0.1.

```
MAIN BATHROOM  ✅
  Floor tiles ................   9.0 m²
  Wall tiles .................  29.6 m²   (includes 2 niches)
  Feature tiles ..............   6.0 m²   behind the vanity
```

Rules:

- ✅ or ⚠️ against the room name, and against any individual line that needs confirming.
- A short plain note in the right-hand column where the number needs context
  (*behind the vanity*, *splashback only*, *tiles run under the vanity*).
- **No arithmetic in this section.** Not one `×`. It all lives in §10.5.
- Where a room's tiling is unusual, say so in one plain line, because that's the line that
  stops him quoting the wrong thing:
  *"The laundry is not a tiled room — it's a 450 high splashback over the bench, nothing
  else."*

### 10.4 — Other trades  *(only if in scope)*

Same shape, kept short. Painters get walls and ceilings.

### 10.5 — HOW WE GOT THESE NUMBERS

Everything else, below a clear divider, in this order:

1. **The straight measurements** — the same table without the extra for cuts, at full
   precision, so anyone can apply their own percentage.
2. **Room-by-room working** — every `×` and every subtraction, per §8.
3. **What we double-checked** — the §5 checks, written as plain statements with ✅/⚠️,
   *not* as a pass/fail matrix. e.g. *"We added up the four wall drawings and compared them
   to the walls on the floor plan. Both come to 13,330 mm — dead on."*
4. **What we had to fill in** — every assumption, each phrased as a question (§10.6).
5. **The drawings we read** — sheet numbers, titles, scale, revision.
6. **Before you quote** — the closing checklist (§11).

### 10.6 — Every assumption is a question

Any value inferred, scaled, taken as standard practice, or carried over from another room
is written as a question a busy tradie can answer in one word.

```
The main bath window is 1000 wide on the plan, but no sheet says how tall it is.
We used 1360 and took 1.4 m² off that wall. What's the real height?
```

Never:

```
Assumed window height 1360mm.
```

The first can be answered before the quote goes out. The second can only be discovered on
site, too late.

---

## 11. Before you quote — the closing checklist

Every takeoff ends with this, unticked, in plain language:

```
[ ] The sheet numbers and dates above match the drawings you were given
[ ] You've answered the questions at the top
[ ] Anything marked ⚠️ is sorted, or left out of your quote
[ ] Tiling heights confirmed with the designer or on site
[ ] Door and window sizes confirmed
[ ] You agree with what we took off and what we left in (under the vanity? behind the bath?)
[ ] Tile size and lay direction confirmed — that's what drives the extra for cuts
[ ] You're happy with 10% extra for cuts, or you've told us to change it
[ ] Waterproofing, screed and floor prep are NOT in these numbers
[ ] You've re-checked at least two numbers by hand against the plan
```
