# Theorem: Quotient Map from the Local Invariant Orbit

## Setup

Let the current seeded local signed-lift model determine a mod-2 edge state
\[
\varepsilon : E \to \mathbb Z_2.
\]

Define the local cluster invariants
\[
A := \varepsilon(e00),
\]
\[
\sigma := \varepsilon(e02)+\varepsilon(e05)+\varepsilon(e10)\pmod 2,
\]
\[
\tau := \varepsilon(e01)+\varepsilon(e04)+\varepsilon(e07)\pmod 2.
\]

Let the local bridge signature be
\[
(R,Q,W)\in \mathbb Z_2^3,
\]
where:
- \(R\) is the return-type class signature,
- \(Q\) is the square-type class signature,
- \(W\) is the twist-type class signature.

---

## Quotient map

Define the map
\[
\Phi:\mathbb Z_2^3 \to \mathbb Z_2^3
\]
by
\[
\Phi(A,\sigma,\tau) = (0,\;A+\sigma,\;A+\tau).
\]

Then the current local bridge signature is given by
\[
(R,Q,W)=\Phi(A,\sigma,\tau).
\]

Equivalently,
\[
R=0,\qquad Q=A+\sigma,\qquad W=A+\tau.
\]

---

## Theorem

In the present seeded local signed-lift neighborhood, the class-based bridge signature is the image of the local invariant orbit under the quotient map
\[
\Phi(A,\sigma,\tau)=(0,\;A+\sigma,\;A+\tau).
\]

More precisely:

1. edge-level local perturbations induce changes in the lift state \(\varepsilon\);

2. these edge-level changes collapse to the invariant triple
   \[
   (A,\sigma,\tau)\in \mathbb Z_2^3;
   \]

3. the bridge signature depends only on this triple, through \(\Phi\);

4. therefore the bridge signature is a quotient of the local invariant state space.

---

## Proof sketch

The factorization formulas
\[
R=0,\qquad Q=A+\sigma,\qquad W=A+\tau
\]
were already established directly from the chosen class representatives.

The orbit-classifier computation then adds two further facts.

### 1. Many edge-level perturbations collapse to the same invariant triple

Different flip patterns were found to produce the same \((A,\sigma,\tau)\).
In particular, the theorem bucket
\[
(A,\sigma,\tau)=(0,0,1)
\]
contains many distinct perturbation realizations.

So the invariant triple is genuinely coarser than the raw edge-level state.

### 2. Each tested invariant triple determines exactly one bridge signature

Across the tested orbit, whenever two perturbations produced the same invariant triple, they also produced the same bridge signature.

Thus the bridge signature is constant on the fibers of the projection from edge-level states to invariant triples.

It follows that the bridge signature factors through the invariant orbit and is exactly the image of that orbit under \(\Phi\). ∎

---

## Corollary

The current local bridge should be read as a three-stage structure:

\[
\text{edge-level lift state}
\;\longrightarrow\;
(A,\sigma,\tau)
\;\xrightarrow{\ \Phi\ }\;
(R,Q,W).
\]

So the return/square/twist class split is not primary at edge level.
It emerges as a quotient of the local invariant state space.

---

## Example buckets

### Theorem bucket
\[
(A,\sigma,\tau)=(0,0,1)
\quad\Longrightarrow\quad
(R,Q,W)=(0,0,1).
\]

This bucket contains many tested realizations, including:
- the baseline seed,
- several boundary flips,
- several spectator flips,
- several compensating core double flips.

### Other buckets
Examples from the tested orbit include:
\[
(0,0,0)\mapsto(0,0,0),
\]
\[
(0,1,0)\mapsto(0,1,0),
\]
\[
(0,1,1)\mapsto(0,1,1),
\]
\[
(1,0,1)\mapsto(0,1,0),
\]
\[
(1,0,0)\mapsto(0,1,1),
\]
\[
(1,1,1)\mapsto(0,0,0).
\]

So distinct invariant triples may project to the same bridge signature.
This is why the bridge signature is properly understood as a quotient object.

---

## Plain-English reading

The local bridge is no longer best described as “some edges flip and some loops change.”

The stronger statement is:

- the microscopic lift data collapses to three coarse mod-2 invariants;
- those three invariants feed a simple law;
- that law produces the return/square/twist signature.

So the bridge signature is an emergent quotient of the local invariant orbit.

---

## Status

This remains a local seeded theorem checkpoint.
What is established is that, on the tested local orbit, the bridge signature is completely controlled by the quotient map
\[
\Phi(A,\sigma,\tau)=(0,\;A+\sigma,\;A+\tau).
\]

What remains open is whether an analogous quotient description persists in fuller lift completions and in the broader global construction.

