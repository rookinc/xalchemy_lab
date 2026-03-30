# Current Findings — Graph-Theoretic Status Note

## Status
Working synthesis note

## Purpose

This note freezes the current rigorously established graph-theoretic position of the passage-witness problem.

The goal is to state clearly:

- what is proved,
- what is reduced,
- what is not yet derivable,
- and where the conjecture now actually lives.

This note deliberately avoids paper-decoration language and keeps only the graph-theoretic core.

---

## 1. Fixed setup

Let

\[
G_{15}\cong L(\mathrm{Petersen})
\]

be the \(15\)-vertex quotient core.

Let

\[
G_{30}\to G_{15}
\]

be the signed \(2\)-lift, and let

\[
[\varepsilon]\in H^1(G_{15};\mathbb F_2)
\]

be the induced nontrivial cocycle class.

A representative is an edge-labeling

\[
\varepsilon:E(G_{15})\to \mathbb F_2
\]

defined up to switching.

The paper states that the switching class admits a representative of minimal support size

\[
|S|=6.
\]

Let

\[
H=(V(G_{15}),S)
\]

be the support subgraph of such a support-minimal representative.

---

## 2. Theorem-level reduction

Since \(G_{15}\) is \(4\)-regular, switching at a vertex toggles all four incident edges.

If a support vertex has support degree

\[
k=d_S(v),
\]

then switching changes support size by

\[
4-2k.
\]

Because \(S\) is support-minimal, support size cannot decrease. Therefore

\[
4-2k\ge 0,
\]

hence

\[
k\le 2.
\]

### Theorem 2.1
For every vertex \(v\in V(G_{15})\),

\[
d_S(v)\le 2.
\]

### Corollary 2.2
The support graph \(H\) is a disjoint union of paths and cycles.

So the witness is forced to be **one-dimensional**.

This is the strongest unconditional structural theorem currently derived in chat.

---

## 3. Exact shape fork at support size 6

Because \(|S|=6\) and every connected component of \(H\) is either a path or a cycle, the support problem reduces to a small finite family.

### 3.1 Closed branch
If \(H\) is endpoint-free, then every support vertex has degree \(2\), so every connected component is a cycle.

At six edges, the only simple closed possibilities are:

\[
C_6
\qquad\text{or}\qquad
C_3\sqcup C_3.
\]

### 3.2 Open branch
If \(H\) has endpoints, then at least one component is a path.

The connected open extreme is:

\[
P_7.
\]

Other disconnected endpoint-bearing cases are unions of shorter paths, possibly mixed with a cycle, so long as the total number of edges remains \(6\).

So the exact global fork is:

\[
\text{open witness} \qquad\text{vs}\qquad \text{closed witness}.
\]

And inside the closed branch:

\[
C_6 \qquad\text{vs}\qquad C_3\sqcup C_3.
\]

---

## 4. Conditional hexagon lemma

The following is fully proved.

### Lemma 4.1
If a support-minimal representative is closed and connected, then its support graph is

\[
H\cong C_6.
\]

### Proof
A closed support has no endpoints, so every support vertex has even degree. Since support degrees are at most \(2\), every support vertex has degree exactly \(2\). A connected \(2\)-regular graph is a cycle. Since the support has exactly \(6\) edges, that cycle must be \(C_6\). ∎

### Lemma 4.2
If a support-minimal representative is closed and disconnected, then

\[
H\cong C_3\sqcup C_3.
\]

### Proof
A closed disconnected support is a disjoint union of cycles. Since every cycle has length at least \(3\) and the total number of edges is \(6\), the only possibility is \(3+3\). ∎

Thus the closed branch is completely classified.

---

## 5. Meta-theorem: minimality alone does not imply hexagonality

This is now rigorously settled.

### Meta-Theorem 5.1
Support-minimality on a \(4\)-regular graph implies only that the support has maximum degree \(2\). It does **not** imply:

- Eulerianity,
- connectedness,
- or hexagonality.

### Reason
The same switching formula gives:

- if \(k=2\), then
  \[
  4-2k=0,
  \]
  so switching preserves minimality;
- if \(k=1\), then
  \[
  4-2k=2,
  \]
  so switching at an endpoint increases support size.

Therefore endpoints are not locally removable by the basic switching move. Minimality kills degrees \(3\) and \(4\), but it does **not** kill degree \(1\).

So support-minimality alone cannot force

\[
\partial S = 0.
\]

Hence it cannot force closedness.

Likewise, even if closedness were known, it would still not force connectedness, because

\[
C_3\sqcup C_3
\]

is a closed size-\(6\) support.

Thus any proof of

\[
H\cong C_6
\]

must use information beyond abstract support-minimality.

---

## 6. Exact current conclusion

The exact present graph-theoretic conclusion is:

> A support-minimal representative of the nontrivial cocycle class on \(G_{15}\cong L(\mathrm{Petersen})\) has support size \(6\) and support graph of maximum degree \(2\). Hence the support is a disjoint union of paths and cycles. The remaining problem is to decide whether the witness is open or closed, and if closed, whether it is connected.

This is the cleanest rigorous compression currently available.

---

## 7. What remains genuinely open

At present, the following are **not yet proved**:

1. that every support-minimal representative is closed,
2. that every support-minimal representative is connected,
3. that path-based support is impossible,
4. that \(C_3\sqcup C_3\) is impossible,
5. that the minimal connected witness is necessarily \(C_6\).

So the conjecture has not been disproved, but it has been properly localized.

---

## 8. Where the conjecture now lives

The hexagon claim no longer lives in abstract minimality.

It lives in the **specific cocycle data** of the signed lift.

The problem has been reduced to:

1. determine the actual cocycle class in explicit coordinates,
2. solve the corresponding minimum-weight support problem,
3. inspect whether the minimum supports are open or closed,
4. and, if closed, whether they are connected.

So the correct guiding statement is:

> Hexagonality is not a generic consequence of minimal support on a \(4\)-regular graph. If true, it is a special fact about this cocycle class on \(L(\mathrm{Petersen})\).

---

## 9. Tree-gauge normalization finding

A separate rigorous finding now also holds.

Choose a spanning tree

\[
T\subseteq G_{15}.
\]

In tree gauge, every tree edge has cocycle value \(0\), and the cocycle parity of each fundamental cycle is read directly from the corresponding non-tree edge.

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

where \(a_j\) is the unique non-tree edge defining \(C_j\).

Thus the cocycle is fully coordinatized by the chord bits in tree gauge.

What is still missing is the **actual chord-sign pattern**.

So tree gauge gives the correct coordinate system, but not yet the actual coordinates.

---

## 10. Sharp algebraic formulation

Let

\[
x\in\mathbb F_2^{30}
\]

be the support indicator vector on \(E(G_{15})\).

Let

\[
A\in M_{16\times 30}(\mathbb F_2)
\]

be the cycle-edge incidence matrix for the chosen fundamental cycle basis, and let

\[
s\in\mathbb F_2^{16}
\]

be the cocycle syndrome.

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

be the mod-\(2\) vertex-edge incidence matrix of \(G_{15}\). Then

\[
Bx=0
\]

is exactly the algebraic closedness condition.

So the conjecture has reduced to:

- does every minimum-weight solution satisfy \(Bx=0\)?
- if yes, is every such solution connected?

This is the precise algebraic version of the remaining graph-theoretic fork.

---

## 11. Locked preferred organization if the witness is hexagonal

A project-level organizational preference has been locked for the hexagonal witness, conditional on hexagonality being true.

If the minimal connected witness is \(C_6\), the preferred cyclic incidence register is

\[
W-X-Y-Z-T-I-W,
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

This is a preferred labeling and organization, not an additional theorem.

---

## 12. One-line compression

\[
|S|=6,\quad d_S(v)\le 2
\Longrightarrow
H \text{ is a union of paths and cycles;}
\]

therefore

\[
\text{closed}+\text{connected}
\Longrightarrow
H\cong C_6,
\]

but

\[
\text{minimality alone}
\not\Longrightarrow
\text{closedness or connectedness.}
\]

So the remaining problem is no longer broad shape intuition.
It is:

\[
\textbf{determine the actual cocycle syndrome and the minimum-weight solution class.}
\]

