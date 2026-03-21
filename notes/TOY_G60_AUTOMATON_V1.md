# Toy G60 Automaton v1

## Purpose

This is the first explicit upstairs toy mechanism proposed to satisfy the current local `G60` interface.

It is not a proof and not yet a theorem.
It is a minimal candidate mechanism whose job is to descend to the local normal form already established.

---

## Components

The toy automaton has five local upstairs components:

- `H`  = anchor packet
- `O`  = odd exchange branch
- `E1` = continuation sheet 1
- `E2` = continuation sheet 2
- `K`  = rigid distal skeleton

Symbolically:

\[
\mathcal A_{60}^{(1)} = (H,\;O,\;E1,\;E2,\;K).
\]

---

## Roles

### 1. Anchor packet `H`
`H` is the only flexible local control center.

It is the upstairs source of the anchored control surface.

### 2. Odd exchange branch `O`
`O` carries the anchor-side odd exchange mode.

Its local descent is responsible for the anchored odd generator and the odd-side mixed traces.

### 3. Continuation sheets `E1`, `E2`
`E1` and `E2` are sibling continuation sheets.

They represent the two anchored even arms and their downstream continuation structure.

### 4. Rigid distal skeleton `K`
`K` carries the parity-stable distal transport structure.

Its local descent is responsible for the rigid odd backbone and rigid even backbone.

---

## Control register

The toy automaton is driven by three local controls:

\[
(A,\sigma,\tau)\in\mathbb Z_2^3.
\]

These are not defined upstairs as mere labels.
They act as local control operations on the couplings of the automaton.

---

## Primitive control actions

### Action 1. `tau` — anchor/odd coupling
`tau` toggles the coupling of the anchor packet `H` to the odd branch `O`.

Interpretation:
- `tau = 1` means anchor-side odd exchange is armed
- `tau = 0` means anchor-side odd exchange is disarmed

This is the proposed upstairs source of the local effect:
- `(A,O,O,O)` odd when armed
- `(A,O,O,O)` even when disarmed

---

### Action 2. `sigma` — anchor/E1 coupling
`sigma` toggles the coupling of the anchor packet `H` to continuation sheet `E1`.

Interpretation:
- `sigma = 1` activates the anchored `E1` sheet
- `sigma = 0` leaves the anchored `E1` sheet unactivated

This is the proposed upstairs source of the local effect:
- `(A,E1,E1,E1)` odd when activated
- `(E1,E1,E1,E2)` odd when activated

---

### Action 3. `A` — anchored sheet swap + odd rearm
`A` acts at the anchor as a polarity swap between `E1` and `E2`, together with odd rearming.

Interpretation:
- `A = 0` leaves the anchor in its baseline sheet orientation
- `A = 1` swaps the anchored parity role of `E1` and `E2` and simultaneously rearms the anchor odd mode

This is the proposed upstairs source of the local effect:
- anchored `E1` oddness can switch off
- anchored `E2` oddness can switch on
- `(A,O,O,O)` can rearm

---

## Descent rules

The toy automaton descends by the following local receipts.

### Rule D1. Anchored control surface
The flexible local trace classes are determined by the control actions on `H`:

- `(A,O,O,O)` depends on `H <-> O`
- `(A,E1,E1,E1)` depends on `H <-> E1`
- `(A,E2,E2,E2)` depends on anchored sheet polarity
- `(E1,E1,E1,O)` records oddness transfer when odd anchor exchange is disarmed
- `(E1,E1,E1,E2)` records `E1` activation into mixed continuation closure

So the anchored control surface is the descent of the control behavior of `H`.

### Rule D2. Distal skeleton rigidity
All distal backbone classes descend from `K` and are parity-stable under nearby control actions.

So the controls \((A,\sigma,\tau)\) act on `H`, not directly on `K`.

This is the proposed upstairs source of the rigid local backbone.

### Rule D3. Mixed cancellation
The trace
- `(D,E1,O,M+)`

is even because the odd-branch contribution and the distal-defect contribution cancel in one mixed closure pattern.

In the toy automaton this is represented as a destructive interference rule between:
- one branch-induced odd tendency from `O`
- one distal odd tendency from `K`

This is the proposed upstairs source of the local mixed cancellation law.

### Rule D4. Bridge quotient
The fine local descent first produces the trace catalog.
That catalog is then compressed to the invariant receipt
\[
(A,\sigma,\tau),
\]
which is then compressed again to the bridge signature
\[
(R,Q,W)=(0,\;A+\sigma,\;A+\tau).
\]

So the bridge signature is not read directly from the automaton.
It is the final quotient receipt.

---

## Expected local behavior

The toy automaton is intended to reproduce the following already observed local controls.

### Baseline `(0,0,1)`
- odd anchor branch active
- no anchored `E1` activation
- no anchored `E2` activation
- rigid distal backbone unchanged

### `(0,0,0)`
- anchor odd branch disarmed
- oddness transferred into downstream mixed `E1/O` trace
- rigid distal backbone unchanged

### `(0,1,1)`
- odd anchor branch active
- anchored `E1` activated
- rigid distal backbone unchanged

### `(0,1,0)`
- odd anchor branch disarmed
- anchored `E1` activated
- rigid distal backbone unchanged

### `(1,1,0)`
- anchored sheet polarity swapped
- anchored `E2` activated
- anchor odd branch rearmed
- same bridge signature as baseline, but different anchored trace catalog

---

## Interface test targets

This toy automaton should be judged against the current checklist.

### Positive targets
It should reproduce:
- anchored control surface
- rigid odd backbone
- rigid even backbone
- mixed cancellation class
- bridge-signature degeneracy of `(0,0,1)` and `(1,1,0)`

### No-go avoidance
It must not produce:
- control-sensitive rigid distal backbone
- simultaneous parity swap of both anchored even sheets under one primitive control
- violation of the mixed cancellation class
- anchor odd rearming without anchored control-surface change

---

## Strongest current interpretation

This toy automaton proposes that the local law is generated by:

- controls acting only at the anchor packet `H`,
- branch/sheet structure carried by `O`, `E1`, `E2`,
- and parity-stable distal transport carried by `K`.

So the local normal form is read as the descent of a controlled anchor packet over a rigid transport skeleton.

---

## Status

This is the first explicit upstairs candidate mechanism.

It is not yet verified.
Its function is to provide the smallest concrete object that can now be tested against the full local interface and no-go filter.

