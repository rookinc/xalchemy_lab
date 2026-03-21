# First Class-Based Actual-Edge Bridge Checkpoint

## Checkpoint

The local/global bridge is now expressed using actual-edge representatives of geometric classes.

### global_return
Even return-type representative:
- q0 -> q1 -> q0

### global_square
Even 4-cycle representative:
- q0 -> q1 -> q6 -> q3 -> q0

### global_twist
Odd 4-cycle representative:
- q0 -> q1 -> q5 -> q2 -> q0

## Local side

- mismatch parity remains the kernel channel
- local lift_bit remains the active bridge observable

## Main result

Across the tested bridge rows, the local lift_bit continues to match the global class representatives:

- return-type -> 0
- square-type -> 0
- twist-type -> 1

and every tested row currently reports `MATCH`.

## Strongest current reading

The bridge is no longer merely symbolic.

It is now:

- actual-edge grounded
- class-based
- stable on the currently filled local lift neighborhood

