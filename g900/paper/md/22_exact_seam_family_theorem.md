# Exact Seam Family Theorem for Frame 2

## Status
Established from direct verification

## Purpose
State the sharpest current theorem about the retained frame-2 seam: every retained frame-2 \(d_A=1\) state differs from the exact normalized prototype in exactly one coordinate, namely slot 4.

---

## 1. Exact prototype

The normalized exact frame-2 prototype is
\[
E_2=[o4,s0,t0,s2,t2,s4].
\]

This is the dihedrally normalized representative of the raw frame-2 action cell.

---

## 2. Verified scaffold facts

The direct seam verification shows:

- every retained frame-2 \(d_A=1\) state agrees with \(E_2\) in positions
  \[
  0,1,2,3,5,
  \]
- every retained frame-2 \(d_A=1\) state differs from \(E_2\) in exactly one slot,
- that slot is always slot \(4\),
- every retained frame-2 \(d_A=1\) state begins with
  \[
  [o4,s0,t0],
  \]
  with no alternative \(o4,s4,\dots\) orientation,
- every retained frame-2 \(d_A=1\) state has shape
  \[
  [o4,s0,t0,s2,x,s4]
  \]
  for some slot-4 value \(x\).

---

## 3. Main theorem

### Theorem 3.1. Exact seam family theorem
Let
\[
E_2=[o4,s0,t0,s2,t2,s4].
\]

Then every retained frame-2 \(d_A=1\) state \(c\) satisfies
\[
c_j=(E_2)_j \quad\text{for}\quad j\in\{0,1,2,3,5\},
\]
and differs from \(E_2\) in exactly the single coordinate \(j=4\).

Equivalently, every retained frame-2 \(d_A=1\) state has normalized form
\[
[o4,s0,t0,s2,x,s4]
\]
for a unique choice of \(x\).

### Proof
This is exactly what is certified by the scaffold verification, orientation verification, and slot-4 family verification:

1. positions \(0,1,2,3,5\) agree with \(E_2\) in all 28 retained frame-2 \(d_A=1\) rows,
2. the only mismatch position is slot \(4\),
3. no alternative anchored orientation occurs,
4. the resulting family is precisely
   \[
   [o4,s0,t0,s2,x,s4].
   \]
∎

---

## 4. Slot-4 family corollary

### Corollary 4.1. Exact seam slot-4 family
The set of possible slot-4 values in the retained frame-2 seam is exactly
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Proof
Immediate from Theorem 3.1 and the slot-4 family verification table. ∎

---

## 5. Frozen-five corollary

### Corollary 5.1. Frozen-five seam theorem
The retained frame-2 seam is rigid in positions
\[
0,1,2,3,5
\]
and varies only in position
\[
4.
\]

### Proof
Immediate from Theorem 3.1. ∎

---

## 6. Residue corollary

### Corollary 6.1. Seam-local \(O\)-support law
For every retained frame-2 \(d_A=1\) state \(c\),
\[
\operatorname{Supp}_O(c)\subseteq\{o4\}.
\]

### Proof
In the exact seam family form
\[
[o4,s0,t0,s2,x,s4],
\]
the only possible \(o\)-symbol outside the leading \(o4\) is \(x=o4\). Hence no seam-local retained state contains \(o0,o1,o2,o3\). ∎

---

## 7. Witness-language corollary

Identify
\[
[o4,s0,t0,s2,x,s4]
\]
with the witness
\[
[W,X,Y,Z,T,I].
\]

Then
\[
W=o4,\quad X=s0,\quad Y=t0,\quad Z=s2,\quad I=s4,
\]
and only \(T=x\) varies.

### Corollary 7.1. T-sector localization
In witness language, the retained frame-2 seam is a one-vertex deformation family at \(T\). Equivalently, only the edges incident to \(T\),
\[
ZT,\qquad TI,
\]
vary across the seam family.

---

## 8. Interpretation

The retained frame-2 seam is not merely a set with an eight-symbol slot-4 alphabet. It is exactly the one-coordinate Hamming-1 neighborhood of the exact prototype \(E_2\) inside the retained frame-2 slice.

So the obstruction is now sharply identified:

- exact closure requires the slot value \(t2\),
- the retained frame-2 seam preserves the exact prototype scaffold,
- but the exact value \(t2\) is punctured out of the seam family.

This is the strongest current theorem-level statement of the frame-2 obstruction.
