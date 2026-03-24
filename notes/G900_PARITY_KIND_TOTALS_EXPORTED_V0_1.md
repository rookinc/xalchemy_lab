# G900 Parity Kind Totals Exported v0.1

## Hard result
Parity-distinguished prism kind totals are now exported into artifacts.

Updated artifacts:

- specs/paper/g60/even_slice_prism_support_v0_1.json
- specs/paper/g60/odd_slice_prism_support_v0_1.json
- specs/paper/g60/parity_prism_comparison_v0_1.json

## Exported parity kind totals

### Even slice
- bit0_face = 160
- macro_rung = 240
- bit1_face = 320

### Odd slice
- bit0_face = 260
- macro_rung = 195
- bit1_face = 130

## What is now locked
The even and odd slices:

- share the same triangular-prism support
- do not share the same kind totals
- therefore realize a parity-distinguished weight redistribution layer on a fixed prism carrier

## Important artifact interpretation
The side-specific artifact field:

- prism_model.weights

is currently only a symbolic equal-share placeholder of the form total/3.

Those entries are not yet exact extracted edge-level parity weights.

So the exported hard data is:

- exact support stability
- exact parity-distinguished kind totals

not exact edge-by-edge parity prism weights.

## Structural consequence
This confirms the current best reading:

- branch split = coarse centered prism layer
- parity split = distinct redistribution layer on that same prism support

So branch split and parity split remain distinct binary layers.

## Exact frontier
Still open:

> exact edge-level parity weights on the fixed prism support

Now locked:

> parity-distinguished kind totals on the fixed prism support

