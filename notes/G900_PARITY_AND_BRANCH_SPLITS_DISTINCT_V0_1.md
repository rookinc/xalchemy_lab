# G900 Parity and Branch Splits Distinct v0.1

## Hard result
The current G900 probes show two different binary layers.

### 1. Branch layer
The coarse weighted prism is centered:

- top face = 140
- vertical / center = 145
- bottom face = 150

So the coarse branch law is:

140 | 145 | 150

and the coarse collapse law is:

140 + 150 = 290

### 2. Parity layer
The parity slice probes show a different split on the same prism carrier.

Even slice totals:
- bit0_face = 160
- macro_rung = 240
- bit1_face = 320

Odd slice totals:
- bit0_face = 260
- macro_rung = 195
- bit1_face = 130

So parity changes weights while preserving prism support.

## Structural conclusion
Parity split and branch split are not the same binary layer.

Instead:

- branch split = coarse centered top/bottom structure around center 145
- parity split = weight redistribution on that fixed prism carrier

## Important artifact status note
The current files:

- specs/paper/g60/even_slice_prism_support_v0_1.json
- specs/paper/g60/odd_slice_prism_support_v0_1.json

still contain the shared scaffold weights 140,145,150.

So those files do not yet reflect the extracted parity-distinguished weight laws shown by the live probes.

## Best current reading
The G900 descent currently exhibits:

1. a support-stable branch prism
2. a distinct parity-weight redistribution layer on that prism
3. a coarse collapse law 140 + 150 = 290

