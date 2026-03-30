# Graph-Theoretic Next Blade Note

## Status
Working note

## Purpose

This note states the next rigorous blade after the current graph-theoretic witness reduction.

The present position is:

- the support-minimal passage witness has size \(6\),
- its support graph has maximum degree \(2\),
- hence it is a disjoint union of paths and cycles.

So the remaining problem is no longer broad.
It has split into two exact graph-theoretic blades:

1. open versus closed,
2. if closed, connected versus disconnected.

This note isolates those blades cleanly.

---

## 1. Present proved base

Let

\[
G_{15}\cong L(\mathrm{Petersen}),
\]

and let

\[
[\varepsilon]\in H^1(G_{15};\mathbb F_2)
\]

be the nontrivial cocycle class arising from the signed \(2\)-lift

\[
G_{30}\to G_{15}.
\]

Let \(S\subseteq E(G_{15})\) be a support-minimal representative of size

\[
|S|=6.
\]

Then the support graph

\[
H=(V(G_{15}),S)
\]

satisfies

\[
d_S(v)\le 2 \qquad \forall v\in V(G_{15}),
\]

so every connected component of \(H\) is either a path or a cycle.

This is the locked graph-theoretic base.

---

## 2. First remaining blade: open versus closed

The first unresolved question is whether \(H\) must be endpoint-free.

### Definition 2.1
The witness is **closed** if every support vertex has even degree.

Equivalently,

\[
\partial S = 0
\]

in the mod-\(2\) vertex-boundary sense.

### Definition 2.2
The witness is **open** if some support vertex has odd degree.

Equivalently,

\[
\partial S \neq 0.
\]

Since \(d_S(v)\le 2\), this means:

- closed witness: every support vertex has degree \(2\),
- open witness: some support vertices have degree \(1\).

So the first true graph-theoretic blade is:

\[
\text{Must } \partial S = 0\text{?}
\]

If yes, the witness is cycle-only.
If no, path-based support survives.

---

## 3. Why this is the first blade

The open/closed distinction is prior to all finer shape claims.

If \(H\) is open, then the support is not itself a mod-\(2\) cycle object.
Its nontriviality is only visible through the ambient cycle structure of \(G_{15}\).

If \(H\) is closed, then the support itself is already a cycle-space object.

So the graph-theoretic question is not first “is it a hexagon?”
It is first:

> Is the minimal witness itself a cycle object, or only an obstruction visible through surrounding cycles?

That is the exact first blade.

---

## 4. Second remaining blade: connected versus disconnected

Assume now that \(H\) is closed.

Then every connected component of \(H\) is a cycle, and because \(|S|=6\), the only simple possibilities are

\[
C_6
\qquad\text{or}\qquad
C_3\sqcup C_3.
\]

So once the open branch is killed, the next blade becomes:

\[
\text{Must closed support be connected?}
\]

If yes, then \(H\cong C_6\).

If no, then the remaining disconnected closed rival is

\[
C_3\sqcup C_3.
\]

Thus the hexagon claim factors through connectedness only after closedness is established.

---

## 5. Conditional theorem chain

The current logic can therefore be written as a short chain of conditional statements.

### Proposition 5.1
If a support-minimal representative is closed, then its support is a disjoint union of cycles.

### Proposition 5.2
If a support-minimal representative is closed and connected, then its support is isomorphic to

\[
C_6.
\]

### Proposition 5.3
If a support-minimal representative is closed and disconnected, then the only simple possibility at support size \(6\) is

\[
C_3\sqcup C_3.
\]

So the only missing steps between current theorem-level facts and the desired hexagon are:

1. prove closedness,
2. prove connectedness.

That is the whole remaining graph-theoretic ladder.

---

## 6. Exact reduction of the conjecture

The hexagon conjecture can now be restated in strict graph language as:

### Conjecture 6.1
Every support-minimal representative of the nontrivial cocycle class on \(G_{15}\cong L(\mathrm{Petersen})\) is closed and connected.

By the previous reductions, this conjecture is equivalent to:

### Conjecture 6.2
Every support-minimal representative has support graph

\[
H\cong C_6.
\]

So the conjecture does not need to be attacked directly as “hexagonality.”
It can be attacked via the two sharper subclaims:

- closedness,
- connectedness.

That is the right decomposition.

---

## 7. Boundary-language formulation

Let \(B\) be the mod-\(2\) vertex-edge incidence matrix of \(G_{15}\).

Write the support indicator of \(S\) as \(x\in \mathbb F_2^{30}\).

Then

\[
Bx = \partial S.
\]

So:

- \(Bx=0\) means the witness is closed,
- \(Bx\neq 0\) means the witness is open.

This makes the first blade completely algebraic.

The graph-theoretic question “open or closed?” is exactly:

\[
\text{Does every minimum-weight representative satisfy } Bx=0?
\]

This is the cleanest algebraic version of the first blade.

---

## 8. Why connectedness is a separate issue

Even if one proves

\[
Bx=0,
\]

connectedness does not follow automatically.

A closed witness of six edges can still split as

\[
C_3\sqcup C_3.
\]

So the disconnected closed rival is not killed by Eulerianity alone.

This is why the second blade is genuinely independent.

One needs some further argument to show that the passage witness condenses onto one component rather than two.

In strict graph language, that means:

> Eulerian support does not imply connected support.

So the hexagon claim cannot be reached by parity alone.

---

## 9. Strongest present graph statement

The strongest rigorous statement available now is the following.

### Theorem 9.1
Let \(S\subseteq E(G_{15})\) be a support-minimal representative of the nontrivial cocycle class of the signed \(2\)-lift \(G_{30}\to G_{15}\), with \(|S|=6\). Then the support graph \(H=(V(G_{15}),S)\) has maximum degree \(2\), and hence is a disjoint union of paths and cycles.

### Corollary 9.2
If \(H\) is closed and connected, then \(H\cong C_6\).

### Corollary 9.3
If \(H\) is closed and disconnected, then \(H\cong C_3\sqcup C_3\).

These statements are exact and fully graph-theoretic.

---

## 10. Best next rigorous move

The next rigorous move is not to restate the hexagon conjecture again.

It is to attack the first blade directly:

> Can one prove that a support-minimal representative must satisfy \(Bx=0\)?

That is the most important remaining structural question.

If the answer is yes, the open branch is dead.

Then only the connectedness problem remains.

So the best immediate next note should focus on:

\[
\textbf{Can support-minimality force Eulerianity?}
\]

That is the correct next graph-theoretic blade.

---

## 11. One-line compression

The witness problem has now been reduced to this exact ladder:

\[
|S|=6,\ d_S(v)\le 2
\Longrightarrow
\text{paths-or-cycles};
\]

then

\[
Bx=0\ ?\ \Longrightarrow\ \text{closed branch};
\]

then

\[
\text{connected?}
\Longrightarrow
C_6.
\]

So the remaining problem is no longer “find the shape.”
It is:

\[
\textbf{prove or disprove Eulerianity, then prove or disprove connectedness.}
\]

