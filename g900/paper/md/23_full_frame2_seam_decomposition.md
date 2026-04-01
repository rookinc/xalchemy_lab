# Full Frame-2 Seam Decomposition

## Status
Working theorem note

## Purpose
Distinguish the full normalized frame-2 seam from the smaller slot-4 slice selected by the locked witness regime.

---

## 1. Exact prototype

Let
\[
E_2=[o4,s0,t0,s2,t2,s4]
\]
be the normalized exact frame-2 prototype.

---

## 2. Full normalized frame-2 seam

Define the full normalized frame-2 seam by
\[
\Sigma_2^{\mathrm{full}}
:=
\{c:\ c \text{ is classified as an action-cell},\ d_A(c,E_2)=1,\ \text{and frame }2\text{ is among the nearest action frames}\}.
\]

This is the full normalized distance-1 seam around the exact prototype \(E_2\).

---

## 3. Coordinate slices

For each coordinate \(j\in\{0,1,2,3,4,5\}\), define the \(j\)-slice
\[
\Sigma_2^{(j)}
:=
\{c\in\Sigma_2^{\mathrm{full}}:\ c_k=(E_2)_k\text{ for all }k\neq j\}.
\]

So \(\Sigma_2^{(j)}\) consists of those seam states that differ from the exact prototype in exactly the single coordinate \(j\).

---

## 4. Computational decomposition

The raw-slot verification shows that the full normalized frame-2 seam contains states differing from \(E_2\) in each normalized coordinate \(j\in\{0,1,2,3,4,5\}\).

Thus the full seam is not identical to the slot-4 family.

The seam survivors found by raw-slot mutation are:

### Slice \(j=0\)
\[
[o0,s0,t0,s2,t2,s4],\ 
[o1,s0,t0,s2,t2,s4],\ 
[o2,s0,t0,s2,t2,s4],\ 
[o3,s0,t0,s2,t2,s4].
\]

### Slice \(j=1\)
\[
[o4,s0,t0,s2,t2,s0],\ 
[o4,s0,t0,s2,t2,s2],\ 
[o4,s0,t0,s2,t2,s3],\ 
[o4,s0,t0,s2,t2,t0],\ 
[o4,s0,t0,s2,t2,t3],\ 
[o4,s0,t0,s2,t2,t4].
\]

### Slice \(j=2\)
\[
[o4,s0,t0,s2,o4,s4],\ 
[o4,s0,t0,s2,s0,s4],\ 
[o4,s0,t0,s2,s2,s4],\ 
[o4,s0,t0,s2,s3,s4],\ 
[o4,s0,t0,s2,s4,s4],\ 
[o4,s0,t0,s2,t0,s4],\ 
[o4,s0,t0,s2,t3,s4],\ 
[o4,s0,t0,s2,t4,s4].
\]

### Slice \(j=3\)
\[
[o4,s0,t0,o4,t2,s4],\ 
[o4,s0,t0,s0,t2,s4],\ 
[o4,s0,t0,s3,t2,s4],\ 
[o4,s0,t0,s4,t2,s4],\ 
[o4,s0,t0,t0,t2,s4],\ 
[o4,s0,t0,t3,t2,s4],\ 
[o4,s0,t0,t4,t2,s4].
\]

### Slice \(j=4\)
\[
[o4,s0,o4,s2,t2,s4],\ 
[o4,s0,s0,s2,t2,s4],\ 
[o4,s0,s2,s2,t2,s4],\ 
[o4,s0,s3,s2,t2,s4],\ 
[o4,s0,s4,s2,t2,s4],\ 
[o4,s0,t3,s2,t2,s4],\ 
[o4,s0,t4,s2,t2,s4].
\]

### Slice \(j=5\)
\[
[o4,s2,t0,s2,t2,s4],\ 
[o4,s3,t0,s2,t2,s4],\ 
[o4,s4,t0,s2,t2,s4].
\]

---

## 5. Provisional theorem statement

### Proposition 5.1. Full seam decomposition
The full normalized frame-2 seam decomposes into coordinate slices
\[
\Sigma_2^{\mathrm{full}}=\bigcup_{j=0}^5 \Sigma_2^{(j)}.
\]

### Proof status
Supported by the raw-slot verification table. A polished proof would require showing that the listed seam survivors exhaust the normalized Hamming-1 seam around \(E_2\).

---

## 6. Interpretation

The exact seam family theorem does not describe the whole normalized frame-2 seam. It describes one distinguished coordinate slice of that seam.

So the right structural picture is:

1. the full normalized frame-2 seam is a union of single-coordinate slices around \(E_2\),
2. the locked witness regime selects one of those slices,
3. the bounded obstruction studied here occurs inside that selected slice.

