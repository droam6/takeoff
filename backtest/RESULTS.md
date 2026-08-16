# Backtest scoreboard

**Run:** 2026-08-16 · **Depth:** structure probe (gate + extract, no model) · **Plans:** 9

**2 passed the gate · 7 rejected · 0 errored**

| File | Pages | Intake | Why | Rooms found | Headline areas | Flags | Runtime |
|---|---|---|---|---|---|---|---|
| `creativehomeplans-sample.pdf` | 8 | 🛑 FAIL | 4 floor plan(s) and 1 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area | — | — | ⚠️ rejected: wet_area_elevations | 0.3s |
| `derbyshire-construction-sample.pdf` | 23 | ✅ PASS | 4 plan / 6 elev (4 internal wet) · 494 chains | none identified | — | ⚠️ mixed drawing scales in one set (1:1 @ A3, 1:100 @ A3, 1:200 @ A3, 1:50 @ A3) - anyone who scales off it will be wrong on some sheets | 3.9s |
| `eastcoast-sample-plan-set.pdf` | 30 | 🛑 FAIL | 2 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area | — | — | ⚠️ rejected: wet_area_elevations | 1.2s |
| `housedesigners-working-drawings.pdf` | 12 | 🛑 FAIL | 3 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area | — | — | ⚠️ rejected: wet_area_elevations | 0.6s |
| `ncc-building-plans-example.pdf` | 50 | 🛑 FAIL | 6 dimension chains check out (0.12 per page, need 5 and 0.4/page); 4 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area | — | — | ⚠️ rejected: dimension_chains<br>⚠️ rejected: wet_area_elevations | 3.2s |
| `phone-scan-of-da-plans.pdf` | 6 | 🛑 FAIL | 0 extractable characters (need 200); 0 characters per page (need 20); text quality: 0.0% of characters usable, 0% of words recognised (need 90% / 15%); 0 mm dimension tokens found (need 30); 0 dimension chains check out (0.00 per page, need 5 and 0.4/page); 0 sheet(s) carry a real dimension chain; couldn't confidently identify any sheet names across 6 sheets; couldn't confidently identify sheet names; 0 floor plan(s) and 0 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area | — | — | ⚠️ rejected: text_layer<br>⚠️ rejected: text_density<br>⚠️ rejected: text_quality<br>⚠️ rejected: dimension_tokens<br>⚠️ rejected: dimension_chains<br>⚠️ rejected: dimensioned_pages<br>⚠️ rejected: plan_pages<br>⚠️ rejected: elevation_pages<br>⚠️ rejected: wet_area_elevations | 0.8s |
| `sample_plans.pdf` | 25 | ✅ PASS | 4 plan / 13 elev (6 internal wet) · 144 chains | Guest Bed Ensuite, Laundry, Main Bath, Master Ensuite | — | ⚠️ mixed drawing scales in one set (1 : 20@A3, 1 : 25@A3) - anyone who scales off it will be wrong on some sheets<br>⚠️ no section sheets - a raked ceiling could not be resolved from this set | 5.2s |
| `ssc-da181440-architectural.pdf` | 34 | 🛑 FAIL | 4 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area | — | — | ⚠️ rejected: wet_area_elevations | 13.2s |
| `ssc-da220327-architectural.pdf` | 23 | 🛑 FAIL | 5 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area | — | — | ⚠️ rejected: wet_area_elevations | 3.1s |

---

## Rejections in full

### `creativehomeplans-sample.pdf`

**Gate said:** 4 floor plan(s) and 1 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

The letter we would actually send:

```
### ✗ 4 floor plan(s) and 1 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

**What this means:** The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**What to send:** Ask for the internal elevations / joinery sheets for each wet area. If they don't exist, we can still do floor areas - just say the word.
```

### `eastcoast-sample-plan-set.pdf`

**Gate said:** 2 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

The letter we would actually send:

```
### ✗ 2 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

**What this means:** The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**What to send:** Ask for the internal elevations / joinery sheets for each wet area. If they don't exist, we can still do floor areas - just say the word.
```

### `housedesigners-working-drawings.pdf`

**Gate said:** 3 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

The letter we would actually send:

```
### ✗ 3 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

**What this means:** The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**What to send:** Ask for the internal elevations / joinery sheets for each wet area. If they don't exist, we can still do floor areas - just say the word.
```

### `ncc-building-plans-example.pdf`

**Gate said:** 6 dimension chains check out (0.12 per page, need 5 and 0.4/page); 4 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

The letter we would actually send:

```
### ✗ 6 dimension chains check out (0.12 per page, need 5 and 0.4/page)

**What this means:** Text is present but not reliably readable. On a real drawing the numbers in a chain add up to the total printed beside them - 100 + 840 + 790 = 1730. We can't find enough of those here, which is what OCR'd scans look like: numbers that are individually plausible and never add up.

**What to send:** Send the original vector PDF from the drawing software. If this is already the original, let us know and we'll look at it by hand.

### ✗ 4 floor plan(s) and 4 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

**What this means:** The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**What to send:** Ask for the internal elevations / joinery sheets for each wet area. If they don't exist, we can still do floor areas - just say the word.
```

### `phone-scan-of-da-plans.pdf`

**Gate said:** 0 extractable characters (need 200); 0 characters per page (need 20); text quality: 0.0% of characters usable, 0% of words recognised (need 90% / 15%); 0 mm dimension tokens found (need 30); 0 dimension chains check out (0.00 per page, need 5 and 0.4/page); 0 sheet(s) carry a real dimension chain; couldn't confidently identify any sheet names across 6 sheets; couldn't confidently identify sheet names; 0 floor plan(s) and 0 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

The letter we would actually send:

```
### ✗ 0 extractable characters (need 200)

**What this means:** The file is a scan or photo, so the dimensions are pixels rather than numbers we can read. We won't OCR them and we won't scale off the drawing.

**What to send:** Ask your designer to re-export the PDF straight out of their drawing software - not printed and scanned.

### ✗ 0 characters per page (need 20)

**What this means:** Most pages carry no readable text - likely images with a text title block.

**What to send:** Re-export the full set as vector PDF from the drawing software.

### ✗ text quality: 0.0% of characters usable, 0% of words recognised (need 90% / 15%)

**What this means:** There is text in this file, but it doesn't read like a drawing sheet - which is what a scan looks like after OCR has been run over it.

**What to send:** Send the original PDF exported from the drawing software, not a scan.

### ✗ 0 mm dimension tokens found (need 30)

**What this means:** We can read text but can't find printed millimetre dimensions. We measure from stated dimensions only - we never scale off the drawing.

**What to send:** Send drawings with the dimension strings printed on them, in mm.

### ✗ 0 dimension chains check out (0.00 per page, need 5 and 0.4/page)

**What this means:** Text is present but not reliably readable. On a real drawing the numbers in a chain add up to the total printed beside them - 100 + 840 + 790 = 1730. We can't find enough of those here, which is what OCR'd scans look like: numbers that are individually plausible and never add up.

**What to send:** Send the original vector PDF from the drawing software. If this is already the original, let us know and we'll look at it by hand.

### ✗ 0 sheet(s) carry a real dimension chain

**What this means:** The set looks like cover sheets,
```

### `ssc-da181440-architectural.pdf`

**Gate said:** 4 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

The letter we would actually send:

```
### ✗ 4 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

**What this means:** The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**What to send:** Ask for the internal elevations / joinery sheets for each wet area. If they don't exist, we can still do floor areas - just say the word.
```

### `ssc-da220327-architectural.pdf`

**Gate said:** 5 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

The letter we would actually send:

```
### ✗ 5 floor plan(s) and 2 elevation sheet(s) found, but none of the elevations is a dimensioned internal elevation of a wet area

**What this means:** The elevations in this set look like external elevations - the outside of the building. Wall tile quantities come from internal elevations: the wall drawings of each bathroom, ensuite and laundry, with tiling heights on them.

**What to send:** Ask for the internal elevations / joinery sheets for each wet area. If they don't exist, we can still do floor areas - just say the word.
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
