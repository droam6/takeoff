# Held-out test sources

Six Australian residential plan PDFs, none previously in `backtest/SOURCES.md`, fetched
**23 August 2026** for the held-out stress test. Same redistribution policy as the main
corpus: **the PDFs are not committed** (`backtest/heldout_inbox/` is gitignored — every
file carries its author's copyright); the URLs below make the basket re-fetchable.

Stage-1 hunting notes, for the record: these files were found and downloaded by the same
session that will later run the test, so the hunter saw the files before the gate did —
selection involved opening each PDF far enough to identify what kind of document it is
(page counts, sheet inventory, subject of the DA). No gate, probe or measurement was run
on any of them in stage 1. The hunt aimed for the requested spread; the "set with
internal wall elevations" slot could not be confirmed filled from open sources — searches
across designer samples, council trackers, joinery/wet-area queries and tender documents
surfaced no downloadable Australian set advertising internal wet-area elevation sheets
(the main corpus's derbyshire set remains the only one found on the open web). The two
fullest sets below are the closest candidates either way.

| File | Source |
|---|---|
| `arei-example-plan.pdf` | AREI Designs (NSW drafting service) — published example plan set. <https://www.areidesigns.com.au/wp-content/uploads/AREI-EXAMPLE-PLAN.pdf> |
| `bodc-da137-dwelling.pdf` | Break O'Day Council (TAS) advertised development applications — DA 137-2026, dwelling with deck & pergola, separate garage with secondary residence, art studio. <https://www.bodc.tas.gov.au/wp-content/uploads/2026/08/Advert-Plans-DA-137-2026.pdf> |
| `bodc-da142-dwelling.pdf` | Break O'Day Council (TAS) advertised development applications — DA 142-2026, secondary residence with attached deck. <https://www.bodc.tas.gov.au/wp-content/uploads/2026/08/Advert-Plans-DA-142-2026.pdf> |
| `uralla-da45-2020-313-gostwyck-rd.pdf` | Uralla Shire Council (NSW) DA tracking — DA 45-2020, 313 Gostwyck Road. <https://www.uralla.nsw.gov.au/files/assets/public/v/1/council-services/building-development/da-tracking/2020/nov-2020/da-45-2020-313-gostwyck-road-uralla-see.pdf> |
| `desirehomes-coen-283.pdf` | Desire Homes (QLD builder) — published house plan brochure, "The Coen 283". <https://www.desirehomes.com.au/wp-content/uploads/The-Coen-283.pdf> |
| `dp-wilston-house-extension.pdf` | Designer Planning (QLD building designer) — published plan example, Wilston house extension. <https://www.designerplanning.com.au/wp-content/uploads/2018/07/WILSTON-HOUSE_Merge.pdf> |

## Hosts tried and blocked in this hunt (for reproducibility)

- `moyne.vic.gov.au` planning-application PDFs — connection reset / 403 (WAF)
- `yourhome.gov.au` house-design PDFs — 403
- `housing.qld.gov.au` / `chde.qld.gov.au` standardised & indicative floor plans — 403
- `files.metricon.com.au` design-collection brochures — 403
- `gilgandra.nsw.gov.au` tender drawings — connection reset
- `midwestern.nsw.gov.au` DA-on-exhibition PDFs — 404 (files rotated off exhibition)
