# Backtest sources

Where each plan set in `backtest/inbox/` came from. All are publicly published documents —
council DA exhibition material, regulator guidance, or sample drawings put on the open web
by the firms that drew them.

> **The PDFs themselves are not committed.** `backtest/inbox/` is gitignored. Every one of
> these drawings carries a copyright notice from the practice that produced it (the sample
> set's own notes block reads *"This drawing is subject to copyright laws and may not be
> copied without permission"*). Re-publishing them in a public repo would be redistribution,
> not fair testing use. The URLs below make the run reproducible without us becoming a
> distributor of other people's drawings.

Fetched **16 August 2026**.

---

## Target spread

| Bucket | Wanted | Got |
|---|---|---|
| Proper working-drawing sets with dimensioned internal elevations | 2 | 2 |
| DA-level sets that should fail or degrade to floors-only | 2 | 4 |
| Scanned / raster that must fail | 1 | 1 |
| Adversarial extra: OCR'd scan with a junk text layer | — | 1 |
| Known-good control | — | 1 |

---

## 1. Working-drawing sets — expected to pass

### `sample_plans.pdf` — control
The set already in this repo. Harper Lane Design, project 24107, 5 Ellalong Road,
Cremorne NSW. 25 sheets, 1:20 @ A3 (sheet 12.01 is 1:25). Supplied by Angus, customer #1.
Not downloaded — copied from the repo root so the control runs through the same harness.

### `derbyshire-construction-sample.pdf`
Derbyshire Homes (Geelong VIC) — published construction documentation sample.
23 sheets. Cover, general notes, site plan, floor plan, slab setout, external elevations,
RCP, electrical, roof, four sections, door/window schedules, and **four sheets of plan
details + internal elevations** covering master ensuite & WIR, bath & bed 3, laundry &
pantry & kitchen, and kitchen.
<https://derbyshire.com.au/wp-content/uploads/2016/03/Construction-Document-Sample-1.pdf>

## 2. DA-level and general residential sets — expected to fail or degrade

### `ssc-da220327-architectural.pdf`
Sutherland Shire Council DA tracker — DA220327, original architectural drawings, 23 sheets.
Drawn by Plan Land. Real lodged NSW residential DA.
<https://propertydevelopment.ssc.nsw.gov.au/PublicEPropertyPDF/riDA220327%20Original%20Architectural%20Drawings%20-%20%5BA8164807%5D.pdf>

### `ssc-da181440-architectural.pdf`
Sutherland Shire Council DA tracker — DA181440, revised architectural plans (rev 8,
29/10/2019), 34 sheets. Same practice. Real lodged NSW residential DA.
<https://propertydevelopment.ssc.nsw.gov.au/PublicEPropertyPDF/DA181440%20Revised%208%20Architectural%20Plans%202019%2010%2029%20dropbox%20-%20%5BA6487554%5D.pdf>

### `housedesigners-working-drawings.pdf`
The House Designers (QLD) — published "Example Working Drawings, Sloping Site". 12 sheets:
site plan, floor plan, elevations, sections, roof, electrical, bracing, slab.
<https://thehousedesigners.com.au/wp-content/uploads/2015/11/working-drawings-sample.pdf>

### `creativehomeplans-sample.pdf`
Creative Home Plans (AU) — published sample DA drawing set, 8 sheets. The drawing list is
explicitly DA-level: location plan, survey plan, site plan, floor plans, elevations.
<https://creativehomeplans.com.au/wp-content/uploads/2016/09/Sample-Drawings-for-Web-Page.pdf>

### `eastcoast-sample-plan-set.pdf`
East Coast Building Design (AU) — published sample plan set, 30 sheets.
<https://eastcoastbuildingdesign.com.au/wp-content/uploads/2013/09/2012.sample-plan-set.pdf>

## 3. Raster — must fail

### `phone-scan-of-da-plans.pdf` — **derived, not third-party**
6 pages of `ssc-da220327-architectural.pdf` flattened to images at 110 dpi and re-wrapped
as a PDF. Zero text layer, zero vector geometry — exactly what arrives when a tradie
photographs or scans a printed plan, which is the single most common bad input we expect.

**Why it's derived rather than downloaded.** Genuine third-party scans exist in council and
state archives (City of Sydney Archives, PROV, Central Darling Shire's stamped DA drawings),
and all of them were blocked in this session — `403 Access Denied` from CDN/WAF layers on
`centraldarling.nsw.gov.au`, `midwestern.nsw.gov.au` and `archives.cityofsydney.nsw.gov.au`.
Rather than claim a source we couldn't actually retrieve, this case is built from a real
plan by a documented, reproducible transformation. It exercises the gate identically.

Reproduce with:

```python
import fitz
src = fitz.open('ssc-da220327-architectural.pdf'); out = fitz.open()
for i in range(6):
    pg = src[i]; pix = pg.get_pixmap(dpi=110)
    out.new_page(width=pg.rect.width, height=pg.rect.height).insert_image(
        fitz.Rect(0, 0, pg.rect.width, pg.rect.height), pixmap=pix)
out.save('phone-scan-of-da-plans.pdf', deflate=True)
```

## 4. Adversarial extra — OCR'd scan with a junk text layer

### `ncc-building-plans-example.pdf`
Australian Building Codes Board — "Building plans and documentation", 50 sheets, published
with the National Construction Code. It is a **scanned drawing set that has been run through
OCR**, so it carries a text layer full of noise (`I§J`, `C---'`, `'<:::; BAY RD851`).
Commercial rather than residential, kept deliberately: it is the input most likely to defeat
a naive text-layer check, and that is worth knowing about.
<https://ncc.abcb.gov.au/sites/default/files/download/2021-07/Building%20plans%20and%20documentation%20(1).pdf>

---

## Sources consulted while hunting (no usable file retrieved)

- Clarence Valley Council DA exhibition documents — links resolve to an HTML shell
- Mid-Western Regional Council `das-on-exhibition` — HTTP 403 on both page and file paths
- Central Darling Shire stamped DA drawings — HTTP 403 from the CDN
- City of Sydney Archives digitised plans — no direct download link exposed in the HTML
- NSW Planning Portal `daex` exhibition pages — 301 redirect loop between `pp.` and `www.`
- NSW Planning Portal document endpoint — returned a lodgement guide, not plans
