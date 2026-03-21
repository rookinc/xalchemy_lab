# Cluster-Invariant Ansatz

## Goal

Replace the current edge-by-edge bridge description with a smaller set of coarse invariants.

The current local bridge data suggests that the signature is not controlled by all nearby edges individually, but by:

- one rigid anchor edge
- one twist-support cluster
- one square-support cluster

So the next algebraic move is to compress the local bridge into cluster variables.

---

## Definitions

Let the current mod-2 lift state be
\[
\varepsilon : E \to \mathbb Z_2.
\]

Define the three coarse variables:

### 1. Anchor variable
\[
A := \varepsilon(e00).
\]

### 2. Twist-cluster variable
Let
\[
T := \{e01,e04,e07\}.
\]

Define
\[
\tau := \varepsilon(e01)+\varepsilon(e04)+\varepsilon(e07)\pmod 2.
\]

### 3. Square-cluster variable
Let
\[
S := \{e02,e05,e10\}.
\]

Define
\[
\sigma := \varepsilon(e02)+\varepsilon(e05)+\varepsilon(e10)\pmod 2.
\]

---

## Immediate bridge formulas

For the current chosen representatives:

### Return-type
The return representative uses only the anchor edge twice, so
\[
R = A + A = 0 \pmod 2.
\]

So return parity is automatically even in this mod-2 reading.

### Twist-type
The chosen odd twist representative uses the twist cluster:
\[
W = \varepsilon(e00)+\varepsilon(e04)+\varepsilon(e07)+\varepsilon(e01).
\]

Hence
\[
W = A + \tau.
\]

### Square-type
The chosen even square representative uses the square cluster:
\[
Q = \varepsilon(e00)+\varepsilon(e05)+\varepsilon(e10)+\varepsilon(e02).
\]

Hence
\[
Q = A + \sigma.
\]

So the bridge signature is compressed to:
\[
(R,Q,W) = (0,\;A+\sigma,\;A+\tau).
\]

---

## Baseline seeded checkpoint

In the current seeded local model:

- \(A = \varepsilon(e00)=0\)
- \(\tau = \varepsilon(e01)+\varepsilon(e04)+\varepsilon(e07)=1+0+0=1\)
- \(\sigma = \varepsilon(e02)+\varepsilon(e05)+\varepsilon(e10)=1+1+0=0\)

So:
\[
(R,Q,W)=(0,\;0+0,\;0+1)=(0,0,1).
\]

This matches the observed class-based bridge signature.

---

## Interpretation

The current bridge does not need to be read primarily as a statement about seven individual edges.

It can be read as a statement about three coarse invariants:

- anchor state \(A\)
- square-cluster state \(\sigma\)
- twist-cluster state \(\tau\)

with
\[
Q=A+\sigma,\qquad W=A+\tau.
\]

Thus the active square/twist distinction is controlled by the relative mod-2 states of the two clusters against the anchor.

---

## Robustness reading

This ansatz explains several observed facts.

### 1. Why return stays even
Because \(R=A+A=0\) identically mod 2.

### 2. Why flipping a whole cluster can destroy its class
Because the full cluster parity changes:
- flipping the whole twist cluster changes \(\tau\)
- flipping the whole square cluster changes \(\sigma\)

### 3. Why some double flips compensate
Because double flips inside a 3-edge cluster can leave the cluster parity unchanged mod 2.

So the theorem can survive even when individual edges change, provided the effective coarse variable is preserved.

### 4. Why some boundary flips do not matter
Because they alter local 4-cycle counts without changing \(A,\tau,\sigma\) in the representative formulas.

---

## Ansatz

The current local class-based bridge is governed, to first approximation, by the triple
\[
(A,\sigma,\tau)\in \mathbb Z_2^3,
\]
with bridge signature
\[
(R,Q,W)=(0,\;A+\sigma,\;A+\tau).
\]

At the present checkpoint, the observed seeded state is
\[
(A,\sigma,\tau)=(0,0,1).
\]

---

## Next test

The next mathematical task is to check whether all theorem-preserving perturbations are exactly those that preserve the induced values of:

- \(A\)
- \(A+\sigma\)
- \(A+\tau\)

If so, the bridge has been reduced from an edge-level description to a small invariant-level description.

