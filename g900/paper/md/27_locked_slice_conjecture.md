# Locked Slice Conjecture

## Status
Main local conjecture

## Purpose
State the cleanest remaining local explanation problem after the exact seam family theorem, full seam decomposition, and slot-4 puncture identification have been established.

---

## 1. Exact prototype and full seam

Let
\[
E_2=[o4,s0,t0,s2,t2,s4]
\]
be the normalized exact frame-2 prototype.

Let
\[
\Sigma_2^{\mathrm{full}}
\]
be the full normalized frame-2 Hamming-1 seam around \(E_2\).

This seam decomposes into single-coordinate slices
\[
\Sigma_2^{\mathrm{full}}=\bigsqcup_{j=0}^5 \Sigma_2^{(j)},
\]
where
\[
\Sigma_2^{(j)}
=
\{c\in\Sigma_2^{\mathrm{full}}:\ c_k=(E_2)_k \text{ for all } k\neq j\}.
\]

---

## 2. Distinguished slot-4 slice

The slot-4 slice
\[
\Sigma_2^{(4)}
\]
is the unique scaffold-preserving slice of the full seam. Equivalently, it is the unique punctured slice characterized by
\[
\pi_4(c)\neq t2.
\]

By the exact seam family theorem,
\[
\Sigma_2^{(4)}
=
\{[o4,s0,t0,s2,x,s4]:
x\in\{o4,s0,s2,s3,s4,t0,t3,t4\}\}.
\]

Thus the slot-4 slice is simultaneously:

- the punctured slice,
- the scaffold-preserving slice,
- the \(T\)-sector slice in witness language.

---

## 3. Locked witness set

The locked witness set is
\[
L=
\{
[o4,s0,t0,s2,t4,s4],\,
[o4,s0,t0,s2,o4,s4],\,
[o4,s0,t0,s2,s3,s4],\,
[o4,s0,t0,s2,s0,s4]
\}.
\]

So
\[
L\subseteq \Sigma_2^{(4)}.
\]

Let
\[
\Sigma_2^L
\]
denote the seam states reachable from \(L\) under the retained seam dynamics.

---

## 4. Main conjecture

### Conjecture 4.1. Locked slice invariance
\[
\Sigma_2^L\subseteq \Sigma_2^{(4)}.
\]

In words:

> the seam dynamics generated from the locked witnesses preserve the unique scaffold-preserving punctured slice of the full normalized frame-2 Hamming shell.

---

## 5. Stronger expected form

### Conjecture 5.1. Locked slice exactness
\[
\Sigma_2^L=\Sigma_2^{(4)}.
\]

In words:

> the locked witness regime generates exactly the full slot-4 slice, and no other seam slice.

This is the strongest natural local theorem target.

---

## 6. Why this is the right conjecture

The previous formulations of the open problem can now be unified.

The conjecture is no longer merely about “slot 4” in isolation. It is about preservation of a uniquely characterized slice of the full seam:

- puncture view:
  \[
  \pi_4\neq t2,
  \]
- scaffold view:
  \[
  [o4,s0,t0,s2,\_,s4],
  \]
- witness view:
  only \(T\) varies in \(WXYZTIW\).

If the locked dynamics preserve one of these descriptions, they preserve all three.

So the conjecture is really about preservation of the unique pure-defect direction in the ambient frame-2 Hamming shell.

---

## 7. Proof routes

### Route 7.1. Puncture invariance route
Prove:

1. the full seam decomposes into six Hamming-1 slices;
2. only \(\Sigma_2^{(4)}\) satisfies \(\pi_4\neq t2\);
3. the locked dynamics preserve \(\pi_4\neq t2\).

Then
\[
\Sigma_2^L\subseteq \Sigma_2^{(4)}.
\]

This is the cleanest formal route.

### Route 7.2. Scaffold preservation route
Prove directly that a seam-to-seam step from a locked witness preserves agreement with \(E_2\) in coordinates
\[
0,1,2,3,5.
\]

Then locked-slice invariance follows immediately.

### Route 7.3. Pure-defect dynamics route
Interpret \(\Sigma_2^{(4)}\) as the unique scaffold-preserving defect direction and show that the retained locked dynamics can move the defect but cannot alter the scaffold.

This is conceptually strongest, but likely comes after Route 7.1.

---

## 8. Present evidence

Current results already support the conjecture strongly:

- \(L\subseteq \Sigma_2^{(4)}\),
- the bounded slot-4 exclusion theorem gives
  \[
  \pi_4(c)\neq t2
  \]
  throughout the bounded locked regime,
- the exact seam family theorem shows that the reachable seam family from the locked witnesses has the form
  \[
  [o4,s0,t0,s2,x,s4].
  \]

So the locked regime already appears confined to the distinguished slot-4 slice.

---

## 9. Role in the paper

This conjecture is now the cleanest remaining local explanation frontier.

The exact seam family theorem identifies the slot-4 slice.
The full seam decomposition identifies the ambient shell.
The present conjecture asks why the locked witness dynamics preserve exactly that slice instead of mixing into the other seam directions.

So the true remaining question is no longer “what is the locked seam family?” but rather:

> why is the locked seam family dynamically invariant?

