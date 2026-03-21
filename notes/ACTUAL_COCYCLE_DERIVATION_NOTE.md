# Actual Cocycle Derivation Note

## True evaluator

The true global bridge bit is not assigned by loop role.
It is computed from the signed-lift cocycle.

Let

    ε : E(G15) -> Z2

be the cocycle of the signed 2-lift G30 -> G15, where:

- ε(e) = 0 for parallel lift
- ε(e) = 1 for crossed lift

Then for any closed loop C in G15, the holonomy parity is

    ω(C) = sum_{e in C} ε(e) mod 2

This is the actual global evaluator.

## Practical reading for current loop types

### global_return
If the loop is an out-and-back walk [x, x^-1], then the corresponding closed walk uses the same base edge twice with opposite orientation.
Over Z2, orientation does not matter for parity counting, so:

    ω(global_return) = ε(x) + ε(x) = 0 mod 2

So the out-and-back loop is automatically even.

### global_square
If the loop is a 4-step closed cycle [s1,s2,s3,s4], then

    ω(global_square) = ε(s1)+ε(s2)+ε(s3)+ε(s4) mod 2

This value must be computed from actual cocycle edge data.

### global_twist
If the loop is a two-path comparison with paths [a,b] and [c,d], then the associated closed cycle is

    [a,b,d^-1,c^-1]

and therefore

    ω(global_twist) = ε(a)+ε(b)+ε(d)+ε(c) mod 2

since orientation does not change the mod-2 edge value.

## Tree gauge simplification

If a tree gauge representative is used, then ε vanishes on tree edges.
So for a fundamental cycle created by a non-tree edge e, one has

    ω(C_e) = ε(e)

This is the cleanest basis-level computation.

## Current bottleneck

The repo still needs actual cocycle edge data, for example from one of:

- signed_lift_edges.json
- cocycle_vector.csv
- tree_gauge_representative.csv
- fundamental_cycle_holonomy.csv

Until one of those is present, the evaluator formula is derived but the numerical values remain uncomputed.

