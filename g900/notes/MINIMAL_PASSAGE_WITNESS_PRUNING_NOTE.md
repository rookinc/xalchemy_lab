# Minimal Passage Witness Pruning Note

## Status
Working derivation note

## Purpose

This note records the current first-principles pruning of the minimal support problem on the passage side.

The setup is:

- the paper gives a signed 2-lift
  \[
  G30 \to G15,
  \]
  with a nontrivial \(\mathbb Z_2\)-valued cocycle,
- the cocycle is only defined up to switching,
- and the paper states that the switching class admits a representative of minimal support size \(6\). 0

The question is:

> What can be derived, without shortcuts, about the shape of a support-minimal representative of size \(6\)?

This note records the cuts that already hold.

---

## 1. Setup

Let \(G15 \cong L(\mathrm{Petersen})\), so \(G15\) is 4-regular. 1

Let \(S \subseteq E(G15)\) be the support of a cocycle representative in its switching class, chosen to have minimal support size:

\[
|S| = 6.
\]

We study the support subgraph

\[
H := (V(G15), S).
\]

The goal is to derive constraints on \(H\).

---

## 2. First cut: support-degree bound

If a vertex \(v\) has \(k=d_S(v)\) support edges incident to it, then switching at \(v\) toggles all four edges incident to \(v\), since \(G15\) is 4-regular.

So the support size changes by:

\[
|S'| = |S| - k + (4-k) = |S| + 4 - 2k.
\]

Because \(S\) is support-minimal, this cannot decrease support size. Therefore:

\[
4 - 2k \ge 0,
\]

hence

\[
k \le 2.
\]

### Proposition 2.1
For every vertex \(v\in V(G15)\),

\[
d_S(v)\le 2.
\]

### Consequence
The support subgraph \(H\) has maximum degree \(2\).

So every connected component of \(H\) is either:

- a path,
- or a cycle.

This is the first major pruning.

---

## 3. Immediate eliminations

Because every vertex of \(H\) has degree at most \(2\), the following are impossible:

- tetrahedral support (\(K_4\)),
- any support graph with a branching vertex,
- any support graph with a vertex of degree \(3\) or \(4\).

### Corollary 3.1
A tetrahedral passage witness is impossible.

This kills the earlier tetrahedral conjecture.

The passage witness, if minimal, must be 1-dimensional.

---

## 4. Global shape classes with 6 edges

Since \(H\) is a disjoint union of paths and cycles and has exactly \(6\) edges, only a small family of shapes survives.

These fall into two broad regimes.

### 4.1 Endpoint-free regime
No support vertex has degree \(1\).

Then every component of \(H\) is a cycle.

With only \(6\) edges total, the only simple possibilities are:

\[
C_6
\quad\text{or}\quad
C_3 \sqcup C_3.
\]

So if the witness is endpoint-free, it is already reduced to these two options.

### 4.2 Endpoint-bearing regime
At least one support vertex has degree \(1\).

Then at least one component of \(H\) is a path.

The connected extreme is:

\[
P_7,
\]

a path of length \(6\).

Disconnected endpoint-bearing cases are disjoint unions of shorter paths, possibly mixed with a cycle, so long as the total number of edges remains \(6\).

Thus the only surviving regimes are:

- closed cycle-based witness,
- open path-based witness.

Everything else is gone.

---

## 5. Degree-2 vertices are movable

If a support vertex has degree \(2\), then switching at that vertex changes support size by

\[
4 - 2\cdot 2 = 0.
\]

So switching at a degree-2 support vertex preserves minimality.

### Consequence
Degree-2 vertices are not rigid.

This means a support containing long chains or cycles of degree-2 vertices may be shape-flexible inside its switching class.

So the literal geometric embedding of the support may not itself be the invariant.

What may matter more is:

- connectedness,
- endpoint count,
- and whether the support is cycle-only or contains paths.

---

## 6. Degree-1 vertices are costly

If a support vertex has degree \(1\), then switching there changes support size by

\[
4 - 2\cdot 1 = 2.
\]

So the support grows.

### Consequence
Endpoints are expensive.

This makes open path components qualitatively different from cycles:

- cycle supports are entirely degree-\(2\),
- path supports have degree-\(1\) endpoints that are resistant to removal by a single switch.

So the support problem is not merely about edge count.
It is also about endpoint structure.

---

## 7. The exact reduced fork

The problem has now been cut down to this fork.

### Closed witness
The support is endpoint-free, hence cycle-only.

Then the only simple possibilities are:

\[
C_6
\quad\text{or}\quad
C_3 \sqcup C_3.
\]

### Open witness
The support has endpoints, hence contains at least one path component.

Then the support is path-based, with connected extreme:

\[
P_7.
\]

This is the exact reduced shape fork.

---

## 8. Conceptual meaning of the fork

The fork is no longer “tetrahedron or not.”

It is now:

\[
\text{closed witness} \quad\text{vs}\quad \text{open witness}.
\]

This has a genuine mathematical meaning.

### Closed witness
The support is itself a mod-2 cycle object.
Passage condenses on a self-contained loop witness.

### Open witness
The support is not itself a cycle.
Passage condenses on a sparse obstruction that only expresses its nontriviality through the ambient graph and switching class.

This is the real conceptual split now.

---

## 9. What is still unresolved

At present, we have **not** yet proved any of the following:

- that the support must be connected,
- that the support must contain a cycle,
- that the support cannot be open,
- that the support is Eulerian,
- that the support must be \(C_6\),
- that the support must be \(C_3 \sqcup C_3\),
- that the support must be \(P_7\).

Those remain open.

But the space of possibilities has been sharply narrowed.

---

## 10. Strongest current derived statement

The strongest current derived statement is:

> A support-minimal passage witness of size \(6\) on the signed lift over \(G15\) must be a 1-dimensional support subgraph of maximum degree \(2\). Hence it is a disjoint union of paths and cycles, and the problem reduces to deciding whether the witness is closed \((C_6 \text{ or } C_3\sqcup C_3)\) or open (path-based support). 

This is the first real pruning of the passage problem.

---

## 11. Plain-language summary

Plainly said:

The minimal passage witness cannot be a tetrahedron, cannot branch, and cannot be a little 3D core.

It has to be line-like.

So the only real question left is whether the witness is:

- a loop,
- two loops,
- or an open corridor.

That is the current narrow path.

---

## 12. One-line compression

For a support-minimal size-6 cocycle representative on \(G15\), every support vertex has degree at most \(2\), so the witness is forced to be a union of paths and cycles; the problem is now exactly “closed witness or open witness?”

