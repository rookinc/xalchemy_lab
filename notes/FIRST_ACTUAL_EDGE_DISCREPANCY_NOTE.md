# First Actual-Edge Discrepancy Note

## Checkpoint

Using the first partially filled actual-edge signed-lift seed, the resolved loop parities are:

- global_return = 0
- global_square = 1
- global_twist = 1

## Why this matters

This is the first point where an actual-edge computation disagrees with the earlier symbolic role assignment.

Earlier symbolic scaffold:
- global_return = 0
- global_square = 0
- global_twist = 1

First actual-edge seed:
- global_return = 0
- global_square = 1
- global_twist = 1

So the first disagreement is on `global_square`.

## Interpretation

This does not yet kill the bridge.

It means at least one of the following must be reconsidered:

1. the chosen actual representative for `global_square`
2. the chosen actual representative for `global_twist`
3. the old symbolic assumption that the square-type specimen should be even

## Current strongest reading

The first actual-edge seed preserves:

- return = even
- twist = odd

but makes the currently chosen square representative odd as well.

That is the first real geometric tension revealed by the lift-backed computation.

## Next step

Search for a different actual 4-cycle or small closed walk in the full template that is a better candidate for the even square-type bridge specimen.

