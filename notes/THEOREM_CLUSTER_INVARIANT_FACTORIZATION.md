# Theorem: Cluster-Invariant Factorization of the Local Bridge

## Statement

In the current seeded local signed-lift model, the tested class-based bridge signature factors through the three mod-2 invariants

\[
A := \varepsilon(e00),
\]
\[
\sigma := \varepsilon(e02)+\varepsilon(e05)+\varepsilon(e10)\pmod 2,
\]
\[
\tau := \varepsilon(e01)+\varepsilon(e04)+\varepsilon(e07)\pmod 2.
\]

The return, square, and twist class signatures are then given by

\[
R = 0,
\qquad
Q = A+\sigma,
\qquad
W = A+\tau
\pmod 2.
\]

## Meaning

The local/global bridge does not require an edge-by-edge description at leading order.

Instead, it factors through:

- one anchor invariant \(A\),
- one square-cluster invariant \(\sigma\),
- one twist-cluster invariant \(\tau\).

So the bridge is controlled by a three-variable mod-2 law.

## Evidence

This factorization matches all tested cases:
- baseline
- single core flips
- single boundary flips
- single spectator flips
- core double flips
- cluster triple flips

In every tested case, the predicted signature from \((A,\sigma,\tau)\) matched the actual signature.

## Conclusion

At this checkpoint, the strongest current local theorem is that the class-based bridge signature factors through the invariant triple

\[
(A,\sigma,\tau)\in\mathbb Z_2^3.
\]

