# Tree Gauge Cocycle Test Plan

## Status
Working test plan

## Purpose

This note records the next honest step in the passage ladder.

The form ladder is already locked by the paper:

\[
G60 \to G30 \to G15 \to Q \to \{14,9,5,4\},
\]

with

\[
Q = MM^{\mathsf T} = A^3 + 2A^2 + 2I.
\]

So the unresolved pressure point is no longer the core geometry.
It is the signed lift layer:

\[
G30 \to G15 \to \varepsilon \to \chi.
\]

The goal of this note is to turn that layer into a concrete test object before any further interpretation is trusted.

The paper already provides the correct route:
choose a spanning tree, pass to tree gauge, and read holonomy from the resulting fundamental cycles. 0

---

## 1. Authoritative input

The paper establishes:

1. the quotient tower
   \[
   G60 \to G30 \to G15,
   \qquad
   G15 \cong L(\mathrm{Petersen}),
   \]

2. a signed 2-lift
   \[
   G30 \to G15,
   \]

3. a cocycle
   \[
   \varepsilon : E(G15) \to \mathbb Z_2,
   \]

4. a holonomy parity map on cycles
   \[
   \chi(C) := \sum_{e\in C}\varepsilon(e)\pmod 2,
   \]

5. and the fact that the switching class admits a representative of minimal support size \(6\). 1

This note uses those facts as the hard base.

---

## 2. Why tree gauge comes next

The cocycle is only defined up to switching.

So if one wants to inspect its actual support pattern, the first requirement is to choose a convenient representative of the switching class.

The paper recommends the standard normalization:

- choose a spanning tree \(T \subseteq G15\),
- switch so that every tree edge has value \(0\).

This is called **tree gauge**.

In tree gauge:

- the cocycle vanishes on all tree edges,
- all nontrivial information lives on the non-tree edges,
- and holonomy becomes directly readable on the fundamental cycle basis. 2

That is why tree gauge is the next proper move.

---

## 3. Spanning tree and fundamental cycles

Fix a spanning tree

\[
T \subseteq G15.
\]

Since \(G15\) has \(15\) vertices and \(30\) edges, a spanning tree has:

\[
|E(T)| = 14.
\]

So there are:

\[
30 - 14 = 16
\]

non-tree edges.

For each non-tree edge \(a_j\), there is a unique fundamental cycle

\[
C_j
\]

formed by adjoining \(a_j\) to the unique path in the tree joining its endpoints.

Thus the non-tree edges determine a canonical finite basis of cycles:

\[
\mathcal F := \{C_j\}.
\]

This is the correct first family to inspect.

---

## 4. Holonomy in tree gauge

In tree gauge, every tree edge has cocycle value \(0\).

Therefore the parity of each fundamental cycle is determined entirely by its non-tree edge:

\[
\omega(C_j) = \varepsilon_T(a_j).
\]

This is the key simplification.

Instead of summing many nonzero contributions around a cycle, one reads parity directly from the support edge in tree gauge.

This makes the signed lift layer as transparent as it can be.

---

## 5. Immediate computational goals

The next concrete tasks are now clear.

### Task 1
Construct or import \(G15 \cong L(\mathrm{Petersen})\).

### Task 2
Choose a spanning tree \(T\subseteq G15\).

### Task 3
Put the cocycle into tree gauge relative to \(T\).

### Task 4
List the \(16\) non-tree edges.

### Task 5
For each non-tree edge \(a_j\), record the parity
\[
\omega(C_j)=\varepsilon_T(a_j).
\]

### Task 6
Identify the support set:
the subset of non-tree edges with value \(1\).

### Task 7
Compare that support set to the paper's statement that a minimal-support representative has support size \(6\). 3

This is the first genuine normalization of the passage layer.

---

## 6. Why this step matters more than further interpretation

At present, almost every interpretive story about the lift layer is downstream of a structure we have not actually inspected.

That is backwards.

Before asking whether there is a natural chart, or whether odd holonomy “belongs” to one family of walks rather than another, one must first see the cocycle in its simplest canonical support form.

Only then can any further organization claim be trusted.

So this note marks the point where interpretation yields to normalization.

---

## 7. First falsification target

Once the support set is visible in tree gauge, the first real question is:

> Does the support-minimal odd-parity pattern exhibit a structural organization that survives coordinate changes, or does it simply look scattered?

This is the first place where a lift chart can truly live or die.

If the odd-parity support pattern is:

- sparse,
- clustered,
- and aligned with some meaningful cycle-family distinction,

then there is room for a surviving higher-level story.

If it is:

- sparse but arbitrary,
- or scattered with no natural grouping,

then the signed lift remains real, but extra chart language should be demoted.

---

## 8. Relation to earlier chart ideas

This note deliberately postpones all use of Type III-style language.

No reference to:

- axial family,
- orthogonal family,
- world-building sector,
- or bridge language

should be trusted until after the tree-gauge support has been inspected.

That is a methodological rule.

This note therefore acts as a gatekeeper:
no higher chart survives unless it can explain or organize the normalized cocycle support.

---

## 9. Expected outcomes

There are three realistic outcomes.

### Outcome A
The tree-gauge support pattern is clearly structured.

This would justify trying to define a genuine walk-family chart.

### Outcome B
The support pattern is real but only weakly structured.

This would justify a minimal descriptive language, but not a strong organizational claim.

### Outcome C
The support pattern is sparse and effectively unstructured from the current point of view.

This would mean the cocycle remains an invariant, but any extra chart is probably only visualization.

The point of the test is to decide which of these worlds we are in.

---

## 10. Best current one-line summary

The next correct move on the passage ladder is to choose a spanning tree of \(G15\), put the cocycle into tree gauge, enumerate the fundamental cycles, and inspect the minimal odd-parity support before trusting any further organization story. 4

---

## 11. Plain-language summary

Plainly said:

Before we tell a story about how the signed layer behaves, we need to simplify it as much as possible and actually look at where the oddness lives.

Tree gauge is how we do that.

Once that is done, then and only then do we ask whether the odd cycles come in a pattern or not.

