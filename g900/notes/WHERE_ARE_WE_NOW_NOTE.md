# Where Are We Now

## Status
Working position snapshot

## Short answer

We have completed the **generic graph-theoretic pruning**.

We have **not** yet proved that the minimal witness is a hexagon.

So the remaining work is no longer broad shape intuition. It is now a **class-specific cocycle decoding problem**.

---

## 1. What is proved

Let

\[
G_{15}\cong L(\mathrm{Petersen})
\]

and let

\[
[\varepsilon]\in H^1(G_{15};\mathbb F_2)
\]

be the nontrivial cocycle class induced by the signed \(2\)-lift

\[
G_{30}\to G_{15}.
\]

The paper states that the switching class admits a representative of minimal support size

\[
|S|=6.
\]

For any support-minimal representative \(S\subseteq E(G_{15})\), the support graph

\[
H=(V(G_{15}),S)
\]

satisfies

\[
d_S(v)\le 2
\qquad\forall v\in V(G_{15}).
\]

Therefore:

\[
H \text{ is a disjoint union of paths and cycles.}
\]

This is the strongest unconditional graph-theoretic theorem currently established.

---

## 2. Exact reduced shape fork

Because \(|S|=6\) and every connected component is a path or cycle, the witness problem reduces to:

### Open branch
The support has endpoints, so it contains a path component.

Connected extreme:

\[
P_7.
\]

### Closed branch
The support is endpoint-free, so every component is a cycle.

Only simple possibilities at size \(6\):

\[
C_6
\qquad\text{or}\qquad
C_3\sqcup C_3.
\]

So the exact reduced fork is:

\[
\text{open witness}
\qquad\text{vs}\qquad
\text{closed witness}.
\]

And inside the closed branch:

\[
C_6
\qquad\text{vs}\qquad
C_3\sqcup C_3.
\]

---

## 3. Conditional hexagon result

The following is already proved.

If the support-minimal witness is:

- closed, and
- connected,

then it must be

\[
C_6.
\]

Reason:
a connected \(2\)-regular graph with \(6\) edges is exactly a 6-cycle.

Likewise, if the witness is:

- closed, and
- disconnected,

then it must be

\[
C_3\sqcup C_3.
\]

So the closed branch is fully classified.

---

## 4. What is not proved

The following are still open:

1. that the witness must be closed,
2. that the witness must be connected,
3. that path-based support is impossible,
4. that \(C_3\sqcup C_3\) is impossible,
5. that the minimal connected witness is necessarily \(C_6\).

---

## 5. Key meta-finding

Minimality alone does **not** imply hexagonality.

More precisely, support-minimality on a 4-regular graph implies only:

\[
d_S(v)\le 2.
\]

It does **not** imply:

- Eulerianity,
- connectedness,
- or a single cycle.

So the claim

\[
H\cong C_6
\]

cannot be derived from abstract minimality alone.

If hexagonality is true, it must be a **special fact about the actual cocycle class**, not a generic fact about support-minimal representatives on 4-regular graphs.

---

## 6. Tree-gauge finding

A rigorous normalization fact is also now established.

Choose a spanning tree

\[
T\subseteq G_{15}.
\]

In tree gauge:

- every tree edge has cocycle value \(0\),
- every fundamental cycle parity is read directly from its defining non-tree edge.

So if

\[
\mathcal F=\{C_0,\dots,C_{15}\}
\]

is the fundamental cycle basis determined by \(T\), then the syndrome vector

\[
s=(s_0,\dots,s_{15})\in\mathbb F_2^{16}
\]

is given by

\[
s_j=\omega(C_j)=\varepsilon_T(a_j),
\]

where \(a_j\) is the corresponding chord.

Thus tree gauge gives the correct coordinate system for the cocycle.

What is still missing is the actual chord-sign pattern.

---

## 7. Exact algebraic form of the remaining problem

Let

\[
x\in\mathbb F_2^{30}
\]

be the support indicator vector on the 30 edges of \(G_{15}\).

Let

\[
A\in M_{16\times 30}(\mathbb F_2)
\]

be the cycle-edge incidence matrix for the chosen cycle basis, and let

\[
s\in\mathbb F_2^{16}
\]

be the actual cocycle syndrome.

Then representatives of the cocycle class satisfy

\[
Ax=s.
\]

A support-minimal representative is a minimum-weight solution of

\[
\min |x|
\qquad\text{subject to}\qquad
Ax=s.
\]

Let

\[
B
\]

be the mod-2 vertex-edge incidence matrix of \(G_{15}\). Then:

\[
Bx=0
\]

means the support is closed.

So the remaining problem is exactly:

1. determine the actual syndrome \(s\),
2. solve \(Ax=s\) at minimum weight,
3. test whether all minimum solutions satisfy \(Bx=0\),
4. if yes, test connectedness.

That is the current sharp mathematical core.

---

## 8. Preferred labeling if the witness is hexagonal

If the minimal connected witness does turn out to be \(C_6\), the locked preferred organization is:

\[
W-X-Y-Z-T-I-W
\]

with intrinsic triad-of-diads decomposition

\[
(W,X),\qquad (Y,Z),\qquad (T,I),
\]

diad edges

\[
WX,\quad YZ,\quad TI,
\]

and coupler edges

\[
XY,\quad ZT,\quad IW.
\]

This is a project-level preferred organization, not an additional theorem.

---

## 9. Plain-language summary

We are no longer trying to guess the shape.

We already know the minimal witness must be a 1-dimensional 6-edge object.

So the only real remaining questions are:

- does it have endpoints or not?
- if not, is it one loop or two triangles?

Those cannot be settled from generic minimality alone.

To finish the problem, we need the actual cocycle/sign data of the signed lift.

---

## 10. One-line compression

\[
|S|=6,\quad d_S(v)\le 2
\Longrightarrow
H \text{ is a union of paths and cycles;}
\]

\[
\text{closed}+\text{connected}
\Longrightarrow
H\cong C_6;
\]

but

\[
\text{minimality alone}
\not\Longrightarrow
\text{closedness or connectedness.}
\]

So the next move is not more generic pruning.
The next move is to decode the actual cocycle class.

