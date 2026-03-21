# First Bridge Match Note

## Context

The tri-patch transport program has now reached the first explicit local/global bridge checkpoint.

On the **local side**, the current augmented local binary law is:

### Kernel law
\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2
\]

### Lift law
\[
\lambda
=
\mathbf 1_{\mathrm{stall}}
\oplus
\mathbf 1_{\mathrm{2\text{-}advancer\ LR\ route}}
\]

where \(\lambda = \texttt{lift\_bit}\) composes additively mod 2 on tested route words.

On the **global side**, a first named family of loop labels and binary values was supplied:

- `global_square = 0`
- `global_twist = 1`
- `global_return = 0`

These are still simple user-supplied bridge labels, not yet machine-derived from the signed-lift artifact layer.
But they are enough for the first explicit bridge table.

---

## 1. The bridge table result

The local/global bridge table compared the following local words to the supplied global loop bits:

- `w_bundled`  ↔  `global_square = 0`
- `w_hold`     ↔  `global_twist = 1`
- `w_LR_1`     ↔  `global_twist = 1`
- `w_LR_2`     ↔  `global_twist = 1`
- `w_LL`       ↔  `global_return = 0`

The outcome was the same on both local polarities `u1R` and `d1R`.

---

## 2. What matched

For every row in the current bridge table:

### local mismatch parity
\[
\texttt{mismatch\_parity}=0
\]

in all cases.

So mismatch parity does **not** distinguish the supplied global odd/even assignments.
It remains a kernel condition only.

### local lift bit
\[
\texttt{lift\_bit}=0
\]
for the bundled and `LL` rows, and

\[
\texttt{lift\_bit}=1
\]
for the hold and `LR` rows.

This matches the supplied global binary assignments exactly in the current table.

So the first explicit bridge match is:

> **lift\_bit tracks the supplied global 0/1 values, while mismatch parity does not.**

---

## 3. Why this matters

This is the first point in the project where the local model does more than merely suggest the right structure.

Before this table:

- mismatch parity had already been identified as a kernel law
- the lift register had already been identified as a cocycle-like binary channel
- but no explicit local/global comparison had yet been written down

Now there is one.

The table does not yet prove a true theorem about the signed-lift cocycle.
But it does establish the first concrete bridge pattern:

\[
\text{kernel channel} \neq \text{global bit candidate}
\]

\[
\text{lift bit} = \text{best current local bridge candidate}
\]

That is a real step.

---

## 4. Local interpretation

The local side now separates clearly into two different binary roles.

### Kernel channel
\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2
\]

This says what local mismatch holonomy is allowed.
It does not produce odd/even classification among the tested bridge rows.

### Lift channel
\[
\lambda=\texttt{lift\_bit}
\]

This is the binary quantity that actually distinguishes the table rows in the same way the supplied global bits do.

So the local model now has:

- a **selection rule** in the mismatch sector
- and a **bridge candidate observable** in the lift sector

That is the right split.

---

## 5. Current bridge reading

The strongest safe statement at this point is:

> In the first explicit local/global comparison table, the local lift bit matches the supplied global loop parity assignments, while local mismatch parity remains identically zero and therefore functions only as the kernel channel.

That is the first bridge match.

This does **not** yet prove that the local lift bit is the signed-lift cocycle.
But it is the first local quantity that behaves the right way in an explicit table.

---

## 6. What this does not prove

Several important cautions remain.

### 1. The global loop labels are still user-supplied placeholders
They are named loops with assigned bits, but not yet extracted directly from signed-lift loop artifacts.

### 2. The pairing is still hand-chosen
The local words and global loop labels were paired intentionally for the first test.
This is enough for a bridge checkpoint, but not for a definitive correspondence.

### 3. The comparison family is still tiny
This is a first table, not a large dataset.

So the bridge is now plausible in a more concrete way, but not yet formal.

---

## 7. Best current statement

### First Bridge Match Claim

In the first explicit local/global comparison table, the local lift register \(\lambda\) reproduces the supplied global binary loop assignments on the tested rows, while the local mismatch-parity channel remains identically zero and therefore acts only as the kernel condition.

This is the best current bridge claim.

---

## 8. What remains next

The next step is obvious:

> replace the named global placeholders with actual loop representatives and actual cocycle values from the signed-lift side.

That is the next real upgrade.

Once that happens, the same bridge table will stop being a toy comparison and become an actual signed-lift/local-transport test.

---

## 9. Working summary

The current local/global state is now:

### Local kernel
\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2
\]

### Local bridge candidate
\[
\lambda=\texttt{lift\_bit}
\]

### First explicit bridge match
\[
\lambda \text{ matches the supplied global bits in the current bridge table}
\]

So the first bridge checkpoint is now in place.

