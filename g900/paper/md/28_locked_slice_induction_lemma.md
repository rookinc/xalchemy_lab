# Locked Slice Induction Lemma

## Status
Main attack note

## Purpose
Reduce the remaining locked-slice conjecture to a one-step seam-to-seam induction statement.

---

## 1. Ambient setup

Let
\[
E_2=[o4,s0,t0,s2,t2,s4]
\]
be the normalized exact frame-2 prototype.

Let
\[
\Sigma_2^{\mathrm{full}}
\]
be the full normalized frame-2 seam, and let
\[
\Sigma_2^{(4)}
=
\{c\in\Sigma_2^{\mathrm{full}}:\pi_4(c)\neq t2\}
\]
be the distinguished punctured slot-4 slice.

Let
\[
L\subseteq \Sigma_2^{(4)}
\]
be the locked witness set.

---

## 2. Remaining conjecture

The remaining local conjecture is that the locked witness dynamics preserve the punctured slot-4 slice:
\[
\Sigma_2^L\subseteq \Sigma_2^{(4)}.
\]

Equivalently, starting from \(L\), the retained seam dynamics never restore
\[
\pi_4=t2.
\]

---

## 3. Induction reduction

### Lemma 3.1. Locked slice induction lemma
Suppose \(c\in\Sigma_2^{(4)}\) is reachable from \(L\), and suppose \(c'\) is a retained seam-to-seam one-edit child of \(c\). Then
\[
\pi_4(c')\neq t2.
\]

If this lemma holds, then by induction on path length every seam state reachable from \(L\) remains in \(\Sigma_2^{(4)}\).

### Proof
The base case holds because
\[
L\subseteq\Sigma_2^{(4)}.
\]
If the induction step holds, then every one-step retained seam successor of a state in \(\Sigma_2^{(4)}\) remains in \(\Sigma_2^{(4)}\). Therefore every reachable seam state from \(L\) lies in \(\Sigma_2^{(4)}\). ∎

---

## 4. Equivalent formulation

Because puncture identifies the distinguished slice, Lemma 3.1 is equivalent to:

> no retained seam-to-seam one-edit move from the locked slot-4 slice restores the prototype slot value \(t2\).

This is the sharpest local attack on the remaining conjecture.

---

## 5. Script target

The natural verification task is therefore:

1. enumerate the states in the distinguished slot-4 slice,
2. enumerate all one-edit retained seam-to-seam children,
3. test whether any child satisfies
   \[
   \pi_4=t2.
   \]

If none do, then the induction lemma holds for the computed slot-4 slice.

---

## 6. Role in the theorem stack

This note isolates the exact remaining dynamical question.

Everything else is already in place:

- the full seam decomposition,
- puncture identification,
- the exact seam family theorem,
- bounded locked-slice invariance.

The only remaining local step is the one-step seam-to-seam induction lemma.

