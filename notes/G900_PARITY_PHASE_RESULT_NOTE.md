# G900 parity phase result note

## Current result

The order-30 triangular subdivision carrier yields a 900-cell candidate presentation whose first coarse `(macro, bit)` quotient support is exactly the triangular prism.

The coarse weighted prism law is:

- bit-0 face edges = 140
- macro rungs = 145
- bit-1 face edges = 150

This result is exact.

---

## New result

The weighted prism law is not primitive.

A layer-parity probe shows that the coarse weights arise as the aggregate shadow of a strong alternating parity-phase law.

Even-layer contribution totals:

- bit-0 face = 160
- macro rung = 240
- bit-1 face = 320

Odd-layer contribution totals:

- bit-0 face = 260
- macro rung = 195
- bit-1 face = 130

These sum exactly to the coarse prism weights:

- `160 + 260 = 420`
- `240 + 195 = 435`
- `320 + 130 = 450`

and hence recover the full weighted contact totals.

---

## Interpretation

Layer is not merely radial depth.

Layer carries a phase.

Specifically:

- even layers favor the bit-1 face class
- odd layers favor the bit-0 face class

So the carrier alternates sheet preference as depth increases inward.

This means the coarse weighted prism

- 140 / 145 / 150

should be read as a compressed average of a deeper alternating two-phase law rather than as a single uniform contact law.

---

## Strong statement

The G900 candidate carrier is a layered triangular sampled carrier whose first coarse quotient is a weighted triangular prism, and whose prism weights arise from an alternating parity-phase law across inward layers.

---

## Immediate consequence

There are now two meaningful quotient levels already visible:

1. coarse 6-class weighted prism quotient
2. parity-refined prism slices:
   - even-layer prism contribution
   - odd-layer prism contribution

This strengthens the interpretation that the sampled carrier contains a lift-like or sheet-like alternation, not just a static coloring.

---

## Next burden

Construct the even-only and odd-only 6-class quotient matrices separately and test:

1. whether each parity slice still has exact prism support
2. whether the two slices are dual or complementary in a clean sense
3. whether rung weights behave as bridge terms between the two parity regimes

