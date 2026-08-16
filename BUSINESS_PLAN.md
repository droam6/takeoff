# CHALKLINE — Business Plan

**Measured, not guessed.**

*Version 2 · 16 August 2026 · reviewed every Sunday*

---

## 1. What it is

**A done-for-you plan-measurement service for trades.**

A tradie sends a plan set. He gets back a branded PDF the same day: room-by-room m², what to
order, what to check, and every number's working. Nothing to install, nothing to learn, no
seat licence, no onboarding call.

**It is a service they send plans to, not software they have to learn.** That distinction is
the entire positioning. A solo tiler does not want a measurement tool. He wants the measuring
to have already happened.

What comes back:

- Floor m² per room, net of what he doesn't tile
- Wall m² per wall, at true tiling heights — not assumed ceiling heights
- Feature-tile zones priced separately, because they're a different SKU
- Niches, skirting, linear metres
- An **ANSWER PACK** — three pages: what to order, what to check, what to answer
- **THE PROOF** behind a divider — every number's working, for checking not reading

---

## 2. The model — three tiers, locked

Three tiers, in order. **We do not skip ahead**, and the last one is a maybe.

### Tier 1 — operator-run service. Now, and for as long as it works.

Plans arrive by **text, email or WhatsApp**. A person runs the pipeline, reviews the output,
and sends a **branded PDF back the same day**. **Priced per job.** No login, no dashboard, no
account to create.

Every job is read by a human before it goes out. That is what makes the accuracy claim
keepable, and it is how we keep learning from drawings we didn't choose. The tradie's entire
experience is *send plans, get numbers* — the same as sending them to an estimator, at a
price and speed that works for a $6k bathroom.

**The software is private machinery. It is never sold.**
Not as a licence, not white-labelled, not on-prem, not as an API for someone else's app, and
never as a one-time download. The pipeline is what makes the service possible; selling it
turns us into a software vendor competing with Groundplan on their terms, with their support
burden and none of their distribution. This will be asked for. The answer is *we'll do the
takeoff*.

### Tier 2 — a front door, when volume demands it.

A dedicated number and a simple one-page site that feeds the same queue, plus an
auto-acknowledgement that asks the three job questions.

This is plumbing, not a product. It removes the operator from the *receiving* of work, never
from the checking of it. **Triggered by volume, not by ambition** — specifically, when intake
admin exceeds roughly a quarter of the time spent measuring.

### Tier 3 — hosted subscription, only if demand pulls it.

Seats for larger outfits — builders and multi-crew operations sending several jobs a week —
who want to upload their own plans and manage their own queue.

Built **only** when customers are actively asking for it and the per-job model is straining.
Never because it looks like a better multiple. It trades away the human sign-off (§5.6), so
it is a genuinely different product and gets its own accuracy bar before it ships.

**Never a one-time exe.** Subscription seats or nothing. A perpetual licence is the same
mistake as selling the program, with a version-support tail attached.

---

## 3. The problem

**Solo tradies lose 45+ minutes per quote measuring plans at night.**

The quoting happens after the tools go down. Six on site, then dinner, then a set of PDFs on
a laptop at the kitchen table with a scale rule and a calculator. It's the least enjoyable
hour of the day and it's unpaid.

And it's high-stakes:

- **One wrong wall eats the job's margin.** Measure a 2700 ceiling where the drawing calls a
  450 splashback and you've quoted 29 m² of tiling that doesn't exist — or the reverse, and
  you wear it.
- **A bounding-box read of a non-rectangular room is catastrophic.** In the sample set, the
  master ensuite measures **19.9 m² as a rectangle and 10.7 m² as a tiled floor** — a 9 m²
  over-order, which at typical porcelain prices is well over a thousand dollars of tile
  before the labour hours quoted against floor that isn't there.
- **The error is invisible until the tiles run out.** By then he's on site, short, and
  eating it.

Angus, customer #1, a North Shore tiler and the source of the sample set in this repo:

> **"It's a pain in the arse for all tradies."**

*All tradies.* Not "for me." He volunteered the market size in the same breath as the
complaint. That is the sentence this business is built on.

He is not looking for a tool. He has been offered tools. He wants the problem to go away.

---

## 4. Why it wins

The market splits into two camps and neither serves a solo tradie well.

**Camp 1 — DIY takeoff software** (Groundplan, Metres.ai, Bluebeam, PlanSwift). Genuinely
good products. They ask the tradie to learn software, set up a project, calibrate a scale,
trace areas with a mouse, and maintain a subscription. That is a *new evening task* replacing
an old one. They sell to the tradie who wants to become an estimator. Most don't.

**Camp 2 — human estimating services.** Accurate, trusted, and priced for builders —
typically **$200+** and multi-day turnaround. Structurally unable to serve a $6k bathroom
quote where the tradie needs an answer tonight.

**CHALKLINE sits in the gap: the outcome of camp 2, at a price and speed that works for camp
1's customer.**

### 4.1 Marginal cost is near zero

Deterministic extraction (PyMuPDF) plus a model doing the one thing models are good at here —
associating printed dimensions with the elements they describe — running on a subscription
that is already paid for. That is what makes **per-job pricing at $30–150** viable. A human
estimator cannot get there. A software company charging per seat has no reason to try.

### 4.2 Distribution nobody else has

**Face-to-face trade contact, six days a week.**

This is the moat on the demand side. Trades don't answer cold email, don't read LinkedIn,
don't attend webinars, and don't trust software companies. They trust the person standing in
front of them who knows what a nib wall is.

An incumbent with 50× the funding still has to buy ads against "tile takeoff software" and
convert a stranger. We get a warm conversation on a job site and the ability to hand back a
finished takeoff for a job he's quoting this week.

### 4.3 We compete on accuracy, and we can prove it

Everyone claims accuracy. We are the only ones who hand over the working, list what we
weren't sure about, and refuse jobs we can't measure properly.

---

## 5. The accuracy doctrine (the moat)

Accuracy is the product. If the numbers are wrong nothing else matters; if they're reliably
right, nothing else has to be perfect.

**5.1 Intake requirements, enforced.** Every job passes an automated gate before any
analysis: vector PDF with a real text layer, printed mm dimensions, elevations if walls are
wanted. Fail → a polite `REJECTED_<job>.md` saying what's missing and what to send. Turning
work away is the cheapest quality control that exists.

**5.2 Deterministic extraction and deterministic math.** The model never does arithmetic that
matters and never reads a number off a picture. **We measure from stated dimensions only. We
never scale off the drawing.**

**5.3 AI does exactly one thing** — associating a printed dimension with the element it
describes. Not arithmetic, not inventing missing numbers.

**5.4 A cross-check engine, not a spot check.** Six checks on every job, logged pass/fail in
the delivered document. The strongest: wall runs must reconcile with the floor perimeter,
tying two independently drawn sheets together. On the sample set that came back at **0 mm on
three rooms and 11 mm on a 12-sided cross-shaped ensuite**.

**5.5 Never guess — ask.** Every inferred value becomes a numbered question with **what it's
worth in m²**, so he spends his time on the two that matter and ignores the eight that don't.

**5.6 Human sign-off before delivery.** Nothing goes out unread.

**5.7 Accuracy benchmarked by customer red-pen rounds.**

```
accuracy = 1 − (corrected m² ÷ total m² delivered)
```

Target: **≥98% after one correction round by pilot #5.** Published to customers.

**We already stress-test ourselves.** Nine plan sets we didn't choose, pulled off council DA
trackers and published sample sets, run through the gate cold — and the write-up
(`STRESS_REPORT.md`) leads with our own failures, not the passes. That document is a sales
asset as much as a QA one. Nobody else in this market publishes what broke.

---

## 6. Scale rings — measure the house once, sell the answer N times

**The product is measured geometry.** Once a house is measured, the geometry is done and it
never changes. What changes is which surfaces a given trade cares about, and how the numbers
are re-cut.

That is the whole leverage in this business: **the expensive part happens once, and the
answer sells N times.** A second trade on the same house is a re-cut of numbers we already
hold — minutes of work, not another takeoff.

### Ring 1 — adjacent trades, same maths

Already measured. No new method, no new drawings, no new intake.

| Trade | What they get | Where it comes from |
|---|---|---|
| **Flooring installers** | Floor m² per room + **skirting in lineal metres** | The floor polygons and room perimeters, already computed |
| **Waterproofers** | **Wet zones, priced** — shower areas, hobs, upturns, floor extents | The shower alcoves and bath platforms already deducted from the tiler's floor |
| **Renderers / plasterers** | Wall m² + ceiling m² | The wall runs and gross floor polygons, already computed as the painter's balance |

Sold as a **re-cut add-on**: *"I've already measured this house for the tiler — want the
render quantities for $X?"* Near-zero marginal cost, and it makes the first sale worth more
without another customer conversation.

### Ring 2 — upstream

Where one relationship buys many jobs.

**Small builders.** A whole-house **measured pack** that all their subs price from — floors,
walls, ceilings, wet zones, skirting, split by room and by trade. The builder's benefit is
that every quote he receives is priced off the *same* numbers, so he can compare subs on rate
rather than on who measured optimistically. That is worth real money to him, and it is a
recurring relationship rather than a job.

**Interior designers.** Bundle a takeoff with every drawing issue. The designer looks more
professional, the trades quoting off their drawings get consistent numbers, and the designer
finds out where their own set is under-dimensioned before a builder does. Our questions
section is genuinely useful to them — a free QA pass on their documentation.

### Ring 3 — channels

Where volume arrives without us selling one job at a time.

**Tile and flooring showrooms.** Counter customers walk in holding plans and ask *"how much
do I need?"* Right now the counter staff eyeball it or send the customer away. Instead: the
shop sends the plans in, a **co-branded takeoff** comes back the same day, and the customer
buys the right quantity **from them**.

Why a showroom says yes:

- They convert a browsing customer into a confident order, same day.
- Correct quantities mean fewer returns and fewer "I've run short" callbacks.
- It's a service they offer that the shop down the road doesn't.
- It costs them nothing per job if priced as a wholesale rate or a monthly retainer.

One showroom relationship can be worth more monthly volume than ten individual tradies, and
it comes with implicit endorsement — the tradie hears about us from a supplier he already
trusts.

### Parked — electricians and plumbers

Their takeoffs are **count-based**, not area-based: points, fittings, fixtures, runs. That is
a different method, a different verification layer and a different set of sanity ranges.
Genuinely adjacent, genuinely not the same product. **Revisit after Ring 1 is proven.**
Naming it as parked is deliberate — it is the most tempting distraction on this list.

---

## 7. Getting the name out

Four channels, all cheap, all consistent with a business whose product is proof.

### 7.1 Every anonymised job becomes a 30-second video

The content writes itself, because every takeoff contains a number that surprises a tradie.

> *"This ensuite looks like 20 square metres. It's actually 10.7. Here's over a thousand
> dollars of tile you'd have ordered and never laid."*

Format: the plan on screen, the naive rectangle measurement, then the real polygon. Thirty
seconds, no music, no face required. Australian trade audiences.

It works because it isn't advertising — it's a useful fact with our name at the end. And we
generate one for free with every job we do. **Anonymised always**: no address, no client
name, no title block.

### 7.2 Australian trade Facebook groups

Tiling, renovation and building groups where tradies already ask each other measuring
questions.

**Offer, never spam.** Answer the measuring questions people are already posting, with actual
numbers and working. Post the free-first-job offer where group rules allow it and nowhere
else. One salesy post gets you banned from the only room your customers are standing in.

### 7.3 A referral line in every delivered PDF

Baked into the footer of the takeoff, not run as a campaign:

> *"Know another tradie who hates measuring plans at night? Send them my way — their first
> one's on me."*

Trades are a referral market. This is the only distribution that compounds.

### 7.4 Face-to-face, six days a week

The channel nobody can copy. See §4.2.

---

## 8. The sales ladder

Lowest friction first. Each rung earns the next.

### Rung 1 — the free-first-job wedge

The whole pitch, one message:

> **"Send me any plan set you're quoting this week. First one's free, same-day, mark up
> anything wrong."**

Every objection is answered before it's raised: no cost, no commitment, no software, no
delay, and he is explicitly invited to find fault. **Ask for the mark-up, not the sale** —
mark-ups tell us whether the product works; "looks good mate" tells us nothing.

### Rung 2 — customer #1 plus two referrals

Angus, plus the two names he gives us. A referral from him is worth more than fifty cold
messages, and asking for two is the natural close on a job we did for free.

### Rung 3 — 5 pilots with testimonials

Free, in exchange for marked-up corrections and a testimonial if the numbers stand up. Five
is enough to find the systematic errors and few enough that it stays a pilot rather than a
habit.

### Rung 4 — pricing on, referral ask in every delivery

Trigger: **accuracy ≥98% after one correction round, across at least 3 pilots.** Go back to
the pilots first — a pilot who converts is the real pricing validation.

### Rung 5 — showroom partnership pitch

Only once there are testimonials and a rejection-rate number to quote. Walk in with five
completed takeoffs and a tiler who'll vouch. Pitch the co-branded counter service (§6,
Ring 3).

### Rung 6 — content engine live

Once there's a steady job flow to draw material from. Content without a body of real jobs
behind it is just claims.

---

## 9. Pricing hypothesis

**Final numbers are set by discovery.** These are anchors to test, not decisions.

The anchor sits between two real reference points: **the hour he saves**, and **the $200+ a
human estimator charges**. Price below the hour and it reads as unreliable; price near the
estimator and we've lost the reason we exist.

| Product | Hypothesis | What it covers |
|---|---|---|
| **Wet-areas pack** | **$30–50** | One to three wet areas — floors, walls, niches, skirting |
| **Whole-house interior** | **$80–150** | Every room, one trade, full measured pack |
| **Multi-trade re-cut** | **add-on** | Same house, second trade. Priced as an add-on because the geometry is already done (§6, Ring 1) |
| **Subscriptions** | later | Tier 3 only, and only if demand pulls |

Principles:

- **Per job, not per seat.** He pays when he quotes.
- **Anchor against the alternative** — 45 minutes of his evening plus the risk of a wrong
  wall — not against software seat prices.
- **Never price below the value of the risk removed.** Cheap signals unreliable in trades.
- **Re-issue after answered questions is free.** Charging for the second pass would punish
  the exact behaviour the accuracy doctrine depends on.
- **First 5 customers free.** Not a discount — a named pilot, with a job to do.

---

## 10. What it costs to open the doors

**Under $200.** That is the whole barrier, and it is why the kill criteria in §13 can be
honoured without flinching.

| Item | Cost | Note |
|---|---|---|
| ABN | **$0** | Free from the ABR |
| Business name registration (ASIC) | **~$45–100** | ~$44 for one year, ~$102 for three — verify current fee |
| `.com.au` domain | **~$20/yr** | Requires the ABN |
| One-page site | **$0** | Built in-house |
| WhatsApp Business | **$0** | |
| **Total to open** | **under $200** | |

### From the first *paid* job — not before

| Item | Cost | Why |
|---|---|---|
| **Professional indemnity insurance** | **~$40–70/month** | We supply numbers people quote off |
| **Properly worded terms** | one-off | Scope, limits, and what a takeoff is and isn't |

**Why PI matters here, specifically.** A tradie quotes off our number. If it's wrong he wears
the difference, and he will look at us. That risk is real and it is the price of being useful.

Two lines of defence, in order:

1. **The confirm-before-quoting checklist** at the end of every takeoff, plus the questions
   section, the ⚠ marks, and the rule that anything unresolved is *excluded from the order
   total* rather than quietly included. This is the first line because it prevents the loss
   rather than paying for it. It is also why every takeoff states in plain words what it does
   **not** cover.
2. **PI insurance**, for when the first line fails.

Deliberately staged: **no insurance until money changes hands.** Free pilots are explicitly
framed as pilots, and the exposure is a testimonial rather than a claim. The month the first
invoice is paid, PI goes on.

---

## 11. The unit economics ladder

Four rungs. Each is a real decision point, not a projection.

| Rung | Volume | Monthly revenue | What it proves |
|---|---|---|---|
| **0** | 5 free pilots | **$0** | The numbers are right, and tradies will send plans |
| **1** | **10 paid jobs/month** | **$500–1,000** | People pay. Covers PI, domain and costs with room over |
| **2** | **30 paid jobs/month** | **$1,500–3,000** | A real side income. Forces the Tier 2 front door |
| **3** | Showroom channel + multi-trade re-cuts | beyond | Volume arrives without selling one job at a time |

**Marginal cost is near zero** on the existing Claude subscription. At volume, compute becomes
a small per-job line — and at $30–150 a job it stays a rounding error against price. The
binding constraint is not cost. It is **operator time**, because of the human sign-off rule in
§5.6.

### The three numbers that decide it

1. **Effective hourly rate** — monthly gross profit ÷ hours worked. Below what he earns on
   the tools, this is a hobby regardless of revenue.
2. **Break-even jobs/month** — fixed costs ÷ (price − variable cost). At ~$60/month of fixed
   costs that is **one or two jobs**. The downside is genuinely small.
3. **Capacity ceiling** — the point where human sign-off has to change. Know it before
   hitting it.

### To fill in after pilots

| `P` price | `J` jobs/wk | Monthly revenue | Monthly hours | Effective $/h |
|---|---|---|---|---|
| `$__` | `__` | | | |
| `$__` | `__` | | | |

---

## 12. Milestone gates

**Reviewed Sundays. Anything that fails a gate dies without ceremony.**

### Gate 1 — customer #1

**Pass:** Angus returns a marked-up takeoff **and names a price he'd have paid.** Accuracy
after one correction round is the number that matters.

**Fail:** he can't find the errors *and* won't name a price — meaning it is neither accurate
enough to trust nor valuable enough to buy. A polite "looks good mate" with no price is a
fail, not a pass.

### Gate 2 — two weeks out

**Pass: 5 pilots run, 2 converted to paid.**

**Fail:** fewer than 2 convert within 30 days of pricing going live. Pilots who love it and
go quiet at the invoice are the clearest signal there is.

### Gate 3 — month two

**Pass: 10 paid jobs.** On passing, and not before:

- register the business name with ASIC
- professional indemnity insurance on
- content engine live

Note the sequencing — **the money comes before the paperwork and the marketing.** Registering
a business name and filming content for a business with no paying customers is procrastination
with a receipt.

---

## 13. Risks and kill criteria

Written in advance, because the point of a kill criterion is that it is decided while you are
still objective.

### Risk 1 — Accuracy fails after one correction round

A pilot marks up a takeoff, we fix it and re-issue, and he *still* finds material errors — or
the errors are idiosyncratic rather than systematic, meaning there is no rule to learn.

> **KILL: accuracy below 95% after one correction round on 3 of the first 5 pilots.**

**Mitigation first:** narrow the scope. Floors only, rectangular rooms only, one trade. A
small guarantee kept beats a broad one broken.

### Risk 2 — Tradies won't pay

Pilots love it, use it, praise it — and go quiet when pricing turns on. The pain is real but
intermittent; a tradie quoting two jobs a month may absorb 90 minutes rather than open his
wallet.

> **KILL: fewer than 2 of the first 5 pilots pay for a second job within 30 days of pricing
> going live.** (Same as Gate 2.)

**Mitigation first:** ask "what would you pay?" at pilot #2, not pilot #5. Test per-job
against a small retainer for high-volume quoters.

### Risk 3 — Real-world plans are too poor for intake

**The most likely failure mode, and we are now collecting data on it.** Nine plan sets pulled
off the open web — real lodged NSW DAs, published working-drawing samples, an ABCB reference
set — have been run through the gate, and the results are in `STRESS_REPORT.md`.

The early read is that the binding constraint is more likely to be *sets without internal
elevations* — so, floors only — than sets we cannot read at all. **Floors-only is still a
sellable product**, which softens this risk considerably.

> **KILL: more than 60% of genuinely-submitted sets fail intake, and tradies can't get better
> files from their designers.**

**Mitigation first:** sell floors-only where elevations are missing. Then go upstream to the
designers and builders who *produce* the sets (§6, Ring 2) — a different business, but a real
one, and this failure mode points straight at it.

### Risk 4 — Platform dependency (watch, not kill)

The pipeline runs on a third-party model subscription. **Watch:** cost per job, monthly.
**Mitigate:** extraction is already deterministic and portable; only the association step is
model-dependent, and it is model-agnostic in principle.

### The Sunday gate

**Every Sunday, one hour.** Four questions, in order:

1. What did the metrics do this week?
2. Did any kill criterion trigger?
3. What did customers actually say — quoted, not paraphrased?
4. What is the single most important thing to do next week?

**If a kill criterion has triggered, it dies without ceremony.** No pivot in the same meeting,
no "let's give it two more weeks." The criterion was set when we were objective; honour it.

*If it can't hold numbers, it doesn't deserve to exist* — true of the product and true of the
business.

---

## 14. The first 30 days

Weekday evening blocks, roughly 90 minutes after the tools, plus a Sunday review.

### Week 1 — prove it on real plans

| Day | Block |
|---|---|
| **Mon** | Finalise the sample takeoff. Read it as a tiler would. |
| **Tue** | **Send to Angus.** Two questions: mark the errors, name your price. |
| **Wed** | Draft the intake message and the three job questions. |
| **Thu** | List 15 tradies in the existing network. Names, trade, how you know them. |
| **Fri** | Chase Angus gently if quiet. Prep the in-person ask. |
| **Sat** | On-site conversations. Ask the 45-minute question. Say nothing about software. |
| **☉ Sun** | **Gate 1.** Did a marked-up takeoff come back? Could he name a price? |

### Week 2 — pilots 1–3

| Day | Block |
|---|---|
| **Mon** | Fix every correction from Angus. Re-issue free. Log each as a test case. |
| **Tue** | Send 8 messages from the list of 15. Free-first-job wedge, verbatim. |
| **Wed** | Run pilot #2 end to end. Time it — that is the real turnaround number. |
| **Thu** | Deliver #2 with the red-pen ask. Follow up the 8 messages once. |
| **Fri** | Run and deliver pilot #3. |
| **Sat** | Face-to-face. Two more pilots booked. Ask each what they'd pay. |
| **☉ Sun** | Accuracy so far? Turnaround? Any kill criterion triggered? |

### Week 3 — pilots 4–5 and pricing discovery

| Day | Block |
|---|---|
| **Mon** | Fold week-2 corrections into `TAKEOFF_METHOD.md`. This is the compounding asset. |
| **Tue** | Run pilot #4. |
| **Wed** | Deliver #4. Explicit pricing conversation: *"what's this worth to you?"* |
| **Thu** | Run and deliver pilot #5. |
| **Fri** | Collect all five pricing answers. Take the **median**, not the top. Set the tiers. |
| **Sat** | Ask the two happiest pilots for a testimonial and one referral each. |
| **☉ Sun** | **Gate 2.** 5 pilots run? Accuracy ≥98%? If yes, pricing goes live Monday. |

### Week 4 — switch pricing on

| Day | Block |
|---|---|
| **Mon** | **Pricing live.** Message all five: *"it's $X a job now — want me to keep doing yours?"* |
| **Tue** | Add the referral line to the delivery template. Work week-3 referrals. |
| **Wed** | First paid job, start to finish. Time it. Record the true cost. |
| **Thu** | Fill in §11 with real numbers. Compute the effective hourly rate. |
| **Fri** | Film the first 30-second video from an anonymised job. |
| **Sat** | Face-to-face on whatever channel actually produced pilots. |
| **☉ Sun** | **30-day verdict.** 2 of 5 converted? Effective $/h clears the bar? |

### The 30-day verdict

| | Continue if | Kill if |
|---|---|---|
| **Accuracy** after one correction round | ≥ 98% | < 95% on 3 of 5 |
| **Pilot → paid** within 30 days | ≥ 2 of 5 | < 2 of 5 |
| **Effective hourly rate** | > on-the-tools rate | < it, with no path up |

Month two is Gate 3: **10 paid jobs**, then register the name, PI on, content engine live.

---

*CHALKLINE measures from stated dimensions only. It never scales off the drawing, and it
never guesses. That rule is the product, it is the tagline, and it is the business.*
