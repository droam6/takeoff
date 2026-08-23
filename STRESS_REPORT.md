# STRESS REPORT — nine plan sets we didn't choose

> **CURRENT RESULT — Round 4 (23 August 2026), with model page recognition, honest
> letters and the drawing-page denominator: 12 of 13 runnable sets agree with their
> labels across both corpora** — both held-out misses fixed, one new miss (`ncc`, whose
> pathological text layer is now the gate's sharpest known edge, logged for round 5).
> See [ROUND 4](#round-4--letters-model-page-recognition-and-the-honest-denominator).
> Rounds 1–3 and JOB 2 below are kept because they document what each round fixed; their
> headline numbers are superseded. (Round 2's "scanned and OCR'd" diagnosis of `ncc` was
> itself wrong — round 4 established it is vector CAD with a corrupt text encoding.)

**Run:** 16 August 2026 · `backtest/backtest.py` · structure probe over 9 sets
**Sources:** `backtest/SOURCES.md` · **Scoreboard:** `backtest/RESULTS.md`

The sample set in this repo was supplied by a customer and I measured it by hand. That
proves the method works on one set of drawings I had already read. It proves nothing about
drawings I hadn't.

So: eight real plan PDFs pulled off the open web — NSW council DA trackers, published
sample working drawings, an ABCB reference set — plus one raster case, all run through the
gate cold.

**Round 1: 5 passed, 4 rejected** *(superseded — round 2 below is current)*. The headline is
not the split. It's that **three of the four rejections were rejected for a reason that isn't
true**, and **one of the five passes should have been rejected.**

---

## 1. Scoreboard

| Plan set | Pages | Gate | Verdict | Why it matters |
|---|---|---|---|---|
| `sample_plans.pdf` | 25 | ✅ PASS | **Right** | Control. Flags reproduced two findings I'd made by hand. |
| `derbyshire-construction-sample.pdf` | 23 | ✅ PASS | **Right verdict, bad map** | Real VIC construction set with 4 sheets of wet-area internal elevations. Probe reported "no wet areas". |
| `eastcoast-sample-plan-set.pdf` | 30 | ✅ PASS | Right | AU sample set. Scale flag was noise. |
| `creativehomeplans-sample.pdf` | 8 | ✅ PASS | Right | DA-level sample. Passed on thin evidence — 1 plan / 1 elevation sheet detected. |
| `ncc-building-plans-example.pdf` | 50 | ✅ PASS | **WRONG — should have failed** | OCR'd scan. Passed on 578 dimension tokens made of OCR noise. |
| `ssc-da220327-architectural.pdf` | 23 | 🛑 FAIL | **Right verdict, wrong reason** | Real lodged NSW DA. Told "0 floor plan sheets" — it has them. |
| `ssc-da181440-architectural.pdf` | 34 | 🛑 FAIL | **Right verdict, wrong reason** | Same. |
| `housedesigners-working-drawings.pdf` | 12 | 🛑 FAIL | **Wrong reason** | QLD working drawings with plan, elevations and sections. Told "0 floor plan sheets". |
| `phone-scan-of-da-plans.pdf` | 6 | 🛑 FAIL | **Right, for exactly the right reason** | 0 characters, 0 vector geometry. The case the gate exists for. |

---

## 2. What passed, and whether it deserved to

### `sample_plans.pdf` — the control ✅

Passed with 4 plan / 13 elevation sheets and 567 dimension tokens. Two flags, both correct
and both things I had found by hand over several hours:

- *mixed scales in one set (1:20, 1:25)* — true, sheet 12.01 is the odd one out
- *no sections — raked ceilings could not be resolved* — true, and it is precisely why the
  master ensuite walls are still unquotable

That the probe rediscovers those in 7 seconds is the most encouraging result in the run.
The deterministic layer is doing real work, not decorating.

### `derbyshire-construction-sample.pdf` — passed, but the map was wrong ⚠

A genuine Victorian construction-documentation set: cover, notes, site, floor plan, slab
setout, external elevations, RCP, electrical, roof, **four sections**, door and window
schedules, and **four sheets of plan details and internal elevations** covering master
ensuite & WIR, bath, laundry, pantry and kitchen.

That is a fully measurable job. The probe reported **"no wet areas identified by sheet
title"** and **"no sections"** — both false.

Cause: the sheet names run over two lines (`PLAN DET. & INT. ELEV -` / `MASTER BED ENS. &
WIR`), and `_sheet_title` reads a single line. The room detector never saw the word
"ensuite". The section sheets are titled `SECTION 1`…`SECTION 4 SHT.2` and *were* counted by
the gate — but the probe's own section check looked at a different field.

Nobody would have been harmed: it passed, and a human would have caught it. But an
automated "we found no wet areas in your set" on a set with four wet-area sheets is exactly
the kind of confidently wrong statement the whole product is supposed to avoid.

### `creativehomeplans-sample.pdf` and `eastcoast-sample-plan-set.pdf` — passed, correctly, on thin evidence

Both are DA-level sample sets published by AU designers. Both correctly reported no wet-area
elevations. But `creativehomeplans` passed the gate on **one** detected plan sheet and
**one** elevation sheet out of eight pages, which is under-detection getting the right answer
by luck rather than by reading.

### `ncc-building-plans-example.pdf` — passed, and shouldn't have 🛑

The one that matters.

This is the Australian Building Codes Board's *Building plans and documentation* reference
set: 50 sheets, **scanned and then run through OCR**. The text layer it carries is noise:

```
I§J          C---'        '<:::; BAY RD851        00 UJ        C') ='
```

The gate saw 105,247 extractable characters, 2,105 characters per page, and **578 "mm
dimension tokens"** — and passed it on all four text checks.

Every one of those numbers is an artefact. `DIM_RE` matches any 2–5 digit integer between 20
and 20000, and OCR garbage on a drawing produces those by the hundred. The gate's entire
premise is *we can read the printed dimensions*, and it never actually tested that premise —
it tested that integers exist.

**This is a scanned document that got through the scan detector.** It is commercial rather
than residential, and I kept it deliberately for that reason: it is the input most likely to
defeat a naive text-layer check, and it did.

---

## 3. What failed, and whether the gate was right

### `phone-scan-of-da-plans.pdf` — RIGHT, for the right reason ✅

Six pages of a real DA set flattened to images. Zero characters, zero vector geometry.
Rejected on four checks in 0.0 seconds, and the letter it generated is the letter I would
want sent:

> **✗ 0 extractable characters (need 200)**
> **What this means:** The file is a scan or photo, so the dimensions are pixels rather than
> numbers I can read. We won't OCR them and we won't scale off the drawing.
> **What to send:** Ask your designer to re-export the PDF straight out of their drawing
> software — not printed and scanned.

Correct verdict, correct reason, correct remedy, no cost incurred. This is the gate working
exactly as designed.

### The three DA / working-drawing sets — right instinct, false statement 🛑

`ssc-da220327`, `ssc-da181440` and `housedesigners` were all rejected with:

```
0 floor plan sheet(s) detected;  0 elevation sheet(s) detected
```

**All three contain floor plans.** The two Sutherland Shire sets are real lodged NSW
residential DAs — 23 and 34 sheets of site plans, floor plans, elevations and sections. The
House Designers set is a published QLD working-drawing example with a floor plan, four
elevation sheets and sections.

Cause: `_sheet_title` takes the shortest all-caps line carrying a drawing-type keyword, and
on these sets the title block is dominated by copyright boilerplate —

```
THESE DRAWINGS ARE THE PROPERTY OF PLAN LAND.
PLAN LAND ACCEPTS NO LIABILITY OR ...
NOTIFY PLAN LAND ...
```

— which contains the word **PLAN**, in capitals, on almost every page. The heuristic locked
onto the boilerplate and never found the sheet names.

**Was the gate right to fail them?** On outcome, mostly yes: none of the three carries
dimensioned internal elevations of wet areas, so none of them can support a wall-tile
takeoff. The correct behaviour was *pass the gate, then flag "no wet-area elevations — floors
only, or send the internal elevations"*.

Instead we told a tradie his drawings contain no floor plan. That is not a judgement call he
can argue with — it is a factual claim about his own file, and it is wrong. He opens the PDF,
sees the floor plan, and concludes we can't read drawings. **In a business whose entire
pitch is "our numbers are right", a confidently false rejection letter does more damage than
a missed job.**

---

## 4. Suspicious numbers

| Number | Where | Why it's suspicious | Reasoning |
|---|---|---|---|
| **578 dimension tokens** | `ncc-...` | Should be ~0 | It's an OCR'd scan. The tokens are noise passing a numeric filter. |
| **1:1, 1:3, 1:4, 1:6, 1:8, 1:10** | `eastcoast-...` | Not drawing scales | The regex matches any `1:N` in the text. These are mortar mixes, roof pitches and floor falls in the notes blocks. The flag fires on every set with a specification note. |
| **1 plan sheet / 8 pages** | `creativehomeplans-...` | Too few | A DA set with a location plan, survey plan, site plan and floor plans should register more than one. Under-detection again. |
| **"no sections"** | `derbyshire-...` | Demonstrably false | Four sheets titled `SECTION 1`–`SECTION 4 SHT.2`. |
| **13 elevation sheets** | `sample_plans.pdf` | Over-count | There are 11 elevation sheets. Two 3D sheets carry the word in an annotation. Harmless here, but it's the same fragility in the other direction. |
| **2,105 chars/page** | `ncc-...` | Suspiciously high | Real drawing sheets run 800–1,700. Well above that usually means OCR spray, not richer annotation. Worth using as a signal. |

Nothing in the *measured* numbers is suspicious — no measurement was produced for any set
except the control, because the model takeoff was only run on the control and was still
running when this was written. **That is itself a limit of this report**, stated rather than
papered over: this run tests the gate and the structure probe hard, and the measurement
method not at all beyond the set I'd already checked by hand.

---

## 5. Top 3 weaknesses

### 1. Sheet-title detection is a single point of failure, and it fails silently

Two of the gate's nine checks (plan sheets, elevation sheets), the entire room map, and the
"measurable / floors-only" decision all hang off one fragile heuristic: *the shortest
all-caps line containing a drawing-type keyword.*

It broke on **4 of 9 sets** — three into a false rejection, one into a false "no wet areas".
It broke on the two most realistic inputs in the whole run, the actual lodged council DAs.

The failure is silent: nothing in the output says *"I couldn't find a sheet name on any
page"*, which is a very different statement from *"this set has no floor plan"*.

**Fix:** decide from content, not titles. A page with a closed grey wall polygon and
orthogonal dimension chains is a plan; a page with one long horizontal run and vertical
height chains is an elevation. The vector-geometry extraction that measured the sample set
already does this — it just isn't wired to the gate. Keep titles as a secondary signal, read
multi-line titles, and read the sheet-number field. And when no title can be found at all,
say *that*, not something stronger.

### 2. The gate tests that text exists, not that it can be read

Checks 1–4 are satisfied by any OCR'd scan. `ncc-building-plans-example.pdf` walked through
all of them on garbage. Since "we work from a real text layer" is the premise the whole
accuracy doctrine sits on, an unverified premise is the most expensive kind of bug here —
it doesn't produce an error, it produces a confident wrong answer.

**Fix:** a text-quality check before the dimension check. Three cheap signals, any one of
which catches OCR: the proportion of extracted characters outside the set a CAD title block
actually uses; whether dimension tokens sit adjacent to vector geometry or float over an
image; and image-coverage per page (an image covering >80% of a sheet is a scan regardless
of what text is layered over it). `ncc` fails all three.

### 3. The flags cry wolf

Every passing set drew a *mixed scales* flag, mostly from `1:3` mortar mixes and `1:100`
falls in notes blocks. Every set without a section sheet drew *no sections*, including ones
where nothing is raked.

This is the same failure Part C existed to fix, reappearing in QA clothing. A takeoff with
15 undifferentiated questions at the top gets skimmed; a flag list where four of five entries
are noise gets skimmed too, and the one real flag goes with it. On `derbyshire` the noise
flags sat directly above a false claim about wet areas, and nothing distinguished them.

**Fix:** rank flags by whether they can change a number, surface the top few, and put the
rest below the fold — the ANSWER PACK / PROOF split, applied to our own QA output. And scope
the scale regex to sheets' title blocks rather than the whole page.

---

## 6. What I'd do next, in order

1. **Content-based sheet classification.** Fixes weakness 1, and unlocks a real room map.
2. **Text-quality gate.** Fixes weakness 2. Cheap, deterministic, high value.
3. **Never state a stronger fact than we checked.** "I couldn't identify sheet names" ≠
   "this set has no floor plan." A pass through every rejection reason for over-claiming.
4. **Rank the flags.**
5. **Then re-run this harness with `--analyse`** across all five passing sets and score the
   measured numbers, which this run does not do.

---

## 7. Honest limits of this run

- **The measurement method was not stress-tested.** Only the control set was put through the
  full model takeoff, and it was still running at the time of writing. Everything above tests
  the gate and the deterministic probe.
- **One of the nine is derived, not found.** `phone-scan-of-da-plans.pdf` was built by
  rasterising a real DA set, because every third-party scan archive I tried was behind a WAF
  (`403` from Central Darling, Mid-Western, City of Sydney Archives). Documented in
  `SOURCES.md` rather than dressed up as a download.
- **One of the nine is commercial, not residential.** `ncc-building-plans-example.pdf` is an
  office/warehouse set. Kept because it is the best adversarial OCR case available, and it
  earned its place by defeating the gate.
- **Sample size is nine.** Enough to find structural weaknesses. Not enough to estimate a
  rejection rate, which is a number `BUSINESS_PLAN.md` §8 Risk 3 needs and this run cannot
  provide.


---
---

# ROUND 2 — after the fixes

**Re-run:** 16 August 2026, same nine sets, same harness.
**Result: 2 passed, 7 rejected — every verdict right, and every stated reason true.**

The pass count went *down*, which is the point. Round 1 passed five sets; two of those three
new rejections are sets that genuinely cannot support a wall takeoff, and the third is a scan.

## Before and after

| Plan set | Round 1 | Round 2 | Reason stated in round 2 | True? |
|---|---|---|---|---|
| `sample_plans.pdf` | ✅ PASS | ✅ **PASS** | 4 plan / 13 elev (6 internal wet) · 144 chains | ✅ |
| `derbyshire-construction-sample.pdf` | ✅ PASS, "no wet areas" *(false)* | ✅ **PASS** | 4 plan / 6 elev (**4 internal wet**) · 494 chains | ✅ |
| `ncc-building-plans-example.pdf` | ✅ PASS *(should have failed)* | 🛑 **FAIL** | *"6 dimension chains check out (0.12 per page)"* → **text present but not reliably readable** | ✅ |
| `ssc-da220327-architectural.pdf` | 🛑 "0 floor plan sheets" *(false)* | 🛑 **FAIL** | *"**5 floor plan(s)** and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area"* | ✅ |
| `ssc-da181440-architectural.pdf` | 🛑 "0 floor plan sheets" *(false)* | 🛑 **FAIL** | *"**4 floor plan(s)** and 2 elevation sheet(s) found, but none is an internal wet-area elevation"* | ✅ |
| `housedesigners-working-drawings.pdf` | 🛑 "0 floor plan sheets" *(false)* | 🛑 **FAIL** | *"**3 floor plan(s)** and 2 elevation sheet(s) found, but none is an internal wet-area elevation"* | ✅ |
| `creativehomeplans-sample.pdf` | ✅ PASS | 🛑 **FAIL** | *"4 floor plan(s) and 1 elevation sheet found, but none is an internal wet-area elevation"* | ✅ |
| `eastcoast-sample-plan-set.pdf` | ✅ PASS | 🛑 **FAIL** | *"2 floor plan(s) and 4 elevation sheet(s) found, but none is an internal wet-area elevation"* | ✅ |
| `phone-scan-of-da-plans.pdf` | 🛑 FAIL | 🛑 **FAIL** | 0 extractable characters | ✅ |

**Nine for nine on truthfulness.** Every rejection now names what we *did* find before saying
what we didn't — which is the difference between a letter that builds trust and one that tells
a tradie his floor plan doesn't exist.

## What changed

### Fix 1 — readability, not existence

Two new checks sit between "there is text" and "there are numbers".

**Dimension chains that check out.** A chain is a run of two or more labels lying along one
line whose values sum to another printed value within 5 mm — `100 + 840 + 790 = 1730`. Real
drawings are full of them, because that is how a chain is dimensioned. **OCR noise is not:**
random integers do not sum to other random integers on the same axis, within 5 mm, except by
accident.

The separation is not close:

| Set | Chains/page | |
|---|---|---|
| derbyshire | **21.5** | real |
| ssc-da220327 | **9.7** | real |
| housedesigners | **7.2** | real |
| sample_plans | **5.8** | real |
| eastcoast | **3.3** | real |
| creativehomeplans | **1.6** | real |
| **ncc (OCR'd scan)** | **0.12** | **noise** |

Threshold set at 5 chains total and 0.4/page — an order of magnitude below the weakest real
set, and three times above the scan. *(Like every gate threshold, this was tuned on these
nine sets and evaluated on the same nine. No held-out set exists yet: tuned-on-corpus,
pending validation on live jobs.)*

**A text-quality score** — the share of characters that belong on a drawing sheet, and the
share of alphabetic tokens that are real words, scored against an embedded vocabulary rather
than a system dictionary (so the verdict doesn't depend on which machine it ran on).

**Honest finding: the word-hit rate did not do the work.** The OCR'd set scored 0.315 and a
perfectly good set (`eastcoast`) scored 0.307 — the score cannot separate them. **The chain
check is what actually caught the scan.** Reporting the opposite would have been easy and
wrong. *(Follow-through: the word-hit score has since been demoted to advisory — recorded
and warned on in the intake report, never a hard gate. A check that blocks nothing today
could one day block something legitimate.)*

### Fix 2 — sheet titles from the title block

The round-1 root cause was **not** the copyright boilerplate. It was that the old heuristic
required ALL CAPS, and the sets it failed on set their sheet names in **mixed case** —
`Ground Floor Plan`, `Floor Plan - Lower`, `First Floor Plan`. The boilerplate only won
because nothing else was eligible.

Titles are now **scored, not guessed**, on the three signals a real title block always has:

1. the line is large relative to the rest of the page,
2. it hugs a page edge, where title blocks live,
3. a sheet number sits within ~220 pt of it.

Plus: case-insensitive matching, boilerplate excluded by phrase, sentences excluded (a line
ending in "." with more than three words is prose, not a name), and **wrapped names joined** —
so derbyshire's `PLAN DET. & INT. ELEV. -` / `BATH & BED 3` is read as one title instead of
two fragments.

Result on sheet-name recognition:

| Set | Round 1 | Round 2 |
|---|---|---|
| `sample_plans` | 25/25 | 25/25 |
| `ssc-da220327` | 0 named | 15/23, incl. 5 floor plans |
| `ssc-da181440` | 0 named | 10/34, incl. 4 floor plans |
| `housedesigners` | 0 named | 8/12, incl. 3 floor plans |
| `derbyshire` | wet areas missed | 4 internal wet-area elevation sheets found |

### Fix 3 — only verifiable facts, and a new honest reason

Rejection messages now state what was established and nothing stronger:

- Sheets were named and none is a plan → *"no floor plan among the 15 sheets we could name"*
- No sheet could be named at all → *"couldn't confidently identify any sheet names across 23
  sheets — that may be our end, not yours"*
- Never *"0 floor plan sheets detected"* off a failed guess.

And the check that legitimately rejects a DA set now exists: **wet-area elevations.** An
elevation sheet counts as an internal wet-area elevation when it carries at least four
distinct wet-area terms including at least one *fitting* (basin, vanity, shower, mixer,
splashback, niche, hob, screen) and at least five dimension tokens.

That threshold came from the data, not from taste:

| Sheet | Wet terms found | |
|---|---|---|
| derbyshire internal elevations | basin, bath, ens, laundry, mixer, shower, splashback, tile, toilet (**9**) | internal ✅ |
| derbyshire *external* elevations | powder, shower (**2**) | external ✅ |
| ssc-da220327 elevations | laundry, wc (**2**) | external ✅ |
| ssc-da181440 elevations | bath, toilet (**2**) | external ✅ |

The 2-vs-9 gap is the difference between a room label leaking onto an external elevation and
a sheet that actually draws the bathroom wall.

### Fix 4 — the flags stopped crying wolf

The scale flag now requires **scale context** — `1:100 @ A3`, or the word *scale* within 18
characters — so it no longer fires on `1:3` mortar mixes, `1:100` floor falls or roof pitches.
`eastcoast` went from nine bogus "scales" to none. `sample_plans` still correctly reports its
real 1:20 / 1:25 mix, and `derbyshire` reports a genuine 1:1 / 1:50 / 1:100 / 1:200 spread.

Flags are also now only raised when true of that set: "no sections" only fires where there
are wet-area elevations that might be raked, and a new flag reports when sheet names were
read on fewer than half the sheets, so an incomplete room map announces itself.

## What this run cost us, honestly

**Two sets that previously passed now fail** — `creativehomeplans` and `eastcoast`. Both are
DA-level sample sets with external elevations only. Rejecting them is correct *for a wall
quote*, and the letter says so and offers floors-only instead. But it is worth stating plainly
that the gate is now stricter, and that the right commercial answer to most of these
rejections is **"we can still do your floors"** rather than "no".

That reframes Risk 3 in the business plan: of nine sets, **two were genuinely unreadable**
(`ncc` is OCR spray, `phone-scan` is a raster) and **five could be measured for floors but
not walls.** The addressable failure isn't unreadability — it's missing internal elevations,
and there's a product on the other side of it.

---
---

# ROUND 3 — the PARTIAL tier

**Re-run:** 23 August 2026, fresh machine, `backtest/backtest.py`, structure probe.
**Result: 2 PASS · 5 PARTIAL · 2 FAIL — every verdict right, every stated reason true.**

## What changed

The gate now returns three verdicts instead of two:

- **PASS** — every hard check passed. Full takeoff.
- **PARTIAL** — dimensioned floor plans, but no internal wet-area elevations (the only
  hard failures are the wall-evidence checks). **This is a job, not a rejection:** a
  floors + tile-skirting takeoff is produced now, its walls section reads *"Walls: not
  measured — this set has no internal wet-area elevations. Send the internal elevations
  and we'll add every wall,"* and a `PARTIAL_<job>.md` letter goes with it naming exactly
  which sheets unlock the rest.
- **FAIL** — anything else. Rejection letter, nothing measured.

Round 2 already knew the commercial answer to most rejections was "we can still do your
floors" — but offered it only in the last line of a rejection letter, with no floors-only
deliverable defined anywhere. Round 3 turns the most common real-world input into the
product's default smaller job. Also in this round: the word-hit score was demoted to
advisory (round 2 showed it separates nothing), and every threshold is now labelled
tuned-on-corpus pending live validation.

## Scoreboard

**Corpus availability, stated plainly:** this run was made on a fresh machine.
5 of the 8 web sets re-downloaded fine; the two Sutherland Shire DA sets now 403 behind
the council's WAF, and `phone-scan` is derived from one of them, so those three were
**not re-run** — their verdicts below are mapped from their recorded round-2 check
results (the mapping is mechanical: which checks failed decides the verdict). One new
derived set was added to exercise the tier: the control with its 6 internal wet-area
elevation sheets removed.

| Plan set | Round 2 | Round 3 | How |
|---|---|---|---|
| `sample_plans.pdf` | ✅ PASS | ✅ **PASS** · 4 plan / 13 elev (6 internal wet) · 144 chains | re-run |
| `derbyshire-construction-sample.pdf` | ✅ PASS | ✅ **PASS** · 4 plan / 6 elev (4 internal wet) · 494 chains | re-run |
| `ssc-da220327-architectural.pdf` | 🛑 FAIL | 🟨 **PARTIAL** — 5 floor plans, no internal wet elevations | mapped from round-2 checks (WAF blocks re-fetch) |
| `ssc-da181440-architectural.pdf` | 🛑 FAIL | 🟨 **PARTIAL** — 4 floor plans, no internal wet elevations | mapped from round-2 checks (WAF blocks re-fetch) |
| `housedesigners-working-drawings.pdf` | 🛑 FAIL | 🟨 **PARTIAL** · 3 plan / 2 elev · 86 chains | re-run |
| `creativehomeplans-sample.pdf` | 🛑 FAIL | 🟨 **PARTIAL** · 4 plan / 1 elev · 13 chains | re-run |
| `eastcoast-sample-plan-set.pdf` | 🛑 FAIL | 🟨 **PARTIAL** · 2 plan / 4 elev · 100 chains | re-run |
| `ncc-building-plans-example.pdf` | 🛑 FAIL | 🛑 **FAIL** — 0.12 chains/page: text present but not reliably readable | re-run |
| `phone-scan-of-da-plans.pdf` | 🛑 FAIL | 🛑 **FAIL** — 0 extractable characters | mapped from round-2 checks (source set unavailable) |
| `sample-floors-only-derived.pdf` *(new)* | — | 🟨 **PARTIAL** · 4 plan / 7 elev (0 internal wet) · 93 chains | derived + run |

Every PARTIAL set gets the *floors first* letter instead of a rejection: what's being
measured today, what the gap is, and that sending the internal elevations adds every wall
to the same job. Full letters in `backtest/RESULTS.md`.

## What this means commercially

Round 2's framing stands, sharpened: of nine sets we didn't choose, **two are genuinely
unreadable and five are floors-only** — and floors-only is now a deliverable with a
defined document, a defined letter, and a harness-tested path, not a hypothetical in the
last line of a rejection. The most likely real-world job is a PARTIAL one, and the product
now treats it as the default smaller job rather than a failure.

## Honest limits of this round

- **The structure probe ran; the model takeoff did not.** Verdicts and letters are
  harness-tested; no measured numbers were produced in this round.
- **Three of nine corpus sets were mapped, not re-run** (WAF). The mapping uses their
  recorded round-2 per-check results, and the verdict function is deterministic in those
  results — but a live re-run on the original machine should confirm it.
- **The derived floors-only set shares geometry with the control.** It proves the PARTIAL
  path, not the gate's behaviour on unfamiliar floors-only drawings — the three re-run
  DA-level sets cover that.
- Thresholds remain tuned-on-corpus. Nothing in this round adds held-out validation.

---
---

# JOB 2 — the measurement method on unfamiliar drawings

**Run:** 23 August 2026 · **in-session model runs** — the headless `claude` subprocess
cannot launch in this remote environment, so the model performed both takeoffs directly,
following `TAKEOFF_METHOD.md`; the subprocess pipeline itself still gets exercised on the
local machine separately. Deliverables: `backtest/TAKEOFF_derbyshire.md` / `.pdf` (full)
and `backtest/TAKEOFF_eastcoast.md` / `.pdf` (PARTIAL tier). This is the first time the
measurement method has run end-to-end on plan sets nobody here had measured before.

## Headline results

| Set | Tier | Floors | Walls | Other |
|---|---|---|---|---|
| `derbyshire` (VIC construction set) | FULL | **28.179 m²** measured → 31.0 m² order | **30.606 m²** measured → 33.7 m² order | 0.578 m² mosaic splashback · 4.26 m tile skirting · laundry splashback + skirting held as questions |
| `eastcoast` (QLD quote set) | PARTIAL | **~25.7 m² provisional — nothing order-grade** | not measured (no internal elevations) — the standing offer sent instead | empty ORDER THIS box, and that is the correct output |

## Did the method hold? Mostly — and where it strained, it strained loudly.

### What measured clean (derbyshire)

A completely different practice style from the control — 1:100 plan + 1:50 plan details
with internal elevations, mixed-case titles, joinery-heavy — and the method's core loop
worked unchanged: chains → polygons → elevation heights → checks. **Every dimension chain
closed to 0 mm**, including the house-length chain (20,185) and six independent ceiling
chains that each sum to exactly 2,700 by different routes (300+1,500+40+560+300 ·
450+500+1,750 · 900+150+600+1,050 · 500+1,000+300+900 · 600+2,100 · 300+1,350+150+900).
Rooms closed both ways round. Fixture cross-checks landed (the 1800 bath, 900 benches on
every sheet, 2,100 screens twice).

### What the checks caught that a naive read would have guessed

- **Tile bands, not tiled rooms.** This practice tiles a 900-high band in the ensuite and
  full height only on feature/shower walls — the heights are printed and differ wall by
  wall (900 / 300 under-vanity / 150 splashback / 2,700). A naive "room × 2,700" read
  would have roughly **doubled the ensuite wall figure**. The §5.6 sanity ratio fired at
  1.34/1.82 (below the 2.0–5.5 band) precisely because of this — and the right response
  was to explain the flag, not suppress it: the ratio range itself assumes full-height
  tiling and needs a caveat for band-tiled practices.
- **Windows that don't exist inside.** Rev A plastered W2 and W2A over internally
  (clouded on the ensuite sheet). A reader working from the window schedule would have
  deducted two openings from walls that no longer have any. The revision-cloud rule
  (§4) is what surfaced it.
- **The laundry sheet with no lengths.** A19 prints vertical chains only — not one
  horizontal dimension. Bench run and skirting runs are genuinely unmeasurable, so the
  laundry splashback (~1.6 m²) and skirting (~4 m) shipped as questions instead of
  quantities. A naive read would have scaled them off the 1:50 detail.
- **A bathroom with no bath, a bedroom with tile.** The room called BATH is a shower
  room; the only tub is in the ensuite. And BED 3's floor is marked TILES while BED 2 is
  carpet — flagged for confirmation rather than silently priced either way.
- **Scope cliff.** Entry, passage, kitchen, dining, living and bed 3 are all tiled on
  the plan — several times the wet-area quantity — and the kitchen splashback is glass,
  not tile. Both went to NOT INCLUDED with a question, not into the totals.

### Where the method strained

- **§5.3 (wall runs vs floor perimeter) lost its independence.** Derbyshire's internal
  elevations print height chains but no run lengths, so both sides of the check derive
  from the same plan chains. It still closed (13,780 = 13,780; 12,560 = 12,560) but as a
  consistency check, not the two-sheet cross-check it is on the control set. The method
  should record which sheets each side came from and say when they're the same.
- **The eastcoast finding — the PARTIAL premise has a floor of its own.** The gate's
  PARTIAL logic assumes *dimensioned floor plans ⇒ measurable floors*. Eastcoast passes
  every text/chain check honestly — 100 chains verify, the 17,990 and 10,630 building
  chains close exactly — **and no wet room carries a single printed extent.** It's a
  quote-issue set ("QUOTE SET ONLY – NOT FOR CONSTRUCTION"): the structure is
  dimensioned, the rooms are not. The method's no-scaling rule held (the deliverable is
  an empty order box, provisional zone reads, and a request for the Construction Set),
  but the gate currently can't tell this set from a room-dimensioned one. **Gate idea
  for round 4: a room-level dimension coverage signal — how many enclosed room polygons
  have ≥2 printed extents adjacent — so PARTIAL can say "floors measurable" vs "floors
  provisional" before any measuring starts.**

## Suspicious numbers, with reasoning

| Number | Where | Why it's suspicious | Resolution |
|---|---|---|---|
| Wall:floor 1.34 / 1.82 | derbyshire ENS/BATH | Below the 2.0–5.5 sanity band | Real: band tiling. Every height traces to a printed chain. Flag explained, not suppressed |
| 3,610 vs 3,620 | derbyshire bed 2 | Same wall, two values | Reference faces (100 vs 90 ticks); totals agree. Noted, not an error |
| 10 mm segment | bath south chain (1,100 + **10** + 910) | Oddly small | The shower-screen line's own thickness; chain closes to 0 mm with it |
| Laundry bench "2,400" | derbyshire | Not printed anywhere | Provisional from drawn bays; shipped as a question, worth ~1.6 m² |
| Every eastcoast room figure | eastcoast | No printed room extents | All provisional by design; order box left empty |
| 343.17 m² schedule total | eastcoast | Printed but unverifiable at room level | Used as a sanity anchor only |

## Honest limits of this run

- **These are in-session model runs.** The same model that wrote the method executed it;
  the subprocess pipeline (headless CLI, timeouts, file handoff) was not exercised here
  and still needs its local-machine run.
- **Nobody has verified these numbers by hand.** The control set's numbers were
  hand-measured and cross-checked; derbyshire's 28.179/30.606 are chain-verified but
  await a second reader. They are exactly what the answer-form workflow is for.
- **Two sets is two sets.** One construction-documentation practice and one quote-set
  practice. The method generalised across that gap; that is evidence, not proof.

## Verdict on generalisation

**The method generalises; the gate's optimism about floor plans doesn't, and the checks
are the reason we know.** On a real construction set the full loop produced an
order-grade takeoff with every number traceable to a printed chain, and its strains were
visible in the check log rather than hidden in the totals. On a quote set the method
correctly refused to manufacture numbers, and the refusal surfaced a specific, fixable
gate gap. Both documents ship with their uncertainty printed on page 1 — which is the
product working as designed.

---
---

# ROUND 4 — letters, model page recognition, and the honest denominator

**Run:** 23 August 2026 · full harness, both inboxes, model page classification via
committed sidecars (`backtest/page_classes/`) · built from `backtest/HELD_OUT_TEST.md`'s
four logged defects, nothing else.

## What changed

1. **Letters state only verified facts**, and every rejection and PARTIAL letter now ends
   with the appeal line — *"Reckon we've got this wrong? Reply — a human will personally
   look at your file within the day."* Gate misses must convert to human review, not lost
   jobs. The two misdiagnosing templates are gone: the chains letter no longer claims
   "OCR'd scan", the wet-area letter no longer describes elevations it didn't find.
2. **Page recognition is a model task** (sidecar in-session / headless CLI in subprocess
   mode; classes floor_plan · internal_elevation · external_elevation · detail ·
   document · marketing_render · scan), with the deterministic layer unchanged as the
   sole trust authority — a class never makes a quantity. Fallback to title heuristics
   announces itself. (`TAKEOFF_METHOD.md` §0b.)
3. **Chains-per-page counts classified drawing pages only.**

## Round-4 scoreboard vs round 3 — 13 runnable sets, both label sets

| Set | Label | Round 3 | Round 4 | Δ |
|---|---|---|---|---|
| `sample_plans` | PASS | ✅ PASS ✓ | ✅ PASS ✓ | — |
| `derbyshire` | PASS | ✅ PASS ✓ | ✅ PASS ✓ (and now counts exactly 1 floor plan, not 4 title-hits) | — |
| `eastcoast` | floors-only | 🟨 ✓ | 🟨 ✓ | — |
| `housedesigners` | floors-only | 🟨 ✓ | 🟨 ✓ | — |
| `creativehomeplans` | floors-only | 🟨 ✓ | 🟨 ✓ | — |
| `sample-floors-only-derived` | floors-only | 🟨 ✓ | 🟨 ✓ | — |
| `ncc` | FAIL | 🛑 ✓ | 🟨 **PARTIAL ✗** | **NEW MISS** |
| `arei` *(held-out)* | floors-only | 🛑 ✗ | 🟨 ✓ | **FIXED** |
| `bodc-da137` *(held-out)* | floors-only | 🟨 ✓ | 🟨 ✓ | — |
| `bodc-da142` *(held-out)* | floors-only | 🛑 ✗ | 🟨 ✓ | **FIXED** |
| `uralla-da45` *(held-out)* | scan | 🛑 ✓ | 🛑 ✓ | — |
| `desirehomes` *(held-out)* | marketing | 🛑 ✓ | 🛑 ✓ | — |
| `dp-wilston` *(held-out)* | floors-only | 🟨 ✓ | 🟨 ✓ | — |

**Round 3: 11/13 · Round 4: 12/13.** Both held-out misses flipped to correct; one corpus
set regressed. (`ssc-da220327`, `ssc-da181440`, `phone-scan` remain un-runnable on this
machine — a scan classification would fail phone-scan on 0 characters exactly as before,
and the two DA sets' floor plans would classify like the other DA packs; both statements
are inference, not runs.)

## The new miss, dissected — and a discovery about the set itself

`ncc` flipped FAIL → PARTIAL, and the letter now tells its owner "your floor plans are
dimensioned and readable." They are not. Three guards each missed by a margin:

- **Classification told the truth** — and that truth was new: the pages are **vector CAD
  with ~9,500–15,400 vector strokes per page and a corrupt text encoding**, not the
  "scanned and OCR'd" set round 2 diagnosed. Round 2's confident diagnosis was itself
  wrong; the honest classes are floor_plan/detail/elevation, so the recognition layer
  correctly refused to call it a scan.
- **The clean-ratio check passes garbage** (99.5%+): the corrupt encoding emits ordinary
  ASCII, and the word-hit score — demoted to advisory in round 3 precisely because it
  separates nothing — reads 29%, above its old bar.
- **The chain rate crossed the new denominator**: 6 coincidence-chains over 11 drawing
  pages = 0.55/page, over the 0.4 bar that nine sets tuned. Round 2's protection was the
  50-page denominator — a coincidence of document-heavy packs, not a design.

Not fixed this round — round 4 built only from the held-out evidence, and this defect
surfaced during its own re-run. **Logged for round 5** with a proposed fix: require
verified chains *on the floor-plan pages themselves* — a "dimensioned floor plan" whose
own chains never add up is not readable, whatever the set-wide rate says. (ncc's two
floor-plan pages carry garbage tokens and effectively zero verified chains; every real
floor plan in both corpora carries several.)

## Counts for the round

| Count | Value |
|---|---|
| Crashes | **0** (13 sets, two inboxes) |
| Wrong verdicts | **1 of 13** (`ncc`, new) — was 2 of 13 in round 3 |
| Silent guesses | **0** — no letter carries a quantity; but note the PARTIAL letter's fixed phrase "dimensioned and readable" is itself a confident claim the ncc miss falsifies. Same defect family as round 3's letters; goes to round 5 with the fix above |

## Verdict

The seeing task moved to the thing that can see, and both held-out misses — three rounds
of the same title-detection family, and the diluted denominator — flipped to correct
without touching a threshold. The cost was honestly measured: one regression, from a set
whose text layer is pathological in a way no current deterministic check individually
catches, now the sharpest known edge of the gate. The safety net for exactly this case —
the appeal line and the human-review rule — is on every letter it would send.
