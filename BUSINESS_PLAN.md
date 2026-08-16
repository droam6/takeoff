# TAKEOFF — Business Plan

*Version 1 · 16 August 2026 · reviewed every Sunday*

---

## 1. What it is

**TAKEOFF is a done-for-you plan-measurement service for trades.**

A tradie sends us their plan set. We send back a room-by-room m² breakdown the same day.
Every number shows its working. Every gap in the drawings comes back as a question, not a
guess.

That's the whole product. There is nothing to install, nothing to learn, no seat licence,
no onboarding call.

**It is a service they send plans to, not software they have to learn.** That distinction
is the entire positioning, and it is the reason this can win against better-funded
products. A solo tiler does not want a measurement tool. He wants the measuring to have
already happened.

What comes back:

- Floor m² per room, net of what he doesn't tile
- Wall m² per wall, at true tiling heights — not assumed ceiling heights
- Feature-tile zones priced separately, because they're a different SKU
- Niches, skirting, linear metres
- Wastage toggle: measured / +10% / +15%, side by side, his choice
- A **QUESTIONS FOR YOU** section leading the document
- A **CONFIRM BEFORE QUOTING** checklist closing it

Delivery: PDF or markdown, back by end of day. Intake by email or WhatsApp — wherever he
already is.

---

## 2. The problem

**Solo tradies lose 45+ minutes per quote measuring plans at night.**

The quoting happens after the tools go down. Six on site, then dinner, then a set of PDFs
on a laptop at the kitchen table with a scale rule and a calculator, working out how many
square metres of wall tile are in a bathroom. It's the least enjoyable hour of the day and
it's unpaid.

And it's high-stakes:

- **One wrong wall eats the job's margin.** Measure a 2700 ceiling where the drawing calls
  a 450 splashback and you've quoted 29 m² of tiling that doesn't exist — or the reverse,
  and you wear the difference.

- **A bounding-box read of a non-rectangular room is catastrophic.** In our sample set, the
  master ensuite measures 19.9 m² as a rectangle and 10.7 m² as a tiled floor. That's a
  9 m² over-order — roughly $1,400 of porcelain plus the labour hours quoted against area
  that isn't there.

- **The error is invisible until the tiles run out.** By then he's on site, short, and
  eating it.

Our first customer — a Sydney tiler, and the source of the sample set in this repo — put it
plainly:

> **"It's a pain in the arse for all tradies."**

*All tradies.* Not "for me." He volunteered the market size in the same breath as the
complaint. That is the sentence this business is built on.

The competitive nuance underneath: he is not looking for a tool. He has been offered tools.
He wants the problem to go away.

---

## 3. Why it wins

The market splits into two camps and neither serves a solo tradie well.

**Camp 1 — DIY takeoff software** (Groundplan, Metres.ai, Bluebeam, PlanSwift).
Genuinely good products. They ask the tradie to learn software, set up a project, calibrate
a scale, trace areas with a mouse, and maintain a subscription. That is a *new evening
task* replacing an old one. Adoption among solo operators is poor for exactly this reason.
They sell to the tradie who wants to become an estimator. Most don't.

**Camp 2 — human estimating services.**
Accurate, trusted, and priced for builders and commercial contractors — typically several
hundred dollars and multi-day turnaround. Structurally unable to serve a $6k bathroom quote
where the tradie needs an answer tonight.

**TAKEOFF sits in the gap: the outcome of camp 2 at a price and speed that works for camp 1's
customer.**

Three things make that possible:

### 3.1 The AI pipeline runs on an existing subscription

The marginal cost of a takeoff is close to zero. Deterministic extraction (PyMuPDF) plus a
model doing the one thing models are actually good at here — associating printed dimensions
with the elements they describe — running on a subscription that's already paid for. That
is what makes **per-job pricing** viable at a price a solo tradie will pay without thinking
about it. A human estimator cannot get there. A software company charging per seat has no
reason to try.

### 3.2 Distribution nobody else has

**The founder talks to tradies face-to-face six days a week.**

This is not a growth hack, it's the actual moat on the demand side. The hardest thing about
selling to trades is that they don't answer cold email, don't read LinkedIn, don't attend
webinars, and don't trust software companies. They trust the person standing in front of
them who knows what a nib wall is.

An incumbent with 50× the funding still has to buy Google ads against "tile takeoff
software" and convert a stranger. We get a warm conversation on a job site, an existing
relationship, and the ability to hand back a finished takeoff for a job the tradie is
quoting *this week*. Customer #1 came from that. So will customers #2 through #5.

### 3.3 We compete on accuracy, and we can prove it

Everyone claims accuracy. We are the only ones who will hand over the working, list what we
weren't sure about, and refuse jobs we can't measure properly. Section 4 is the mechanism.

---

## 4. The accuracy doctrine (the moat)

Accuracy is the product. Not speed, not price, not the interface. If the numbers are wrong,
nothing else matters, and if they're reliably right, nothing else has to be perfect.

Six commitments, each of them a real mechanism already built into this repo:

### 4.1 Intake requirements, enforced

Bad input is the largest single source of bad output, and it is the cheapest to eliminate.
Every job passes an automated gate (`INTAKE.md`, `takeoff.py`) **before** any analysis:
vector PDF with a real text layer, printed mm dimensions, elevations if walls are wanted,
notes pages included, plus three answers from the tradie.

Fail → a polite `REJECTED_<job>.md` saying exactly what's missing and what to send instead.
No partial takeoff, no best-effort guess.

Turning work away looks like lost revenue. It is the opposite: it is the only way to make
"our numbers are right" a claim we can keep. And "I can't measure this yet, here's what I
need" is a message no competitor sends, which is precisely why it builds trust.

### 4.2 Deterministic extraction and deterministic math

The model never does arithmetic that matters and never reads a number off a picture.

- Text and coordinates come out of the PDF with PyMuPDF. Deterministic.
- Areas are computed by explicit formulas from those extracted values. Deterministic.
- **We measure from stated dimensions only. We never scale off the drawing** — a plan
  printed "fit to page" is no longer at its stated scale, and scaling it produces numbers
  that look right and are 3–8% wrong.

### 4.3 AI is used for exactly one thing

Associating a printed dimension with the element it describes: *which wall is this 2150
the height of? is this a wall dimension or a fixture centreline? does this "450" mean a
splashback or a cabinet?*

That is a judgement task on a drawing, which is where a model genuinely outperforms a rule.
It is not asked to do arithmetic, not asked to invent a missing number, and not asked to
decide anything it can't point at on a sheet.

### 4.4 A cross-check engine, not a spot check

Six checks on every job (`TAKEOFF_METHOD.md` §5), all logged with pass/fail in the delivered
document:

1. Segment chains sum to their stated totals
2. Opposite elevations of the same room agree
3. **Wall runs reconcile with the floor perimeter** — the strongest check available,
   because it ties two independently drawn sheets together

4. Height chains reconcile within each elevation
5. Fixture dimensions agree between plan and elevation
6. Totals fall inside sanity ranges

On the sample set, check 3 came back at 0 mm error on three rooms and 11 mm on a 12-sided
cross-shaped ensuite. That's not a claim of accuracy; it's a demonstration the customer can
read.

Every room then carries a mechanical **confidence rating — HIGH / MED / LOW** — derived from
which checks passed. A LOW room is flagged as not-quotable until its questions are answered.

### 4.5 Never guess — ask

Every inferred value becomes a **numbered question** at the top of the document, phrased so
a tradie can answer it in one word. Not "assumed window height 1360mm" buried in a footnote,
which can only be discovered on site. Instead: *"the window height isn't dimensioned on
sheet 7.02 — I've used 1360 and deducted 1.36 m². What's the actual height?"*

The first can be answered before the quote goes out. The second can only be discovered
after.

**Asking beats assuming. That is the brand.** In practice it also converts: a supplier who
tells you what they don't know is the one you believe about what they do.

### 4.6 Human sign-off before delivery

Nothing goes to a customer unread. The founder reviews every takeoff before it's sent —
scanning the cross-check log, the confidence ratings and the questions list — for as long as
volume allows. Sign-off is what makes it a service rather than an API, and it's where we
learn what the checks are still missing.

### 4.7 Accuracy benchmarked by customer red-pen rounds

The only accuracy metric that counts: **give the tradie a red pen and ask him to mark every
number he thinks is wrong.**

Every pilot delivery asks for it. Every correction becomes a test case and, where it
generalises, a new rule in `TAKEOFF_METHOD.md`. Tracked as:

```
accuracy = 1 − (corrected m² ÷ total m² delivered)
```

Target: **≥98% after one correction round by pilot #5.** Published to customers. If it
can't hold that, section 8 applies.

---

## 5. Offer and pricing

**Per-job pricing, set by discovery.** We ask what it's worth before we tell them what it
costs — customer #1's brief is literally *"mark the errors, and name your price."*

Placeholder tiers, to be replaced with real numbers after five discovery conversations:

| Tier | Scope | Placeholder | Turnaround |
|---|---|---|---|
| **Single room** | One wet area, floor + walls | `$__` | Same day |
| **Whole reno** | 3–6 rooms, floor + walls + niches + skirting | `$__` | Same day |
| **Full house** | Whole set, multi-trade breakdown | `$__` | 24–48 h |

Pricing principles:

- **Per job, not per seat.** He pays when he quotes. No subscription to forget about.
- **Anchor against the alternative**, which is 45 minutes of his evening plus the risk of a
  wrong wall — not against software seat prices.

- **Never price below the value of the risk removed.** Cheap signals unreliable in trades.
- **Re-issue after answered questions is free.** Charging for the second pass would punish
  the exact behaviour the accuracy doctrine depends on.

### The pilot offer

**The first 5 customers are free.** Not a discount — free, explicitly and with a name:
*the pilot*.

In exchange, two things:

1. **Marked-up corrections.** Red pen on the delivered takeoff, every number he thinks is
   wrong.

2. **A testimonial**, if the numbers stand up.

Why free is right here: it removes every objection at once, buys the highest-quality
training data available (a professional's corrections on real drawings), and makes the ask
for corrections *fair* rather than cheeky. Five is enough to find the systematic errors and
few enough that it stays a pilot rather than a habit.

---

## 6. Go-to-market, play by play

### Phase 0 — This week

Send the sample takeoff to **customer #1** (the Sydney tiler whose plans are in this repo).
Two questions, nothing else:

> **1. Mark every number you think is wrong.**
> **2. What would you have paid for this?**

That's the whole message. No pitch, no deck, no pricing page. He already said it's a pain
in the arse; this is the thing that makes it stop being one.

**Success = a marked-up document comes back.** Not a sale. A marked-up document tells us
whether the product works. A polite "looks good, mate" tells us nothing — if that's what
comes back, push once for specifics.

### Phase 1 — 5 free pilots

Source, in priority order:

1. Existing client network — people who already know and trust the founder
2. Face-to-face, on site, six days a week
3. Cold outreach as the top-up, not the strategy

**The in-person ask** (the one that actually converts):

> "How long do you spend measuring plans off for a quote? … Right. Send me the PDF for the
> next one and I'll do it for free — you tell me if I got it wrong. No catch, I'm trying to
> work out if this is worth building."

**Cold SMS:**

> Hey [Name] — [Referrer] gave me your number. I do plan takeoffs for tilers — you send the
> PDF, I send back the m² per room same day, all the working shown. Doing 5 free while I
> get it right. Want me to do your next quote? — [Name]

**Cold Instagram / Facebook DM** (tradies live on Instagram):

> Saw your work on the [suburb] bathroom — nice job. Quick one: how long do you spend
> measuring plans for a quote? I've built something that does the takeoff off the PDF —
> m² per room, walls, niches, the lot, back same day. Giving away 5 free to get it right.
> Want yours done?

**Follow-up if no reply after 3 days** (once, then stop):

> No worries if it's not for you — if you've got a plan set sitting there for a quote this
> week, send it through and I'll knock it over free. Takes me minutes, saves you an evening.

**Delivery ritual for every pilot** — this is what turns a delivery into learning:

1. Send the takeoff
2. *"Grab a red pen — mark anything you reckon is wrong. Even if you're not sure."*
3. Log every correction as a test case
4. Fix the method, re-issue free
5. Ask: *"what would you have paid for that?"*

### Phase 2 — Switch pricing on

Trigger: **accuracy ≥98% after one correction round, across at least 3 pilots.**

- Set real prices from what the five pilots said they'd pay. Take the median, not the top.
- Go back to the pilots first: *"It's live now — $X a job. Want me to keep doing yours?"*
  A pilot who converts is worth more than a new lead, and their answer is the real pricing
  validation.

- **Bake the referral ask into every single delivery.** Not a campaign, a line at the bottom
  of the document:

  > *"Know another tradie who hates measuring plans at night? Send them my way — their first
  > one's on me."*

  Trades are a referral market. This is the only distribution that compounds.

### Phase 3 — Front door and scale

- **Dedicated intake.** A real email address (`plans@…`) and a WhatsApp number. Tradies use
  WhatsApp; meet them there. Auto-acknowledge on receipt with the three intake questions.

- **Scale outreach** on whatever channel actually produced pilots — not all of them.
- **Weekly metrics**, reviewed at the Sunday gate:

  | Metric | Definition | Target by day 30 |
  |---|---|---|
  | **Accuracy after corrections** | `1 − (corrected m² ÷ delivered m²)` | ≥ 98% |
  | **Turnaround time** | plans received → takeoff delivered | < 8 working hours |
  | **Pilot → paid conversion** | pilots who pay for a second job | ≥ 40% |
  | **$ per job** | revenue ÷ jobs delivered | ≥ placeholder tier |
  | Intake rejection rate | rejected ÷ submitted | tracked, not targeted |
  | Questions per job | avg. items in QUESTIONS FOR YOU | trending down |

---

## 7. Unit economics — template

Fill after discovery. Formulas are fixed; the numbers are deliberately blank because
inventing them now would be exactly the guessing this business exists to avoid.

### Inputs

| | Symbol | Value |
|---|---|---|
| Price per job | `P` | `$____` |
| Jobs per week | `J` | `____` |
| Minutes per job (review + send) | `M` | `____` |
| Weeks per month | `W` | `4.33` |
| Model / infra cost per job | `C_v` | `$____` |
| Fixed monthly cost (subscription, tools) | `C_f` | `$____` |
| Founder's target hourly rate | `R` | `$____/h` |

### Formulas

```
Monthly revenue          = P × J × W
Monthly variable cost    = C_v × J × W
Monthly gross profit     = (P − C_v) × J × W
Gross margin %           = (P − C_v) ÷ P
Monthly hours            = (M ÷ 60) × J × W
Effective hourly rate    = Monthly gross profit ÷ Monthly hours
Monthly net              = Monthly gross profit − C_f
Break-even jobs/month    = C_f ÷ (P − C_v)
Capacity ceiling (jobs)  = available hours/month ÷ (M ÷ 60)
```

### The three numbers that decide it

1. **Effective hourly rate** — if this is below what the founder earns on the tools, the
   business is a hobby regardless of revenue.

2. **Break-even jobs/month** — if this is more than a handful, pricing is wrong.
3. **Capacity ceiling** — the point where human sign-off (§4.6) has to change. Know it
   before hitting it, and decide then whether to hire a reviewer or narrow the checks.

### Sensitivity to fill in after pilots

| `P` | `J`/wk | Monthly revenue | Monthly hours | Effective $/h |
|---|---|---|---|---|
| `$__` | `__` | | | |
| `$__` | `__` | | | |
| `$__` | `__` | | | |

---

## 8. Risks and kill criteria

Written down in advance, because the point of a kill criterion is that it's decided while
you're still objective.

### Risk 1 — Accuracy fails after one correction round

**The signal:** a pilot marks up a takeoff, we fix it and re-issue, and he *still* finds
material errors. Or errors are idiosyncratic rather than systematic — meaning there's no
rule to learn, just noise.

**Why it kills it:** the entire proposition is that these numbers are trustworthy. A
takeoff that needs checking is worse than useless — the tradie now does his own measuring
*and* reads ours.

> **KILL: if accuracy is below 95% after one correction round on 3 of the first 5 pilots.**

**Mitigation before then:** narrow the scope. Floors only, rectangular rooms only, one trade.
A small guarantee kept beats a broad one broken.

### Risk 2 — Tradies won't pay

**The signal:** pilots love it, use it, praise it — and go quiet when pricing turns on. Or
they name a price that doesn't clear the effective hourly rate in §7.

**Why it might happen:** the pain is real but intermittent. A tradie quoting two jobs a
month may absorb 90 minutes rather than open his wallet. Free changes behaviour in ways
that don't survive a price.

> **KILL: if fewer than 2 of the first 5 pilots pay for a second job within 30 days of
> pricing going live.**

**Mitigation before then:** test pricing earlier — ask "what would you pay?" at pilot #2,
not pilot #5. Test a per-job price against a small monthly retainer for high-volume quoters.

### Risk 3 — Real-world plans are too poor for intake

**The signal:** a high proportion of submitted sets fail the gate. Photos of plans, raster
scans, undimensioned sketches, floor plans with no elevations. The addressable market is
then much smaller than the number of tradies who have the problem.

**This is the most likely failure mode**, and it's the one the sample set already hints at:
a professionally-produced architectural pack from a Sydney design studio still arrived
missing a floor plan sheet, with an undimensioned ceiling height, three undimensioned
windows, no door heights, and two chains that contradict each other by 165 mm. If *that's*
the good end of the distribution, the middle is rough.

> **KILL: if more than 60% of genuinely-submitted sets fail intake, and tradies won't or
> can't get better files from their designers.**

**Mitigation before then:** go upstream. Sell to the designers and builders who *produce*
the sets, or partner with them so the plans arrive measurable. That's a different business —
but it's a real one, and this failure mode points straight at it.

### Risk 4 — Platform dependency (watch, not kill)

The pipeline runs on a third-party model subscription. Pricing or terms could change.
**Watch:** cost per job monthly. **Mitigate:** the extraction layer is already deterministic
and portable; only the association step is model-dependent, and it is model-agnostic in
principle.

### The Sunday gate

**Every Sunday, one hour.** Four questions, in order:

1. What did the metrics do this week? (§6 Phase 3 table)
2. Did any kill criterion trigger?
3. What did customers actually say — quoted, not paraphrased?
4. What's the single most important thing to do next week?

**If a kill criterion has triggered, it dies without ceremony.** No pivot in the same
meeting, no "let's give it two more weeks." The criterion was set when we were objective;
honour it. Write down what was learned and stop.

This is the discipline the whole plan rests on. *If it can't hold numbers, it doesn't
deserve to exist* — that's true of the product and it's true of the business.

---

## 9. The first 30 days

Built around weekday evening blocks (roughly 90 minutes, after the tools) and a Sunday
review. Nothing here requires quitting anything.

### Week 1 — Prove it on real plans

| Day | Block |
|---|---|
| **Mon** | Finalise the sample takeoff. Read it as a tiler would, not as a builder. |
| **Tue** | **Send to customer #1.** Two questions: mark the errors, name your price. |
| **Wed** | Draft the intake email/WhatsApp template and the three questions. |
| **Thu** | List 15 tradies in the existing network. Names, trade, how you know them. |
| **Fri** | Chase customer #1 gently if quiet. Prep the in-person ask (§6). |
| **Sat** | On-site conversations. Ask the 45-minute question. Say nothing about software. |
| **☉ Sun** | **Gate 1.** Did a marked-up takeoff come back? What was wrong, and was it systematic? |

### Week 2 — Pilots 1–3

| Day | Block |
|---|---|
| **Mon** | Fix every correction from customer #1. Re-issue free. Add each as a test case. |
| **Tue** | Send 8 cold SMS/DMs from the list of 15. |
| **Wed** | Run pilot #2's plan set end to end. Time it — that's the real turnaround number. |
| **Thu** | Deliver pilot #2 with the red-pen ask. Follow up the 8 messages once. |
| **Fri** | Run and deliver pilot #3. |
| **Sat** | Face-to-face. Two more pilots booked. Ask every one what they'd pay. |
| **☉ Sun** | **Gate 2.** Accuracy so far? Turnaround? Any kill criterion triggered? |

### Week 3 — Pilots 4–5, and pricing discovery

| Day | Block |
|---|---|
| **Mon** | Fold week-2 corrections into `TAKEOFF_METHOD.md`. This is the compounding asset. |
| **Tue** | Run pilot #4. |
| **Wed** | Deliver #4. Explicit pricing conversation: *"what's this worth to you?"* |
| **Thu** | Run and deliver pilot #5. |
| **Fri** | Collect all five pricing answers. Take the median. Set the three tiers. |
| **Sat** | Ask the two happiest pilots for a testimonial and one referral each. |
| **☉ Sun** | **Gate 3 — the big one.** Accuracy ≥98%? If yes, pricing goes live Monday. If no, fix or kill. |

### Week 4 — Switch pricing on

| Day | Block |
|---|---|
| **Mon** | **Pricing live.** Message all five pilots: *"it's $X a job now — want me to keep doing yours?"* |
| **Tue** | Set up the front door: `plans@` address, WhatsApp number, auto-acknowledge with the three questions. |
| **Wed** | Add the referral line to the delivery template. Work the referrals from week 3. |
| **Thu** | First paid job, start to finish. Time it. Record the true cost per job. |
| **Fri** | Fill in §7 with real numbers. Compute the effective hourly rate. |
| **Sat** | Face-to-face outreach on the channel that actually produced pilots. |
| **☉ Sun** | **Gate 4 — the 30-day verdict.** Conversion ≥40%? Effective $/h clears the bar? Continue, narrow, or stop. |

### The 30-day verdict

Three numbers decide it. Everything else is commentary.

| | Continue if | Kill if |
|---|---|---|
| **Accuracy** after one correction round | ≥ 98% | < 95% on 3 of 5 |
| **Pilot → paid** within 30 days of pricing | ≥ 2 of 5 | < 2 of 5 |
| **Effective hourly rate** | > on-the-tools rate | < on-the-tools rate with no path up |

---

*TAKEOFF measures from stated dimensions only. It never scales off the drawing, and it never
guesses. That rule is the product, and it is the business.*
