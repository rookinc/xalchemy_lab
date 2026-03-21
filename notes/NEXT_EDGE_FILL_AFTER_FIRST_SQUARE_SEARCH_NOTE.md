# Next Edge Fill After First Square Search Note

## Current result

The first actual-edge square search found exactly one fully supported 4-cycle:

- q0 -> q1 -> q5 -> q2 -> q0

with parity 1.

So no even square candidate exists yet in the currently filled neighborhood.

## Meaning

This does not settle the question.
It only means the current filled edge set is too small.

There are still many skipped 4-cycles whose parity cannot yet be evaluated.

## Next step

Fill more actual lift edges in the local neighborhood around the current bridge zone.

Recommended next batch:

- e05
- e08
- e10
- e11

Then rerun:

- run_derive_cocycle_from_signed_lift
- run_search_even_square_candidates

## Goal

See whether an even square-type loop appears once the local neighborhood is enlarged.

