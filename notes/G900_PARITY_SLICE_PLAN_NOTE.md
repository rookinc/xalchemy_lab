# G900 parity slice plan note

## Goal

Refine the coarse weighted prism quotient by separating even and odd layer contributions.

The current coarse prism weights are:

- bit-0 face = 140
- macro rung = 145
- bit-1 face = 150

But parity-phase probing shows these are aggregated from two different layer regimes.

So the next explicit task is to build:

- even-layer 6-class quotient matrix
- odd-layer 6-class quotient matrix

---

## Questions

1. Does the even slice still have exact triangular-prism support?
2. Does the odd slice still have exact triangular-prism support?
3. Are the two slices related by a clean exchange law?
4. Do rung weights sit between the two bit-face weights in both slices?

---

## Expected even totals

- bit-0 face = 160
- macro rung = 240
- bit-1 face = 320

## Expected odd totals

- bit-0 face = 260
- macro rung = 195
- bit-1 face = 130

---

## Why this matters

If both parity slices retain prism support, then the prism is stable under parity refinement.

If their weights invert in a clean way, then the carrier is exhibiting a genuine alternating two-phase law rather than a numerical accident.

