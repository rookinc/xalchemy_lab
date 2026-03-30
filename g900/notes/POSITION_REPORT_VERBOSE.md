# Position Report — Verbose Working Note

## Status
Working synthesis
This note separates:
- what is established,
- what has been derived in chat,
- what remains conjectural,
- and what the next disciplined moves are.

The goal is not to inflate confidence.
The goal is to preserve a clean boundary between theorem, derivation, and live program.

---

## 1. Executive summary

We now have a stable backbone.

There is a quotient tower

\[
G_{60} \to G_{30} \to G_{15},
\qquad
G_{15} \cong L(\mathrm{Petersen}),
\]

and on the 15-vertex core there is an exact quadratic overlap law

\[
Q := MM^{\mathsf T} = A^3 + 2A^2 + 2I.
\]

Independently, the intermediate layer carries a signed 2-lift

\[
G_{30} \to G_{15}
\]

with a nontrivial \mathbb Z_2-valued cocycle class

\[
[\varepsilon] \in H^1(G_{15};\mathbb Z_2).
\]

That much is solid.

The current conceptual compression is that the whole construction presents two irreducible invariant layers:

- **Form**: the quadratic overlap structure on the quotient core
- **Passage**: the mod-2 holonomy structure on the signed lift

This is the central position we have reached.

Everything beyond that must be graded carefully by certainty.

---

## 2. What is theorem-level

### 2.1 Quotient graph tower
The quotient graph ladder is:

\[
G_{60} \to G_{30} \to G_{15},
\qquad
G_{15} \cong L(\mathrm{Petersen}).
\]

This is the graph-theoretic skeleton of the construction.

### 2.2 Core incidence structure
On G_{15}, there is a distinguished 15\times 30 0-1 matrix

\[
M \in \{0,1\}^{15\times 30},
\]

whose rows encode a transport-induced family of edge subsets of the core.

### 2.3 Quadratic overlap law
Its Gram matrix

\[
Q := MM^{\mathsf T}
\]

satisfies the exact polynomial identity

\[
Q = A^3 + 2A^2 + 2I,
\]

where A is the adjacency matrix of G_{15}.

Equivalently, the overlap values are distance-controlled:

\[
Q_{uv} =
\begin{cases}
14, & d(u,v)=0,\\
9, & d(u,v)=1,\\
5, & d(u,v)=2,\\
4, & d(u,v)=3.
\end{cases}
\]

This is the exact core theorem.

### 2.4 Spectral and geometric consequences
The overlap form has the induced spectrum obtained by applying

\[
p(x)=x^3+2x^2+2
\]

to the spectrum of A, and the centered normalized row family produces a rigid three-angle spherical realization.

These are consequences of the overlap theorem, not separate centers of gravity.

### 2.5 Signed 2-lift and cocycle
The intermediate covering

\[
G_{30} \to G_{15}
\]

is a signed 2-lift, giving a cocycle

\[
\varepsilon:E(G_{15})\to \mathbb Z_2
\]

up to switching, hence a cohomology class

\[
[\varepsilon]\in H^1(G_{15};\mathbb Z_2).
\]

For cycles C\subseteq G_{15},

\[
\chi(C):=\sum_{e\in C}\varepsilon(e)\pmod 2
\]

detects whether the lifted walk closes on the same or opposite sheet.

The class is nontrivial.

### 2.6 Independence of the two layers
The cocycle is not detected by Q.

So the construction really carries two different invariant structures of different type:

\[
Q
\qquad \text{and} \qquad
[\varepsilon].
\]

This split is not decoration.
It is structural.

---

## 3. The strongest conceptual formulation we currently trust

The current best compression is:

\[
\text{Form} := Q = MM^{\mathsf T}
\]

\text{Passage} := \chi(C)=\sum_{e\in C}\varepsilon(e)\pmod 2


with the verbal summary:

- **Form remembers what overlaps**
- **Passage remembers how closure occurred**

This is the cleanest high-level statement we have that still respects the exact mathematics.

It avoids mystical language while preserving the philosophical force of the split.

---

## 4. What we derived ourselves in chat

This section is important.
These points are not yet theorem-level in the paper.
They are current derivations from the setup.

### 4.1 Minimal support problem for passage
We asked about a support-minimal representative of the nontrivial cocycle class, using the paper's statement that a representative of support size 6 exists.

Let S\subseteq E(G_{15}) be such a support-minimal representative.

Because G_{15} is 4-regular, switching at a vertex toggles all four incident edges.
If k of those are in the support, switching changes the support size by

\[
4-2k.
\]

Minimality forbids decrease, so:

\[
4-2k \ge 0 \quad\Longrightarrow\quad k\le 2.
\]

Hence:

\[
d_S(v)\le 2 \qquad \forall v.
\]

This is the first serious pruning result.

### 4.2 Consequence: one-dimensional support only
Since every support vertex has degree at most 2, the support subgraph is a disjoint union of:

- paths
- cycles

This immediately kills:

- tetrahedral support
- branching support
- any degree-3 or degree-4 support vertex

So the minimal passage witness, if size 6, cannot be a tetrahedral or trivalent core.
It must be 1-dimensional.

### 4.3 Closed vs open fork
This reduced the problem to:

- **closed witness**: cycle-based
- **open witness**: path-based

For six edges, the closed branch reduces to:

\[
C_6
\quad \text{or} \quad
C_3 \sqcup C_3.
\]

The connected open extreme is:

\[
P_7.
\]

So the original shape problem was pruned down to a very narrow fork.

### 4.4 Comparative pruning
We then pruned by plausibility:

- tetrahedral support: dead
- branching support: dead
- C_3\sqcup C_3: weakened because it looks too local-star-like for a cocycle the theorem says is nonlocal
- disconnected path support: weakened because it looks too basis-like and not self-contained

This left the main fight as:

\[
C_6 \quad \text{vs} \quad P_7.
\]

### 4.5 Current lock
We then locked

\[
\boxed{C_6}
\]

as the leading target for the minimal passage witness.

This is not proved.
But it is the best current target after pruning.

---

## 5. Cube grammar program

After locking C_6, we stopped treating it as a picture and turned to a generator.

### 5.1 Basic idea
The cube is not merely a sketch host.
It is a walk host with a grammar.

So instead of asking only what the minimal witness looks like, we asked what the shortest nontrivial closed walk word is whose passage image is six-cyclic.

### 5.2 Grammar
We introduced a minimal alphabet such as

\[
\{F,L,R,X\},
\]

where:

- F: move within a face-thread / band
- L,R: quarter turns
- X: crossing to a companion band / seam

This is not theorem-level graph language yet.
It is the current upstairs generating language.

### 5.3 Two outputs from one word
For a word w, we separated:

- a **form projection** downstairs
- a **passage projection** upstairs

This became the seed of the translator idea.

### 5.4 Six-step seed
We identified the alternating six-step seed

\[
FXFXFX
\]

as the cleanest unsteered candidate for a six-step passage loop.

Then, under the provisional heading recursion with crossing rule \phi(h)=-h\pmod 4, we derived a closure condition for words of the form

\[
w = F\alpha_1X\,F\alpha_2X\,F\alpha_3X,
\qquad \alpha_i\in\{e,L,R\}.
\]

The heading closure equation becomes

\[
2h_0 + \delta_1 - \delta_2 + \delta_3 \equiv 0 \pmod 4.
\]

This gave concrete candidate words:

- axial candidate:
\[
  FXFXFX
\]
- orthogonal candidate:
\[
  FRX\,FLX\,FX
\]

This is real derivation work, but still provisional because the grammar itself is not yet theorem-level.

---

## 6. Chirality-budget reading

We also observed the two useful gauges for steering.

Since

\[
R=L^{-1}=L^3
