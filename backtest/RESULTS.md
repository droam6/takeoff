# Backtest scoreboard

**Run:** 20260823-074716 · **Depth:** structure probe (gate + extract, no model) · **Plans:** 7

**2 passed · 5 partial (floors + skirting) · 0 rejected · 0 errored**

*Every run archives to `backtest/results/<timestamp>/`; the committed `backtest/RESULTS.md` always holds the latest full run only.*

| File | Pages | Intake | Why | Rooms found | Headline areas | Flags | Runtime |
|---|---|---|---|---|---|---|---|
| `creativehomeplans-sample.pdf` | 8 | 🟨 PARTIAL | 3 plan / 1 elev (0 internal wet) · 13 chains → floors + skirting now, walls when the internal elevations arrive | none identified | — | ⚠️ mixed drawing scales in one set (1:100 A3, 1:200 A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ elevations are external only - no dimensioned internal wet-area elevations found | 2.5s |
| `derbyshire-construction-sample.pdf` | 23 | ✅ PASS | 1 plan / 6 elev (4 internal wet) · 494 chains | none identified | — | ⚠️ mixed drawing scales in one set (1:1 @ A3, 1:100 @ A3, 1:200 @ A3, 1:50 @ A3) - anyone who scales off it will be wrong on some sheets | 6.7s |
| `eastcoast-sample-plan-set.pdf` | 30 | 🟨 PARTIAL | 2 plan / 4 elev (0 internal wet) · 100 chains → floors + skirting now, walls when the internal elevations arrive | none identified | — | ⚠️ elevations are external only - no dimensioned internal wet-area elevations found<br>⚠️ sheet names read on only 14 of 30 sheets - the room map may be incomplete | 15.9s |
| `housedesigners-working-drawings.pdf` | 12 | 🟨 PARTIAL | 2 plan / 2 elev (0 internal wet) · 86 chains → floors + skirting now, walls when the internal elevations arrive | none identified | — | ⚠️ mixed drawing scales in one set (1:100 @ A3, 1:100 @A3, 1:200 @ A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ elevations are external only - no dimensioned internal wet-area elevations found | 3.0s |
| `ncc-building-plans-example.pdf` | 50 | 🟨 PARTIAL | 2 plan / 1 elev (0 internal wet) · 6 chains → floors + skirting now, walls when the internal elevations arrive | none identified | — | ⚠️ mixed drawing scales in one set (SCALE 1:10, SCALE 1:100, SCALE 1:200, SCALE 1:50, SCALE1:100) - anyone who scales off it will be wrong on some sheets<br>⚠️ elevations are external only - no dimensioned internal wet-area elevations found<br>⚠️ sheet names read on only 12 of 50 sheets - the room map may be incomplete | 15.8s |
| `sample-floors-only-derived.pdf` | 19 | 🟨 PARTIAL | 4 plan / 6 elev (0 internal wet) · 93 chains → floors + skirting now, walls when the internal elevations arrive | Laundry, Master Ensuite | — | ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ elevations are external only - no dimensioned internal wet-area elevations found<br>⚠️ wet rooms with a plan but no elevations: Guest Bed Ensuite, Main Bath | 9.5s |
| `sample_plans.pdf` | 25 | ✅ PASS | 4 plan / 12 elev (6 internal wet) · 144 chains | Guest Bed Ensuite, Laundry, Main Bath, Master Ensuite | — | ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ no section sheets - a raked ceiling could not be resolved from this set | 9.4s |

---

## Rejections in full

_None._

## Partial notices in full

### `creativehomeplans-sample.pdf`

**Gate said:** 3 plan / 1 elev (0 internal wet) · 13 chains → floors + skirting now, walls when the internal elevations arrive

The letter we would actually send:

```
# Floors first - creativehomeplans-sample

**File:** `creativehomeplans-sample.pdf`  |  **Checked:** 2026-08-23  |  **Pages:** 8

Good news and a gap.

**The good news:** your floor plans are dimensioned and readable, so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** the set has no internal wet-area elevations - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess.

- **3 floor plan(s) and 1 elevation sheet(s) found, but none of the elevations reads as a dimensioned internal elevation of a wet area** - None of the elevation sheets we could read is a dimensioned internal elevation of a wet area - wall tile quantities come from those internal wall drawings: each bathroom, ensuite and laundry with tiling heights printed. We may not have recognised yours.

**Send the internal elevations and we'll add every wall** - same job, no extra back-and-forth. Ask your designer for the internal elevation / joinery sheets for each wet area.

---

**Reckon we've got this wrong? Reply - a human will personally look at your file within the day.**

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

- **2 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations reads as a dimensioned internal elevation of a wet area** - None of the elevation sheets we could read is a dimensioned internal elevation of a wet area - wall tile quantities come from those internal wall drawings: each bathroom, ensuite and laundry with tiling heights printed. We may not have recognised yours.

**Send the internal elevations and we'll add every wall** - same job, no extra back-and-forth. Ask your designer for the internal elevation / joinery sheets for each wet area.

---

**Reckon we've got this wrong? Reply - a human will personally look at your file within the day.**

*We measure from stated dimensions only. We never scale off the drawing, and we never guess - that's the whole point.*
```

### `housedesigners-working-drawings.pdf`

**Gate said:** 2 plan / 2 elev (0 internal wet) · 86 chains → floors + skirting now, walls when the internal elevations arrive

The letter we would actually send:

```
# Floors first - housedesigners-working-drawings

**File:** `housedesigners-working-drawings.pdf`  |  **Checked:** 2026-08-23  |  **Pages:** 12

Good news and a gap.

**The good news:** your floor plans are dimensioned and readable, so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** the set has no internal wet-area elevations - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess.

- **2 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations reads as a dimensioned internal elevation of a wet area** - None of the elevation sheets we could read is a dimensioned internal elevation of a wet area - wall tile quantities come from those internal wall drawings: each bathroom, ensuite and laundry with tiling heights printed. We may not have recognised yours.

**Send the internal elevations and we'll add every wall** - same job, no extra back-and-forth. Ask your designer for the internal elevation / joinery sheets for each wet area.

---

**Reckon we've got this wrong? Reply - a human will personally look at your file within the day.**

*We measure from stated dimensions only. We never scale off the drawing, and we never guess - that's the whole point.*
```

### `ncc-building-plans-example.pdf`

**Gate said:** 2 plan / 1 elev (0 internal wet) · 6 chains → floors + skirting now, walls when the internal elevations arrive

The letter we would actually send:

```
# Floors first - ncc-building-plans-example

**File:** `ncc-building-plans-example.pdf`  |  **Checked:** 2026-08-23  |  **Pages:** 50

Good news and a gap.

**The good news:** your floor plans are dimensioned and readable, so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** the set has no internal wet-area elevations - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess.

- **2 floor plan(s) and 1 elevation sheet(s) found, but none of the elevations reads as a dimensioned internal elevation of a wet area** - None of the elevation sheets we could read is a dimensioned internal elevation of a wet area - wall tile quantities come from those internal wall drawings: each bathroom, ensuite and laundry with tiling heights printed. We may not have recognised yours.

**Send the internal elevations and we'll add every wall** - same job, no extra back-and-forth. Ask your designer for the internal elevation / joinery sheets for each wet area.

---

**Reckon we've got this wrong? Reply - a human will personally look at your file within the day.**

*We measure from stated dimensions only. We never scale off the drawing, and we never guess - that's the whole point.*
```

### `sample-floors-only-derived.pdf`

**Gate said:** 4 plan / 6 elev (0 internal wet) · 93 chains → floors + skirting now, walls when the internal elevations arrive

The letter we would actually send:

```
# Floors first - sample-floors-only-derived

**File:** `sample-floors-only-derived.pdf`  |  **Checked:** 2026-08-23  |  **Pages:** 19

Good news and a gap.

**The good news:** your floor plans are dimensioned and readable, so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** the set has no internal wet-area elevations - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess.

- **4 floor plan(s) and 6 elevation sheet(s) found, but none of the elevations reads as a dimensioned internal elevation of a wet area** - None of the elevation sheets we could read is a dimensioned internal elevation of a wet area - wall tile quantities come from those internal wall drawings: each bathroom, ensuite and laundry with tiling heights printed. We may not have recognised yours.

**Send the internal elevations and we'll add every wall** - same job, no extra back-and-forth. Ask your designer for the internal elevation / joinery sheets for each wet area.

---

**Reckon we've got this wrong? Reply - a human will personally look at your file within the day.**

*We measure from stated dimensions only. We never scale off the drawing, and we never guess - that's the whole point.*
```


## Per-plan detail

### `derbyshire-construction-sample.pdf`

- Sheets: 1 plan / 6 elev (4 internal wet) · 494 chains
- Page classification: sidecar derbyshire-construction-sample.classes.json
- Scales: 1:1 @ A3, 1:100 @ A3, 1:200 @ A3, 1:50 @ A3
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed drawing scales in one set (1:1 @ A3, 1:100 @ A3, 1:200 @ A3, 1:50 @ A3) - anyone who scales off it will be wrong on some sheets

### `sample_plans.pdf`

- Sheets: 4 plan / 12 elev (6 internal wet) · 144 chains
- Page classification: sidecar sample_plans.classes.json
- Scales: 1 : 20@A3, 1 : 25@A3
- Wet rooms with plan **and** elevations: **4**
- Rooms: Guest Bed Ensuite, Laundry, Main Bath, Master Ensuite
- Headline: —
- ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets
- ⚠️ no section sheets - a raked ceiling could not be resolved from this set

### `creativehomeplans-sample.pdf`

- Sheets: 3 plan / 1 elev (0 internal wet) · 13 chains → floors + skirting now, walls when the internal elevations arrive
- Page classification: sidecar creativehomeplans-sample.classes.json
- Scales: 1:100 A3, 1:200 A3
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed drawing scales in one set (1:100 A3, 1:200 A3) - anyone who scales off it will be wrong on some sheets
- ⚠️ elevations are external only - no dimensioned internal wet-area elevations found

### `eastcoast-sample-plan-set.pdf`

- Sheets: 2 plan / 4 elev (0 internal wet) · 100 chains → floors + skirting now, walls when the internal elevations arrive
- Page classification: sidecar eastcoast-sample-plan-set.classes.json
- Scales: none printed
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ elevations are external only - no dimensioned internal wet-area elevations found
- ⚠️ sheet names read on only 14 of 30 sheets - the room map may be incomplete

### `housedesigners-working-drawings.pdf`

- Sheets: 2 plan / 2 elev (0 internal wet) · 86 chains → floors + skirting now, walls when the internal elevations arrive
- Page classification: sidecar housedesigners-working-drawings.classes.json
- Scales: 1:100 @ A3, 1:100 @A3, 1:200 @ A3
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed drawing scales in one set (1:100 @ A3, 1:100 @A3, 1:200 @ A3) - anyone who scales off it will be wrong on some sheets
- ⚠️ elevations are external only - no dimensioned internal wet-area elevations found

### `ncc-building-plans-example.pdf`

- Sheets: 2 plan / 1 elev (0 internal wet) · 6 chains → floors + skirting now, walls when the internal elevations arrive
- Page classification: sidecar ncc-building-plans-example.classes.json
- Scales: SCALE 1:10, SCALE 1:100, SCALE 1:200, SCALE 1:50, SCALE1:100
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed drawing scales in one set (SCALE 1:10, SCALE 1:100, SCALE 1:200, SCALE 1:50, SCALE1:100) - anyone who scales off it will be wrong on some sheets
- ⚠️ elevations are external only - no dimensioned internal wet-area elevations found
- ⚠️ sheet names read on only 12 of 50 sheets - the room map may be incomplete

### `sample-floors-only-derived.pdf`

- Sheets: 4 plan / 6 elev (0 internal wet) · 93 chains → floors + skirting now, walls when the internal elevations arrive
- Page classification: sidecar sample-floors-only-derived.classes.json
- Scales: 1 : 20@A3, 1 : 25@A3
- Wet rooms with plan **and** elevations: **2**
- Rooms: Laundry, Master Ensuite
- Headline: —
- ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets
- ⚠️ elevations are external only - no dimensioned internal wet-area elevations found
- ⚠️ wet rooms with a plan but no elevations: Guest Bed Ensuite, Main Bath
