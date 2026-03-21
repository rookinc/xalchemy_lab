# Local Lift Register Note

## Context

The tri-patch transport program has now reached a useful structural split.

The earlier local model already established:

1. **Bundled rail law**  
   Exact affine transport on the preferred bundled route.

2. **Defect algebra**  
   Stable stress/mismatch defect transport on the bundled rail.

3. **Holonomy lattice**  
   Additive route-class corrections for admissible off-rail middle-route deviations.

4. **Parity shadow**  
   The explicit binary law
   \[
   dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
   \]

That last law showed that the local model realizes a kernel condition.
But it did **not** produce a genuine odd/even binary observable analogous to the global signed-lift cocycle.

So an augmented toy model was introduced with an explicit binary register:

\[
\texttt{lift\_bit} \in \mathbb Z_2.
\]

This note records the outcome.

---

## 1. Why add a lift register?

The local tri-patch model, without augmentation, repeatedly showed:

- raw local route classes stay in the even-mismatch kernel
- differences of local route classes stay in the even-mismatch kernel
- composite local words stay in the even-mismatch kernel
- even stitched local charts stay in the even-mismatch kernel

So the local transport state space was rich enough to discover the **kernel** of a binary law, but not rich enough to generate the odd sector.

That suggested a missing degree of freedom.

The natural candidate was an explicit extra binary state:
a sheet flag, lift bit, or local cocycle register.

---

## 2. Exploratory lift-bit rule

The first augmented toy used a very simple candidate toggle rule.

The lift bit toggles on:

- `hold_all`
- dyadic `LR` sign-transfer events

and does **not** toggle on:

- singleton routes
- `advance_L1_L2`
- bundled triad `advance_L1_L2_R1`

This was explicitly exploratory.
The point was not to claim a final law, but to test whether the local model could sustain two binary layers at once:

1. kernel parity law in mismatch
2. independent binary lift register

It can.

---

## 3. Single-step lift-bit classes

The resulting single-step classification is:

### lift_bit = 1
- `hold_all`
- `advance_L1_R1`
- `advance_L2_R1`

### lift_bit = 0
- `advance_L1`
- `advance_L2`
- `advance_R1`
- `advance_L1_L2`
- `advance_L1_L2_R1`

This classification is mirrored exactly between positive and negative rail polarity.

So the lift bit is not a random artifact of sign choice.

---

## 4. Kernel remains intact

Crucially, the old parity law survives unchanged.

For every tested route and tested route word,

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

So introducing the lift bit does **not** break the earlier kernel structure.

This is exactly what we wanted.

The augmented model now carries:

- a binary selection rule in mismatch,
- and a second binary observable in the lift register.

---

## 5. Composition law

The next question was whether the lift bit behaves like a cocycle or merely like a local tag.

The composition probes showed:

### Word length 2
\[
\texttt{lift\_bit}(w_1w_2)
=
\texttt{lift\_bit}(w_1)+\texttt{lift\_bit}(w_2)\pmod 2.
\]

### Extended test
The same additivity held for all tested words of lengths:

- 1
- 2
- 3
- 4

on both positive and negative rails.

So the current augmented toy satisfies a genuine additive law on the tested route semigroup.

That is the first local binary observable in the transport model that behaves cocycle-like.

---

## 6. Two-layer interpretation

The local augmented model now has a very clear architecture.

### Layer 1: mismatch kernel
\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

This is a selection rule.
It says which mismatch parity sectors are allowed.

### Layer 2: lift register
\[
\texttt{lift\_bit}(w_1\cdots w_n)
=
\bigoplus_i \texttt{lift\_bit}(w_i).
\]

This is an additive binary observable on route words.

So the transport model now separates:

- **kernel condition**
from
- **binary cocycle-like channel**

inside one local toy.

---

## 7. Why this matters

This is the first time the local transport side has the right logical shape to mirror the global signed-lift story.

Previously, the local model only knew the even sector.
Now it contains:

- a built-in even-kernel law,
- plus a separate binary register that can actually carry odd/even information.

That does **not** prove identification with the global cocycle.
But it does mean the local side is now structurally capable of supporting such a bridge.

That is a real advance.

---

## 8. Best current statement

The strongest safe statement at this point is:

> The tri-patch augmented with a lift register supports a local binary observable that behaves additively mod 2 on the tested route semigroup, while the original even-mismatch law remains as a kernel condition.

This is the right replacement for the older “kernel not cocycle” picture.

A better phrasing now is:

> the unaugmented local model realizes the kernel, and the augmented local model supplies a candidate cocycle channel.

---

## 9. Current conjecture

### Local Lift Register Conjecture

There exists a lift-aware augmentation of the tri-patch transport model in which:

1. total mismatch parity remains even as a kernel law
2. an independent binary lift register composes additively mod 2 on route words
3. this lift register is the correct local transport-side candidate for the odd/even sector of the global signed-lift cocycle

That is the current best bridge conjecture.

---

## 10. What remains open

The current lift register is still exploratory.
Several things remain to be settled.

### 1. Rule uniqueness
Is the chosen toggle rule the right one, or only one among several that fit the current data?

### 2. Geometric meaning
Can the toggling events be described in more invariant language than “hold_all” and “LR sign transfer”?

### 3. Relation to global cocycle
Does this local lift register actually match the signed-lift cocycle on corresponding loop classes?

### 4. Minimal augmentation
Is one binary bit enough, or will a more faithful local lift state need additional structure?

These are the next real questions.

---

## 11. Working summary

The local transport picture now looks like:

### Bundled rail
Exact affine transport.

### Holonomy layer
Additive route-class correction lattice.

### Kernel law
\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

### Lift register
A cocycle-like binary channel additive on tested route words.

So the current best description is:

> **The augmented tri-patch supports a kernel/cocycle split.**

That is the new local architecture.

