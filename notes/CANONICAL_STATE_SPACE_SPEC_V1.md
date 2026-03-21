# Canonical State Space Spec v1

## Status

This document defines the current canonical **local** state-space specification for the realized G60 lens.

It is a local spec, not yet a global theorem about all of `G60`.

It records the structure that is already established by:

- the realized local state cube,
- the validated Toy G60 Automaton v2,
- the trace receipt law,
- the quotient bridge signature,
- and the unfolded state-sheet visualization.

---

## 1. Canonical state register

The canonical local state is the 3-bit register

\[
S = (A,\sigma,\tau)\in \mathbb Z_2^3.
\]

### Intended meanings

- `A` = anchored chart selector
- `sigma` = `E1`-sheet activation
- `tau` = odd-branch activation

These are not treated as three symmetric abstract bits.

The bit `A` has a distinguished structural role because it selects the anchored chart.

---

## 2. Realized local state set

The current realized local state set is the full 3-bit cube:

- `000`
- `001`
- `010`
- `011`
- `100`
- `101`
- `110`
- `111`

So at the current local level, the realized state space is

\[
\mathcal S_{\mathrm{realized}} = \mathbb Z_2^3.
\]

---

## 3. Chart split

The state space splits into two anchored charts:

### Chart A = 0
States:
- `000`
- `001`
- `010`
- `011`

Interpretation:
- odd/E1 control chart

### Chart A = 1
States:
- `100`
- `101`
- `110`
- `111`

Interpretation:
- E2-dominant anchored chart

This chart split is canonical in the current local law.

---

## 4. Canonical readout ladder

Each state has a canonical readout ladder

\[
S
\to
\text{trace receipts}
\to
(R,Q,W).
\]

So the state is not read directly only through the quotient bridge signature.

The canonical readout proceeds in stages:

1. state register,
2. trace receipt law,
3. quotient bridge signature.

---

## 5. Anchored receipt law

The anchored readout is chart-dependent.

### A = 0 chart

For `A=0`, the anchored traces obey:

- `AOOO = tau`
- `AE1E1E1 = sigma`
- `AE2E2E2 = 0`

Mixed anchored traces:
- `E1E1E1O = 1` exactly when `sigma = tau`
- `E1E1E1E2 = sigma`

So `A=0` is the odd/E1 anchored chart.

### A = 1 chart

For `A=1`, the anchored traces obey:

- `AE2E2E2 = 1`
- `AE1E1E1 = 1` except at `(sigma,tau)=(1,0)`
- `AOOO = 1` except at `(sigma,tau)=(0,1)`

Mixed anchored traces:
- `E1E1E1O = 1` exactly when `sigma = tau`
- `E1E1E1E2 = sigma`

So `A=1` is the E2-dominant anchored chart.

---

## 6. Rigid distal backbone

Across the full realized local cube, the following traces remain odd:

- `DE1E1E2`
- `DE1E1M+`
- `DE1E2E2`
- `E2E2E2E2`

Across the full realized local cube, the following traces remain even:

- `DE1OM+`
- `E1E1M+M+`
- `E1E2E2E2`
- `E1E2M+M+`
- `E1M+M+O`
- `E2E2E2O`

So the distal backbone is rigid in the current local state-space spec.

---

## 7. Quotient bridge signature

The quotient bridge signature is

\[
(R,Q,W)=(0,\;A+\sigma,\;A+\tau).
\]

This quotient is canonical but not complete.

It forgets:
- trace-catalog distinctions,
- anchored chart distinctions,
- and some local receipt structure.

So the bridge signature is part of the canonical readout ladder, but not the whole state law.

---

## 8. Canonical visual receipt model

Each state admits a canonical unfolded 2D receipt-sheet projection.

This projection is encoded as a black/white triangular face-sheet system.

### Intended interpretation

- black = active / odd / occupied receipt
- white = inactive / even / unoccupied receipt

The face channels are currently interpreted as:

- `H/O` = anchor / odd face
- `E1` = E1 face
- `E2` = E2 face
- `Do` = distal odd face
- `De` = distal even face
- `C` = cancellation / seam face

This does not replace the trace law.
It provides a visual canonical projection of it.

---

## 9. Canonical validation statement

The current canonical local state-space spec is validated by Toy G60 Automaton v2 on the full realized local cube.

Validation result:
- total checks = 120
- mismatches = 0
- matches = 120

So the current canonical local state-space spec is fully consistent with the realized cube and its validated toy automaton.

---

## 10. Strongest current sentence

The canonical local state space is the full 3-bit register `(A,sigma,tau)`, split into two anchored charts, equipped with a chart-dependent anchored receipt law, a rigid distal backbone, a quotient bridge signature, and a canonical black/white triangular receipt-sheet projection.

---

## 11. Scope limit

This is a local canonical state-space spec.

It does **not** yet prove:

- a global `G60` derivation,
- a unique geometric origin of the chart split,
- or a global gluing law across all chamber packets.

Those remain next-stage questions.

