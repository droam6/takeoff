# STRESS REPORT — nine plan sets we didn't choose

**Run:** 16 August 2026 · `backtest/backtest.py` · structure probe over 9 sets
**Sources:** `backtest/SOURCES.md` · **Scoreboard:** `backtest/RESULTS.md`

The sample set in this repo was supplied by a customer and I measured it by hand. That
proves the method works on one set of drawings I had already read. It proves nothing about
drawings I hadn't.

So: eight real plan PDFs pulled off the open web — NSW council DA trackers, published
sample working drawings, an ABCB reference set — plus one raster case, all run through the
gate cold.

**5 passed, 4 rejected.** The headline is not the split. It's that **three of the four
rejections were rejected for a reason that isn't true**, and **one of the five passes should
have been rejected.**

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
