# Z2 x Z2 Location Exploration

## Question

Where does the four-state `Z2 x Z2` structure live?

## Candidate locations

### Model A: kernel-resolved
Both bits are present in `r1`.

- `r1 = (localized_site, centroid_orientation, m, d, grammar_seed)`

Interpretation:
The kernel resolves the full four-state orientation class immediately.

### Model B: split
One bit is resolved in `r1`, the other appears in first propagation.

Interpretation:
- one generator belongs to localization/orientation
- one generator belongs to downstream motion

### Model C: downstream-only
The two-bit structure is not part of `r1`.
It appears only in the propagation grammar.

Interpretation:
The kernel stays smaller and the four-state family is a property of the next layer.

## Working intuition

A plausible split is:

- mirror-rotation belongs to local orientation
- diameter-flip belongs to propagation across the scaffold

## Strongest sentence

The next question is whether the `Z2 x Z2` structure is resolved by the kernel or emerges during propagation.

