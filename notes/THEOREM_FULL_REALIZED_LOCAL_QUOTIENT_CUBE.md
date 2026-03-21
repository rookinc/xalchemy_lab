# Theorem: Full Realized Local Quotient Cube

## Theorem

In the tested local signed-lift model, the full invariant cube
\[
(A,\sigma,\tau)\in \mathbb Z_2^3
\]
is realized.

Moreover, the class-based bridge signature is the quotient image of this full realized cube under the map
\[
\Phi:\mathbb Z_2^3 \to \mathbb Z_2^3,
\qquad
\Phi(A,\sigma,\tau)=(0,\;A+\sigma,\;A+\tau).
\]

Thus the local bridge signature is completely described by the composition
\[
\text{edge-level lift state}
\;\longrightarrow\;
(A,\sigma,\tau)\in \mathbb Z_2^3
\;\xrightarrow{\ \Phi\ }\;
(R,Q,W).
\]

---

## Definitions

Let the mod-2 edge state be
\[
\varepsilon : E \to \mathbb Z_2.
\]

Define:
\[
A := \varepsilon(e00),
\]
\[
\sigma := \varepsilon(e02)+\varepsilon(e05)+\varepsilon(e10)\pmod 2,
\]
\[
\tau := \varepsilon(e01)+\varepsilon(e04)+\varepsilon(e07)\pmod 2.
\]

Let the bridge signature be
\[
(R,Q,W),
\]
where:
- \(R\) is the return-type class signature,
- \(Q\) is the square-type class signature,
- \(W\) is the twist-type class signature.

Then
\[
R=0,\qquad Q=A+\sigma,\qquad W=A+\tau.
\]

---

## Proof sketch

### 1. Factorization

The previously established local factorization law gives
\[
R=0,\qquad Q=A+\sigma,\qquad W=A+\tau,
\]
hence
\[
(R,Q,W)=\Phi(A,\sigma,\tau).
\]

### 2. Realization of all 8 invariant states

Orbit classification over the tested perturbation family realized seven of the eight possible states of \(\mathbb Z_2^3\), with only
\[
(1,1,0)
\]
initially absent.

A subsequent targeted search produced explicit realizations of this missing state, using perturbations of the form:
- flip \(e00\),
- flip one edge from \(\{e02,e05,e10\}\),
- flip one edge from \(\{e01,e04,e07\}\).

Thus all eight invariant triples are realized.

### 3. Quotient conclusion

Since the full cube is realized and the bridge signature depends only on \((A,\sigma,\tau)\) through \(\Phi\), the local bridge signature is the quotient image of the full realized invariant cube. ∎

---

## Consequences

### 1. The bridge signature is many-to-one
The map \(\Phi\) is not injective.
So distinct invariant triples may determine the same bridge signature.

For example, the theorem signature
\[
(0,0,1)
\]
has at least the two invariant preimages:
\[
(0,0,1),\qquad (1,1,0).
\]

### 2. The bridge signature is genuinely coarser than the invariant cube
So the local bridge is not most naturally described at edge level, and not even primarily at invariant-triple level.
Its most natural current description is as a quotient of the invariant cube.

### 3. The bridge hierarchy is now explicit
At this checkpoint the local structure is:

\[
\text{edge state}
\;\to\;
\text{cluster invariants }(A,\sigma,\tau)
\;\to\;
\text{bridge signature }(R,Q,W).
\]

---

## Plain-English reading

The important result is now very strong:

- the microscopic lift data collapses to three mod-2 invariants;
- all 8 possible invariant states actually occur;
- the return/square/twist bridge signature is the quotient image of that full state space.

So the bridge is not just a trick of one seed, one loop, or one perturbation family.
It is the shadow of a fully realized local 3-bit state space.

---

## Status

This remains a local seeded theorem checkpoint, not the final full global theorem.

But it is the strongest local statement obtained so far:
the local bridge signature is the quotient image of the full realized invariant cube.

