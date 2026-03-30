# G30 Type III Working Model

## Status
Current working relaunch model
Revisable if later evidence forces a return to the full involution comparison

## Purpose

This note promotes Type III from a merely possible involution on launch classes to the current working model for the G30 relaunch machine.

This is a modeling decision, not a theorem.
It is chosen because it is the first nontrivial relaunch law that:

- preserves the locked G15/G30 machine
- keeps 0° and 180° stable
- makes 90° and 270° into a meaningful companion pair

This note records the consequences of that decision.

---

## 1. Locked first-order machine

The first-order walker machine remains:

\[
W(x,\varepsilon,h) = (x,-\varepsilon,\phi(h))
\]

with

\[
W^2 = \mathrm{id}.
\]

This encodes:

\[
n_{15} = -n_0
\]
\[
n_{30} = n_0.
\]

Nothing in this note changes that backbone.

---

## 2. Type III heading law

The current working heading involution is:

\[
\phi(0)=0,\qquad \phi(2)=2,\qquad \phi(1)=3,\qquad \phi(3)=1.
\]

So:

- heading class 0 is fixed
- heading class 2 is fixed
- heading classes 1 and 3 are exchanged

This is the working relaunch law.

---

## 3. Relaunch classes

For a restored state \(n\), define:

\[
\mathcal R(n)=\{Q_0 n,\ Q_{90} n,\ Q_{180} n,\ Q_{270} n\}.
\]

Under Type III, this relaunch space splits as:

\[
\mathcal R(n)=\{Q_0 n,\ Q_{180} n\}\ \sqcup\ \{Q_{90} n,\ Q_{270} n\}.
\]

The two subsets play different roles.

---

## 4. Axial sector

The axial relaunch classes are:

\[
Q_0 n,\qquad Q_{180} n.
\]

These are fixed by the heading involution.

So one G15 cycle sends:

\[
W(Q_0 n)=-(Q_0 n)
\]
\[
W(Q_{180} n)=-(Q_{180} n).
\]

Thus the axial relaunches remain in their own class under one-cycle action.

---

## 5. Orthogonal companion sector

The orthogonal relaunch classes are:

\[
Q_{90} n,\qquad Q_{270} n.
\]

These are exchanged by the heading involution.

So one G15 cycle sends:

\[
W(Q_{90} n)=-(Q_{270} n)
\]
\[
W(Q_{270} n)=-(Q_{90} n).
\]

Thus the orthogonal relaunches form a companion pair.

---

## 6. Two-cycle restoration

Because \(\phi^2=\mathrm{id}\), two cycles restore every relaunch class:

\[
W^2(Q_k n)=Q_k n
\]

for all \(k\in\{0,1,2,3\}\).

So:

- one cycle flips sign and possibly exchanges launch class
- two cycles restore both sign and launch class

This is the second-order version of G30 restoration.

---

## 7. Launch graph

The induced launch graph under Type III is:

- fixed axial node \(Q_0\)
- fixed axial node \(Q_{180}\)
- exchange edge \(Q_{90}\leftrightarrow Q_{270}\)

So the G30 relaunch machine is not uniform.
It contains:

- a stable axial pair
- a nontrivial orthogonal companion pair

This is the first explicit internal geometry of the restored hinge.

---

## 8. Meaning of the step up

Under Type III, G30 is no longer merely the statement “the walker comes back.”

It is the statement that the restored walker carries an internal launch structure:

- two fixed axial restart modes
- one orthogonal companion exchange mode

So the machine has stepped up from first-order walker transformation to second-order restored relaunch geometry.

---

## 9. Current boundary

### Locked
- first-order sign-closing / identity-restoring machine

### Working model
- Type III relaunch involution

### Still open
- whether Type III is ultimately correct
- how this couples to the edge/vertex ladders
- whether the orthogonal companion pair connects to the larger G60 story

This note keeps those boundaries explicit.

---

## 10. One-line summary

Under the current Type III working model, G30 carries a relaunch-space geometry with fixed axial classes and an exchanged orthogonal companion pair.

