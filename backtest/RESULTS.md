# Backtest scoreboard

**Run:** 20260823-060410 · **Depth:** structure probe (gate + extract, no model) · **Plans:** 7

**2 passed · 4 partial (floors + skirting) · 1 rejected · 0 errored**

*Every run archives to `backtest/results/<timestamp>/`; the committed `backtest/RESULTS.md` always holds the latest full run only.*

*Corpus note for this run: 7 of the 9-set corpus. `ssc-da220327` and `ssc-da181440` are
behind the council's WAF (403 on re-fetch) and `phone-scan-of-da-plans` was derived from
one of them, so those three could not be re-run on this machine — their round-2 check
results map to PARTIAL / PARTIAL / FAIL under the new verdicts (`STRESS_REPORT.md` round 3).
`sample-floors-only-derived.pdf` is new: the control set with its 6 internal wet-area
elevation sheets removed, built to exercise the PARTIAL tier.*

| File | Pages | Intake | Why | Rooms found | Headline areas | Flags | Runtime |
|---|---|---|---|---|---|---|---|
| `creativehomeplans-sample.pdf` | 8 | 🟨 PARTIAL | 4 plan / 1 elev (0 internal wet) · 13 chains → floors + skirting now, walls when the internal elevations arrive | none identified | — | ⚠️ mixed drawing scales in one set (1:100 A3, 1:200 A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ elevations are external only - no dimensioned internal wet-area elevations found | 2.4s |
| `derbyshire-construction-sample.pdf` | 23 | ✅ PASS | 4 plan / 6 elev (4 internal wet) · 494 chains | none identified | — | ⚠️ mixed drawing scales in one set (1:1 @ A3, 1:100 @ A3, 1:200 @ A3, 1:50 @ A3) - anyone who scales off it will be wrong on some sheets | 6.1s |
| `eastcoast-sample-plan-set.pdf` | 30 | 🟨 PARTIAL | 2 plan / 4 elev (0 internal wet) · 100 chains → floors + skirting now, walls when the internal elevations arrive | none identified | — | ⚠️ elevations are external only - no dimensioned internal wet-area elevations found<br>⚠️ sheet names read on only 14 of 30 sheets - the room map may be incomplete | 14.8s |
| `housedesigners-working-drawings.pdf` | 12 | 🟨 PARTIAL | 3 plan / 2 elev (0 internal wet) · 86 chains → floors + skirting now, walls when the internal elevations arrive | none identified | — | ⚠️ mixed drawing scales in one set (1:100 @ A3, 1:100 @A3, 1:200 @ A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ elevations are external only - no dimensioned internal wet-area elevations found | 3.1s |
| `ncc-building-plans-example.pdf` | 50 | 🛑 FAIL | 6 dimension chains check out (0.12 per page, need 5 and 0.4/page); 4 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area | — | — | ⚠️ rejected: dimension_chains<br>⚠️ rejected: wet_area_elevations | 5.4s |
| `sample-floors-only-derived.pdf` | 19 | 🟨 PARTIAL | 4 plan / 7 elev (0 internal wet) · 93 chains → floors + skirting now, walls when the internal elevations arrive | Laundry, Master Ensuite | — | ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ elevations are external only - no dimensioned internal wet-area elevations found<br>⚠️ wet rooms with a plan but no elevations: Guest Bed Ensuite, Main Bath | 9.9s |
| `sample_plans.pdf` | 25 | ✅ PASS | 4 plan / 13 elev (6 internal wet) · 144 chains | Guest Bed Ensuite, Laundry, Main Bath, Master Ensuite | — | ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ no section sheets - a raked ceiling could not be resolved from this set | 9.2s |

---

## Rejections in full

### `ncc-building-plans-example.pdf`

**Gate said:** 6 dimension chains check out (0.12 per page, need 5 and 0.4/page); 4 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

The letter we would actually send:

```
### ✗ 6 dimension chains check out (0.12 per page, need 5 and 0.4/page)

**What this means:** Text is present but not reliably readable. On a real drawing the numbers in a chain add up to the total printed beside them - 100 + 840 + 790 = 1730. We can't find enough of those here, which is what OCR'd scans look like: numbers that are individually plausible and never add up.

**What to send:** Send the original vector PDF from the drawing software. If this is already the original, let us know and we'll look at it by hand.

### ✗ 4 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

**What this means:** The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**What to send:** Ask for the internal elevations / joinery sheets for each wet area. Meanwhile we'll measure your floors and skirting off the plans - send the internal elevations and we'll add every wall.
```


## Partial notices in full

### `creativehomeplans-sample.pdf`

**Gate said:** 4 plan / 1 elev (0 internal wet) · 13 chains → floors + skirting now, walls when the internal elevations arrive

The letter we would actually send:

```
# Floors first - creativehomeplans-sample

**File:** `creativehomeplans-sample.pdf`  |  **Checked:** 2026-08-23  |  **Pages:** 8

Good news and a gap.

**The good news:** your floor plans are dimensioned and readable, so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** the set has no internal wet-area elevations - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess.

- **4 floor plan(s) and 1 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area** - The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**Send the internal elevations and we'll add every wall** - same job, no extra back-and-forth. Ask your designer for the internal elevation / joinery sheets for each wet area.

---

*We measure from stated dimensions only. We never scale off the drawing, and we never guess - that's the whole point.*
```

### `eastcoast-sample-plan-set.pdf`

**Gate said:** 2 plan / 4 elev (0 internal wet) · 100 chains → floors + skirting now, walls when the internal elevations arrive

The letter we would actually send:

```
# Floors first - eastcoast-sample-plan-set

**File:** `eastcoast-sample-plan-set.pdf`  |  **Checked:** 2026-08-23  |  **Pages:** 30

Good news and a gap.

**The good news:** your floor plans are dimensioned and readable, so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** the set has no internal wet-area elevations - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess.

- **2 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area** - The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**Send the internal elevations and we'll add every wall** - same job, no extra back-and-forth. Ask your designer for the internal elevation / joinery sheets for each wet area.

---

*We measure from stated dimensions only. We never scale off the drawing, and we never guess - that's the whole point.*
```

### `housedesigners-working-drawings.pdf`

**Gate said:** 3 plan / 2 elev (0 internal wet) · 86 chains → floors + skirting now, walls when the internal elevations arrive

The letter we would actually send:

```
# Floors first - housedesigners-working-drawings

**File:** `housedesigners-working-drawings.pdf`  |  **Checked:** 2026-08-23  |  **Pages:** 12

Good news and a gap.

**The good news:** your floor plans are dimensioned and readable, so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** the set has no internal wet-area elevations - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess.

- **3 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area** - The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**Send the internal elevations and we'll add every wall** - same job, no extra back-and-forth. Ask your designer for the internal elevation / joinery sheets for each wet area.

---

*We measure from stated dimensions only. We never scale off the drawing, and we never guess - that's the whole point.*
```

### `sample-floors-only-derived.pdf`

**Gate said:** 4 plan / 7 elev (0 internal wet) · 93 chains → floors + skirting now, walls when the internal elevations arrive

The letter we would actually send:

```
# Floors first - sample-floors-only-derived

**File:** `sample-floors-only-derived.pdf`  |  **Checked:** 2026-08-23  |  **Pages:** 19

Good news and a gap.

**The good news:** your floor plans are dimensioned and readable, so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** the set has no internal wet-area elevations - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess.

- **4 floor plan(s) and 7 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area** - The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**Send the internal elevations and we'll add every wall** - same job, no extra back-and-forth. Ask your designer for the internal elevation / joinery sheets for each wet area.

---

*We measure from stated dimensions only. We never scale off the drawing, and we never guess - that's the whole point.*
```


## Per-plan detail

### `derbyshire-construction-sample.pdf`

- Sheets: 4 plan / 6 elev (4 internal wet) · 494 chains
- Scales: 1:1 @ A3, 1:100 @ A3, 1:200 @ A3, 1:50 @ A3
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed drawing scales in one set (1:1 @ A3, 1:100 @ A3, 1:200 @ A3, 1:50 @ A3) - anyone who scales off it will be wrong on some sheets

### `sample_plans.pdf`

- Sheets: 4 plan / 13 elev (6 internal wet) · 144 chains
- Scales: 1 : 20@A3, 1 : 25@A3
- Wet rooms with plan **and** elevations: **4**
- Rooms: Guest Bed Ensuite, Laundry, Main Bath, Master Ensuite
- Headline: —
- ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets
- ⚠️ no section sheets - a raked ceiling could not be resolved from this set

### `creativehomeplans-sample.pdf`

- Sheets: 4 plan / 1 elev (0 internal wet) · 13 chains → floors + skirting now, walls when the internal elevations arrive
- Scales: 1:100 A3, 1:200 A3
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed drawing scales in one set (1:100 A3, 1:200 A3) - anyone who scales off it will be wrong on some sheets
- ⚠️ elevations are external only - no dimensioned internal wet-area elevations found

### `eastcoast-sample-plan-set.pdf`

- Sheets: 2 plan / 4 elev (0 internal wet) · 100 chains → floors + skirting now, walls when the internal elevations arrive
- Scales: none printed
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ elevations are external only - no dimensioned internal wet-area elevations found
- ⚠️ sheet names read on only 14 of 30 sheets - the room map may be incomplete

### `housedesigners-working-drawings.pdf`

- Sheets: 3 plan / 2 elev (0 internal wet) · 86 chains → floors + skirting now, walls when the internal elevations arrive
- Scales: 1:100 @ A3, 1:100 @A3, 1:200 @ A3
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed drawing scales in one set (1:100 @ A3, 1:100 @A3, 1:200 @ A3) - anyone who scales off it will be wrong on some sheets
- ⚠️ elevations are external only - no dimensioned internal wet-area elevations found

### `sample-floors-only-derived.pdf`

- Sheets: 4 plan / 7 elev (0 internal wet) · 93 chains → floors + skirting now, walls when the internal elevations arrive
- Scales: 1 : 20@A3, 1 : 25@A3
- Wet rooms with plan **and** elevations: **2**
- Rooms: Laundry, Master Ensuite
- Headline: —
- ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets
- ⚠️ elevations are external only - no dimensioned internal wet-area elevations found
- ⚠️ wet rooms with a plan but no elevations: Guest Bed Ensuite, Main Bath
