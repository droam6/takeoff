# Customer profile — <NAME>

Copy this file to `customers/<name>.md` and fill it in from the answers to
`PROFILE_QUESTIONS.md`. Load it with `takeoff.py --customer <name>`.

Anything left at the default is treated as **not yet answered**, and every takeoff will say
so and repeat the question. Nothing in here can change a measured area — only the conversion
from measured to order.

```
customer: <NAME>
trade: tiler
status: DEFAULTS - not yet confirmed

# Q1  default lay pattern, and the extra for cuts he runs for each
default_lay_pattern: straight
wastage_straight: 10
wastage_brick_bond: 10
wastage_diagonal: 15
wastage_herringbone: 15

# Q2  skirting in the order box, or kept separate
skirting_in_order_box: yes

# Q3  box counts as well as m2, when we know the tile coverage
want_box_counts: yes

# Q4  rounding:  0.1  (to a decimal)  |  whole  (rounded up to whole m2)
rounding: 0.1

# Q5  tile-source quirks, as added percentage points on top of the cut allowance
batch_variation_buffer: 0
reorder_lead_time_buffer: 0

# Q6  things to flag on every job regardless
always_flag: waterproofing zones, trims in lineal metres
```

## Notes

Free text. Anything worth remembering about how this customer works — suppliers he uses,
jobs he's had trouble on, who he quotes for, what he says he'd pay.
