# G900 Competing Offset Statistics Sweep v0.1

## Goal
Perform the last protocol-level stress test on the offset side.

Question:

> Is there any other carrier-derived statistic, besides the half-layer value L/2, that could plausibly serve as the centered prism branch displacement?

## Current accepted candidate
- d = L / 2 = 5

This candidate is currently strongest because it is:
- carrier-derived
- midpoint-centered
- symmetric
- exact on the observed prism law
- compatible with the predecessor-shell scale story

## What counts as a competitor
A serious competing statistic must be:

1. carrier-derived
2. tied to midpoint / predecessor-shell structure
3. symmetric-branch compatible
4. exact on the prism law
5. not just a renamed form of L/2

## Immediate competitor families to check

### A. Shell-index statistics
Examples:
- predecessor shell index = 4
- midpoint index = 5
- midpoint minus predecessor = 1

### B. Contact-gap statistics
Examples:
- same-layer minus inward contact
- outward minus inward
- rung-face differences
- parity face differences

### C. Population statistics
Examples:
- shell population gap
- half-population rounding
- bit imbalance
- macro contact half-difference

### D. Other quotient-level centers/gaps
Examples:
- parity-triangle gap 15
- macro/bit population center 150
- macro-contact center 290

## Protocol criterion
If every serious competitor either:
- fails exact reconstruction,
- fails midpoint compatibility,
- fails branch-level status,
- or reduces to the same half-layer rule in disguise,

then the half-layer step is close to theorem-grade by structural exclusion.

