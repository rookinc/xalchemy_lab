# Formal Objects for the G900 Witness-Machine Obstruction Program

## Status
Working draft

## Purpose
Fix the formal objects used in the bounded-regime frame-2 obstruction analysis, separating definitions from conjectures and computational observations.

---

## 1. Normalized state space

Let \(X\) denote the normalized witness-state space under the normalization convention fixed elsewhere in this project.

Each state \(c \in X\) is represented as a normalized 6-slot word
\[
c = (x_0,x_1,x_2,x_3,x_4,x_5),
\]
where each slot value \(x_j\) lies in the installed witness alphabet allowed by the machine grammar.

We write
\[
\pi_j : X \to \mathcal{A}
\]
for the projection onto slot \(j\), so that
\[
\pi_j(c) = x_j.
\]

The distinguished projection in the present analysis is
\[
\pi_4 : X \to \mathcal{A},
\]
the slot-4 projection.

---

## 2. One-edit move grammar

Let
\[
\to \;\subseteq X \times X
\]
denote the normalized one-edit transition relation induced by the witness-machine move grammar.

Thus \(c \to c'\) means that \(c'\) is obtained from \(c\) by one legal edit, followed by normalization.

We regard \((X,\to)\) as the directed one-edit state graph.

---

## 3. Action distance

Let
\[
d_A : X \times X \to \mathbb{Z}_{\ge 0}
\]
denote the normalized action distance.

For a subset \(Y \subseteq X\), define
\[
d_A(c,Y) := \min_{y \in Y} d_A(c,y).
\]

This induces the action-distance shells around any designated comparison set.

---

## 4. Exact frame-2 set

Let
\[
F_2^{\mathrm{exact}} \subseteq X
\]
denote the exact frame-2 set.

This is the set of normalized states that satisfy the exact frame-2 installation condition.

The present program uses the already established slot-4 necessity principle:

### Frame-2 exactness necessity
If
\[
c \in F_2^{\mathrm{exact}},
\]
then
\[
\pi_4(c) = t2.
\]

At minimum, this is taken as a necessary condition for exact frame-2 closure in the normalized setting used here.

---

## 5. Frame-2 seam

Define the frame-2 seam
\[
\Sigma_2 := \{ c \in X : d_A(c,F_2^{\mathrm{exact}})=1 \}.
\]

Thus \(\Sigma_2\) is the normalized near-action seam around the exact frame-2 set.

The current obstruction program focuses on the distinguished residual portion of this seam reached after exact-preference repair of the dominant chamber.

---

## 6. Locked witness subset

Let
\[
L \subset \Sigma_2
\]
denote the distinguished locked witness subset consisting of the four normalized states

\[
(o4,s0,t0,s2,t4,s4),
\]
\[
(o4,s0,t0,s2,o4,s4),
\]
\[
(o4,s0,t0,s2,s3,s4),
\]
\[
(o4,s0,t0,s2,s0,s4).
\]

These are characterized by the following properties:

1. each lies at frame-2 action distance one from exact closure,
2. in each case the residual mismatch is localized at slot 4,
3. none has an exact one-edit child.

These states serve as the seed set for the bounded escape-return regime.

---

## 7. Bounded escape-return regime

Define the bounded regime
\[
B \subseteq X
\]
to be the smallest subset satisfying:

1. \(L \subseteq B\),
2. whenever \(c \in B\) and \(c \to c'\) is a legal one-edit move with
   \[
   d_A(c',F_2^{\mathrm{exact}}) \le 3,
   \]
   then \(c' \in B\).

Equivalently, \(B\) is the forward closure of the locked witness set \(L\) under legal one-edit moves subject to the action-distance cutoff \(d_A \le 3\).

This is the bounded escape-return regime studied computationally.

---

## 8. Slot-4 image sets

For any subset \(Y \subseteq X\), define its slot-4 image by
\[
\pi_4(Y) := \{ \pi_4(c) : c \in Y \}.
\]

Two slot-4 image sets are especially relevant:

1. the global bounded slot-4 image
   \[
   \pi_4(B),
   \]
2. the seam slot-4 image
   \[
   \pi_4(B \cap \Sigma_2).
   \]

The theorem program seeks to explain these sets structurally rather than merely report them computationally.

---

## 9. Projected slot-4 transport relation

A central proof-program object is the projected slot-4 transport relation
\[
\rightsquigarrow_4 \;\subseteq \mathcal{A} \times \mathcal{A},
\]
defined by
\[
a \rightsquigarrow_4 b
\]
if and only if there exist states \(c,c' \in B\) such that

- \(c \to c'\),
- \(\pi_4(c)=a\),
- \(\pi_4(c')=b\).

The guiding idea is that a proof of slot-4 exclusion should proceed by showing that the reachable slot-4 alphabet is closed under this projected transport relation and does not contain \(t2\).

---

## 10. Defect-localization viewpoint

The current working interpretation is that, after exact-preference repair of the dominant chamber, the remaining obstruction localizes to a single unsatisfied installation condition at slot 4.

Under this interpretation:

- the residual basin funnels into \(\Sigma_2\),
- the slot-4 mismatch is the visible defect coordinate,
- bounded one-edits transport the defect without annihilating it.

This interpretation is not yet adopted as a theorem, but it provides the conceptual frame for the proof program.

---

## 11. Separation of status levels

The present paper lane distinguishes three status levels.

### Definitions
The objects \(X\), \(\to\), \(d_A\), \(F_2^{\mathrm{exact}}\), \(\Sigma_2\), \(L\), \(B\), and \(\pi_4\).

### Computationally established facts
Statements verified in the saturated bounded regime.

### Structural conjectures
Claims intended for proof from the move grammar, normalization law, orbit structure, or invariant theory.

This separation is essential for keeping the obstruction argument mathematically clean.

---

## 12. Immediate target statement

The main theorem-shaped target is the bounded slot-4 exclusion law:

### Target statement
For all \(c \in B\),
\[
\pi_4(c) \neq t2.
\]

Together with frame-2 exactness necessity, this yields the bounded no-closure corollary:
for all \(c \in B\),
\[
c \notin F_2^{\mathrm{exact}}.
\]

The remainder of the paper program is aimed at proving this exclusion law structurally.
