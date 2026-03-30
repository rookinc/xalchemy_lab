# Form and Passage: A Dual-Invariant Note

## Status
Working formal note

## Purpose

This note records the cleanest formal distillation currently available from the transport construction.

The project has now reached a point where a large amount of exploratory language can be compressed to a simple structural claim:

> the construction carries two irreducible invariant layers

One layer records overlap geometry on the quotient core.
The other records sheeted holonomy on the signed lift.

This note formalizes that split.

---

## 1. Common origin

Let the local transport construction produce the quotient tower

\[
G60 \to G30 \to G15,
\qquad
G15 \cong L(\mathrm{Petersen}).
\]

This is the common source of both invariant layers.

The point of the present note is that the resulting mathematical content is not exhausted by a single object.

Instead, the construction yields at least two distinct and irreducible forms of information:

1. an overlap geometry on the quotient core,
2. a sheet-holonomy invariant on the signed lift.

These must be kept separate.

---

## 2. The form invariant

On the quotient core \(G15\), let

\[
M \in \{0,1\}^{15\times 30}
\]

denote the sector–edge incidence matrix, with rows indexed by vertices of \(G15\) and columns indexed by edges of \(G15\).

Define the Gram matrix

\[
Q := MM^{\mathsf T}.
\]

The paper proves the exact polynomial identity

\[
Q = A^3 + 2A^2 + 2I,
\]

where \(A\) is the adjacency matrix of \(G15\). Equivalently, for vertices \(u,v\in V(G15)\),

\[
Q_{uv}=|S(u)\cap S(v)|
\]

depends only on graph distance, with values

\[
14,\ 9,\ 5,\ 4
\]

at distances \(0,1,2,3\). 0

### Definition 2.1 (Form invariant)
The **form invariant** of the construction is the quadratic overlap object

\[
Q := MM^{\mathsf T}.
\]

It records the coexistence structure of sectors on the quotient core.

### Interpretation
The form invariant forgets transport history and retains only overlap geometry.

In compressed language:

\[
\text{Form remembers what overlaps.}
\]

---

## 3. The passage invariant

The paper also states that the intermediate quotient

\[
G30 \to G15
\]

is a signed 2-lift. For each base edge \(e\in E(G15)\), the lift is either parallel or crossed, yielding a cocycle

\[
\varepsilon:E(G15)\to \mathbb Z_2.
\]

For any cycle \(C\subseteq G15\), define its holonomy parity by

\[
\chi(C):=\sum_{e\in C}\varepsilon(e)\pmod 2.
\]

The paper's holonomy criterion is:

- \(\chi(C)=0\) if and only if the lifted walk closes on the same sheet,
- \(\chi(C)=1\) if and only if the lifted walk closes on the opposite sheet. 1

### Definition 3.1 (Passage invariant)
The **passage invariant** of the construction is the mod-2 holonomy map

\[
\chi: Z_1(G15;\mathbb Z_2)\to \mathbb Z_2,
\qquad
\chi(C)=\sum_{e\in C}\varepsilon(e)\pmod 2.
\]

It records how transport closes on the signed lift.

### Interpretation
The passage invariant forgets overlap magnitude and retains only sheet-history along loops.

In compressed language:

\[
\text{Passage remembers how closure occurred.}
\]

---

## 4. Formal types of the two invariants

The two invariants live on different mathematical objects.

### Form layer
\[
Q:\ V(G15)\times V(G15)\to \mathbb Z_{\ge 0}
\]

This is a quadratic overlap object on sectors / vertices.

### Passage layer
\[
\chi:\ Z_1(G15;\mathbb Z_2)\to \mathbb Z_2
\]

This is a parity / holonomy object on cycles.

So even before interpretation, the two invariants differ by type:

- \(Q\) is a matrix on pairs of core vertices
- \(\chi\) is a cocycle-derived functional on cycle space

They are therefore not interchangeable descriptions of the same thing.

---

## 5. Irreducibility of the split

The paper explicitly states that the signed-lift cocycle is a companion invariant **not detected by** the quadratic overlap matrix \(Q\). 2

This gives the core structural conclusion.

### Proposition 5.1
The transport construction carries at least two irreducible invariant layers:

1. a form layer, encoded by
   \[
   Q = MM^{\mathsf T},
   \]
2. a passage layer, encoded by
   \[
   \chi(C)=\sum_{e\in C}\varepsilon(e)\pmod 2.
   \]

### Corollary 5.2
No complete account of the transport construction can be reduced to overlap geometry alone.

That is the first serious formal distillation of the whole project thread.

---

## 6. What each invariant forgets

The distinction becomes sharper when stated negatively.

### The form invariant forgets:
- the detailed path history of a walk,
- the sheet on which a lifted walk closes,
- the cocycle parity of loops.

It retains only overlap geometry.

### The passage invariant forgets:
- sector cardinalities,
- overlap magnitudes,
- the quantitative Gram structure of the core sectors.

It retains only sheeted closure history.

Thus each invariant is incomplete without the other.

This is why the split is not decorative.
It is mathematically real.

---

## 7. Refined statement of the construction

The transport construction should therefore be understood as yielding a pair

\[
(Q,\chi)
\]

rather than a single master object.

### Definition 7.1 (Dual invariant structure)
The **dual invariant structure** of the transport construction is the ordered pair

\[
(Q,\chi),
\]

where:

- \(Q=MM^{\mathsf T}\) is the form invariant on the quotient core,
- \(\chi\) is the passage invariant on the signed lift.

This pair is currently the most compressed clean formal object extracted from the project discussion.

---

## 8. Relation to earlier informal language

Earlier discussion used terms such as:

- sign flip
- same sheet / opposite sheet
- world
- passage
- shape
- closure

These are now best disciplined as follows.

### “Shape” / “world” / “coexistence”
belongs primarily to the form layer

\[
Q = MM^{\mathsf T}.
\]

### “Sign flip” / “sheet” / “return”
belongs primarily to the passage layer

\[
\chi(C)=\sum_{e\in C}\varepsilon(e)\pmod 2.
\]

This preserves the underlying intuition while making the language mathematically cleaner.

---

## 9. Clean compressed principle

The current best compressed principle is:

\[
\text{Form remembers what overlaps.}
\]
\[
\text{Passage remembers how closure occurred.}
\]

This is not merely poetic shorthand.
It accurately reflects the mathematical types of \(Q\) and \(\chi\).

---

## 10. Strongest one-line formalization

The strongest current one-line formalization is:

> The dodecahedral transport construction induces a dual invariant structure consisting of a quadratic form invariant on the quotient core and a mod-2 holonomy invariant on the signed lift; the first classifies sector coexistence, and the second classifies sheeted return of loops. 3

---

## 11. What remains open

This note intentionally stops before several further questions.

It does **not** yet settle:

- how the current Type III chart should be phrased in switching-invariant cycle-space terms,
- whether there is a meaningful organizational partition of cycles into “axial” and “orthogonal” families,
- whether the edge/vertex bridge
  \[
  20 \rightsquigarrow 9
  \]
  can be made rigorous,
- whether higher closures such as G60 or G900 should be read primarily through \(Q\), through \(\chi\), or through a further extension.

Those remain open.

This note is only about the dual invariant split itself.

---

## 12. Plain-language summary

Plainly said:

The construction gives two truths.

One truth says which things belong together.
That is the overlap geometry.

The other truth says whether a journey returns on the same sheet or the opposite sheet.
That is the holonomy.

The first truth is about form.
The second truth is about passage.

Both are real.
Neither reduces to the other.

---

## 13. One-line compression

\[
\text{Form} := Q = MM^{\mathsf T},
\qquad
\text{Passage} := \chi(C)=\sum_{e\in C}\varepsilon(e)\pmod 2.
\]

These are the two irreducible invariant layers currently visible in the transport construction.

