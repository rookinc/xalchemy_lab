# Derived Next Square Constraints Note

Current known actual-edge values:

- e00 = 0
- e01 = 1
- e04 = 0
- e07 = 0

## Candidate square 1

Cycle:
- q0 -> q1 -> q6 -> q3 -> q0

Edges:
- e00, e05, e10, e02

Parity:
- e00 + e05 + e10 + e02
- = e05 + e10 + e02

So this square is even iff:

    e02 + e05 + e10 = 0 mod 2

## Candidate square 2

Cycle:
- q0 -> q2 -> q8 -> q3 -> q0

Edges:
- e01, e08, e11, e02

Parity:
- e01 + e08 + e11 + e02
- = 1 + e08 + e11 + e02

So this square is even iff:

    e02 + e08 + e11 = 1 mod 2

## Meaning

The next edge fill should not be arbitrary.

It should be guided by these parity constraints if the goal is to search for an even square-type representative near the current bridge zone.

