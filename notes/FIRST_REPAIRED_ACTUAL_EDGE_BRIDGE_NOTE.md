# First Repaired Actual-Edge Bridge Note

## Checkpoint

After replacing the original odd square representative with an actual even 4-cycle from the partially filled lift neighborhood, the resolved loop parities are now:

- global_return = 0
- global_square = 0
- global_twist = 1

## What changed

The first actual-edge square candidate
- q0 -> q1 -> q5 -> q2 -> q0

was odd.

So the bridge was repaired by searching for a better actual square-type representative.

An even 4-cycle was found:
- q0 -> q1 -> q6 -> q3 -> q0

and assigned as the new `global_square`.

## Meaning

This is the first time the bridge signature

- return = even
- square = even
- twist = odd

has been recovered from actual-edge computation rather than from symbolic role assignment alone.

## Strongest reading

The bridge is still alive under actual-edge testing.

The first discrepancy was not fatal.
It was a representative-choice problem.

## Next step

Feed this repaired actual-edge square representative back into the main bridge table and confirm that the local lift-bit rows still match the repaired actual-edge global roles.

