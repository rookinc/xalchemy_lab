# Pure Graph Theory Lexicon Note

## Status
Working translation note

## Purpose

This note translates the current project language into pure graph-theoretic terms.

The goal is to remove machine metaphor, traversal rhetoric, and custom intuitive vocabulary wherever possible, while preserving the actual mathematical structure already established.

The guiding principle is:

> describe the system only in terms of graphs, coverings, incidence matrices, adjacency operators, cycle space, and cohomology.

This note is therefore a lexicon reduction.

---

## 1. Quotient graph tower

The paper gives the quotient tower

\[
G_{60} \to G_{30} \to G_{15},
\qquad
G_{15} \cong L(\mathrm{Petersen}).
\]

This is the primary graph-theoretic backbone of the construction. 0

### Graph-theoretic meaning
- \(G_{60}\): a connected 4-regular graph on 60 vertices arising from the local transport construction
- \(G_{30}\): an intermediate quotient graph
- \(G_{15}\): the 15-vertex quotient core, isomorphic to the line graph of the Petersen graph

This tower is the correct starting point for all graph-theoretic reformulation.

---

## 2. Distinguished incidence structure on the core

On the quotient core \(G_{15}\), the paper defines a distinguished family of subsets of \(E(G_{15})\), called sectors.

This data is encoded by a \(0\)-\(1\) matrix

\[
M \in \{0,1\}^{15\times 30},
\]

with rows indexed by \(V(G_{15})\) and columns indexed by \(E(G_{15})\). 1

### Graph-theoretic meaning
The matrix \(M\) is a structured vertex-by-edge incidence-type matrix associated with a distinguished row family of edge subsets.

So:

- row \(v\) corresponds to a distinguished subset \(S(v)\subseteq E(G_{15})\)
- column \(e\) records membership of \(e\) in each such subset

This is the pure graph-theoretic replacement for the more project-specific connective vocabulary.

---

## 3. Quadratic overlap form

Define

\[
Q := MM^{\mathsf T}.
\]

Then \(Q\) is a symmetric \(15\times 15\) matrix indexed by \(V(G_{15})\), with entries

\[
Q_{uv}=|S(u)\cap S(v)|.
\]

The paper proves the exact identity

\[
Q = A^3 + 2A^2 + 2I,
\]

where \(A\) is the adjacency matrix of \(G_{15}\). 2

Equivalently, \(Q_{uv}\) depends only on graph distance in \(G_{15}\), with values

\[
14,\ 9,\ 5,\ 4
\]

at distances \(0,1,2,3\). 3

### Graph-theoretic meaning
The matrix \(Q\) is:

- the Gram matrix of the row family \(M\),
- a quadratic overlap form on \(V(G_{15})\),
- and an element of the adjacency algebra of \(G_{15}\).

This is the pure graph-theoretic replacement for earlier “form” language.

---

## 4. Signed 2-lift and cocycle class

The intermediate quotient map

\[
G_{30} \to G_{15}
\]

is a signed 2-lift. The paper defines a sign function on \(E(G_{15})\), equivalently a cocycle

\[
\varepsilon : E(G_{15}) \to \mathbb Z_2.
\]

This cocycle is defined only up to switching, so the correct invariant is its cohomology class

\[
[\varepsilon] \in H^1(G_{15};\mathbb Z_2).
\]

The paper proves that this class is nontrivial. 4

### Graph-theoretic meaning
The signed lift determines a nonzero element of the first mod-2 cohomology of the quotient core.

This is the pure graph-theoretic replacement for earlier “passage” language.

---

## 5. Holonomy parity on cycle space

For any cycle \(C\in Z_1(G_{15};\mathbb Z_2)\), define

\[
\chi(C):=\sum_{e\in C}\varepsilon(e)\pmod 2.
\]

The paper states:

- \(\chi(C)=0\) iff the lift of \(C\) closes on the same sheet
- \(\chi(C)=1\) iff the lift of \(C\) closes on the opposite sheet. 5

### Graph-theoretic meaning
The cocycle class \([\varepsilon]\) induces a linear functional

\[
\chi : Z_1(G_{15};\mathbb Z_2)\to \mathbb Z_2
\]

on cycle space.

This is the correct graph-theoretic replacement for:
- same-sheet / opposite-sheet return
- sign closure
- sheet-flip talk

Everything here is now cycle-space language.

---

## 6. Dual invariant structure

The current system is best represented graph-theoretically by the ordered pair

\[
(Q,[\varepsilon]).
\]

Here:

- \(Q\) is a quadratic overlap form on \(V(G_{15})\),
- \([\varepsilon]\) is a nontrivial mod-2 cohomology class on \(E(G_{15})\).

These are distinct objects of different type:

\[
Q:\ V(G_{15})\times V(G_{15})\to \mathbb Z_{\ge 0},
\]

\[
[\varepsilon]\in H^1(G_{15};\mathbb Z_2).
\]

The paper explicitly states that the cocycle is a companion invariant not detected by \(Q\). 6

### Graph-theoretic conclusion
The construction is governed by two irreducible invariant layers:

1. a quadratic overlap form,
2. a nontrivial cohomology class.

That is the pure graph-theoretic core.

---

## 7. Translation dictionary

This section replaces project-specific words with graph-theoretic equivalents.

### Quotient core
“core”
\(\to\)
the graph \(G_{15}\cong L(\mathrm{Petersen})\)

### Sector system
“distinguished local connective family”
\(\to\)
row family of edge subsets \(S(v)\subseteq E(G_{15})\)

### Form
“form”
\(\to\)
the Gram / overlap matrix \(Q=MM^{\mathsf T}\)

### Passage
“passage”
\(\to\)
the induced mod-2 holonomy functional \(\chi\) on cycle space

### Same sheet / opposite sheet
“same sheet / opposite sheet”
\(\to\)
\(\chi(C)=0\) / \(\chi(C)=1\)

### Signed lift layer
“passage layer”
\(\to\)
the nontrivial cohomology class \([\varepsilon]\in H^1(G_{15};\mathbb Z_2)\)

### Minimal passage witness
“minimal passage witness”
\(\to\)
a support-minimal representative of the nontrivial switching/cohomology class

This is the lexicon reduction.

---

## 8. Minimal support problem in pure graph language

Let \(S\subseteq E(G_{15})\) be the support of a representative of \([\varepsilon]\), chosen to have minimal support size \(6\), as stated in the paper. 7

By first-principles switching analysis on the 4-regular graph \(G_{15}\), we derived:

\[
d_S(v)\le 2 \quad \forall v\in V(G_{15}).
\]

### Graph-theoretic consequence
The support subgraph induced by \(S\) is a disjoint union of paths and cycles.

So the minimal-support problem becomes:

> classify support-minimal representatives of a nontrivial class in \(H^1(G_{15};\mathbb Z_2)\) whose support subgraph has 6 edges and maximum degree at most 2.

This is the pure graph-theoretic restatement of the “minimal passage witness” problem.

---

## 9. Current leading candidate in graph-theoretic terms

After pruning:

- tetrahedral support is impossible,
- branching support is impossible,
- the leading closed candidate is a simple 6-cycle \(C_6\),
- the main open competitor is a connected 6-edge path \(P_7\).

So the current leading graph-theoretic target is:

> a support-minimal representative whose support subgraph is a simple 6-cycle.

This replaces the more interpretive “face-threaded six-step passage witness.”

---

## 10. Walk language in graph-theoretic terms

A walk word or cube grammar should be translated as:

- a word in a finite generating alphabet,
- inducing a walk in the lift or on the quotient core,
- together with:
  - an incidence footprint on \(E(G_{15})\),
  - and a parity evaluation on cycle space.

So the “translator” or “transducer” language becomes graph-theoretically:

### Definition 10.1
A **walk-to-incidence-and-holonomy map** is a map

\[
\mathcal T : \mathcal W \to \mathbb Z^{E(G_{15})} \times \mathbb Z_2
\]

sending a word \(w\) to:

1. its edge-incidence footprint on \(G_{15}\),
2. its mod-2 holonomy parity in the signed lift.

This is the correct graph-theoretic replacement for the action/form/passage interface idea.

---

## 11. Best compressed formal statement

The entire system may now be stated graph-theoretically as follows.

> A local transport construction yields a quotient tower
> \[
> G_{60}\to G_{30}\to G_{15},
> \qquad
> G_{15}\cong L(\mathrm{Petersen}),
> \]
> together with two independent invariant structures on the quotient core: a quadratic overlap form
> \[
> Q=MM^{\mathsf T}=A^3+2A^2+2I
> \]
> lying in the adjacency algebra of \(G_{15}\), and a nontrivial cohomology class
> \[
> [\varepsilon]\in H^1(G_{15};\mathbb Z_2)
> \]
> arising from the signed 2-lift \(G_{30}\to G_{15}\). The first is a vertex-level overlap invariant; the second is an edge/cycle-level holonomy invariant. 8

This is the pure graph-theoretic core.

---

## 12. Plain-language summary

Plainly said, in graph terms:

- there is a 60-to-30-to-15 quotient ladder,
- on the 15-vertex core there is an exact overlap matrix governed by adjacency,
- and above that same core there is a nontrivial signed covering class visible only on loops.

Everything else should be built from those facts.

---

## 13. One-line compression

\[
(G_{60}\to G_{30}\to G_{15},\ Q,\ [\varepsilon])
\]

with

\[
Q=MM^{\mathsf T}=A^3+2A^2+2I,
\qquad
[\varepsilon]\in H^1(G_{15};\mathbb Z_2)
\]

is the current system in pure graph-theoretic lexicon.

