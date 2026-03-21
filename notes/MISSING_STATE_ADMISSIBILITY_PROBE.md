# Missing-State Admissibility Probe

## Problem

The local invariant phase portrait realizes 7 of the 8 possible states
\[
(A,\sigma,\tau)\in \mathbb Z_2^3.
\]

The only missing state is
\[
(1,1,0).
\]

Under the current quotient law
\[
(R,Q,W)=(0,\;A+\sigma,\;A+\tau),
\]
this missing state would map to
\[
(0,0,1),
\]
the same bridge signature as the theorem bucket \((0,0,1)\).

So the question is:

> Is \((1,1,0)\) genuinely forbidden by the local geometry, or merely absent from the tested perturbation orbit?

## G60 reading

Under the toy G60 packet model:

- A is the receipt of anchor channel H
- sigma is the receipt of the square packet {S1,S2,S3}
- tau is the receipt of the twist packet {T1,T2,T3}

the missing state corresponds to:

- anchor flipped
- square packet odd
- twist packet even

So the first admissibility conjecture is:

> the upstairs chamber-transport law may forbid the simultaneous pattern
> anchor exchanged + square packet odd + twist packet even

even though the quotient map itself allows it.

## First test strategy

To search for \((1,1,0)\) downstairs, the smallest candidate perturbations should satisfy:

- flip e00 to force A = 1
- flip an odd number of {e02,e05,e10} to force sigma = 1
- flip an odd number of {e01,e04,e07} to force tau = 0, since baseline tau = 1

So the minimal candidate family is:

- e00
- one edge from {e02,e05,e10}
- one edge from {e01,e04,e07}

That is the first direct search family.

## Interpretation of outcomes

If such a perturbation realizes \((1,1,0)\), then the missing state was only orbit-missing, not geometrically forbidden.

If no such perturbation realizes \((1,1,0)\), then the local quotient cube has an admissibility constraint not visible in the quotient law alone.

