# Slot-4 Puncture Identifies the Distinguished Seam Slice

## Status
Working bridge theorem note

## Purpose
Identify the distinguished slot-4 slice of the full normalized frame-2 seam as exactly the punctured part where the normalized slot-4 value differs from the exact prototype value \(t2\).

This note provides the clean bridge between:

- the full seam decomposition,
- the bounded slot-4 exclusion theorem,
- and locked slot-4 slice invariance.

---

## 1. Exact prototype

Let
\[
E_2=[o4,s0,t0,s2,t2,s4]
\]
be the normalized exact frame-2 prototype.

---

## 2. Full seam decomposition

Let
\[
\Sigma_2^{\mathrm{full}}
\]
denote the full normalized frame-2 seam, and for each coordinate \(j\in\{0,1,2,3,4,5\}\) let
\[
\Sigma_2^{(j)}
:=
\{c\in\Sigma_2^{\mathrm{full}}:\ c_k=(E_2)_k \text{ for all } k\neq j\}.
\]

So \(\Sigma_2^{(j)}\) is the \(j\)-slice of the seam: the set of seam states differing from \(E_2\) in exactly the single coordinate \(j\).

---

## 3. Immediate slot-4 consequence of the slice definition

By definition, if
\[
c\in \Sigma_2^{(j)}
\quad\text{with}\quad
j\neq 4,
\]
then the fourth coordinate is unchanged from the exact prototype:
\[
\pi_4(c)=(E_2)_4=t2.
\]

Thus every seam slice except the slot-4 slice keeps the exact prototype value \(t2\) in normalized slot 4.

By contrast, in the slot-4 slice \(\Sigma_2^{(4)}\), the fourth coordinate is the unique variable coordinate, so \(\pi_4\) may differ from \(t2\).

---

## 4. Slot-4 slice identification

### Proposition 4.1. Slot-4 puncture identifies the slot-4 slice
Inside the full normalized frame-2 seam,
\[
\Sigma_2^{(4)}
=
\{c\in\Sigma_2^{\mathrm{full}}:\ \pi_4(c)\neq t2\}.
\]

### Proof
If \(c\in\Sigma_2^{(j)}\) with \(j\neq 4\), then by the slice definition \(c\) agrees with the exact prototype \(E_2\) at coordinate \(4\), hence
\[
\pi_4(c)=t2.
\]
So any seam state with \(\pi_4(c)\neq t2\) cannot lie in any slice \(\Sigma_2^{(j)}\) for \(j\neq 4\). Therefore it must lie in \(\Sigma_2^{(4)}\).

Conversely, if \(c\in\Sigma_2^{(4)}\), then \(c\) differs from \(E_2\) in coordinate \(4\), so
\[
\pi_4(c)\neq t2.
\]
Hence the two sets are equal. ∎

---

## 5. Computational confirmation

The raw-slot verification matches Proposition 4.1 exactly:

- seam survivors arising from slices \(j=0,1,2,3,5\) all satisfy
  \[
  \pi_4=t2,
  \]
- seam survivors in the distinguished slot-4 slice satisfy
  \[
  \pi_4\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
  \]

Thus the puncture condition \(\pi_4\neq t2\) identifies exactly the distinguished slot-4 slice.

---

## 6. Locked-slice invariance as a corollary

Let
\[
\Sigma_2^L
\]
denote the seam states reachable from the locked witness set under the retained seam dynamics.

The bounded slot-4 exclusion theorem gives:
\[
\forall c\in \Sigma_2^L,\quad \pi_4(c)\neq t2.
\]

Applying Proposition 4.1 yields:

### Corollary 6.1. Locked slot-4 slice invariance
\[
\Sigma_2^L\subseteq \Sigma_2^{(4)}.
\]

So the locked witness dynamics remain inside the distinguished slot-4 slice of the full normalized frame-2 seam.

---

## 7. Conceptual interpretation

The full normalized frame-2 seam is larger than the family seen from the locked witnesses. It decomposes into coordinate slices around the exact prototype \(E_2\).

Among those slices, the slot-4 slice is uniquely characterized by the puncture condition
\[
\pi_4\neq t2.
\]

The locked witnesses already lie in this punctured slice, and the bounded dynamics preserve the puncture condition. Therefore the bounded obstruction theorem can be understood as a theorem about a dynamically selected punctured slice of the full seam.

---

## 8. Role in the theorem stack

This note supplies the clean bridge:

1. `23_full_frame2_seam_decomposition.md` defines the ambient seam and its slices,
2. the bounded slot-4 exclusion theorem supplies puncture invariance,
3. the present note identifies puncture with the distinguished slot-4 slice,
4. `24_locked_slot4_slice_invariance.md` then becomes a direct corollary.

So the exact seam family theorem is most naturally read as a theorem about the punctured slot-4 slice selected by the locked witness regime.

