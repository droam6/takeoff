#!/bin/sh
# Re-fetch the backtest corpus into backtest/inbox/ (gitignored - see SOURCES.md
# for why the PDFs are not committed).
#
# Gets 7 of the 9 sets from a clean clone:
#   - 5 downloaded below
#   - sample_plans.pdf copied from the repo root (the control)
#   - sample-floors-only-derived.pdf built from it (the PARTIAL case)
# The remaining 2 (+1 derived from them) cannot be re-fetched:
#   - ssc-da220327 / ssc-da181440: council WAF returns 403 (verified 2026-08-23)
#   - phone-scan-of-da-plans.pdf derives from ssc-da220327
# They exist only where they were first fetched. See SOURCES.md.

set -e
cd "$(dirname "$0")/inbox" 2>/dev/null || { mkdir -p "$(dirname "$0")/inbox"; cd "$(dirname "$0")/inbox"; }

get() { [ -f "$1" ] || curl -sS -L --max-time 180 -o "$1" "$2"; echo "  $1"; }

get derbyshire-construction-sample.pdf  "https://derbyshire.com.au/wp-content/uploads/2016/03/Construction-Document-Sample-1.pdf"
get housedesigners-working-drawings.pdf "https://thehousedesigners.com.au/wp-content/uploads/2015/11/working-drawings-sample.pdf"
get creativehomeplans-sample.pdf        "https://creativehomeplans.com.au/wp-content/uploads/2016/09/Sample-Drawings-for-Web-Page.pdf"
get eastcoast-sample-plan-set.pdf       "https://eastcoastbuildingdesign.com.au/wp-content/uploads/2013/09/2012.sample-plan-set.pdf"
get ncc-building-plans-example.pdf      "https://ncc.abcb.gov.au/sites/default/files/download/2021-07/Building%20plans%20and%20documentation%20(1).pdf"

cp -n ../../sample_plans.pdf . 2>/dev/null || true
echo "  sample_plans.pdf (control, from repo root)"

python3 - <<'EOF'
import pathlib
import fitz
if not pathlib.Path('sample-floors-only-derived.pdf').exists():
    doc = fitz.open('sample_plans.pdf')
    doc.select([i for i in range(doc.page_count) if i + 1 not in (10, 11, 15, 16, 20, 22)])
    doc.save('sample-floors-only-derived.pdf')
print("  sample-floors-only-derived.pdf (PARTIAL case, derived)")
EOF

echo "Done: 7 of 9 corpus sets. ssc-da220327, ssc-da181440 and phone-scan cannot"
echo "be re-fetched (WAF) - run on the machine that holds them for the full nine."
