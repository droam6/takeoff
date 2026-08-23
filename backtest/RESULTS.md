# Backtest scoreboard

**Run:** 20260823-075812 · **Depth:** structure probe (gate + extract, no model) · **Plans:** 7

**2 passed · 4 partial (floors + skirting) · 1 rejected · 0 errored**

*Every run archives to `backtest/results/<timestamp>/`; the committed `backtest/RESULTS.md` always holds the latest full run only.*

| File | Pages | Intake | Why | Rooms found | Headline areas | Flags | Runtime |
|---|---|---|---|---|---|---|---|
| `creativehomeplans-sample.pdf` | 8 | 🟨 PARTIAL | 1 plan / 1 elev (0 internal wet) · 13 chains → floors + skirting now, walls when the internal elevations arrive | none identified | — | ⚠️ mixed drawing scales in one set (1:100 A3, 1:200 A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ elevations are external only - no dimensioned internal wet-area elevations found | 2.5s |
| `derbyshire-construction-sample.pdf` | 23 | ✅ PASS | 1 plan / 6 elev (4 internal wet) · 494 chains | none identified | — | ⚠️ mixed drawing scales in one set (1:1 @ A3, 1:100 @ A3, 1:200 @ A3, 1:50 @ A3) - anyone who scales off it will be wrong on some sheets | 6.1s |
| `eastcoast-sample-plan-set.pdf` | 30 | 🟨 PARTIAL | 2 plan / 4 elev (0 internal wet) · 100 chains → floors + skirting now, walls when the internal elevations arrive | none identified | — | ⚠️ elevations are external only - no dimensioned internal wet-area elevations found<br>⚠️ sheet names read on only 14 of 30 sheets - the room map may be incomplete | 14.8s |
| `housedesigners-working-drawings.pdf` | 12 | 🟨 PARTIAL | 2 plan / 2 elev (0 internal wet) · 86 chains → floors + skirting now, walls when the internal elevations arrive | none identified | — | ⚠️ mixed drawing scales in one set (1:100 @ A3, 1:100 @A3, 1:200 @ A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ elevations are external only - no dimensioned internal wet-area elevations found | 3.3s |
| `ncc-building-plans-example.pdf` | 50 | 🛑 FAIL | no floor plan whose own dimension chains verify, among the 50 pages [model-classified pages]; 0 floor plan(s) and 1 elevation sheet(s) found, but none of the elevations reads as a dimensioned internal elevation of a wet area | — | — | ⚠️ rejected: plan_pages<br>⚠️ rejected: wet_area_elevations | 5.9s |
| `sample-floors-only-derived.pdf` | 19 | 🟨 PARTIAL | 4 plan / 6 elev (0 internal wet) · 93 chains → floors + skirting now, walls when the internal elevations arrive | Laundry, Master Ensuite | — | ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ elevations are external only - no dimensioned internal wet-area elevations found<br>⚠️ wet rooms with a plan but no elevations: Guest Bed Ensuite, Main Bath | 10.1s |
| `sample_plans.pdf` | 25 | ✅ PASS | 4 plan / 12 elev (6 internal wet) · 144 chains | Guest Bed Ensuite, Laundry, Main Bath, Master Ensuite | — | ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ no section sheets - a raked ceiling could not be resolved from this set | 9.3s |

---

## Rejections in full

### `ncc-building-plans-example.pdf`

**Gate said:** no floor plan whose own dimension chains verify, among the 50 pages [model-classified pages]; 0 floor plan(s) and 1 elevation sheet(s) found, but none of the elevations reads as a dimensioned internal elevation of a wet area

The letter we would actually send:

```
### ✗ no floor plan whose own dimension chains verify, among the 50 pages [model-classified pages]

**What this means:** We looked at every page for a floor plan whose printed dimension chains add up on that sheet (100 + 840 + 790 = 1730 next to a printed 1730). We couldn't verify one. That can mean a text layer we can't read, sparse dimensioning, or our reading of your drawings - we can't tell which from here, and we won't measure without it.

**What to send:** Send the floor plan sheet for every room you want quoted - the original vector PDF from the drawing software - or reply and a human will look at what you've sent.

### ✗ 0 floor plan(s) and 1 elevation sheet(s) found, but none of the elevations reads as a dimensioned internal elevation of a wet area

**What this means:** None of the elevation sheets we could read is a dimensioned internal elevation of a wet area - wall tile quantities come from those internal wall drawings: each bathroom, ensuite and laundry with tiling heights printed. We may not have recognised yours.

**What to send:** Ask for the internal elevations / joinery sheets for each wet area. Meanwhile we'll measure your floors and skirting off the plans - send the internal elevations and we'll add every wall.
```


## Partial notices in full

### `creativehomeplans-sample.pdf`

**Gate said:** 1 plan / 1 elev (0 internal wet) · 13 chains → floors + skirting now, walls when the internal elevations arrive

The letter we would actually send:

```
# Floors first - creativehomeplans-sample

**File:** `creativehomeplans-sample.pdf`  |  **Checked:** 2026-08-23  |  **Pages:** 8

Good news and a gap.

**The good news:** we verified the dimension chains on your floor plan sheet - 4 chains across 1 sheet add up to their printed totals - so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** we couldn't find internal wet-area elevations in the set - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess. (If they exist and we missed them, the reply line below is for exactly that.)

- **1 floor plan(s) and 1 elevation sheet(s) found, but none of the elevations reads as a dimensioned internal elevation of a wet area** - None of the elevation sheets we could read is a dimensioned internal elevation of a wet area - wall tile quantities come from those internal wall drawings: each bathroom, ensuite and laundry with tiling heights printed. We may not have recognised yours.

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

**The good news:** we verified the dimension chains on your floor plan sheets - 93 chains across 2 sheets add up to their printed totals - so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** we couldn't find internal wet-area elevations in the set - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess. (If they exist and we missed them, the reply line below is for exactly that.)

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

**The good news:** we verified the dimension chains on your floor plan sheets - 65 chains across 2 sheets add up to their printed totals - so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** we couldn't find internal wet-area elevations in the set - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess. (If they exist and we missed them, the reply line below is for exactly that.)

- **2 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations reads as a dimensioned internal elevation of a wet area** - None of the elevation sheets we could read is a dimensioned internal elevation of a wet area - wall tile quantities come from those internal wall drawings: each bathroom, ensuite and laundry with tiling heights printed. We may not have recognised yours.

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

**The good news:** we verified the dimension chains on your floor plan sheets - 38 chains across 4 sheets add up to their printed totals - so your **floor areas and tile skirting are being measured now** and you'll have them the same day.

**The gap:** we couldn't find internal wet-area elevations in the set - the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them. Wall tile can only be measured off those, and we won't guess. (If they exist and we missed them, the reply line below is for exactly that.)

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

- Sheets: 1 plan / 1 elev (0 internal wet) · 13 chains → floors + skirting now, walls when the internal elevations arrive
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
