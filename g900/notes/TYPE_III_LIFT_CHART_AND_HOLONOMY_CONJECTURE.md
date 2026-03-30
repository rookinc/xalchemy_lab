# Type III Lift Chart and Holonomy Conjecture

## Status
Working note
Interpretive extension built on the paper's signed-lift layer

## Purpose

This note continues the current program under a strict rule:

- the paper's core overlap geometry on \(G15\) is authoritative
- the signed 2-lift and cocycle on \(G30 \to G15\) are authoritative
- the Type III split is treated only as a candidate **organizational chart** on the lift layer

This note does not modify the paper's theorem.
It attempts to place the earlier expedition language into the paper's actual signed-lift framework.

The underlying paper establishes:

\[
G60 \to G30 \to G15,\qquad G15 \cong L(\mathrm{Petersen}),
\]

together with the sector identity

\[
Q=MM^{\mathsf T}=A^3+2A^2+2I,
\]

and a signed 2-lift with nontrivial \(\mathbb Z_2\)-valued cocycle on \(G30 \to G15\). 0

This note works entirely above that foundation.

---

## 1. Authoritative split from the paper

The paper gives two distinct layers.

### 1.1 Core overlap geometry
On the quotient core

\[
G15 \cong L(\mathrm{Petersen}),
\]

the sector–edge incidence matrix

\[
M \in \{0,1\}^{15\times 30}
\]

defines the Gram matrix

\[
Q:=MM^{\mathsf T},
\]

and the central theorem is

\[
Q=A^3+2A^2+2I.
\]

Equivalently, sector overlaps are completely determined by graph distance on \(G15\), with values

\[
14,\ 9,\ 5,\ 4
\]

for distances \(0,1,2,3\). 1

This is the exact overlap geometry of the core.

### 1.2 Signed lift layer
The paper also states that the intermediate quotient

\[
G30 \to G15
\]

is a signed 2-lift carrying a nontrivial \(\mathbb Z_2\)-valued cocycle, and it emphasizes that this cocycle is **not detected by \(Q\)**. 2

Thus the paper itself already enforces the split:

- \(Q\): metric/incidence geometry on the core
- cocycle: companion signed transport invariant above the core

This note respects that split completely.

---

## 2. Lift language from the paper

For each vertex \(u \in V(G15)\), the signed 2-lift gives two lifted vertices:

\[
u^+,\ u^-.
\]

Each base edge \(uv\) lifts in one of two ways.

### Parallel lift
\[
u^+ \sim v^+,\qquad u^- \sim v^-.
\]

### Crossed lift
\[
u^+ \sim v^-,\qquad u^- \sim v^+.
\]

This yields a sign function on base edges:

\[
\sigma:E(G15)\to\{\pm 1\},
\]

and equivalently a cocycle

\[
\varepsilon:E(G15)\to \mathbb Z_2
\]

defined by:

\[
\varepsilon(e)=
\begin{cases}
0,& \text{parallel lift},\\
1,& \text{crossed lift}.
\end{cases}
\]

This cocycle is the authoritative signed invariant in the current framework. 3

---

## 3. Holonomy criterion

For any cycle \(C\subseteq G15\), define its parity by:

\[
\chi(C):=\sum_{e\in C}\varepsilon(e)\pmod 2.
\]

By the paper's holonomy criterion:

- \(\chi(C)=0\) if and only if the lifted walk closes on the same sheet
- \(\chi(C)=1\) if and only if the lifted walk closes on the opposite sheet. 4

This is the rigorous replacement for earlier informal sign language.

In particular, the earlier shorthand

\[
n_{15}=-n_0
\]

should now be interpreted, when possible, as:

> the relevant projected transport cycle has odd cocycle parity, so the lifted walk returns on the opposite sheet.

And the doubled closure

\[
n_{30}=n_0
\]

should be interpreted as the corresponding doubled traversal having even total parity.

This is a major cleanup.

---

## 4. Role of Type III

The current working Type III model is:

\[
\phi(0)=0,\qquad \phi(2)=2,\qquad \phi(1)=3,\qquad \phi(3)=1.
\]

Previously this was being discussed as though it might itself be a kind of geometry.

That is no longer the right interpretation.

### Correct interpretation
Type III is now treated only as a candidate **chart on lifted transport modes**.

It organizes four relaunch labels into two sectors:

\[
\{Q_0,Q_{180}\} \sqcup \{Q_{90},Q_{270}\}.
\]

This chart does **not** alter:

\[
Q=MM^{\mathsf T}=A^3+2A^2+2I.
\]

Instead, it proposes a way to organize how lifted transport may be experienced or grouped above the core geometry.

So:

- the paper's cocycle is the invariant
- Type III is the candidate chart

This distinction is essential.

---

## 5. Type III sector interpretation on the lift layer

Under the current working chart:

### Axial sector
\[
\mathcal A := \{Q_0,\ Q_{180}\}
\]

### Orthogonal sector
\[
\mathcal O := \{Q_{90},\ Q_{270}\}
\]

The strongest current working interpretation is:

- \(\mathcal A\) = orientation sector within an already-built world
- \(\mathcal O\) = companion sector where exchange and generative behavior become visible

Again, this is not yet a theorem of the paper.
It is a proposed way of reading the lift layer without touching the core theorem.

---

## 6. Lift-walk families

To sharpen the interpretation, define two families of projected walks on \(G15\).

### Axial projected walk family
\[
\Gamma_{\mathrm{ax}}
\]

This denotes projected closed walks on \(G15\) interpreted as arising from axial lift modes.

### Orthogonal projected walk family
\[
\Gamma_{\mathrm{orth}}
\]

This denotes projected closed walks on \(G15\) interpreted as arising from orthogonal companion lift modes.

At present, these are conceptual families, not yet algorithmically defined subsets of cycle space.
The point is to make the conjecture structurally precise enough to test.

---

## 7. Type III holonomy conjecture

The natural next conjecture is now:

### Conjecture
The Type III chart on the signed 2-lift can be organized so that:

\[
\chi(\Gamma_{\mathrm{ax}})\ \text{is predominantly even},
\]

while

\[
\Gamma_{\mathrm{orth}}
\]

is the natural locus in which odd holonomy appears and accumulates.

In plain language:

- axial lift modes mostly preserve sheet in the relevant closure patterns
- orthogonal companion modes are where opposite-sheet behavior becomes naturally active

This is the first clean lift-level version of the old intuition that:

- axial modes orient within a world
- orthogonal modes generate or exchange world-structure

---

## 8. Why this conjecture is plausible

This conjecture is plausible for several reasons.

### 8.1 The paper already separates overlap and lift
The cocycle is explicitly independent of the overlap matrix \(Q\). 5

So there is conceptual room for a lift-level distinction that is invisible at the metric/core level.

### 8.2 Type III already splits launch classes asymmetrically
Under Type III:

- the axial classes are fixed by heading update
- the orthogonal classes are exchanged

So the orthogonal sector is already the place where nontrivial one-step activity lives.

### 8.3 Earlier qualitative read
The current expeditionary interpretation already produced the distinction:

- axial pair feels like one world viewed from opposite directions
- orthogonal pair feels like two halves of one world

This matches very naturally with a conjecture that odd sheet-exchange is organized through the orthogonal sector rather than the axial one.

This is not proof.
But it is coherent with both the paper's lift layer and the current working chart.

---

## 9. Relation to the edge/vertex bridge

The current bridge story was:

\[
20 \rightsquigarrow \{Q_{90},Q_{270}\} \rightsquigarrow 9.
\]

Under the present reinterpretation, this should now be read as:

- edge-side completion is not a claim about \(Q\) directly
- it is a claim about how repeated orthogonal companion transport on the lift layer might accumulate into a stabilized local host visible on the core-side interpretation

So the orthogonal pair becomes:

- not the source of the core theorem
- but the candidate source of the extra signed transport behavior that could support world-building interpretations above the core

This is much cleaner than the earlier mixed language.

---

## 10. What this note does **not** claim

This note does not claim:

1. that Type III has been proved from the cocycle
2. that orthogonal cycles are literally the set of odd-holonomy cycles
3. that axial cycles are all even-holonomy
4. that the edge/vertex bridge is now proven
5. that world-building language is part of the paper's theorem
6. that the cocycle is determined by local heading data alone

All of those remain open.

This note only claims that Type III can now be rephrased in the paper's lift language in a mathematically cleaner way.

---

## 11. Best current rigorous boundary

### Authoritative from the paper
- \(G60 \to G30 \to G15\)
- \(G15 \cong L(\mathrm{Petersen})\)
- \(Q=MM^{\mathsf T}=A^3+2A^2+2I\)
- overlap strata \(14,9,5,4\)
- signed 2-lift on \(G30 \to G15\)
- nontrivial cocycle \(\varepsilon\)
- holonomy criterion via parity \(\chi\) 6

### Working interpretive layer
- Type III as a chart on lifted transport classes
- axial sector \(\mathcal A\)
- orthogonal sector \(\mathcal O\)

### Open conjectural layer
- orthogonal sector as the natural carrier of odd holonomy
- orthogonal sector as the generative locus for world-building interpretations
- coupling of that sector to the bridge
  \[
  20 \rightsquigarrow 9.
  \]

That is the correct current boundary.

---

## 12. Best next technical question

The next real technical target is:

> define, as explicitly as possible, what counts as an axial projected walk and what counts as an orthogonal projected walk, and then compare their cocycle parities.

That is the point where the Type III chart starts becoming falsifiable.

---

## 13. Plain-language summary

Plainly said:

The paper says there are two layers:

- the core overlap geometry
- and a separate sheet-flip transport layer above it

We now place Type III only on the second layer.

That means:
- the core theorem stays untouched
- the Type III split is our current way of organizing lifted transport
- and the next question is whether the sideways / orthogonal sector is really where opposite-sheet behavior naturally lives

---

## 14. One-line summary

Type III should now be treated as a candidate chart on the paper's signed 2-lift \(G30 \to G15\), with the cocycle as the real invariant and the axial/orthogonal split as a proposed organization of how same-sheet versus opposite-sheet transport is encountered.

