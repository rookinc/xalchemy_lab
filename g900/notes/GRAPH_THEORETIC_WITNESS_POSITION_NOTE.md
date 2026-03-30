# Graph-Theoretic Witness Position Note

## Status
Working note

## Purpose

This note restates the current passage-witness position strictly in graph-theoretic language.

The goal is to separate:

- what is proved,
- what is reduced,
- what remains open.

No geometric or interpretive language is used as a premise here.
Only the graph-theoretic core is retained.

---

## 1. Fixed graph-theoretic setup

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

A representative of this class is a function

\[
\varepsilon:E(G_{15})\to \mathbb F_2,
\]

well-defined up to switching.

The support of a representative is the edge set

\[
S:=\{e\in E(G_{15}) : \varepsilon(e)=1\}.
\]

The paper states that the switching class admits a representative of minimal support size

\[
|S|=6.
\]

We study the support subgraph

\[
H=(V(G_{15}),S).
\]

---

## 2. Proved first-principles reduction

Since \(G_{15}\) is \(4\)-regular, switching at a vertex toggles all four incident edges.

If a support vertex \(v\) has support degree

\[
k=d_S(v),
\]

then switching at \(v\) changes support size by

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

### Proposition 2.1
For every vertex \(v\in V(G_{15})\),

\[
d_S(v)\le 2.
\]

### Corollary 2.2
The support subgraph \(H\) is a disjoint union of paths and cycles.

So the passage witness is forced to be one-dimensional.

---

## 3. Exact shape fork at support size 6

Because \(|S|=6\) and every connected component of \(H\) is either a path or a cycle, only a small family of graph types survives.

### 3.1 Closed branch
If \(H\) is endpoint-free, then every support vertex has degree \(2\), so every connected component is a cycle.

At six edges, the only simple closed possibilities are

\[
C_6
\qquad\text{or}\qquad
C_3\sqcup C_3.
\]

### 3.2 Open branch
If \(H\) has endpoints, then at least one component is a path.

The connected extreme is

\[
P_7,
\]

and other disconnected endpoint-bearing cases are unions of shorter paths, possibly mixed with cycles, with total edge count \(6\).

Thus the support-minimal witness problem has been reduced to the exact fork:

\[
\text{open witness} \qquad\text{vs}\qquad \text{closed witness}.
\]

---

## 4. Closed branch internal fork

Inside the closed branch, the support types reduce further to

\[
C_6
\qquad\text{or}\qquad
C_3\sqcup C_3.
\]

So if one proves that a support-minimal witness is closed, the next question is immediately:

- is it connected?
- or does it split into two disjoint triangles?

This is the exact closed-branch fork.

---

## 5. Conditional hexagon lemma

The following statement is immediate from the reductions above.

### Lemma 5.1
If a support-minimal representative is closed and connected, then its support subgraph is isomorphic to

\[
C_6.
\]

### Proof
A closed support has no endpoints, so every support vertex has degree \(2\). A connected \(2\)-regular graph is a cycle. Since the support has exactly \(6\) edges, that cycle must have length \(6\). Therefore the support graph is \(C_6\). ∎

This is the strongest conditional hexagon statement currently available.

---

## 6. What is not yet proved

At present, the following are **not** yet proved:

1. that a support-minimal representative must be closed,
2. that a support-minimal representative must be connected,
3. that the support cannot be path-based,
4. that the support cannot be \(C_3\sqcup C_3\),
5. that the support must be \(C_6\).

So the graph-theoretic position is still genuinely conditional.

---

## 7. Clean graph-theoretic blade

The current live graph-theoretic problem is now sharply split into two questions.

### Question A: open versus closed
Must every support-minimal representative have even support degree at every support vertex?

Equivalently, must the support be Eulerian?

If yes, the open branch dies.

If no, path-based support survives.

### Question B: if closed, connected versus disconnected
Assuming the support is closed, must it be connected?

If yes, the support is \(C_6\) by Lemma 5.1.

If no, the remaining closed rival is

\[
C_3\sqcup C_3.
\]

So the conjectural hexagon claim is now seen to factor through these two sharper graph questions.

---

## 8. Exact present conclusion

The exact current graph-theoretic conclusion is:

> A support-minimal representative of the nontrivial cocycle class on \(G_{15}\cong L(\mathrm{Petersen})\) has support size \(6\) and support graph of maximum degree \(2\). Hence the support is a disjoint union of paths and cycles. The remaining problem is to decide whether the minimal witness is open or closed, and if closed, whether it is connected.

This is the cleanest strict graph-language compression currently available.

---

## 9. One-line compression

\[
|S|=6,\quad d_S(v)\le 2
\quad\Longrightarrow\quad
H \text{ is a union of paths and cycles;}
\]

therefore

\[
\text{closed}+\text{connected}
\Longrightarrow
H\cong C_6,
\]

and the unresolved graph-theoretic problem is exactly the open-vs-closed and connected-vs-disconnected fork.

