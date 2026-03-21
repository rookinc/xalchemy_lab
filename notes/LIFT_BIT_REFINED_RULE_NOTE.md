# Lift Bit Refined Rule Note

## Context

The augmented tri-patch transport model introduced a binary lift register

\[
\lambda=\texttt{lift\_bit}\in\mathbb Z_2
\]

to complement the earlier even-mismatch kernel law

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

Earlier intermediate formulations suggested that the lift bit might be triggered by:

- stalled routes, and
- chirality-mixed dyads.

That was close, but the larger-chart probe has now shown it is not precise enough.

This note records the refined rule.

---

## 1. What failed

The broad chirality rule predicted:

\[
\lambda
=
\mathbf 1_{\mathrm{stall}}
\oplus
\mathbf 1_{\mathrm{chirality\text{-}mixed\ dyad}}.
\]

But the larger-chart test found explicit counterexamples:

- `advance_L1`
- `advance_L2`

These both produce middle interactions of type `LR`, but specifically of subtype

- `complement_exchange`

rather than

- `sign_transfer`.

Their actual lift bits are zero, so the broad “mixed dyad” rule over-predicts.

Thus **not every mixed-chirality dyad contributes**.

That is the key refinement.

---

## 2. Refined rule

The rule that still matches the primitive chart is:

\[
\lambda
=
\mathbf 1_{\mathrm{stall}}
\oplus
\mathbf 1_{\mathrm{LR\ sign\text{-}transfer\ dyad}}.
\]

In words:

> the lift bit turns on exactly for  
> (a) a fully stalled middle route, or  
> (b) an `LR` dyad whose middle event is a sign-transfer event.

This is now the best current local rule.

---

## 3. Primitive classification under the refined rule

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

The important distinction is:

- `advance_L1` and `advance_L2` are `LR`, but only as `complement_exchange`
- `advance_L1_R1` and `advance_L2_R1` are `LR`, specifically as `sign_transfer`

So the lift register is sensitive to the **event subtype**, not merely the chirality pattern.

---

## 4. Why this matters

This shows the lift bit is finer than a simple chirality classifier.

It does **not** measure:

- same-chirality versus mixed-chirality alone,
- nor raw route arity alone.

Instead, it detects a specific interaction mechanism inside the mixed-chirality sector.

That makes the lift register more interesting:

- it is not generic,
- it is transport-mechanism sensitive,
- and it may therefore be closer in spirit to a true cocycle signal than a coarse route label would be.

---

## 5. What survives from the earlier picture

Even after this refinement, the broader local binary architecture remains intact.

### Kernel layer
\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

### Lift layer
\[
\lambda
=
\mathbf 1_{\mathrm{stall}}
\oplus
\mathbf 1_{\mathrm{LR\ sign\text{-}transfer\ dyad}}.
\]

### Composition
The lift register still composes additively mod 2 on tested route words.

So the correction is local to the trigger rule, not to the overall architecture.

---

## 6. Best current statement

The current best safe local binary law is:

> **Lift bit = 1 exactly for stalled routes and LR sign-transfer dyads.**

That is stronger and more accurate than the earlier “mixed dyad” version.

---

## 7. What remains open

The natural next question is now sharper:

> Can `LR sign-transfer` be recognized from primitive route structure alone, without referring to the internal face-event label?

That is the next step toward a genuinely geometric formulation.

Right now the rule is stable and correct, but it still depends on one internal event name.
The next probe should try to remove that dependency.

---

## 8. Working summary

The local augmented transport model now has:

- an even-mismatch kernel law
- a cocycle-like binary register
- a refined trigger rule for that register

The refined trigger is:

\[
\boxed{
\lambda
=
\mathbf 1_{\mathrm{stall}}
\oplus
\mathbf 1_{\mathrm{LR\ sign\text{-}transfer\ dyad}}
}
\]

That is the current best local lift law.

