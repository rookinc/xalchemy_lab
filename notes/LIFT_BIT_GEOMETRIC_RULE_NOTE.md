# Lift Bit Geometric Rule Note

## Context

The augmented tri-patch transport model now has a stable two-layer binary structure:

1. **Mismatch kernel law**
   \[
   dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2
   \]

2. **Lift bit**
   \[
   \lambda=\texttt{lift\_bit}\in\mathbb Z_2
   \]

The lift bit was first introduced operationally through hand-coded toggles, then shown to compose additively mod 2 on tested route words, and finally rewritten as an invariant primitive-route predicate.

This note freezes that rule.

---

## 1. Earlier event-level formulation

The first successful invariant rule was:

\[
\lambda
=
\mathbf 1_{\mathrm{hold\_all}}
\oplus
\mathbf 1_{\mathrm{LR\ sign\text{-}transfer}}.
\]

That already removed the dependence on hub sign and showed the same law on both positive and negative rails.

But it still referenced a specific middle-event label.

So the next question was:

> Can the lift bit be written directly in route language?

The answer is yes.

---

## 2. Primitive geometric rule

The probe found a fully route-level characterization:

\[
\lambda
=
\mathbf 1_{\mathrm{hold\_all}}
\oplus
\mathbf 1_{\mathrm{two\text{-}advancer\ route\ containing\ }R1}.
\]

Equivalently, on the primitive middle-route classes:

### \(\lambda = 1\)
- `hold_all`
- `advance_L1_R1`
- `advance_L2_R1`

### \(\lambda = 0\)
- `advance_L1`
- `advance_L2`
- `advance_R1`
- `advance_L1_L2`
- `advance_L1_L2_R1`

This rule matches exactly on both positive and negative rail polarity.

So the lift bit is not sign-dependent.
It is determined by primitive route geometry.

---

## 3. Interpretation

The rule says the lift bit turns on in exactly two situations:

### 1. Fully stalled middle route
No carrier advances to the opposite hub.

### 2. Two-advancer route carrying the right branch
A dyadic route advances exactly two carriers, and one of them is `R1`.

So the bit is sensitive to a very specific primitive route topology.

It is not measuring:
- stress magnitude
- mismatch magnitude
- or generic off-rail distortion

Instead, it marks a particular binary subdivision of admissible route types.

That is much more cocycle-like in spirit.

---

## 4. Why this is better than the signed-face rule

The earlier invariant event formula used `LR sign_transfer`.
That is correct, but it depends on the internal event name.

The geometric rule is cleaner because it speaks directly in primitive route data:

- how many carriers advance
- whether `R1` participates
- whether the route is a stall

So it is a better candidate for comparison with larger geometric transport structures.

---

## 5. Compatibility with the kernel law

The geometric lift-bit rule does not disturb the earlier mismatch parity result.

For all tested primitive and composite words:

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

So the local augmented state remains:

\[
(\Delta s,\Delta m;\lambda)
\]

with

- \((\Delta s,\Delta m)\) in the even-mismatch kernel
- \(\lambda\) given by the primitive route predicate above

Thus the kernel/cocycle split survives in the more geometric formulation.

---

## 6. Compatibility with composition

The extended composition probe showed that the lift bit satisfies:

\[
\lambda(w_1\cdots w_n)=\bigoplus_i \lambda(w_i)
\]

for all tested route words up to length 4.

So this geometric primitive rule is not just a classification of one-step routes.
It induces a cocycle-like additive grading on the tested route semigroup.

That is a strong local structural result.

---

## 7. Best current local binary law

The local augmented binary architecture can now be summarized as:

### Kernel layer
\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0\pmod 2.
\]

### Lift layer
\[
\lambda
=
\mathbf 1_{\mathrm{hold\_all}}
\oplus
\mathbf 1_{\mathrm{two\text{-}advancer\ route\ containing\ }R1}.
\]

This is the cleanest current local cocycle candidate.

---

## 8. Current conjecture

### Lift Bit Geometric Rule Conjecture

In the augmented tri-patch, the local binary lift register is determined by primitive route geometry:
it turns on exactly for stalled routes and for two-advancer routes carrying `R1`, and composes additively mod 2 on route words.

This is the current best local route-level candidate for the missing odd/even channel not present in the unaugmented kernel-only model.

---

## 9. What remains open

Three natural questions remain.

### 1. Larger charts
Does the same primitive rule survive when the local chart is enlarged beyond the minimal middle-route family?

### 2. Deeper geometric form
Can the rule be expressed without privileged carrier names, in a more invariant graph-theoretic language?

### 3. Global bridge
Does this local route predicate correspond in any clean way to the global signed-lift cocycle on explicit loop classes?

Those are the next tests.

---

## 10. Working summary

The lift bit now has a real geometric primitive rule:

> **Lift bit = 1 exactly for stalled routes and for two-advancer routes that include `R1`.**

Together with the even-total-mismatch kernel, this gives the augmented local model a clear binary architecture.

That is the current best local state law.

