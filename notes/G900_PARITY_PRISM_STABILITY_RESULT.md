# G900 parity prism stability result

The G900 candidate carrier admits a coarse `(macro, bit)` quotient whose support is exactly the triangular prism.

Refining by layer parity shows:

- the even-layer contribution also has exact triangular prism support
- the odd-layer contribution also has exact triangular prism support

So prism support is stable under parity refinement.

Even-slice kind totals:
- bit0 face = 160
- macro rung = 240
- bit1 face = 320

Odd-slice kind totals:
- bit0 face = 260
- macro rung = 195
- bit1 face = 130

Interpretation:

- even layers favor the bit1 sheet
- odd layers favor the bit0 sheet
- the support graph remains prism-shaped in both cases

Therefore the weighted coarse prism is an aggregate shadow of two parity-refined prism laws with opposite sheet bias.

