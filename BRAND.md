# BRAND — CHALKLINE

**Name:** CHALKLINE
**Tagline:** *Measured, not guessed.*

A chalk line is the first true line on a job. You snap it before you lay anything, and
everything after it references back to it. If the line's wrong, the floor's wrong, and no
amount of good work later fixes it.

That is the product in one object. It is also a word every tiler already owns — nobody has
to be taught what it means, which is the same test we apply to every word in a takeoff.

The tagline is the doctrine in three words. It is the promise (*measured*) and the
differentiator (*not guessed*) in the same breath, and it is the sentence the intake gate,
the cross-check engine and the questions section all exist to keep.

---

## 1. Wordmark — typographic only

No logo art. No icon, no monogram, no drawn mark. The wordmark is set type on a rule.

```
CHALKLINE
─────────────────────────────
Measured, not guessed.
```

| | |
|---|---|
| **Wordmark** | `CHALKLINE`, uppercase, heavy sans (700), letter-spacing **+0.14em** |
| **The rule** | 2pt solid, full width of the wordmark block, in Chalk Blue — *this is the snapped line, and it is the only piece of graphic device the brand gets* |
| **Tagline** | `Measured, not guessed.` sentence case, regular weight, 60% grey, sitting under the rule |
| **Lockup** | Wordmark, rule, tagline. Always that order, always left-aligned. Never centred, never stacked differently, never set on an angle. |

**Typeface:** system sans throughout — Helvetica / Arial / the platform default. Deliberate.
A tradie opens this on a phone, in a PDF viewer, in an email preview. A licensed display face
that falls back to Times on someone's Android is worse than a plain face that renders the
same everywhere. Monospace only inside the ORDER THIS box and code/working blocks.

**Never:** stretch it, outline it, put it on a photo, add a tile motif, add a trowel, add a
house shape, or set the wordmark in the accent colour. The wordmark is near-black; the rule
carries the colour.

## 2. Colour

**One accent. That's the whole palette.**

| Role | Hex | Use |
|---|---|---|
| **Chalk Blue** | `#1462A0` | The rule under the wordmark, header strip rule, section dividers, the ORDER THIS box border, ⚠ marks, table header fills at 8% tint |
| Ink | `#1A1A1A` | All body text and the wordmark |
| Grey | `#666666` | Tagline, footer, captions, "not parsed" states |
| Rule grey | `#D8D8D8` | Table borders |
| Paper | `#FFFFFF` | Background |

Chalk Blue is the blue of a chalk line reel — the temporary line you snap and work to. It
survives greyscale printing as a mid-tone, which matters because these get printed in utes
and site sheds on whatever's in the machine.

**No second accent. No green for good, no red for bad.** Colour never carries meaning on its
own — a colour-blind tradie and a black-and-white printer must both get the full message from
the marks and the words alone.

## 3. Iconography

**✅ and ⚠ are the only iconography in the system.** No other symbol, ever.

| Mark | Means |
|---|---|
| ✅ | Ready to order. Use this number. |
| ⚠ | Confirm this first. |

Every ⚠ has a matching tick-box question. Nothing is flagged without being asked.
No confidence scores, no percentages, no stars, no traffic lights, no emoji beyond these two.
See `TAKEOFF_METHOD.md` §6.

## 4. Document header strip

Top of **page 1**, full width, rule underneath in Chalk Blue. Carries the wordmark on the
left and the document control block on the right.

```
CHALKLINE                                    Job ref          TKF-001
─────────────────────                        Takeoff          Rev A
Measured, not guessed.                       Drawings         Rev L, 01/09/25
                                             Supersedes       none
                                             Date             16 Aug 2026
═══════════════════════════════════════════════════════════════════════════
```

**Every field is load-bearing:**

- **Job ref** — `TKF-###`. One per job, sequential. It's what he quotes back to us.
- **Takeoff Rev** — ours. `Rev A` first issue, `Rev B` after his answers, and so on. A
  takeoff that gets re-issued must be distinguishable from the one it replaces, or he'll
  quote off the wrong PDF.
- **Drawings** — *the revision we measured against.* This is the most important line in the
  whole strip. Drawings get superseded constantly. If he's holding Rev N and we measured
  Rev L, every number is stale and this line is the only thing that tells him.
- **Supersedes** — `none`, or the takeoff rev this replaces.
- **Date** — measured, not sent.

**Pages 2+** get the slim strip: wordmark, job ref, takeoff rev, page number. Nothing else.

## 5. Document footer strip

Every page, full width, rule above in rule grey.

```
───────────────────────────────────────────────────────────────────────────
Answer the questions — we re-issue free within 24 hours.   hello@chalkline.example · 04XX XXX XXX      3 / 9
```

The re-issue promise is **said once** — here, as page furniture. It never appears in the
body copy, never gets restated in a section, never turns into a paragraph. It is the
standing offer, and repeating it in prose would make it read like marketing instead of a
term of service.

Contact is a placeholder until the front door exists (`BUSINESS_PLAN.md` Phase 3).

## 6. The ORDER THIS box — the signature

Do not restyle this. It is the most recognisable thing we make, and the dotted leaders are
the reason: they're how a materials list has been written on paper for a hundred years, and
they make a number findable at a glance on a phone.

```
==================================================
          ORDER THIS
==================================================
  Floor tiles ..............   36.4 m²
  Wall tiles ...............   58.6 m²
  Feature tiles ............   12.0 m²
  Tile skirting ............    7.3 m
  + ~50.8 m² master ensuite walls — pending Q1
==================================================
  Straight lay, 10% extra for cuts and breakage —
  trade standard, not your settings yet.
```

Rules:
- Monospace, so the leaders line up.
- ASCII `=` rules top, middle and bottom. Not a styled table, not a coloured panel.
- Dotted leaders between label and figure, always.
- **Pending lines live inside the box**, prefixed `+ ~`, with the question that unblocks
  them. They are part of the answer — a tradie who reads only the box must still learn that
  a room is missing from it. Keeping them outside was hiding the incomplete part of the job
  in a place he could skip.
- The settings line sits under the bottom rule, inside the box (`TAKEOFF_METHOD.md` §10.1).

Sibling box, same construction, immediately after: **NOT INCLUDED**. Same width, same rules,
no dotted leaders — it's a list, not a quantity.

## 7. Boxes generally

Three box types, all built from ASCII rules in monospace so they survive any renderer:

| Box | Where | Contains |
|---|---|---|
| **ORDER THIS** | Page 1, first thing | The quantities. Pending lines included. |
| **NOT INCLUDED** | Page 1, straight after | Scope we did not measure, and anything ⚠-unresolved. |
| **SITE NOTES** | Page 2, after the rooms | Drawing-set quirks a person on site needs to know. |

## 8. Structure — ANSWER PACK, then PROOF

The document is two documents in one binder.

**ANSWER PACK** — pages 1–3. What to order, what to check, what to answer. Written to be
read on a phone, in a ute, once.

**THE PROOF** — everything after the divider. Full working, every cross-check, every sheet.
Written to be checked, not read.

The divider is unmissable and says so in as many words:

```
═══════════════════════════════════════════════════════════════════════════
   THE PROOF — for checking, not reading.
═══════════════════════════════════════════════════════════════════════════
```

That line does real work. A tradie who stops at the divider has everything he needs and
knows he hasn't missed anything. A tradie who wants to audit us has all of it. Neither one
has to wade through the other's document, and nobody has to guess which mode they're in.

## 9. Voice

Short sentences. One idea per line. The word a tradie would use standing in the room.
Never "trapezoid", "reconciliation", "wastage factor", "provisional" — the full substitution
table is in `TAKEOFF_METHOD.md` §9.2 and it is part of the brand, not a style preference.

We say what we don't know before we say what we do. That's the tagline working.
