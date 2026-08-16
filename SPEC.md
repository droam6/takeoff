# SPEC — What TAKEOFF measures, and for whom

TAKEOFF is a done-for-you plan-measurement service. A tradie sends a plan set; we send
back a room-by-room m² breakdown with every number showing its working, plus a list of
questions we need answered before the numbers can be used to quote.

This document defines **what we output**. `TAKEOFF_METHOD.md` defines **how we get there**.
`INTAKE.md` defines **what we require before we start**.

---

## 1. The tiler's takeoff

A tiler quotes labour and material off area. The numbers they need are not "the floor
plan area" — they are the *tiled surface* areas, split by tile type, because different
tiles have different rates, different wastage, and different setout.

### 1.1 Floor area, per room (m²)

- Measured as the **internal floor polygon** from the printed plan dimensions.
- Rooms are rarely rectangles. Stepped walls, nibs and alcoves are measured as a
  rectilinear polygon (band-by-band), never as `overall width × overall depth`.
  > A bounding-box read of the Master Ensuite in the sample set gives 19.9 m². The
  > actual internal polygon is 13.4 m². That is a 6.5 m² / ~$1,000 error on one room.
- **Deducted** from the floor: anything sitting on the floor that the tiler does not
  tile under —
  - built-in bath surrounds / hobs (tiled platform, not floor);
  - floor-standing joinery (vanity, laundry cabinetry) — deducted;
  - shower seats / benches built off the slab;
  - **not** deducted: wall-hung vanities (300 mm clear underneath → tiles run through),
    WC pans, wall-facing toilets, floor wastes.
- Deductions are always listed as separate line items so the tradie can add one back if
  their scope differs.

### 1.2 Wall tile area, per wall (m²)

Measured **per elevation**, as `run length × true tiling height`.

- **True tiling height, not assumed ceiling height.** This is the single biggest source
  of error in an amateur takeoff. Real cases in the sample set:
  | Room | Assumed | Actual |
  |---|---|---|
  | Laundry | 2700 full height | 450 mm splashback over a 2525 bench only |
  | Main Bath, over-bath wall | 2700 from floor | 2150, starting at the 550 bath rim |
  | Main Bath, shower nib | 2700 | 1200 high nib wall |
  | Powder Room | 2700 tiled | 300 mm tile skirting; walls are textured finish |
- Where a ceiling is **raked**, the wall is measured as a trapezoid
  (`run × (h_low + h_high) / 2`), not a rectangle.
- Where the tiling height is not printed, it is **not assumed** — it becomes a question.

### 1.3 Feature-tile zones, measured separately (m²)

Feature tile is a different SKU at a different rate, often laid in a different direction
("FEATURE TILE LAID VERTICALLY" appears five times in the sample set). It is measured and
reported as its own line, **not** merged into the wall total for that room.

### 1.4 Niches (m² and each)

Each niche is reported as a count **and** an area, with the area broken into
back + reveals:

```
back        = w × h
reveals     = 2 × (d × h)  +  2 × (w × d)
```

Niche depth is very often not on the drawing. If it is missing, we say so rather than
picking 70 or 100 mm silently.

### 1.5 Openings deducted

Deducted from the wall run they sit in, and always shown as a line item:
door openings, window openings, shower-screen glazed panels (where the tiler does not
tile behind), and any wall recess taken by joinery.

Openings whose height is not dimensioned are flagged; a provisional height is used
**only** where marked as an assumption.

### 1.6 Wastage

Reported as a **toggle, not a baked-in number**:

| Column | Meaning |
|---|---|
| Measured | The surveyed quantity. No allowance. |
| +10% | Default wastage for straight-lay, rectangular rooms |
| +15% | Suggested where the room has a raked ceiling, diagonal/herringbone lay, many cuts, or large-format tile |

The tiler picks. We show both. We never present a wastage-adjusted number as the
measured number.

### 1.7 Also reported for tilers

- **Linear metres**: tile skirting, shower hobs, bullnose/mitred external corners
  (the sample set specifies mitred corners throughout — that is a labour cost).
- **Floor waste / fall**: noted where shown, because graded falls change cut counts.
- **Waterproofing area**: floor + upturns, as a separate line where asked for.

---

## 2. The painter's takeoff

Painters quote off area too, but a *different* area: the surfaces the tiler leaves alone.

### 2.1 Wall area (m²)

`wall perimeter × ceiling height`, then **minus**:
- every tiled area from §1.2 (a wall that is tiled is not painted);
- door and window openings;
- full-height joinery runs.

For rooms that are part-tiled, the painted area is the balance above the tile line —
e.g. the Laundry is 2700 high with a 450 splashback, so the painted band above the bench
is real and must be measured, not ignored.

Where finishes are specified separately ("TEXTURED FINISH TO WALLS" in the Powder Room),
those areas are reported as their own line because they carry a different rate.

### 2.2 Ceiling area (m²)

- Flat ceiling: equals the gross floor polygon (**not** the net-of-joinery floor number —
  the ceiling runs over the vanity).
- Raked ceiling: the sloping plane area, `plan area × 1/cos(θ)`, or measured directly off
  the section if one is provided. If the rake is undimensioned we ask.

### 2.3 Also reported for painters

- Trim linear metres: skirting, architraves, door/window reveals.
- Coat count and substrate notes where the drawing states them.
- Wastage toggle: painters typically want +5–10%, applied the same way as §1.6.

---

## 3. Output format (every job)

Every `TAKEOFF_<job>.md` is delivered in this order:

1. **QUESTIONS FOR YOU** — the intake answers we are missing plus every assumption
   needing confirmation, phrased as plain questions. This leads the document. Always.
2. **Job summary** — sheets read, scale, date, trade, rooms covered.
3. **Per-room tables** — floor, then wall-by-wall, then niches, with the arithmetic shown
   inline (`2570 × 3895 = 10.010 m²`), plus a **confidence rating** (HIGH / MED / LOW).
4. **Totals per material** — floor tile, wall tile, feature tile, skirting, painted wall,
   painted ceiling.
5. **Wastage-adjusted totals** — measured / +10% / +15% side by side.
6. **Assumptions register** — numbered, each phrased as a question to the tradie.
7. **Cross-check log** — every verification from `TAKEOFF_METHOD.md` §5 with pass/fail.
8. **CONFIRM BEFORE QUOTING** — the checklist the tradie ticks before the number leaves
   their hands.

## 4. What we deliberately do **not** do

- We do not scale off the drawing. Ever. Printed dimensions only.
- We do not price. We measure. Rates are the tradie's business.
- We do not silently pick a number to fill a gap. A gap becomes a question.
- We do not deliver a job that failed intake. We tell them what to send instead.
