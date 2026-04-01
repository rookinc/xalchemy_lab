# Locked Slot-4 Slice Closure Theorem

## Status
Established from direct seam-to-seam verification

## Purpose
Record the strongest local dynamical result now available: the distinguished slot-4 seam slice is closed under retained seam-to-seam one-edit dynamics.

This upgrades the previous locked-slice conjecture to a theorem at the local seam level.

---

## 1. Exact prototype and distinguished slice

Let
\[
E_2=[o4,s0,t0,s2,t2,s4]
\]
be the normalized exact frame-2 prototype.

Let
\[
\Sigma_2^{(4)}
=
\{[o4,s0,t0,s2,x,s4]:
x\in\{o4,s0,s2,s3,s4,t0,t3,t4\}\}
\]
denote the distinguished slot-4 slice of the full normalized frame-2 seam.

Equivalently,
\[
\Sigma_2^{(4)}
=
\{c\in\Sigma_2^{\mathrm{full}}:\pi_4(c)\neq t2\}.
\]

---

## 2. Verified one-step closure data

Direct seam-to-seam verification yields:

- the slot-4 slice contains exactly 8 states,
- every slot-4 slice state has retained seam-to-seam one-edit children,
- the total number of retained seam-to-seam children is 56,
- for every such child \(c'\),
  \[
  \pi_4(c')\in\{o4,s0,s2,s3,s4,t0,t3,t4\},
  \]
- no seam-to-seam child satisfies
  \[
  \pi_4(c')=t2,
  \]
- every seam-to-seam child differs from \(E_2\) in exactly the single coordinate \(4\).

In particular, the child mismatch pattern relative to \(E_2\) is always
\[
[4].
\]

---

## 3. Main theorem

### Theorem 3.1. Locked slot-4 slice closure theorem
Let \(c\in\Sigma_2^{(4)}\), and let \(c'\) be a retained seam-to-seam one-edit child of \(c\). Then
\[
c'\in\Sigma_2^{(4)}.
\]

Equivalently, the distinguished slot-4 slice is closed under retained seam-to-seam one-edit dynamics.

### Proof
The seam-to-seam verification shows that every retained seam-to-seam child of every state in \(\Sigma_2^{(4)}\) has mismatch pattern
\[
[4]
\]
relative to \(E_2\), and no child restores the slot value \(t2\). Therefore every such child remains in the slot-4 slice. ∎

---

## 4. Induction corollary

### Corollary 4.1. Locked slice invariance
Let \(L\subseteq\Sigma_2^{(4)}\) be the locked witness set. Then every seam state reachable from \(L\) by iterating retained seam-to-seam one-edit moves remains in \(\Sigma_2^{(4)}\).

### Proof
The base case holds because \(L\subseteq\Sigma_2^{(4)}\). The induction step is Theorem 3.1. ∎

---

## 5. Closure of the slot-4 alphabet

### Corollary 5.1. Slot-4 alphabet closure
The induced seam-to-seam child relation closes on the 8-symbol slot-4 alphabet
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

In the direct verification, each of these eight values appears equally among the seam-to-seam children.

---

## 6. Interpretation

This theorem completes the local seam story.

The full normalized frame-2 seam is a Hamming-1 shell around \(E_2\), but the distinguished slot-4 slice is not merely a selected subset of that shell. It is a dynamically closed local seam component under retained seam-to-seam one-edit dynamics.

So the locked witness regime does not merely begin in the punctured slot-4 slice. It remains inside that slice under local seam evolution.

---

## 7. Consequence for the theorem stack

The local theorem chain is now:

1. the full frame-2 seam is a normalized Hamming-1 shell around \(E_2\),
2. that shell decomposes into six single-coordinate slices,
3. the slot-4 slice is the unique punctured scaffold-preserving slice,
4. the exact seam family theorem identifies that slice explicitly,
5. the present theorem shows that this slice is dynamically closed under seam-to-seam retained one-edit moves.

So the remaining open questions are no longer about local seam closure. They concern the interaction between this closed seam slice and the larger bounded regime beyond the seam.

