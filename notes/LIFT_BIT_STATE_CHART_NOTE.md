# Lift Bit State Chart Note

## Context

The augmented tri-patch now supports two distinct binary layers:

1. **Mismatch kernel law**
   \[
   dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2
   \]

2. **Lift register**
   \[
   \texttt{lift\_bit}\in\mathbb Z_2
   \]

The recent table probe makes the split explicit on both primitive route classes and short route words.

---

## 1. Kernel layer

For every primitive class and every tested word of length 2, the holonomy correction still satisfies:

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

So the old parity shadow remains completely intact inside the augmented model.

This means the lift register does **not** replace the mismatch kernel.
It sits on top of it.

---

## 2. Primitive lift-bit classes

The primitive routes split into two lift-bit sectors.

### lift\_bit = 1
- `hold_all`
- `advance_L1_R1`
- `advance_L2_R1`

### lift\_bit = 0
- `advance_L1`
- `advance_L2`
- `advance_R1`
- `advance_L1_L2`
- `advance_L1_L2_R1`

This classification is mirrored between positive and negative rail polarity.

So the register is not tied to a specific sign orientation.

---

## 3. Word-level composition

For all tested words up to length 4, the lift register composes by XOR:

\[
\texttt{lift\_bit}(w_1\cdots w_n)
=
\bigoplus_i \texttt{lift\_bit}(w_i).
\]

So the register behaves cocycle-like on the tested route semigroup.

At the same time, mismatch parity remains even for all such words.

So the augmented local state now has the form:

\[
(\Delta s,\Delta m;\,\lambda)
\]

with

- \((\Delta s,\Delta m)\) in the even-mismatch holonomy sector
- \(\lambda=\texttt{lift\_bit}\in\mathbb Z_2\)

---

## 4. State-chart interpretation

The best current interpretation is:

### additive sector
A constrained holonomy lattice in
\[
\mathbb Z^3_s\oplus\mathbb Z^3_m
\]
subject to the even-total-mismatch rule.

### binary grading
An extra
\[
\mathbb Z_2
\]
channel carried by the lift register.

So the local model now looks like:

\[
\text{even-mismatch holonomy sector}
\quad+\quad
\text{binary lift grading}.
\]

This is the first local transport model in the project that has the right architecture to mimic:

- a kernel condition, and
- an independent cocycle-like bit

at the same time.

---

## 5. What is still unsatisfactory

The present lift-bit rule is still hand-coded in event language:

- toggle on `hold_all`
- toggle on `LR` sign-transfer events

That works empirically, but it is not yet invariant.

So the next task is to rewrite the lift bit in a more structural way.

---

## 6. Current conjecture

### Lift Register State Chart Conjecture

The augmented tri-patch carries a local state chart of the form

\[
(\Delta s,\Delta m;\lambda)
\]

where:

1. \((\Delta s,\Delta m)\) lies in the even-mismatch kernel
2. \(\lambda\in\mathbb Z_2\) is a cocycle-like binary grading
3. the grading composes additively on route words
4. the grading is the local candidate for the odd/even sector missing from the unaugmented transport model

---

## 7. Next question

The next question is:

> Can the lift bit be characterized invariantly from route data alone?

That means replacing the hand-coded toggle rule with a formula in terms of route structure.

That is the next probe.

