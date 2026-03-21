# Lift Bit Invariant Rule Note

## Context

The augmented tri-patch transport model now carries two binary layers:

1. **Mismatch kernel law**
   \[
   dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2
   \]

2. **Lift register**
   \[
   \lambda = \texttt{lift\_bit}\in\mathbb Z_2
   \]

The earlier lift-bit implementation used an exploratory toggle rule expressed operationally:

- toggle on `hold_all`
- toggle on dyadic `LR` sign-transfer events

That rule worked empirically and composed additively on tested route words, but it still needed a more invariant statement.

The invariant probe has now supplied that.

---

## 1. Main result

The probe found a simple feature-level law that reproduces the lift bit on both positive and negative rail polarity:

\[
\lambda
=
\mathbf{1}_{\mathrm{hold\_all}}
\oplus
\mathbf{1}_{\mathrm{LR\ sign\text{-}transfer}}.
\]

In words:

> the lift bit is on exactly when the middle route is either  
> (a) a fully stalled triadic hold, or  
> (b) a dyadic `LR` sign-transfer event.

This is the current best invariant rule.

---

## 2. Why this is better than the original toggle description

The earlier rule was procedural:

- inspect the middle event
- toggle on certain cases

The new rule is structural:

- it is a direct binary predicate on route/event type
- it is independent of hub sign
- it uses the same formula on `u1R` and `d1R`

So the register now has a real local classification law rather than a pile of casework.

---

## 3. Explicit classes

The primitive routes now organize cleanly.

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

This matches the invariant rule exactly:

- `hold_all` contributes the first term
- the `LR` sign-transfer routes contribute the second term
- all other primitives contribute neither

---

## 4. Composition law remains true

The extended composition probe showed that for words up to length 4,

\[
\lambda(w_1\cdots w_n)=\bigoplus_i \lambda(w_i).
\]

So the lift register is not just a static route label.
It behaves additively mod 2 on the tested route semigroup.

That is the local cocycle-like feature we were looking for.

---

## 5. Kernel/cocycle split

With the invariant rule in hand, the local model now has a clean two-layer architecture:

### Kernel layer
\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2
\]

### Cocycle-like layer
\[
\lambda
=
\mathbf{1}_{\mathrm{hold\_all}}
\oplus
\mathbf{1}_{\mathrm{LR\ sign\text{-}transfer}}.
\]

So the current local augmented state is naturally written as

\[
(\Delta s,\Delta m;\lambda).
\]

The first part lives in the even-mismatch holonomy sector.
The second part is a binary grading on route words.

---

## 6. Interpretation

This suggests the following provisional picture.

### `hold_all`
A fully stalled middle transport configuration contributes one unit of lift parity.

### `LR` sign-transfer
A chirality-mixed dyadic exchange also contributes one unit of lift parity.

### Everything else
No lift parity contribution.

This is intriguing because it says the bit is not attached to “amount of distortion.”
It is attached to specific **route topology / interaction type**.

That is closer in spirit to a cocycle than to a scalar defect count.

---

## 7. Best current conjecture

### Lift Bit Invariant Rule Conjecture

In the augmented tri-patch local transport model, the lift register is given by

\[
\lambda
=
\mathbf{1}_{\mathrm{hold\_all}}
\oplus
\mathbf{1}_{\mathrm{LR\ sign\text{-}transfer}},
\]

and composes additively mod 2 on route words.

This makes \(\lambda\) the current best local candidate for the binary channel missing from the unaugmented kernel-only model.

---

## 8. What remains open

This rule is compact, but it may still not be maximally geometric.

Two natural improvements remain:

### 1. Collapse to a single predicate
Can
\[
\mathbf{1}_{\mathrm{hold\_all}}
\oplus
\mathbf{1}_{\mathrm{LR\ sign\text{-}transfer}}
\]
be rewritten as one more conceptual geometric condition?

For example:
- “middle route has nontrivial lift-sensitive obstruction”
- or “middle route is not fully bundle-compatible in the lift sense”

### 2. Compare to global cocycle language
Can this local predicate be matched to a recognizable property on the signed-lift side?

That is the next bridge question.

---

## 9. Working summary

The augmented local model now has:

- an even-mismatch kernel law
- a cocycle-like binary register
- an invariant feature formula for that register

So the current best local binary law is:

\[
\boxed{
\lambda
=
\mathbf{1}_{\mathrm{hold\_all}}
\oplus
\mathbf{1}_{\mathrm{LR\ sign\text{-}transfer}}
}
\]

That is the cleanest current local cocycle candidate.

