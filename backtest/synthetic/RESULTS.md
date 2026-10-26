# Synthetic run 1 - results (26 Oct 2026)

Seven plan sets drawn from exact geometry (`make_sets.py`); the answer key
(`sets/answer_key.json`) is computed from the same geometry. Engine run **frozen** -
no fixes during or after the run. Scored twice: once by the operator session and once
by an independent agent that had not seen that scoring. Both agree on every line below.

## Numbers - 14 of 14 exact

| Set | What it tests | Floor | Walls | Niche | Skirting |
|---|---|---|---|---|---|
| S1 simple bath | rectangle, door, niche, wall-hung vanity | 6.48 exact | exact | 0.36 exact | n/a |
| S2 L-ensuite | 6 walls, two tile heights, window in band, door half in band | 6.78 exact | all 6 walls exact | 0.304 exact | n/a |
| S3 laundry + powder | floor-standing joinery taken off, splashback only, skirting only | 2.52 / 1.92 exact | 1.08 exact | n/a | 4.88 m exact |
| S5 trap: bad chain | plan chain 150 mm out | exact | exact | exact | n/a |
| S6 trap: no heights | no height printed anywhere | 6.48 exact | held out, asked | 0.36 exact | n/a |

Wall figures take the niche opening off the wall and add all five niche faces back -
stated in every proof, physically correct. Every order figure = measured x 1.10,
rounded as stated. No arithmetic errors between room lines and totals.

## Traps - 2 of 2 passed

- **S5:** raised the 150 mm discrepancy as a top question; used 2400; 2550 used nowhere.
- **S6:** refused to assume a height; walls kept out of the order and asked; noticed
  that the printed 2700 is a wall length, not a height.

## Gate - 6 of 7 right

- PASS where expected: S1, S2, S3, S5, S6. Scan (S7) rejected as expected.
- **MISS - S4 floors-only:** a clean, fully dimensioned single-room floor plan was
  REJECTED instead of PARTIAL - 28 dimension tokens against a 30-token document
  minimum (`MIN_DIM_TOKENS`). Small single-room jobs can be bounced at the door.
  Logged, not fixed.

## Wording errors - 13, none moved an order number

Worth fixing before a customer sees one:
1. S1 trim length: top edge of wall tile given as 9.4 m; correct is 10.2 m (the door
   head is below the tile top, so it doesn't break that edge).
2. S3: says the splashback length "isn't printed" - it is (200 + 1800). Creates a
   needless warning and question.
3. S6: gives an undimensioned line a length of 820 - a scaled number, against the
   "never scale" rule.
4. S6: says a floor waste is drawn - it is only in the notes.
5. Same drawing, three behaviours: the unlabelled door-leaf line is a top question in
   S1/S5 and silent in S6. Run-to-run consistency is not there yet.

Minor: S1 asks about a ceiling height the elevations already give; S1 what-if quotes
the measured change, not the order change; S2 says a printed 1200 isn't printed; S5
overstates the waterproofing note and once calls the defaults "profile"; S6 shows
skirting as "pending" when none is called up; S6 formula condition incomplete.

## What this does and doesn't prove

- **Proves:** on clean, fully dimensioned plans the measuring method is exact,
  including non-rectangular rooms, partial tile bands, joinery and niches - and it
  refuses to guess when a number is missing or contradicted.
- **Does not prove:** anything about real-world plans. These sets are tidy, drawn in
  one style, and every number is present. Real sets are messier - that is round 2:
  real plans with the architect's own room areas printed as an independent key.
- n = 5 measured sets, one run each. Wording varies run to run (item 5 above).
