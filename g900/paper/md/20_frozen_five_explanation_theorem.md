# Frozen-Five Explanation Theorem for the Frame-2 Seam

## Status
Established from extracted seam-local shape table

## Purpose
Record the strongest current structural explanation of the frame-2 seam alphabet: every retained frame-2 \(d_A=1\) state is a one-slot deformation of a single normalized prototype.

---

## 1. Main extracted fact

The frame-2 \(d_A=1\) shape extraction yields:

- row count: 28,
- distinct frozen-5 shapes: 1,
- unique frozen-5 shape:
  \[
  (o4,s0,t0,s2,s4),
  \]
- slot-4 values:
  \[
  \{o4,s0,s2,s3,s4,t0,t3,t4\}.
  \]

Equivalently, every retained frame-2 \(d_A=1\) normalized cycle is one of:
\[
[o4,s0,t0,s2,o4,s4],
\]
\[
[o4,s0,t0,s2,s0,s4],
\]
\[
[o4,s0,t0,s2,s2,s4],
\]
\[
[o4,s0,t0,s2,s3,s4],
\]
\[
[o4,s0,t0,s2,s4,s4],
\]
\[
[o4,s0,t0,s2,t0,s4],
\]
\[
[o4,s0,t0,s2,t3,s4],
\]
\[
[o4,s0,t0,s2,t4,s4].
\]

---

## 2. Explanation theorem

### Theorem 2.1. Frozen-five seam theorem
Every retained frame-2 \(d_A=1\) state has normalized form
\[
[o4,s0,t0,s2,x,s4]
\]
for a unique choice of
\[
x\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

Thus positions \(0,1,2,3,5\) are rigid on the retained frame-2 seam, and only normalized position \(4\) varies.

### Proof
Immediate from the extracted frame-2 \(d_A=1\) shape table. ∎

---

## 3. Relation to the exact prototype

The normalized exact frame-2 prototype is
\[
E_2=[o4,s0,t0,s2,t2,s4].
\]

Therefore the retained frame-2 seam is exactly the one-slot deformation family obtained by replacing the prototype slot-4 value \(t2\) by one of the eight retained seam-compatible values
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

---

## 4. Alphabet corollary

### Corollary 4.1. Seam alphabet theorem
The retained frame-2 seam slot-4 alphabet is exactly
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Proof
Immediate from Theorem 2.1. ∎

---

## 5. Residue corollary

### Corollary 5.1. Seam-local O-support law
For every retained frame-2 \(d_A=1\) state \(c\),
\[
\operatorname{Supp}_O(c)\subseteq\{o4\}.
\]

### Proof
In the frozen-five form
\[
[o4,s0,t0,s2,x,s4],
\]
the only possible \(o\)-symbol outside position 0 is \(x=o4\). Hence no normalized seam-local state contains any of \(o0,o1,o2,o3\). ∎

---

## 6. Interpretation

The frame-2 seam is not a diffuse neighborhood. It is a rigid one-slot family around the exact prototype.

So the obstruction is now best understood as follows:

- the exact normalized frame-2 form is fixed in five coordinates,
- the remaining failure is concentrated entirely in one slot,
- the missing exact value in that slot is \(t2\),
- the eight observed seam values are the surviving one-slot substitutions compatible with retained frame-2 \(d_A=1\) status.

This is the strongest current explanation theorem.

