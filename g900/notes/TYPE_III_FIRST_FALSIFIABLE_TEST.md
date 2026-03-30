# Type III First Falsifiable Test

## Status
Working test note

## Purpose

This note turns the current Type III lift-chart story into a concrete falsifiable test.

The goal is to stop asking whether the chart feels right and instead ask whether it survives contact with the signed 2-lift cocycle on the quotient tower

\[
G60 \to G30 \to G15,
\qquad
G15 \cong L(\mathrm{Petersen}).
\]

The authoritative inputs come from the paper:

- the quotient tower exists,
- the core geometry on \(G15\) is governed by
  \[
  Q = M M^{\mathsf T} = A^3 + 2A^2 + 2I,
  \]
- the intermediate quotient
  \[
  G30 \to G15
  \]
  carries a signed 2-lift and a nontrivial \(\mathbb Z_2\)-valued cocycle,
- and for any cycle \(C \subseteq G15\), its parity
  \[
  \chi(C) := \sum_{e\in C}\varepsilon(e)\pmod 2
  \]
  determines whether the lifted walk closes on the same or opposite sheet. 0

This note uses that as the hard base.

---

## 1. What is being tested

The current working Type III chart is:

\[
\phi(0)=0,\qquad
\phi(2)=2,\qquad
\phi(1)=3,\qquad
\phi(3)=1.
\]

Interpretively, this yields two candidate sectors:

### Axial sector
\[
\mathcal A = \{Q_0,\ Q_{180}\}
\]

### Orthogonal sector
\[
\mathcal O = \{Q_{90},\ Q_{270}\}.
\]

The current conjectural claim is not that this chart changes the paper's theorem.
It is only that this chart may organize the **lift layer** in a meaningful way.

The sharpened question is:

> Does the cocycle parity on short cycles of \(G15\) actually respect a natural partition compatible with this chart?

That is the test.

---

## 2. Authoritative cocycle input

The paper defines the signed-lift cocycle

\[
\varepsilon : E(G15) \to \mathbb Z_2
\]

and the parity of a cycle \(C\) by

\[
\chi(C):=\sum_{e\in C}\varepsilon(e)\pmod 2.
\]

It states:

- \(\chi(C)=0\) if and only if the lifted walk closes on the **same sheet**
- \(\chi(C)=1\) if and only if the lifted walk closes on the **opposite sheet**. 1

This is the only authoritative lift invariant currently available.

So any Type III story must be judged against \(\chi\), not against intuition alone.

---

## 3. Why short cycles come first

The smallest meaningful test objects are short closed walks in \(G15\).

The first choice should be:

\[
\mathcal C_3 := \{\text{all simple 3-cycles in } G15\}.
\]

These are the most useful first test objects because:

1. they are the smallest nontrivial cycles,
2. cocycle parity is already meaningful on them,
3. \(G15 \cong L(\mathrm{Petersen})\) naturally contains triangle structure,
4. they are small enough to enumerate explicitly and compare.

This makes triangles the first falsifiable test bed.

---

## 4. Test object

Define:

\[
\mathcal C_3 := \{ C \subseteq G15 : C \text{ is a simple triangle} \}.
\]

For each \(C \in \mathcal C_3\), compute its cocycle parity:

\[
\chi(C)=\sum_{e\in C}\varepsilon(e)\pmod 2.
\]

This produces a binary parity label on every triangle:

- even parity = same-sheet closure
- odd parity = opposite-sheet closure

This data is what the Type III chart must face.

---

## 5. What Type III would need

For the Type III chart to do real work, we need more than a relabeling of four headings.
We need a natural partition of the relevant short-cycle family into two classes.

So the target is to find a decomposition

\[
\mathcal C_3 = \mathcal C_{\mathrm{ax}} \sqcup \mathcal C_{\mathrm{orth}}
\]

such that:

- \(\mathcal C_{\mathrm{ax}}\) corresponds naturally to the axial chart \(\mathcal A\),
- \(\mathcal C_{\mathrm{orth}}\) corresponds naturally to the orthogonal chart \(\mathcal O\).

This partition must be defined by actual transport/lift structure, not by after-the-fact parity sorting.

That is essential.

---

## 6. Pass condition

Type III gains real support if the following happen:

### Pass condition A
There exists a natural way to partition the triangles into

\[
\mathcal C_{\mathrm{ax}} \sqcup \mathcal C_{\mathrm{orth}}
\]

that is genuinely compatible with the Type III chart.

### Pass condition B
Odd holonomy is meaningfully concentrated in the orthogonal family.

That is, one finds behavior of the form:

\[
\chi(C)=0 \text{ for most or all } C\in \mathcal C_{\mathrm{ax}},
\]

while

\[
\chi(C)=1 \text{ appears first, or clusters, in } \mathcal C_{\mathrm{orth}}.
\]

This does not need absolute separation at first.
A strong concentration pattern would already be meaningful.

If both conditions hold, then Type III has survived the first real lift-level test.

---

## 7. Fail condition

Type III weakens sharply if either of the following happens.

### Fail condition A
No natural partition of the short-cycle family exists that matches the chart.

That would mean the axial/orthogonal split is not structurally real at the walk level.

### Fail condition B
Odd holonomy is distributed with no meaningful separation between the two candidate families.

That would mean the Type III chart is not organizing the cocycle in a useful way.

If either fail condition occurs, Type III becomes little more than coordinate poetry.

---

## 8. Why triangles are enough for a first test

This note does not claim that triangles are the whole story.

But they are enough for a first falsification attempt because:

- they are the smallest nontrivial closed walks,
- they are easy to enumerate,
- and if the Type III chart cannot show a signal even there, it is unlikely to be a deep organizing principle.

So triangles are not the final test.
They are the first hard test.

---

## 9. Secondary follow-up if triangles are inconclusive

If the triangle test is inconclusive, the next family to examine is:

- short 4-cycles, if present in the relevant projected structure,
- or short geodesic-return loops built from the distance classes of \(G15\).

But none of that should be touched until the triangle test is run.

This note is intentionally disciplined.

---

## 10. Relation to the edge/vertex bridge

The current bridge story

\[
20 \rightsquigarrow 9
\]

should **not** be used during the first falsification test.

Why?

Because the bridge is weaker than the cocycle data.
If Type III cannot first survive the cocycle test on short cycles, there is no reason to trust the bridge.

So the correct order is:

1. test Type III against cocycle parity on short cycles,
2. only then revisit whether the orthogonal sector remains a plausible entry point for the bridge
   \[
   20 \rightsquigarrow 9.
   \]

This keeps the logic honest.

---

## 11. Best current one-line test

The first real question is:

> Can the triangles of \(G15\) be partitioned in a natural Type III-compatible way such that odd cocycle parity is concentrated in the orthogonal family?

That is the first falsifiable version of the current chart.

---

## 12. Plain-language summary

Plainly said:

We stop arguing about whether the Type III split feels right.

Instead, we look at the smallest loops on \(G15\), compute whether they come back on the same sheet or the opposite sheet, and ask whether those loops naturally split into an axial family and an orthogonal family the way Type III says they should.

If yes, the chart has earned something.
If no, the chart gets demoted.

---

## 13. One-line compression

Enumerate the triangles of \(G15\), compute their cocycle parity, and test whether odd holonomy clusters in a natural orthogonal family.

