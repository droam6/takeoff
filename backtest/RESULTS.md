# Backtest scoreboard

**Run:** 2026-08-16 · **Depth:** structure probe (gate + extract, no model) · **Plans:** 9

**5 passed the gate · 4 rejected · 0 errored**

| File | Pages | Intake | Why | Rooms found | Headline areas | Flags | Runtime |
|---|---|---|---|---|---|---|---|
| `creativehomeplans-sample.pdf` | 8 | ✅ PASS | 1 plan / 1 elev sheets, 205 dim tokens | none identified | — | ⚠️ mixed scales in one set (1:100, 1:200) - scaling risk<br>⚠️ no wet areas identified by sheet title | 2.1s |
| `derbyshire-construction-sample.pdf` | 23 | ✅ PASS | 3 plan / 7 elev sheets, 1721 dim tokens | none identified | — | ⚠️ mixed scales in one set (1:1, 1:100, 1:200, 1:50) - scaling risk<br>⚠️ no wet areas identified by sheet title<br>⚠️ no sections - raked ceilings could not be resolved | 5.5s |
| `eastcoast-sample-plan-set.pdf` | 30 | ✅ PASS | 2 plan / 1 elev sheets, 1013 dim tokens | none identified | — | ⚠️ mixed scales in one set (1:1, 1:10, 1:100, 1:20, 1:200, 1:3, 1:4, 1:6, 1:8) - scaling risk<br>⚠️ no wet areas identified by sheet title | 10.7s |
| `housedesigners-working-drawings.pdf` | 12 | 🛑 FAIL | 0 floor plan sheet(s) detected; 0 elevation sheet(s) detected | — | — | ⚠️ rejected: plan_pages<br>⚠️ rejected: elevation_pages | 0.2s |
| `ncc-building-plans-example.pdf` | 50 | ✅ PASS | 3 plan / 5 elev sheets, 578 dim tokens | none identified | — | ⚠️ mixed scales in one set (1:1, 1:10, 1:100, 1:200, 1:50) - scaling risk<br>⚠️ no wet areas identified by sheet title | 12.2s |
| `phone-scan-of-da-plans.pdf` | 6 | 🛑 FAIL | 0 extractable characters (need 200); 0 characters per page (need 20); 0 mm dimension tokens found (need 30); 0 sheet(s) carry a real dimension chain; 0 floor plan sheet(s) detected; 0 elevation sheet(s) detected | — | — | ⚠️ rejected: text_layer<br>⚠️ rejected: text_density<br>⚠️ rejected: dimension_tokens<br>⚠️ rejected: dimensioned_pages<br>⚠️ rejected: plan_pages<br>⚠️ rejected: elevation_pages | 0.0s |
| `sample_plans.pdf` | 25 | ✅ PASS | 4 plan / 13 elev sheets, 567 dim tokens | Guest Bed Ensuite, Laundry, Main Bath, Master Ensuite | — | ⚠️ mixed scales in one set (1:20, 1:25) - scaling risk<br>⚠️ no sections - raked ceilings could not be resolved | 7.2s |
| `ssc-da181440-architectural.pdf` | 34 | 🛑 FAIL | 0 floor plan sheet(s) detected; 0 elevation sheet(s) detected | — | — | ⚠️ rejected: plan_pages<br>⚠️ rejected: elevation_pages | 0.4s |
| `ssc-da220327-architectural.pdf` | 23 | 🛑 FAIL | 0 floor plan sheet(s) detected; 0 elevation sheet(s) detected | — | — | ⚠️ rejected: plan_pages<br>⚠️ rejected: elevation_pages | 0.2s |

---

## Rejections in full

### `housedesigners-working-drawings.pdf`

**Gate said:** 0 floor plan sheet(s) detected; 0 elevation sheet(s) detected

The letter we would actually send:

```
### ✗ 0 floor plan sheet(s) detected

**What this means:** Without a floor plan we cannot measure floor area.

**What to send:** Include the floor plan sheet for every room you want quoted.

### ✗ 0 elevation sheet(s) detected

**What this means:** Wall tiling heights only appear on elevations. Without them we can give you floor area only.

**What to send:** Include the elevation sheets for each room you want wall areas on.
```

### `phone-scan-of-da-plans.pdf`

**Gate said:** 0 extractable characters (need 200); 0 characters per page (need 20); 0 mm dimension tokens found (need 30); 0 sheet(s) carry a real dimension chain; 0 floor plan sheet(s) detected; 0 elevation sheet(s) detected

The letter we would actually send:

```
### ✗ 0 extractable characters (need 200)

**What this means:** The file is a scan or photo, so the dimensions are pixels rather than numbers we can read. We won't OCR them and we won't scale off the drawing.

**What to send:** Ask your designer to re-export the PDF straight out of their drawing software - not printed and scanned.

### ✗ 0 characters per page (need 20)

**What this means:** Most pages carry no readable text - likely images with a text title block.

**What to send:** Re-export the full set as vector PDF from the drawing software.

### ✗ 0 mm dimension tokens found (need 30)

**What this means:** We can read text but can't find printed millimetre dimensions. We measure from stated dimensions only - we never scale off the drawing.

**What to send:** Send drawings with the dimension strings printed on them, in mm.

### ✗ 0 sheet(s) carry a real dimension chain

**What this means:** The set looks like cover sheets, 3D views or renders only.

**What to send:** Include the dimensioned floor plans and elevations.

### ✗ 0 floor plan sheet(s) detected

**What this means:** Without a floor plan we cannot measure floor area.

**What to send:** Include the floor plan sheet for every room you want quoted.

### ✗ 0 elevation sheet(s) detected

**What this means:** Wall tiling heights only appear on elevations. Without them we can give you floor area only.

**What to send:** Include the elevation sheets for each room you want wall areas on.
```

### `ssc-da181440-architectural.pdf`

**Gate said:** 0 floor plan sheet(s) detected; 0 elevation sheet(s) detected

The letter we would actually send:

```
### ✗ 0 floor plan sheet(s) detected

**What this means:** Without a floor plan we cannot measure floor area.

**What to send:** Include the floor plan sheet for every room you want quoted.

### ✗ 0 elevation sheet(s) detected

**What this means:** Wall tiling heights only appear on elevations. Without them we can give you floor area only.

**What to send:** Include the elevation sheets for each room you want wall areas on.
```

### `ssc-da220327-architectural.pdf`

**Gate said:** 0 floor plan sheet(s) detected; 0 elevation sheet(s) detected

The letter we would actually send:

```
### ✗ 0 floor plan sheet(s) detected

**What this means:** Without a floor plan we cannot measure floor area.

**What to send:** Include the floor plan sheet for every room you want quoted.

### ✗ 0 elevation sheet(s) detected

**What this means:** Wall tiling heights only appear on elevations. Without them we can give you floor area only.

**What to send:** Include the elevation sheets for each room you want wall areas on.
```


## Per-plan detail

### `creativehomeplans-sample.pdf`

- Sheets: 1 plan / 1 elev sheets, 205 dim tokens
- Scales: 1:100, 1:200
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed scales in one set (1:100, 1:200) - scaling risk
- ⚠️ no wet areas identified by sheet title

### `derbyshire-construction-sample.pdf`

- Sheets: 3 plan / 7 elev sheets, 1721 dim tokens
- Scales: 1:1, 1:100, 1:200, 1:50
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed scales in one set (1:1, 1:100, 1:200, 1:50) - scaling risk
- ⚠️ no wet areas identified by sheet title
- ⚠️ no sections - raked ceilings could not be resolved

### `eastcoast-sample-plan-set.pdf`

- Sheets: 2 plan / 1 elev sheets, 1013 dim tokens
- Scales: 1:1, 1:10, 1:100, 1:20, 1:200, 1:3, 1:4, 1:6, 1:8
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed scales in one set (1:1, 1:10, 1:100, 1:20, 1:200, 1:3, 1:4, 1:6, 1:8) - scaling risk
- ⚠️ no wet areas identified by sheet title

### `ncc-building-plans-example.pdf`

- Sheets: 3 plan / 5 elev sheets, 578 dim tokens
- Scales: 1:1, 1:10, 1:100, 1:200, 1:50
- Wet rooms with plan **and** elevations: **0**
- Rooms: none identified
- Headline: —
- ⚠️ mixed scales in one set (1:1, 1:10, 1:100, 1:200, 1:50) - scaling risk
- ⚠️ no wet areas identified by sheet title

### `sample_plans.pdf`

- Sheets: 4 plan / 13 elev sheets, 567 dim tokens
- Scales: 1:20, 1:25
- Wet rooms with plan **and** elevations: **4**
- Rooms: Guest Bed Ensuite, Laundry, Main Bath, Master Ensuite
- Headline: —
- ⚠️ mixed scales in one set (1:20, 1:25) - scaling risk
- ⚠️ no sections - raked ceilings could not be resolved
