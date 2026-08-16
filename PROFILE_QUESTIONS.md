# PROFILE QUESTIONS — asked once per customer, applied to every job

The measurements are universal. **The order is personal.**

Two tradies can get the identical set of plans, and the correct measured area is the same
number for both of them. What they should *order* is not — because one lays herringbone and
one lays straight, one buys skirting by the box and one buys it by the lineal metre, one has
been burned by a batch change and now buys 5% over on everything.

So the product splits in two:

```
   PLANS  ──►  MEASURED AREAS  ──►  [ YOUR PROFILE + THIS JOB ]  ──►  ORDER QUANTITIES
               the plans' truth                                        your settings
               never changes                                           changes with you
```

**Nothing in this document can change a measured area.** If a profile setting could move a
measured number, it would be a measurement error dressed up as a preference. These questions
only ever change the conversion from measured to order.

Ask them **once**, on the first job. Store the answers as `customers/<name>.md`. Apply them
to every takeoff for that customer from then on, without asking again.

---

## How to ask them

Not as a form. As part of the first delivery — the tradie has just seen his numbers, so
the questions land as *"how do you want these set up"* rather than *"fill this in before we
start"*. Two minutes on the phone, or a message he can answer in one line each.

If he doesn't answer, we run **trade-standard defaults**, and every takeoff says plainly
that they're defaults and not his settings yet. We never let an unanswered question pass
silently as if it were his choice.

---

## Q1. What's your default lay pattern, and what do you run for cuts?

The single biggest driver of the order quantity. A herringbone floor and a straight floor
over the same room are the same measured area and a materially different order.

Trade-standard defaults we offer — **he can override any of them**:

| Pattern | Default extra for cuts | Why |
|---|---|---|
| **Straight / stack bond** | **10%** | Minimal waste, cuts land on the perimeter |
| **Brick bond / offset** | **10%** | Similar; go 12–15% on a ⅓ offset in large format |
| **Diagonal (45°)** | **15%** | Every perimeter tile is a cut, and the offcuts mostly don't pair up |
| **Herringbone** | **15%** | High cut count; 20% on chevron or on anything over 600 long |

Ask it like this:

> *"What do you normally lay — straight, brick bond, diagonal, herringbone? And what do you
> normally allow for cuts? Most blokes run 10% straight and 15% for diagonal or herringbone —
> if you run something different, tell me and I'll use yours."*

Record the default pattern **and** his percentage for each pattern he uses. Per-job
exceptions are handled at intake (`INTAKE.md` §B4), not here.

## Q2. Do you want skirting in the order box, or kept separate?

Some tilers order tile skirting as part of the tile order. Others cut it from full tiles
and don't want a separate line confusing the count, or they buy it as a trim from a
different supplier entirely.

> *"Tile skirting — do you want it in the main order list, or off to the side?"*

Default: **in the order box**, as lineal metres.

## Q3. Do you want box counts as well as m²?

If we know the tile's coverage, we can convert the order area to **whole boxes, rounded up** —
which is what he actually buys. Suppliers don't sell 36.4 m².

> *"When you tell me the tile, do you want me to work out how many boxes as well as the
> square metres?"*

Default: **yes.** It costs us nothing and it's the number he reads out at the counter.

The m² per box is a **per-job** question (`INTAKE.md` §B5), because the tile changes job to
job. This profile question only records whether he wants the line at all.

## Q4. How do you want numbers rounded?

> *"Do you want them to a decimal — 36.4 m² — or rounded up to whole metres, 37 m²?"*

| Option | What we do |
|---|---|
| **0.1 m²** *(default)* | Round each room to 0.1, then total the rounded rooms |
| **Whole m²** | Round each room **up** to the next whole m², then total |

Whole-m² rounding always rounds **up**, never to nearest — a tradie asking for whole metres
is asking for a buying number, and rounding down a buying number puts him short.

## Q5. Any tile-source quirks we should always allow for?

This is where the scars live, and it's the question that makes a tradie feel like we
actually work in his trade. Two common ones:

**Batch variation buffer.** He's been caught by a dye-lot change mid-job and now buys enough
in one batch to finish, plus spares.

> *"Ever been caught short and had the next batch not match? Do you buy extra to cover it?"*

**Long reorder lead times.** Imported or made-to-order stock where being 2 m² short means the
job stops for six weeks.

> *"Anything you use where a reorder takes forever? Want me to build a bit extra into those?"*

Recorded as **added percentage points on top of the cut allowance**, and always shown as
their own line so he can see exactly what each buffer is costing him:

```
  Measured                33.0 m²
  + 10% extra for cuts     3.3 m²   straight lay, your usual
  + 5% batch buffer        1.7 m²   your standing allowance
  ORDER                   38.0 m²
```

Never folded silently into one percentage. He must be able to see and remove a buffer he set
two years ago for a supplier he no longer uses.

## Q6. Anything you always want flagged?

Things he wants called out on every job whether or not he asked for them on this one.

Common answers:

- **Waterproofing zones** — where the shower zone, hob and upturns are, so he can price
  the membrane or check the waterproofer's scope.
- **Trims in lineal metres** — external corners, edge trims, mitred junctions. In this
  sample set every corner is specified mitred, which is a labour item worth flagging.
- Floor wastes and falls, movement joints, substrate notes, threshold details.

> *"Anything you always want me to point out — waterproofing, trims, falls?"*

Default: **flag waterproofing zones and trims in lineal metres.** Both are cheap for us to
report and expensive for him to miss.

---

## The stored profile

One file per customer at `customers/<name>.md`. Plain `key: value` so a person can read it
and `takeoff.py` can load it. Copy `customers/_TEMPLATE.md` to start one.

```
customer: Sydney Tiler
trade: tiler
status: DEFAULTS - not yet confirmed

default_lay_pattern: straight
wastage_straight: 10
wastage_brick_bond: 10
wastage_diagonal: 15
wastage_herringbone: 15

skirting_in_order_box: yes
want_box_counts: yes
rounding: 0.1

batch_variation_buffer: 0
reorder_lead_time_buffer: 0

always_flag: waterproofing zones, trims in lineal metres
```

`status:` is the honesty switch. While it reads `DEFAULTS - not yet confirmed`, every takeoff
says so on its face and repeats these questions at the bottom. Once he answers, set it to
`CONFIRMED <date>` and the takeoff stops asking.

Load it with:

```bash
python3 takeoff.py plans.pdf --customer sydney-tiler
```

---

## The rule this all rests on

**A profile can never change a measured area.**

Every takeoff prints both sets of numbers, labelled: the measured areas, which are what the
plans say and are the same for everybody; and the order quantities, which are the measured
areas with his settings applied.

If he changes his mind about herringbone, we re-cut the order in seconds and the measured
areas don't move by a millimetre. That's the point of keeping them apart — and it's why he
can trust the measurement even when he disagrees with the allowance.
