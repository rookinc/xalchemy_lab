# G900 Triangle Pushforward Notes v0.1

## Current extracted prism law
- top-face edges = 140
- vertical macro-rung edges = 145
- bottom-face edges = 150

## Immediate base sums
For each triangle edge class:

- AB base = top_ab + bottom_ab = 140 + 150 = 290
- BC base = top_bc + bottom_bc = 140 + 150 = 290
- CA base = top_ca + bottom_ca = 140 + 150 = 290

## Open question
The current collapse artifact still records:

- AB = 140 + 150 + side contribution
- BC = 140 + 150 + side contribution
- CA = 140 + 150 + side contribution

What is not yet settled is whether the side contribution is:

1. additive in the final pushed-forward triangle edge weight,
2. zero after quotient identification,
3. bookkeeping-only support attached to the edge but not added numerically,
4. or encoded through a different normalization.

## Current observation
A striking coincidence is already present:

- base triangle edge sum = 290
- macro contact = 290 = 2 * 145

This makes the hypothesis `side contribution = 0 in the final edge-weight total` especially worth testing.

## Present verdict
- triangle pushforward values: not yet fully extracted
- best current base candidate: 290 on each of AB, BC, CA
- side contribution status: unresolved
