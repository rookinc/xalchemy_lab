# G900 Shell Scale Decision
## First honest definition of \(S_k\) and \(C_k\) for the opening experiment

Date: 2026-03-29

---

## Purpose

This note fixes the first usable definitions of the shell-local and bulk-capacity scales for the opening G900 experiment.

The goal is not perfection.
The goal is to get the first lawful measurement run off the ground without inventing geometry we cannot yet justify.

So the first pass should be:

- empirical
- explicit
- repeatable
- easy to revise later

---

## Decision

For the first run, use:

### Occupancy
\[
N_k = \text{observed vertex count in shell } k
\]

### Shell-local scale
\[
S_k = \max_{\text{comparison runs so far}} N_k
\]

That means \(S_k\) is the empirical shell envelope:
the largest shell occupancy yet observed at shell \(k\) across the comparison family.

### Bulk-capacity scale
\[
C_k = \sum_{j=0}^{k} N_j
\]

That means \(C_k\) is cumulative observed occupancy through shell \(k\).

This is not a final bulk-capacity law.
It is the first honest cumulative capacity proxy.

---

## Why this is the right first move

### Why \(S_k\) is acceptable
It gives a shell-local reference scale without pretending we already know the true shell capacity law.

It answers the practical question:
relative to what local shell size should this shell be read?

### Why \(C_k\) is acceptable
It gives a monotone bulk-like scale built directly from lawful output.

It answers the practical question:
how much total lawful mass has accumulated by the time shell \(k\) is reached?

### Why this pair is good enough
It lets the first lens pair be computed now.

It is:
- simple
- empirical
- transparent
- revisable

That is exactly what Basecamp needs.

---

## Resulting first-pass images

With these definitions:

### Shell image
\[
\rho_{\mathrm{shell}}(k)=\frac{N_k}{S_k}
\]

### Bulk image
\[
\rho_{\mathrm{bulk}}(k)=\frac{N_k}{C_k}
\]

### Difference
\[
\Delta(k)=\rho_{\mathrm{shell}}(k)-\rho_{\mathrm{bulk}}(k)
\]

### Ratio
\[
R(k)=\frac{\rho_{\mathrm{shell}}(k)}{\rho_{\mathrm{bulk}}(k)}
\]
when \(\rho_{\mathrm{bulk}}(k)\neq 0\)

---

## Interpretation discipline

These quantities should initially be read only as:

- empirical shell-normalized density
- empirical cumulative-bulk-normalized density
- empirical difference image
- empirical ratio image

Do not yet call them:
- canonical densities
- theorem-grade normalizations
- intrinsic capacities
- or physical observables

Those promotions come later, if earned.

---

## Known limitation

This first definition makes \(S_k\) comparison-family dependent.

That is acceptable for Basecamp because the immediate goal is not intrinsic finality.
The goal is stable comparison across runs.

Later replacements for \(S_k\) may include:

- grammar-derived shell capacity
- chamber-derived shell capacity
- symmetry-derived shell capacity
- quotient-derived effective shell capacity

Likewise, later replacements for \(C_k\) may include:

- reachable-state capacity
- chamber-completion capacity
- quotient-visible cumulative capacity
- modeled volumetric capacity

---

## First run protocol

For the first experiment family:

1. choose a fixed root convention
2. compute shell counts \(N_k\)
3. update shell envelopes \(S_k\)
4. compute cumulative counts \(C_k\)
5. compute shell and bulk images
6. inspect \(\Delta(k)\) and \(R(k)\)
7. compare across runs before interpreting

---

## Success criterion

This first scale decision succeeds if it yields a stable table that can be compared across runs without ambiguity.

It does not need to be final.
It needs to be usable.

That is enough for first light.

