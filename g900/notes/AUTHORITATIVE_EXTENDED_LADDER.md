# Authoritative Extended Ladder

## Status
Working reference note

## Purpose

This note records the strongest disciplined extension of the current ladder using only objects that are properly grounded in the paper and the current rigorous framework.

The main point is to prevent category confusion.

In the surrounding discussion, several different kinds of objects have appeared:

- quotient graphs,
- cycle-closure milestones,
- core overlap levels,
- lift / holonomy invariants,
- and exploratory milestone labels.

This note separates those into the cleanest possible ladder.

---

## 1. Authoritative quotient graph ladder

The paper gives the quotient tower

\[
G60 \to G30 \to G15,
\qquad
G15 \cong L(\mathrm{Petersen}).
\]

These are the currently authoritative graph levels.

### G60
The 60-vertex chamber / transport graph arising from the dodecahedral transport construction, identified in the paper with AT4val[60,6]. 0

### G30
The intermediate quotient layer. This is also the level at which the signed 2-lift over \(G15\) becomes relevant. 1

### G15
The 15-vertex quotient core, explicitly identified with the line graph of the Petersen graph:

\[
G15 \cong L(\mathrm{Petersen}).
\]

This is the algebraically legible core of the construction. 2

So the primary graph ladder is:

\[
G60 \to G30 \to G15.
\]

---

## 2. Authoritative core-geometry ladder

On the quotient core \(G15\), the paper defines the sector–edge incidence matrix

\[
M \in \{0,1\}^{15\times 30}
\]

and the corresponding quadratic overlap object

\[
Q := MM^{\mathsf T}.
\]

The central theorem states:

\[
Q = A^3 + 2A^2 + 2I,
\]

where \(A\) is the adjacency matrix of \(G15\). 3

This makes the next ladder step:

\[
G15 \to (M,Q).
\]

The overlap entries of \(Q\) are exactly determined by graph distance on \(G15\).

---

## 3. Exact overlap strata

The paper proves that for vertices \(u,v\in V(G15)\),

\[
Q_{uv}=|S(u)\cap S(v)|
\]

takes the values

\[
14,\ 9,\ 5,\ 4
\]

according to graph distance \(0,1,2,3\). 4

So the exact overlap ladder on the core is:

\[
14 \to 9 \to 5 \to 4.
\]

This ladder is not a graph ladder.
It is a metric/incidence ladder on the core sector system.

More precisely:

- \(14\) = self-overlap of a sector
- \(9\) = overlap at graph distance \(1\)
- \(5\) = overlap at graph distance \(2\)
- \(4\) = overlap at graph distance \(3\). 5

Thus the exact geometric extension of the graph ladder is:

\[
G60 \to G30 \to G15 \to (M,Q) \to \{14,9,5,4\}.
\]

---

## 4. Authoritative lift / passage ladder

The paper also gives a second invariant layer above the core geometry.

The intermediate quotient

\[
G30 \to G15
\]

is a signed 2-lift carrying a nontrivial cocycle

\[
\varepsilon : E(G15)\to \mathbb Z_2.
\]

For any cycle \(C\subseteq G15\), define its parity by

\[
\chi(C):=\sum_{e\in C}\varepsilon(e)\pmod 2.
\]

The paper's holonomy criterion states:

- \(\chi(C)=0\) iff the lifted walk closes on the same sheet,
- \(\chi(C)=1\) iff the lifted walk closes on the opposite sheet. 6

So the authoritative passage ladder is:

\[
G30 \to G15 \to \varepsilon \to \chi.
\]

This is a second ladder, parallel to the overlap ladder.

It is not a metric ladder.
It is a lift/holonomy ladder.

---

## 5. Dual-ladder view

The construction therefore naturally extends into two distinct but related ladders.

### Form ladder
\[
G60 \to G30 \to G15 \to (M,Q) \to \{14,9,5,4\}.
\]

This is the graph / incidence / overlap side.

### Passage ladder
\[
G30 \to G15 \to \varepsilon \to \chi.
\]

This is the signed-lift / holonomy side.

These should not be collapsed into one another.

This is the cleanest disciplined extension currently available.

---

## 6. Where the exploratory milestones fit

The following earlier exploratory milestones may still be useful, but they must now be placed carefully.

### 15
May still be used as a walker-side sign / opposite-sheet hinge, but this is not a new graph level. It sits naturally against the lift/holonomy story.

### 30
May still be used as a walker-side restoration count, but as a graph level it is already the intermediate quotient \(G30\).

### 9, 5, 4
Should now be treated first and foremost as the exact overlap strata of the core geometry, not as free-floating ladder numbers. 7

### G9, G5, G4, G900
These are **not** currently authoritative graph objects in the paper's tower.
They may remain exploratory labels, but they are not part of the present hard ladder.

This distinction matters.

---

## 7. Strong current boundary

### Authoritative graph levels
\[
G60,\ G30,\ G15.
\]

### Authoritative form objects
\[
M,\ Q,\ \{14,9,5,4\}.
\]

### Authoritative passage objects
\[
\varepsilon,\ \chi.
\]

### Exploratory attachments
Type III chart language, edge/vertex bridge ideas, and higher milestone labels such as G900.

This is the correct current boundary.

---

## 8. Best current one-line summary

The authoritative extended ladder of the transport construction is the quotient graph tower \(G60 \to G30 \to G15\), extended on the form side to the quadratic sector object \(Q=MM^{\mathsf T}\) and its overlap strata \(\{14,9,5,4\}\), and extended on the passage side to the signed-lift cocycle \(\varepsilon\) and its holonomy map \(\chi\). 8

---

## 9. Plain-language summary

Plainly said:

The construction descends through three graph levels:

- the 60-vertex transport graph,
- the 30-vertex lift layer,
- the 15-vertex core.

On the 15-vertex core, the sectors have an exact overlap law.
That gives the numbers 14, 9, 5, 4.

Above the core, the 30-to-15 lift carries a separate sheet-flip law.
That gives the cocycle and holonomy parity.

So the ladder extends in two directions:
one geometric, one transport-theoretic.

---

## 10. One-line compression

\[
G60 \to G30 \to G15 \to Q \to \{14,9,5,4\},
\qquad
G30 \to G15 \to \varepsilon \to \chi.
\]

That is the current authoritative extended ladder.

