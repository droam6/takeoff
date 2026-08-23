# HELD-OUT TEST — six strangers' drawings against the frozen product

**Run:** 23 August 2026 · product frozen at commit `43296d4` — no edits to `takeoff.py`,
`TAKEOFF_METHOD.md`, `INTAKE.md`, `SPEC.md`, `BRAND.md`, any threshold, logic or template
during the run. Crashes counted as results; defects logged, not fixed.

**Caveats, stated up front:**

- **The labels are prediction-based.** The human labels were assigned from the stage-1
  source descriptions without opening the files. Where gate and label disagree, neither
  side is ground truth; the per-set notes record what inspection of the file suggests,
  clearly marked as post-hoc.
- **The stage-1 hunter saw the files before the gate did.** The same session that ran
  this test found, downloaded and inventoried the sets (page counts, sheet titles, DA
  subjects). Selection was contaminating in that weak sense; no gate, probe or
  measurement ran before stage 2.
- **In-session run.** The pipeline was driven as `python3 takeoff.py <pdf> --job …`
  per the QUICKSTART flow with `--intake-only`; the headless `claude` subprocess cannot
  launch in this environment, so this evaluates **gate + verdicts + letters + templates**.
  The local-machine plumbing (subprocess, timeouts) is tested separately. No set reached
  the measurement stage (see scoreboard), so the method itself was not exercised here.
- **Label → verdict mapping used for grading:** *floors-only* ↔ PARTIAL · *scan* ↔ FAIL ·
  *marketing* ↔ FAIL.

## Human vs gate scoreboard

| Set | Human label | Gate verdict | Agree? | Deliverable produced |
|---|---|---|---|---|
| `arei-example-plan.pdf` | floors-only | 🛑 **FAIL** — plan_pages, elevation_pages, wet_area_elevations | **✗** | `REJECTED_…md` |
| `bodc-da137-dwelling.pdf` | floors-only | 🟨 **PARTIAL** — wet_area_elevations only | ✓ | `PARTIAL_…md` (floors-first letter) |
| `bodc-da142-dwelling.pdf` | floors-only | 🛑 **FAIL** — dimension_chains (7 · 0.28/page), wet_area_elevations | **✗** | `REJECTED_…md` |
| `uralla-da45-2020-313-gostwyck-rd.pdf` | scan | 🛑 **FAIL** — 0 extractable characters, all text checks | ✓ | `REJECTED_…md` |
| `desirehomes-coen-283.pdf` | marketing | 🛑 **FAIL** — 30 chars, 0 dimension tokens/chains | ✓ | `REJECTED_…md` |
| `dp-wilston-house-extension.pdf` | floors-only | 🟨 **PARTIAL** — wet_area_elevations only | ✓ | `PARTIAL_…md` (floors-first letter) |

**Agreement 4 / 6.** Both disagreements are the gate rejecting a set the human labelled
floors-measurable. No full takeoff was demanded: zero sets passed the full gate, so the
"two best PASS sets" cap never bound and the measurement method was not invoked.

## Per-set check log

Exit codes behaved as QUICKSTART documents them: FAIL → 1, PARTIAL → 0, `--intake-only` → 0.

### `arei-example-plan.pdf` — label floors-only, gate FAIL ✗

encryption ✓ · page_count ✓ (9) · text_layer ✓ (25,412) · text_density ✓ (2,824/pp) ·
text_quality ✓ (99.8%) · word_hit advisory ✓ (38%) · dim_tokens ✓ (558) ·
dim_chains ✓ (91 · 10.11/pp) · dimensioned_pages ✓ (9) ·
**plan_pages ✗ ("no floor plan among the 1 sheet(s) we could name")** ·
**elevation_pages ✗** · **wet_area_elevations ✗**

Post-hoc note (not the label's evidence): the stage-1 inventory saw the strings
"FLOOR PLAN" and "ELEVATIONS" in this file's sheet list. The scored title detector named
only 1 of 9 sheets on this practice's title-block style — the round-1 failure family
(title under-detection) surviving round 2's fix on an unseen layout. The letter's
plan-pages wording stays honest ("we read sheet names on 1 of 9 sheets…"), which is the
round-2 wording rule doing its job even while the verdict is wrong per the label.

### `bodc-da137-dwelling.pdf` — label floors-only, gate PARTIAL ✓

All text and chain checks ✓ (58,346 chars · 99.5% · 2,035 tokens · 208 chains, 5.94/pp) ·
plan_pages ✓ (5) · elevation_pages ✓ (3) · **wet_area_elevations ✗** → PARTIAL, floors-first
letter written. Exactly the labelled shape.

### `bodc-da142-dwelling.pdf` — label floors-only, gate FAIL ✗

encryption→dimensioned_pages ✓ except **dim_chains ✗ (7 chains · 0.28/page — needs 5 and
0.4/page)**; plan_pages ✓ (2) · elevation_pages ✓ (3) · **wet_area_elevations ✗**

The chains *count* passed (7 ≥ 5); the *per-page rate* failed on a 25-page pack where
most pages are planning documents, not drawings. Post-hoc note: the file is clean vector
text (99.5% usable), so the rejection letter's diagnosis — "what OCR'd scans look like"
— is a confidently wrong statement sent to a customer holding an original. **Letter
defect logged** (see defects). The per-page denominator counting non-drawing pages is a
threshold-shape defect, also logged.

### `uralla-da45-2020-313-gostwyck-rd.pdf` — label scan, gate FAIL ✓

**0 extractable characters**; every text/dimension/sheet check fails; rejected with the
scan letter (re-export from drawing software). Right verdict, right reason, right remedy.

### `desirehomes-coen-283.pdf` — label marketing, gate FAIL ✓

text_layer ✗ (30 chars) · dim_tokens ✗ (0) · dim_chains ✗ (0) · sheets ✗. Observation
(not a defect): text_density *passed* — 30 chars on 1 page clears the 20/page average —
a reminder that per-page averages degenerate on single-page files; text_layer's absolute
floor is what caught it.

### `dp-wilston-house-extension.pdf` — label floors-only, gate PARTIAL ✓

All hard checks ✓ (79,866 chars · 110 chains, 4.23/pp · 5 plans · 2 elevations) ·
**wet_area_elevations ✗** → PARTIAL, floors-first letter. Notably the 12 pages of
engineering/bore-log content did not sink the chains rate here (4.23/pp).

## Whole-run counts

| Count | Value | Detail |
|---|---|---|
| **Crashes** | **0** | Six runs, six clean verdicts, exit codes per spec |
| **Wrong verdicts** | **2 of 6** (vs prediction-based labels) | `arei` (title under-detection → FAIL instead of PARTIAL), `bodc-142` (chains/page rate → FAIL instead of PARTIAL) |
| **Silent guesses** | **0** | No set reached measurement, and no letter contains a quantity; nothing shipped a number without its flagged assumption |

## Defects logged (frozen run — none fixed)

1. **Title under-detection, third appearance.** The scored `sheet_title` detector named
   1 of 9 sheets on `arei` and turned a floors-measurable set into a rejection. Round 2
   fixed the *wording* of this failure family; the *detection* still fails on unseen
   title-block styles.
2. **`dimension_chains` per-page rate uses all pages as denominator.** DA packs bundle
   planning reports with drawings; `bodc-142`'s 7 verified chains over 8 dimensioned
   sheets became 0.28/page over 25 pages and failed. The threshold is tuned-on-corpus
   (labelled as such since round 3) and this is what that label warned about.
3. **The chains-failure letter asserts "looks like an OCR'd scan" unconditionally.**
   Sent for `bodc-142`, whose text is 99.5% clean vector — a confidently wrong diagnosis
   to a customer holding an original. The letter's escape hatch ("if this is already the
   original, let us know") softens but does not fix it.
4. **The `wet_area_elevations` failure text assumes elevations exist.** On `arei` (0
   elevations found) the letter still says "the elevations in this set look like external
   elevations" — a template that doesn't degrade when the count is zero.

## Bottom line

**Does the current product work on strangers' drawings? Partly — the honest half works,
the reading half still stumbles.** It never crashed, never guessed, never shipped an
unflagged number, and put the right letter on 4 of 6 doors including both junk inputs.
But both misses are the same lesson the corpus already taught: the gate's *reading* of a
set (sheet naming, chains-per-page over mixed packs) is brittle on layouts it hasn't
seen, and each miss turns a same-day floors job into a rejection letter — lost revenue,
not lost trust. The failure wording rules held even when the verdicts were wrong, which
is why these are commercial defects rather than credibility defects.
