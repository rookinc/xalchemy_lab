# G900 3x(2+1) sector note

## Current probe result

A crude mod-9 sector probe on the G900 candidate carrier does not populate all 9 sector classes.

Instead, for every inward layer, the occupancy pattern is:

- sectors 0,1 populated
- sector 2 empty
- sectors 3,4 populated
- sector 5 empty
- sectors 6,7 populated
- sector 8 empty

So the pattern is:

`(live, live, null) x 3`

---

## Immediate interpretation

The G900 layer structure may decompose not as 9 equal sectors, but as:

- 3 repeated macro sectors
- each macro sector containing:
  - 2 live classes
  - 1 null / forbidden / unrealized class

This is a candidate `3 x (2+1)` law.

---

## Layer formulas

For layer `k`, the counts appear as:

`3 * (a_k + (a_k - 1) + 0)`

with the sequence:

- `a_0 = 29`
- `a_1 = 26`
- `a_2 = 23`
- `a_3 = 20`
- `a_4 = 17`
- `a_5 = 14`
- `a_6 = 11`
- `a_7 = 8`
- `a_8 = 5`
- `a_9 = 2`

This descends by 3 each layer.

---

## Conjectural meaning

Possible meanings of the null lane:

1. forbidden class
2. degenerate class
3. unoccupied parity
4. gauge artifact of the current crude sector map
5. adjudication / closure seat rather than transport seat

Do not decide yet.

---

## Next question

Can we define:

- a true 3-sector macro index
- a binary live sub-index inside each macro sector

so that each cell receives coordinates of the form:

`(layer, macro_sector, live_bit)`

with the null lane explained rather than merely observed?

