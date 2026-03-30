# G900 First Experiment Plan
## Basecamp execution note

Date: 2026-03-29

---

## Objective

Turn the first paired-scale candidate into a repeatable experiment.

This experiment is not yet trying to prove the summit law.
It is trying to establish the first lawful readout from which a summit law could emerge.

The first experiment is:

- shell occupancy
- versus
- bulk capacity

---

## Primary question

Given a lawful G900 run, does the same output exhibit a stable relation between:

- shell-local occupancy
- and
- bulk-capacity-normalized occupancy

when indexed by shell or tick?

---

## First experiment object

For each shell \(k\), record:

- raw shell occupancy \(N_k\)
- shell-local reference scale \(S_k\)
- cumulative bulk-capacity scale \(C_k\)
- shell image
- bulk image
- image difference
- image ratio where defined

Do not force logarithms in the first pass.
Record raw ratios first.

---

## Working definitions

### Shell occupancy
\(N_k\): observed count in shell \(k\)

### Shell-local scale
\(S_k\): local shell capacity estimate for shell \(k\)

### Bulk-capacity scale
\(C_k\): cumulative or total reachable capacity through shell \(k\)

### Shell image
\[
\rho_{\mathrm{shell}}(k) = \frac{N_k}{S_k}
\]

### Bulk image
\[
\rho_{\mathrm{bulk}}(k) = \frac{N_k}{C_k}
\]

### Difference image
\[
\Delta(k) = \rho_{\mathrm{shell}}(k) - \rho_{\mathrm{bulk}}(k)
\]

### Ratio image
\[
R(k) = \frac{\rho_{\mathrm{shell}}(k)}{\rho_{\mathrm{bulk}}(k)}
\]
when \(\rho_{\mathrm{bulk}}(k) \neq 0\)

---

## First pass goals

We are looking for any of the following:

- exact equality pattern
- affine trend in \(k\)
- bounded difference
- stabilized ratio
- regime change at closure threshold
- evidence that one image equilibrates while the other drifts

---

## Non-goals

Not yet:

- theorem
- quotient law
- spectral closure
- cocycle interpretation
- final aa law
- physical interpretation

This is a readout experiment.

---

## Data discipline

Every run should preserve:

- run id
- root choice
- tick range
- shell indexing convention
- definition of \(S_k\)
- definition of \(C_k\)
- whether values are empirical or modeled

If these are not fixed, the experiment is noise.

---

## Output artifact

The output of each run should be one table with one row per shell and fields:

- shell_index
- occupancy
- shell_capacity
- bulk_capacity
- shell_density
- bulk_density
- density_difference
- density_ratio
- notes

This table is the first lawful bridge payload.

---

## Success condition

This experiment succeeds if it produces a stable, comparable shell/bulk table across runs.

It does not need to produce a theorem yet.

A stable table is already a success.

