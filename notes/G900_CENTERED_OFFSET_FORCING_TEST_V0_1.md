# G900 Centered Offset Forcing Test v0.1

## Goal
Test whether the midpoint law is forced once the rung is required to be the true center class of the prism weighting.

## Structural assumption
Require the prism weights to be centered around the rung:

- top - rung = -(bottom - rung)

Equivalently:

- (top - rung) + (bottom - rung) = 0
- top + bottom = 2 * rung
- rung = (top + bottom) / 2

## Interpretation
This is stronger than arithmetic face-sum matching.
It says the rung is not merely another weight, but the actual center of the prism offset law.

## Expected effect
The previously surviving noncentered candidates:

- (140, 144, 150)
- (140, 146, 150)

should now be rejected.

## Consequence if confirmed
If this centered-offset rule is accepted as a structural law of the exact prism quotient, then the midpoint identity is forced.

