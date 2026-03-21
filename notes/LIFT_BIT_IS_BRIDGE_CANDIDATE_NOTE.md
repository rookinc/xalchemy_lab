# Lift Bit Is the Bridge Candidate Note

## Corrected checkpoint

The project now cleanly separates two local binary structures.

### 1. Kernel channel
The mismatch sector satisfies

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

This is a selection rule only.
It enforces the even sector and does not distinguish the tested bridge rows.
So it should no longer be treated as the primary candidate for the global \(\mathbb Z_2\) cocycle value.

### 2. Bridge candidate channel
The lift register

\[
\lambda = \texttt{lift\_bit}
\]

is currently given by

\[
\lambda
=
\mathbf 1_{\mathrm{hold\_all}}
\oplus
\mathbf 1_{\mathrm{LR\ sign\text{-}transfer}}.
\]

This quantity composes additively mod 2 on tested route words and is the first local binary quantity that matches the supplied global odd/even assignments in the explicit bridge table.

---

## First bridge checkpoint

The first bridge table showed:

- `w_bundled`  -> `lift_bit = 0`
- `w_hold`     -> `lift_bit = 1`
- `w_LR_1`     -> `lift_bit = 1`
- `w_LR_2`     -> `lift_bit = 1`
- `w_LL`       -> `lift_bit = 0`

while mismatch parity stayed identically zero on all rows.

So the current best bridge reading is:

> mismatch parity is the kernel condition,
> while lift_bit is the current local bridge candidate for the global binary loop invariant.

---

## Correct next test

The next real upgrade is not to search more on the current local mismatch channel.

It is to replace the placeholder global labels with actual signed-lift loop representatives and compare:

\[
\texttt{lift\_bit}(w)
\quad\text{vs}\quad
\omega(\gamma_w)
\]

for the matched local/global rows.

That is the smallest real next step.

---

## Working summary

The bridge target has now moved.

Old candidate:
- mismatch parity

Current best candidate:
- lift_bit

So the next phase should test whether local lift_bit reproduces actual signed-lift loop parity on explicit loop representatives.
