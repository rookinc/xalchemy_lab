# Lift + Twist Identification Operator

## Observation

The current sketch suggests that the half-step operation is not a vertex label but an identification operator.

A local oriented triple:

- `x`
- `y`
- `z`

is acted on by a directed lift+twist move and reconciled into a single identified state:

- `I`

## Interpretation

This gives the kernel an explicit intermediate stage:

- raw local orientation data
- lift+twist half-step
- identified reconciliation state `I`
- resolved state `r1`

## Strongest sentence

Lift+twist acts as an identification operator sending a local oriented triple into a single reconciled state `I`.

## Candidate factorization

A first candidate kernel factorization is:

- `r0 -> local_oriented_frame -> I -> r1`

where `I` is the first explicit identification state produced by reconciliation.

