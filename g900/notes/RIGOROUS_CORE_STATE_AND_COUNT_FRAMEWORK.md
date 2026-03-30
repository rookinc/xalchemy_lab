# Rigorous Core State and Count Framework

## Status
Working rigor note

## Purpose

This note freezes the current project into a strict three-layer structure:

1. **primitive definitions**
2. **statements derivable from those definitions**
3. **conjectures not yet derivable**

The goal is to stop blending:
- metaphor
- observation
- derivation
- and conjecture

into one stream.

This note therefore does **not** try to explain everything.
It only records the cleanest rigorous core currently available.

---

## 1. Primitive sets

We begin with two finite cyclic sets:

\[
\mathbb Z_2 = \{+,-\}
\]

\[
\mathbb Z_4 = \{0,1,2,3\}
\]

Interpretation:

- \(\mathbb Z_2\) will be used for sidedness or sign
- \(\mathbb Z_4\) will be used for heading classes

At this stage, these are simply formal sets.

No geometric interpretation is required yet.

---

## 2. Minimal state space

Let \(X\) be a set of host-position labels.

A minimal walker state is a triple:

\[
s = (x,\varepsilon,h)
\]

where:

- \(x \in X\)
- \(\varepsilon \in \mathbb Z_2\)
- \(h \in \mathbb Z_4\)

Thus the state space is:

\[
S := X \times \mathbb Z_2 \times \mathbb Z_4
\]

Interpretation:

- \(x\) = host placement label
- \(\varepsilon\) = sign / sidedness
- \(h\) = heading class

This is the smallest state space currently needed to express the locked cycle law together with relaunch-class behavior.

---

## 3. Sign-flip operation

Define the sign-flip involution on \(S\) by:

\[
-(x,\varepsilon,h) := (x,-\varepsilon,h)
\]

where the sign on \(\varepsilon\) is flipped and all other components are preserved.

This is not arithmetic negation of the whole state.
It is only a flip of the \(\mathbb Z_2\) sidedness coordinate.

---

## 4. One-cycle operator

Let

\[
W : S \to S
\]

be the one-cycle operator.

Assume \(W\) has the form

\[
W(x,\varepsilon,h) = (x,-\varepsilon,\phi(h))
\]

for some map

\[
\phi : \mathbb Z_4 \to \mathbb Z_4.
\]

This is the current minimal-form operator.

It says:

- host placement \(x\) is preserved at the level of the minimal machine
- sign flips after one full cycle
- heading class may update by the rule \(\phi\)

No more is assumed at this stage.

---

## 5. Locked core axiom

The locked cycle backbone is encoded by the involutivity axiom:

\[
W^2 = \mathrm{id}_S
\]

That is:

\[
W(W(s)) = s
\]

for all \(s \in S\).

This is the rigorous expression of the project law:

- one cycle flips sign
- two cycles restore identity

Equivalently, for a distinguished start state \(s_0\),

\[
W(s_0) = -s_0
\]
\[
W^2(s_0) = s_0
\]

which corresponds to the earlier notation:

\[
n_{15} = -n_0
\]
\[
n_{30} = n_0
\]

---

## 6. First theorem

### Theorem
If

\[
W(x,\varepsilon,h) = (x,-\varepsilon,\phi(h))
\]

and

\[
W^2 = \mathrm{id}_S,
\]

then

\[
\phi^2 = \mathrm{id}_{\mathbb Z_4}.
\]

### Proof

Compute:

\[
W^2(x,\varepsilon,h)
=
W(x,-\varepsilon,\phi(h))
=
(x,\varepsilon,\phi(\phi(h))).
\]

Since \(W^2 = \mathrm{id}_S\), this must equal

\[
(x,\varepsilon,h)
\]

for all \(x,\varepsilon,h\).

Therefore:

\[
\phi(\phi(h)) = h
\]

for all \(h \in \mathbb Z_4\).

Hence:

\[
\phi^2 = \mathrm{id}_{\mathbb Z_4}.
\]

QED.

---

## 7. Classification problem for heading laws

Because \(\phi\) must be an involution, only certain heading-update laws are possible.

The most relevant involutive candidates on \(\mathbb Z_4\) are the following.

### Type I: identity
\[
\phi(h) = h
\]

Interpretation:
all launch classes remain in their own heading class after one cycle.

### Type II: half-turn swap
\[
\phi(h) = h+2 \pmod 4
\]

Interpretation:
every heading class swaps with its opposite.

### Type III: orthogonal companion exchange
\[
\phi(0)=0,\quad \phi(2)=2,\quad \phi(1)=3,\quad \phi(3)=1
\]

Interpretation:
0 and 2 are fixed,
1 and 3 exchange.

### Type IV: axial exchange
\[
\phi(1)=1,\quad \phi(3)=3,\quad \phi(0)=2,\quad \phi(2)=0
\]

Interpretation:
1 and 3 are fixed,
0 and 2 exchange.

At present, the project does **not** yet prove which of these is realized by the host.
That is an open model-choice question.

---

## 8. Launch rotations

Define a launch-rotation operator

\[
Q : S \to S
\]

by

\[
Q(x,\varepsilon,h) = (x,\varepsilon,h+1 \pmod 4).
\]

Thus:

\[
Q^0 = Q_0,\quad Q^1 = Q_{90},\quad Q^2 = Q_{180},\quad Q^3 = Q_{270},\quad Q^4 = \mathrm{id}.
\]

This is the rigorous way to express rotated relaunch classes.

Note carefully:

- \(Q\) changes the starting heading only
- \(Q\) does **not** reverse the walk word
- \(Q\) does **not** define inverse traversal

So post-G30 relaunches should always be expressed as rotated starting states acted on by the same operator \(W\).

---

## 9. Relaunch covariance problem

The relaunch problem is:

> For which launch rotations \(Q^k\) does the same sign-closing law hold?

Formally, for each \(k \in \{0,1,2,3\}\), test whether:

\[
W(Q^k s) = -Q^k s.
\]

Equivalently, one may ask whether:

\[
W \circ Q^k = Q^k \circ W
\]

holds on the relevant class of states.

This note does not settle that question.
It only frames it rigorously.

---

## 10. Observed admissible count data

The project currently includes the following observed admissible count sets.

### Observed admissible vertex counts
\[
V := \{0,1,2,3,4,9,15\}
\]

### Observed admissible edge counts
\[
E := \{0,1,2,3,5,7,8,16,20\}
\]

These are currently observations, not derived theorems.

This note makes no assumption yet about why these exact values appear.
It only records them as data.

---

## 11. Coupling relation between edge and vertex ladders

At present, there is not enough rigor to define a unique coupling function from edge counts to vertex counts.

So instead of a function, define a candidate **coupling relation**

\[
R \subseteq E \times V.
\]

This is the weakest rigorous object that can record possible cross-ladder correspondences without forcing uniqueness.

Current candidate relations include:

\[
(5,4) \in R
\]

and

\[
(20,9) \in R.
\]

These are currently hypotheses suggested by structural fit, not proven facts.

This note records them only as candidate pairings.

---

## 12. Distinguishing operations and relations

A major source of ambiguity in the broader project has been the reuse of composition language for different kinds of combination.

To make the framework more rigorous, we distinguish:

### Equality
\[
=
\]
literal equality of formal objects

### Structural equivalence / heuristic equivalence
\[
\sim
\]
same intended role or same compressed pattern, not literal equality

### Assembly
\[
\oplus
\]
built from components; not yet assumed to be a direct sum in an algebraic sense

### Cycle doubling
\[
2\cdot G
\]
two traversals of the same cycle-scale object; not multiplication in a graph-theoretic sense

### Coupling
\[
(e,v)\in R
\]
candidate relation between edge-side and vertex-side milestones

These distinctions are mandatory for future rigor.

---

## 13. Compression stack in rigorous status form

The current compression stack can now be rewritten with explicit status labels.

### Primitive or near-primitive labels
\[
G0,\ G1,\ G2,\ G3,\ G4
\]

with current intended roles:

- \(G0\): null anchor
- \(G1\): unit state / center
- \(G2\): sign split / polarity layer
- \(G3\): transport kernel
- \(G4\): quarter-sector frame

These are currently role assignments, not yet formal isomorphism classes.

### Strong structural candidate
\[
G5 := G1 \oplus G4
\]

Meaning:
G5 is assembled from a center plus a quartered frame.

### Plausible structural candidate
\[
G9 \sim G1 \oplus G4 \oplus G4
\]

Meaning:
G9 behaves like the first stabilized local host built from one center plus a frame plus a completed or reflected frame.

### Conjectural factorization
\[
G15 \sim G5 \star G3
\]

where \(\star\) is **not yet defined rigorously**.
It currently means:
“generated from the interaction of the grounded seed with the transport kernel.”

This is currently only a disciplined conjectural shorthand.

### Derived cycle doubling
\[
G30 := 2\cdot G15
\]

Meaning:
G30 is the two-pass restoration scale of G15.

This is not graph multiplication.
It is cycle doubling in the walker law sense.

---

## 14. What is actually derivable at present

The following statements are derivable from the current formal core:

### Derivable
1. The minimal state must include at least:
   - placement label
   - sign
   - heading class

2. The one-cycle operator must flip sign.

3. If the two-pass law holds, then the heading map must be an involution.

4. Relaunch classes can be expressed rigorously as rotated starting states under the same walk operator.

These are genuine formal consequences of the setup.

---

## 15. What is not yet derivable at present

The following are **not yet** derivable from the current formal core:

1. which involution \(\phi\) is realized
2. whether Type III is the correct heading law
3. whether \((5,4)\in R\) is correct
4. whether \((20,9)\in R\) is correct
5. whether \(G9 \sim G1 \oplus G4 \oplus G4\) is exact
6. whether \(G15 \sim G5 \star G3\) can be made rigorous
7. whether G60 is a genuinely new machine layer
8. whether AT4val[60,6] realizes the higher compressed state space

These all remain conjectural or model-dependent.

---

## 16. Best current rigorous boundary

The cleanest boundary currently available is:

### Locked / theorem-level
\[
W(x,\varepsilon,h)=(x,-\varepsilon,\phi(h)),\qquad \phi^2=\mathrm{id},\qquad W^2=\mathrm{id}.
\]

### Observed data
\[
V=\{0,1,2,3,4,9,15\},\qquad E=\{0,1,2,3,5,7,8,16,20\}.
\]

### Candidate coupling data
\[
(5,4)\in R,\qquad (20,9)\in R.
\]

### Open structural conjectures
\[
G5 = G1 \oplus G4
\]
\[
G9 \sim G1 \oplus G4 \oplus G4
\]
\[
G15 \sim G5 \star G3
\]
\[
G30 = 2\cdot G15
\]

with the caveat that only the cycle-doubling interpretation of \(G30\) is currently truly firm.

---

## 17. Immediate next proof target

The next rigorous target should be:

> Determine which involution \(\phi\) is realized by the relaunch structure.

This is the cleanest next theorem-sized problem because it sits directly on top of the locked machine and does not yet require the edge/vertex count bridge.

Once \(\phi\) is fixed, the relaunch-class structure becomes much sharper.

---

## 18. Second next proof target

After \(\phi\), the next rigorous target should be:

> Define a precise criterion for when an edge milestone \(e\) couples to a vertex milestone \(v\).

That would turn the candidate relation \(R\) from a picture-based suggestion into a falsifiable formal object.

---

## 19. Plain-language summary

Plainly said:

We now have a clean minimal machine:

- a walker state has place, side, and heading
- one cycle flips side and updates heading
- two cycles restore the original state
- the heading update must be an involution

Separately, we have observed vertex and edge count ladders, but their bridge is not yet proven.

So the current framework is rigorous at the state-law level and observational at the count-ladder level.

That is the correct present status.

---

## 20. One-line summary

The current rigorous core is the involutive state machine
\[
W(x,\varepsilon,h)=(x,-\varepsilon,\phi(h)),\qquad \phi^2=\mathrm{id},
\]
together with observed admissible count ladders \(V\) and \(E\), and a still-open coupling relation \(R\) between them.

