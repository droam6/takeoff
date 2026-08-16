# QUICKSTART

Get a takeoff out of a plan set in about two minutes of typing plus a few minutes of
waiting.

---

## What you need

| | |
|---|---|
| **Python** | 3.9 or newer |
| **PyMuPDF** | `pip install pymupdf` |
| **Claude Code** | installed and logged in, with `claude` on your PATH |
| **A plan set** | vector PDF with a selectable text layer — see `INTAKE.md` |

---

## macOS

### One-time setup

```bash
# from the repo folder
python3 -m pip install --user pymupdf

# confirm Claude Code is on PATH
which claude
# → /Users/you/.local/bin/claude   (any path is fine, as long as it prints one)
```

### Run a job

```bash
cd ~/Desktop/takeoff

python3 takeoff.py sample_plans.pdf \
    --job sample \
    --trade tiler \
    --rooms "main bath and master ensuite - floors and walls" \
    --wastage 10
```

Output lands in `jobs/sample/`:

```
jobs/sample/
├── TAKEOFF_sample.md      ← the deliverable
├── intake_report.md       ← the gate result + the tradie's answers
├── order_settings.md      ← the profile settings applied to this job's ORDER
├── sheet_register.md      ← page → sheet title → scale
├── all_text.txt           ← full text layer, per page
├── text_coords.txt        ← every text run with x/y + rotation
└── pages/page_01.png …    ← one image per page
```

### With a customer profile

```bash
# set the profile up once
cp customers/_TEMPLATE.md customers/dave-tiling.md   # then fill it in

# every job after that
python3 takeoff.py plans.pdf --customer dave-tiling

# this job is different from their usual, and we know the tile
python3 takeoff.py plans.pdf --customer dave-tiling \
    --lay-pattern herringbone --tile-size "600x600 porcelain" --m2-per-box 1.44
```

The profile changes the **order** only — lay pattern, extra for cuts, buffers, rounding,
box counts. It cannot change a measured area. See `PROFILE_QUESTIONS.md`.

Cut-allowance precedence, highest first:

```
--wastage  →  --lay-pattern  →  the profile's default pattern  →  10%
```

A missing or unconfirmed profile never blocks a job: it runs trade-standard defaults, says
so on the order box, and repeats the profile questions at the bottom of the takeoff.

### Useful variations

```bash
# just check whether the plans are measurable - no analysis, no cost
python3 takeoff.py plans.pdf --intake-only

# extract pages and text but don't call Claude (useful for eyeballing a set)
python3 takeoff.py plans.pdf --no-analyse

# floors only - a set with no elevations then passes intake instead of failing
python3 takeoff.py plans.pdf --no-walls --rooms "all floors"

# sharper page images for fine dimension text (slower, bigger files)
python3 takeoff.py plans.pdf --dpi 220

# put jobs somewhere else
python3 takeoff.py plans.pdf --outdir ~/Documents/takeoff-jobs
```

---

## Windows (PowerShell)

### One-time setup

```powershell
# from the repo folder
py -m pip install --user pymupdf

# confirm Claude Code is on PATH
Get-Command claude
# → CommandType  Name        Source
#   Application  claude.cmd  C:\Users\you\AppData\Roaming\npm\claude.cmd
```

> On Windows, Claude Code usually installs as **`claude.cmd`**. `takeoff.py` detects that
> and runs it through `cmd.exe /c` automatically — you don't need to do anything.

### Run a job

```powershell
cd $HOME\Desktop\takeoff

py takeoff.py sample_plans.pdf `
    --job sample `
    --trade tiler `
    --rooms "main bath and master ensuite - floors and walls" `
    --wastage 10
```

Output lands in `jobs\sample\`.

### Useful variations

```powershell
# just check whether the plans are measurable
py takeoff.py plans.pdf --intake-only

# extract only, no analysis
py takeoff.py plans.pdf --no-analyse

# floors only
py takeoff.py plans.pdf --no-walls --rooms "all floors"

# sharper page images
py takeoff.py plans.pdf --dpi 220

# custom output folder
py takeoff.py plans.pdf --outdir $HOME\Documents\takeoff-jobs
```

### If `claude` isn't found

Point at it explicitly:

```powershell
$env:CLAUDE_CLI = "C:\Users\you\AppData\Roaming\npm\claude.cmd"
py takeoff.py plans.pdf
```

macOS/Linux equivalent:

```bash
export CLAUDE_CLI="$HOME/.local/bin/claude"
python3 takeoff.py plans.pdf
```

---

## What happens when the plans aren't good enough

The intake gate runs **before** any analysis. If it fails, you get a
`REJECTED_<job>.md` instead of a takeoff, and nothing is spent on measuring:

```
[1/3] intake gate
      PASS  encryption           PDF is not locked
      PASS  page_count           1 page(s)
      FAIL  text_layer           0 extractable characters (need 200)
      FAIL  dimension_tokens     0 mm dimension tokens found (need 30)
      FAIL  plan_pages           0 floor plan sheet(s) detected

INTAKE FAILED - no analysis run.
Wrote jobs/badinput/REJECTED_badinput.md
We never guess off bad inputs.
```

`REJECTED_<job>.md` is written to be forwarded to the tradie as-is: it says what's missing,
what it means, and what to send instead. See `INTAKE.md` for the full list of requirements.

---

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success — takeoff written (or `--intake-only` / `--no-analyse` completed) |
| `1` | Intake failed (rejection written), or the analysis step produced no file |
| `2` | The PDF path doesn't exist |

Handy for scripting:

```bash
python3 takeoff.py plans.pdf --intake-only && echo "measurable" || echo "send it back"
```

---

## Full option list

```
positional:
  pdf                  path to the plan set PDF

options:
  --job NAME           job name (default: the PDF filename)
  --outdir DIR         where job folders go (default: ./jobs)
  --dpi N              page render resolution (default: 150)
  --trade TRADE        tiler / painter / waterproofer / other
  --rooms TEXT         which rooms and surfaces to quote
  --wastage VALUE      explicit override; normally comes from the lay pattern
  --customer NAME      load customers/<name>.md
  --lay-pattern P      straight / brick bond / diagonal / herringbone - this job only
  --tile-size TEXT     e.g. "600x600 porcelain"
  --m2-per-box N       adds a boxes-to-buy line, rounded up to whole boxes
  --no-walls           floors only; missing elevations warn instead of failing
  --intake-only        run the gate and stop
  --no-analyse         extract pages + text, but don't call Claude
  --timeout SECONDS    analysis timeout (default: 3600)
```

---

## The questions to ask

All of these are flags, but they come from a conversation. If any are missing they're
carried into the output as questions rather than guessed.

**Every job** (`INTAKE.md` §B) — these change what you deliver:

1. **What's your trade?** → `--trade`
2. **Which rooms, and which surfaces?** → `--rooms`
3. **Lay pattern for this job**, if it's not their usual → `--lay-pattern`
4. **Tile size / format?** → `--tile-size`
5. **m² per box?** (optional, gives them a boxes-to-buy line) → `--m2-per-box`

**Once per customer** (`PROFILE_QUESTIONS.md`) — these go in `customers/<name>.md` and get
applied to every job after that, without asking again:

1. Default lay pattern, and the extra for cuts they run for each
2. Skirting in the order box, or kept separate
3. Box counts wanted
4. Rounding — 0.1 m² or whole m²
5. Tile-source quirks — batch variation, long reorder lead times
6. Anything they always want flagged

Ask the profile questions **with the first delivery, not before it.** A tradie who has just
seen his numbers will answer "how do you want these set up". The same questions sent ahead
of any value read as a form.
