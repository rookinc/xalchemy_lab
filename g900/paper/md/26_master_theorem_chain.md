# Master Theorem Chain

## Status
Control note

## Purpose
Record the final logical chain of the current G900 frame-2 obstruction result in its cleanest order, separating:

- the ambient full seam,
- the distinguished locked slot-4 slice,
- the bounded exclusion theorem,
- and the exact seam family theorem.

This note is not a new theorem. It is the control map for the paper.

---

## 1. Exact prototype

Define the normalized exact frame-2 prototype by
\[
E_2=[o4,s0,t0,s2,t2,s4].
\]

This is the normalized representative of the raw frame-2 action cell.

---

## 2. Full normalized frame-2 seam

Let
\[
\Sigma_2^{\mathrm{full}}
\]
denote the full normalized frame-2 seam: the action-cell states at normalized action distance \(1\) from the exact frame-2 prototype, with frame 2 among the nearest action frames.

This is the ambient seam object.

---

## 3. Coordinate-slice decomposition

For each \(j\in\{0,1,2,3,4,5\}\), define the coordinate slice
\[
\Sigma_2^{(j)}
:=
\{c\in\Sigma_2^{\mathrm{full}}:\ c_k=(E_2)_k \text{ for all }k\neq j\}.
\]

Thus
\[
\Sigma_2^{\mathrm{full}}=\bigcup_{j=0}^5 \Sigma_2^{(j)}.
\]

So the full seam decomposes into single-coordinate slices around \(E_2\).

---

## 4. Slot-4 puncture identifies the distinguished slice

Inside the full seam,
\[
\Sigma_2^{(4)}
=
\{c\in\Sigma_2^{\mathrm{full}}:\ \pi_4(c)\neq t2\}.
\]

This follows because every slice \(\Sigma_2^{(j)}\) with \(j\neq 4\) agrees with \(E_2\) at coordinate \(4\), hence keeps \(\pi_4=t2\).

Therefore the puncture condition
\[
\pi_4\neq t2
\]
identifies exactly the distinguished slot-4 slice.

---

## 5. Locked witness set lies in the slot-4 slice

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

Thus
\[
L\subseteq \Sigma_2^{(4)}.
\]

So the locked witness regime begins inside the punctured slot-4 slice.

---

## 6. Bounded slot-4 exclusion theorem

In the bounded retained substitution regime generated from \(L\),
\[
\pi_4(c)\in\{o4,s0,s2,s3,s4,t0,t3,t4\}
\]
for every reachable state \(c\). In particular,
\[
\pi_4(c)\neq t2.
\]

This is the bounded slot-4 exclusion theorem.

---

## 7. Locked slice invariance

Let
\[
\Sigma_2^L
\]
denote the seam states reachable from the locked witness set under the retained seam dynamics.

Since every such state satisfies
\[
\pi_4(c)\neq t2,
\]
the puncture-slice identification yields
\[
\Sigma_2^L\subseteq \Sigma_2^{(4)}.
\]

So the locked witness dynamics preserve the distinguished slot-4 slice.

---

## 8. Exact seam family theorem

The slot-4 slice selected by the locked witness regime is exactly
\[
\Sigma_2^{(4)}
=
\{[o4,s0,t0,s2,x,s4]:
x\in\{o4,s0,s2,s3,s4,t0,t3,t4\}\}.
\]

Equivalently, every seam state reachable from the locked witnesses is obtained from the exact prototype
\[
E_2=[o4,s0,t0,s2,t2,s4]
\]
by changing exactly the single coordinate \(4\).

This is the exact seam family theorem.

---

## 9. Frozen-five and witness corollaries

From the exact seam family theorem it follows that:

- positions \(0,1,2,3,5\) are rigid,
- only position \(4\) varies,
- seam-local \(O\)-support is contained in \(\{o4\}\),
- in witness language \(WXYZTIW\), only \(T\) varies,
- the obstruction localizes to the \(T\)-sector.

These are corollaries, not separate main theorems.

---

## 10. Bounded no-closure corollary

Exact frame-2 closure would require the prototype slot value
\[
t2.
\]

But the bounded locked regime remains in the punctured slot-4 slice and never realizes \(t2\). Therefore no exact frame-2 closure occurs in the bounded locked regime.

---

## 11. Final shortest form

The current result chain is:

1. the full normalized frame-2 seam decomposes into coordinate slices around \(E_2\);
2. the puncture condition \(\pi_4\neq t2\) identifies the distinguished slot-4 slice;
3. the locked witness regime preserves this punctured slice;
4. that slice is exactly the one-coordinate deformation family
   \[
   [o4,s0,t0,s2,x,s4];
   \]
5. therefore the bounded locked regime cannot realize exact frame-2 closure.

---

## 12. Remaining open problem

The remaining structural question is no longer what the locked seam family is. That is now known.

The remaining question is:

> why do the locked witness dynamics preserve the punctured slot-4 slice of the full frame-2 seam?

That is the cleanest next theorem frontier.

