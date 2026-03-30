# Closed Witness Branch Exploration

## Status
Working exploration note

## Purpose

This note continues the pruning of the minimal passage witness problem on the signed lift side.

Previous derivation established the following:

- \(G15 \cong L(\mathrm{Petersen})\) is 4-regular, 0
- the cocycle switching class on the signed 2-lift \(G30 \to G15\) has a representative of minimal support size \(6\), 1
- for a support-minimal representative \(S\subseteq E(G15)\), every support vertex satisfies
  \[
  d_S(v)\le 2,
  \]
  so the support subgraph is a disjoint union of paths and cycles.

Thus the problem was reduced to the fork:

\[
\text{closed witness} \quad\text{vs}\quad \text{open witness}.
\]

This note explores the **closed witness branch**.

---

## 1. Closed witness branch

A closed witness means the support subgraph is endpoint-free.

Since every support vertex already has degree at most \(2\), endpoint-free implies every support vertex has degree exactly \(2\), so every connected component is a cycle.

Because the total support size is \(6\), the only simple closed support types are:

\[
C_6
\quad\text{or}\quad
C_3 \sqcup C_3.
\]

So the closed branch is already sharply reduced to these two possibilities.

---

## 2. Why triangles arise naturally in \(L(\mathrm{Petersen})\)

Since

\[
G15 \cong L(\mathrm{Petersen}),
\]

its vertices are the edges of the Petersen graph, and adjacency in \(G15\) means incidence of those Petersen edges at a common endpoint. 2

Therefore every vertex of the Petersen graph, which has degree \(3\), gives rise to a triangle in its line graph.

So a support of type

\[
C_3 \sqcup C_3
\]

would mean that the minimal passage witness is concentrated on two disjoint Petersen-star triangles.

This is possible in principle, but highly specific.

It would mean the closed witness is built from two separate local star structures rather than one single global loop.

---

## 3. Why a 6-cycle is conceptually attractive

A support of type

\[
C_6
\]

would mean that the minimal passage witness is carried by a single closed loop.

This is conceptually attractive for several reasons:

1. the passage invariant is fundamentally about holonomy on cycles,
2. a single loop is the most direct self-contained witness of odd closure,
3. the witness would be closed without splitting into disconnected local pieces,
4. it aligns naturally with the idea that the passage invariant condenses on a topological loop rather than on a pair of separated local stars.

So among the closed witnesses, \(C_6\) is the most holonomy-native candidate.

---

## 4. Why two disjoint triangles are less natural

The support type

\[
C_3 \sqcup C_3
\]

is still alive, but it is more special.

It would mean:

- the witness is disconnected,
- the passage obstruction is split across two separate local cycle nuclei,
- and the minimal closed support does not condense onto one single loop.

This is mathematically possible a priori, but conceptually less unified than \(C_6\).

So the two-triangle case should remain live, but it should not be treated as the leading closed candidate without further evidence.

---

## 5. Comparative ranking inside the closed branch

At the current stage, the closed branch is best ranked as:

\[
C_6 \quad \text{more plausible than} \quad C_3 \sqcup C_3.
\]

This is not a theorem.
It is a heuristic ranking based on:

- the holonomy nature of the invariant,
- the preference for a single self-contained cycle witness,
- and the relative specialness of the two-triangle configuration.

This ranking must remain provisional.

---

## 6. Relation to the open branch

The open branch remains fully alive.

An open support means the cocycle witness is not itself a mod-2 cycle, but a sparse obstruction whose nontriviality is only visible through the ambient cycle space of \(G15\).

So the global surviving fork is now:

\[
\text{closed branch: } C_6 \text{ or } C_3\sqcup C_3
\]

versus

\[
\text{open branch: path-based support}.
\]

This note only prunes the closed branch internally.
It does not yet decide between closed and open.

---

## 7. Strongest current exploratory statement

The strongest current exploratory statement is:

> If the minimal passage witness is closed, then it must be either a single 6-cycle or two disjoint triangles, with the 6-cycle currently the more natural holonomy witness.

This is the current best understanding of the closed side.

---

## 8. Best next question

The next sharpened question is:

> In \(L(\mathrm{Petersen})\), is a support-minimal nontrivial cocycle representative more naturally realized as one 6-cycle than as two disjoint triangles?

That is the next live blade on the closed branch.

---

## 9. Plain-language summary

Plainly said:

If the minimal witness has no loose ends, then it must either be one loop of length 6 or two separate little triangles.

The single 6-loop feels more natural for a holonomy witness.
The double-triangle option is still alive, but more special.

---

## 10. One-line compression

On the closed branch, the minimal six-edge passage witness is reduced to exactly two possibilities:

\[
C_6 \quad \text{or} \quad C_3 \sqcup C_3,
\]

with \(C_6\) the current leading candidate.

