# G15 Cycle Basis and Cocycle Decoding Note

## Status
Working note

## Purpose
Reduce the minimal passage witness problem to a fully explicit finite binary decoding problem on

\[
G_{15}\cong L(\mathrm{Petersen}).
\]

The point of this note is simple:

- the generic minimality argument proves only one-dimensionality,
- it does **not** force hexagonality,
- so the \(C_6\) conjecture must be decided from the actual cocycle class.

That means the live task is to compute the syndrome of the signed lift on an explicit cycle basis and then solve a minimum-weight binary constraint problem.

---

## 1. Core graph \(G_{15}=L(\mathrm{Petersen})\)

Start with the Petersen graph \(P\) on vertices

\[
u_0,u_1,u_2,u_3,u_4,\qquad v_0,v_1,v_2,v_3,v_4
\]

with indices mod \(5\), and edges:

- outer edges
\[
o_i = u_i u_{i+1},
\]

- spokes
\[
s_i = u_i v_i,
\]

- inner-star edges
\[
t_i = v_i v_{i+2}.
\]

Then the line graph \(G_{15}=L(P)\) has vertex set

\[
V(G_{15})=\{o_0,\dots,o_4,s_0,\dots,s_4,t_0,\dots,t_4\}.
\]

Adjacency in \(G_{15}\) is incidence in \(P\). Concretely:

\[
o_i \sim o_{i-1},\,o_{i+1},\,s_i,\,s_{i+1},
\]

\[
s_i \sim o_{i-1},\,o_i,\,t_i,\,t_{i-2},
\]

\[
t_i \sim s_i,\,s_{i+2},\,t_{i-2},\,t_{i+2}.
\]

So \(G_{15}\) is a connected \(4\)-regular graph on \(15\) vertices with \(30\) edges.

---

## 2. Cycle-space dimension

Over \(\mathbb F_2\),

\[
\dim Z_1(G_{15};\mathbb F_2)=|E|-|V|+1=30-15+1=16.
\]

So any full binary cycle description of the signed lift class needs a \(16\)-cycle basis.

---

## 3. Spanning tree

Choose the spanning tree

\[
T=
\{
o_0o_1,o_1o_2,o_2o_3,o_3o_4,
\;
o_0s_0,o_1s_1,o_2s_2,o_3s_3,o_4s_4,
\;
s_0t_0,s_1t_1,s_2t_2,s_3t_3,s_4t_4
\}.
\]

This is a connected \(14\)-edge tree on all \(15\) vertices.

Therefore the remaining \(16\) edges are chords, and each chord defines one fundamental cycle.

---

## 4. Explicit 16-cycle basis

Take the following basis
\[
\mathcal B=\{C_0,\dots,C_{15}\}.
\]

### 4.1 Outer pentagon

\[
C_0 = (o_0,o_1,o_2,o_3,o_4,o_0).
\]

### 4.2 Five outer triangles

These come from the omitted edges \(o_i s_{i+1}\):

\[
C_1=(o_0,o_1,s_1,o_0),
\]

\[
C_2=(o_1,o_2,s_2,o_1),
\]

\[
C_3=(o_2,o_3,s_3,o_2),
\]

\[
C_4=(o_3,o_4,s_4,o_3),
\]

\[
C_5=(o_4,o_0,s_0,o_4).
\]

### 4.3 Five spoke-to-inner cycles

These come from the omitted edges \(s_i t_{i-2}\):

\[
C_6=(s_2,o_2,o_1,o_0,s_0,t_0,s_2),
\]

\[
C_7=(s_3,o_3,o_2,o_1,s_1,t_1,s_3),
\]

\[
C_8=(s_4,o_4,o_3,o_2,s_2,t_2,s_4),
\]

\[
C_9=(s_0,o_0,o_1,o_2,o_3,s_3,t_3,s_0),
\]

\[
C_{10}=(s_1,o_1,o_2,o_3,o_4,s_4,t_4,s_1).
\]

### 4.4 Five inner-star cycles

These come from the omitted \(t\)-to-\(t\) edges:

\[
C_{11}=(t_0,s_0,o_0,o_1,o_2,s_2,t_2,t_0),
\]

\[
C_{12}=(t_1,s_1,o_1,o_2,o_3,s_3,t_3,t_1),
\]

\[
C_{13}=(t_2,s_2,o_2,o_3,o_4,s_4,t_4,t_2),
\]

\[
C_{14}=(t_3,s_3,o_3,o_2,o_1,o_0,s_0,t_0,t_3),
\]

\[
C_{15}=(t_4,s_4,o_4,o_3,o_2,o_1,s_1,t_1,t_4).
\]

This basis is explicit and sufficient for binary decoding, even if it is not the most symmetric choice.

---

## 5. The cocycle class as a syndrome

Let the signed \(2\)-lift

\[
G_{30}\to G_{15}
\]

determine a cohomology class

\[
[\varepsilon]\in H^1(G_{15};\mathbb F_2).
\]

Relative to the basis above, define the cycle-parity entries

\[
\chi(C_j)=\sum_{e\in C_j}\varepsilon(e)\pmod 2.
\]

Then the class is encoded by the \(16\)-bit syndrome vector

\[
s=
\bigl(
\chi(C_0),\chi(C_1),\dots,\chi(C_{15})
\bigr)\in \mathbb F_2^{16}.
\]

This vector is the actual invariant data needed to resolve the conjecture.

---

## 6. Edge-indicator model

Let \(x\in \mathbb F_2^{30}\) be an edge-indicator vector on \(G_{15}\), meaning:

\[
x_e=1 \iff e \text{ lies in the support}.
\]

Let \(A\) be the \(16\times 30\) cycle-edge incidence matrix, defined by

\[
A_{j,e}=1 \iff e\in C_j.
\]

Then representatives of the cocycle class are exactly the solutions of

\[
Ax=s.
\]

So the support-minimal representative problem is the minimum-weight binary decoding problem

\[
\min |x|
\quad \text{subject to} \quad
Ax=s.
\]

This is the fully explicit finite formulation.

---

## 7. Why the generic argument stops at one-dimensionality

The switching/minimality argument proves only:

\[
d_S(v)\le 2
\qquad\forall v,
\]

hence every support-minimal representative is a disjoint union of paths and cycles.

That is the theorem-level reduction.

But it does **not** imply

\[
S\cong C_6.
\]

In general, a minimum-weight element of an affine cut-space coset can be path-like, cycle-like, or mixed. Therefore hexagonality is **not** forced by minimality alone.

So the conjecture can only be resolved from the actual syndrome \(s\).

---

## 8. Endpoint test via boundary

For a support vector \(x\), define its mod-\(2\) vertex-boundary

\[
\partial x \in \mathbb F_2^{15}
\]

by recording support-degree parity at each vertex.

Then:

- \(\partial x=0\) means the support is Eulerian, hence a union of cycles,
- \(\partial x\neq 0\) means the support has endpoints, hence path components occur.

This gives an immediate discriminator after solving \(Ax=s\).

If every minimum-weight solution satisfies

\[
\partial x=0,
\]

then the minimal witness is cycle-only.

If some minimum-weight solution has

\[
\partial x\neq 0,
\]

then path-type support survives.

---

## 9. Exact resolution criterion for the conjecture

The \(C_6\) conjecture becomes:

1. compute the actual syndrome \(s\),
2. solve
\[
Ax=s
\]
for minimum Hamming weight,
3. inspect the minimum support graphs.

Then:

### Hexagon true
If every minimum connected solution has support isomorphic to

\[
C_6,
\]

the conjecture is true.

### Path rival true
If some minimum solution has support isomorphic to

\[
P_7,
\]

the strong hexagon conjecture is false.

### Non-canonical
If both occur at the same minimum weight, then hexagonality is not canonical.

So the whole problem reduces to the minimum-weight solution set of \(Ax=s\).

---

## 10. What would force the locked hexagon

Because the working program points toward support size \(6\), the strongest clean target is:

> Show that every weight-\(6\) solution of \(Ax=s\) has \(\partial x=0\) and connected support.

Then the degree bound and support size force

\[
\text{connected}+\text{6 edges}+\partial x=0
\Longrightarrow
C_6.
\]

Only after that is established does the preferred cyclic labeling

\[
W-X-Y-Z-T-I-W
\]

become the intrinsic organization of the witness rather than a chosen decoration.

With the user’s preferred organization, the intrinsic triad-of-diads decomposition is

\[
(W,X),\qquad (Y,Z),\qquad (T,I),
\]

with diad edges

\[
WX,\quad YZ,\quad TI
\]

and coupler edges

\[
XY,\quad ZT,\quad IW.
\]

---

## 11. Practical next move

The next concrete step is to write down the \(30\) edge labels of \(G_{15}\) and assemble the matrix schema for

\[
A\in M_{16\times 30}(\mathbb F_2).
\]

Once that is done, the signed lift data can be inserted as the syndrome vector \(s\), and the conjecture becomes a direct finite computation.

---

## 12. Clean conclusion

The conjecture has now been reduced as far as abstract chat reasoning can take it.

The exact current position is:

- theorem-level: minimal support is one-dimensional,
- not yet theorem-level: minimal connected support is hexagonal,
- exact finite resolution path: compute the syndrome \(s\) and solve
\[
Ax=s
\]
at minimum weight.

So the real question is no longer:

> “Is the witness aesthetically a hexagon?”

It is:

\[
\textbf{What is the actual minimum-weight support class of the cocycle syndrome on }L(\mathrm{Petersen})\textbf{?}
\]

