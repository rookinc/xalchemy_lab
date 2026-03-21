# Theorem/Proof (Paper Voice): Cluster-Invariant Factorization of the Local Bridge

## Theorem

Let \(\varepsilon : E \to \mathbb Z_2\) denote the mod-2 edge state induced by the current seeded local signed-lift model.

Define the three cluster invariants
\[
A := \varepsilon(e00),
\]
\[
\sigma := \varepsilon(e02)+\varepsilon(e05)+\varepsilon(e10)\pmod 2,
\]
\[
\tau := \varepsilon(e01)+\varepsilon(e04)+\varepsilon(e07)\pmod 2.
\]

Let \(R,Q,W\in \mathbb Z_2\) denote the return-, square-, and twist-type class signatures determined by the chosen local actual-edge representatives:
- return-type representative:
  \[
  q0 \to q1 \to q0,
  \]
- square-type representative:
  \[
  q0 \to q1 \to q6 \to q3 \to q0,
  \]
- twist-type representative:
  \[
  q0 \to q1 \to q5 \to q2 \to q0.
  \]

Then the local bridge signature factors through the triple \((A,\sigma,\tau)\) according to
\[
R = 0,
\qquad
Q = A+\sigma,
\qquad
W = A+\tau
\pmod 2.
\]

In particular, the class-based bridge signature is controlled, at this checkpoint, by the three coarse invariants \(A,\sigma,\tau\), rather than by the full edge-by-edge state.

---

## Proof

By definition, the return-type representative traverses the anchor edge \(e00\) out and back. Hence
\[
R=\varepsilon(e00)+\varepsilon(e00)=A+A=0 \pmod 2.
\]

Next, the chosen square-type representative is the even 4-cycle
\[
q0 \to q1 \to q6 \to q3 \to q0,
\]
which uses the edge set
\[
\{e00,e05,e10,e02\}.
\]
Therefore
\[
Q=\varepsilon(e00)+\varepsilon(e05)+\varepsilon(e10)+\varepsilon(e02).
\]
Rearranging gives
\[
Q=A+\bigl(\varepsilon(e02)+\varepsilon(e05)+\varepsilon(e10)\bigr)=A+\sigma \pmod 2.
\]

Similarly, the chosen twist-type representative is the odd 4-cycle
\[
q0 \to q1 \to q5 \to q2 \to q0,
\]
with edge set
\[
\{e00,e04,e07,e01\}.
\]
Hence
\[
W=\varepsilon(e00)+\varepsilon(e04)+\varepsilon(e07)+\varepsilon(e01),
\]
so
\[
W=A+\bigl(\varepsilon(e01)+\varepsilon(e04)+\varepsilon(e07)\bigr)=A+\tau \pmod 2.
\]

This proves the factorization formulas
\[
R=0,\qquad Q=A+\sigma,\qquad W=A+\tau.
\]

To verify that this is not merely a formal rewriting of the baseline seed, robustness sweeps were performed across:
- single essential-core flips,
- single boundary/spectator flips,
- double flips within the tested core,
- triple flips of the twist and square clusters.

In every tested case, the directly recomputed bridge signature agreed with the signature predicted by the invariant triple \((A,\sigma,\tau)\). Thus the factorization is empirically exact on the entire tested local perturbation set.

Therefore, within the present seeded local signed-lift neighborhood, the bridge signature factors through the three cluster invariants \(A,\sigma,\tau\). ∎

---

## Corollary

At this checkpoint, the return/square/twist class split is not most naturally regarded as a property of three isolated loops. Rather, it is a property of the invariant triple
\[
(A,\sigma,\tau)\in \mathbb Z_2^3,
\]
with
- return fixed by mod-2 doubling,
- square controlled by \(A+\sigma\),
- twist controlled by \(A+\tau\).

---

## Remark

This is still a local seeded theorem checkpoint. What has been established is a stable local factorization law in the tested actual-edge neighborhood. What remains open is whether the same factorization, or an analogous one, persists under fuller lift completion and in the broader global construction.

