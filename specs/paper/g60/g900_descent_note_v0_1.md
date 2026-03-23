# G900 Descent Note v0.1

**Status:** provisionally checked bundle

## Claim
The G900 carrier admits a two-stage exact quotient descent:
\[
G900 \;\to\; \text{weighted triangular prism} \;\to\; \text{weighted triangle},
\]
with parity support stable across even and odd slices, a shared center of 145, and macro contact count 290.

## Checked bundle status
The current witness bundle is provisionally checked at the scaffold level:
- parity comparison: PASS
- prism-to-triangle collapse: PASS
- shared center 145: PASS
- macro contact 290: PASS

These checks currently certify bundle consistency, pointer existence, provisional witness alignment, symbolic model consistency, symbolic quotient-law admissibility, and weight-table alignment.
They do not yet replace a future fully extracted carrier-level construction proof.

## Descent summary
- **carrier:** 900-cell order-30 triangular subdivision
- **first quotient:** exact weighted triangular prism
- **parity refinement:** prism support stable in even and odd slices
- **second quotient:** exact weighted triangle
- **shared center:** 145
- **macro contact:** 290 = 2 × 145

## Interpretation
The first exact coarse carrier is not merely a triangle but a prism, indicating that the descent retains a doubled or slice-resolved support before final compression.
The parity refinement shows that this prism support is not an artifact of one slice family: it persists in both even and odd layers.
The second quotient collapses this stable doubled support to an exact weighted triangle.
The count 145 functions as the shared central support, and the macro contact count 290 records the doubled contact structure across the two parity families.

## Structural reading
This suggests the following lawful descent spine:

1. **900-cell carrier**  
   A high-cardinality triangular subdivision with order-30 support.

2. **Prism quotient**  
   The first exact quotient retains two linked slice-families rather than immediately collapsing them.
   This is consistent with a parity-resolved transport picture.

3. **Parity stability**  
   Even and odd slices carry the same prism-support law.
   So the prism is a genuine structural quotient, not a sampling artifact.

4. **Triangle quotient**  
   After identifying the parity-resolved support, the macro carrier compresses to an exact weighted triangle.

5. **Shared center**  
   The value 145 is the common center through which the two slice families meet.

6. **Macro contact**  
   The value 290 = 2 × 145 indicates a doubled contact law across the two parity sectors.

## Provisional theorem statement
**Provisional Theorem.**
The G900 carrier descends through an exact weighted triangular prism quotient whose support is stable under even/odd parity slicing, and this prism quotient further descends to an exact weighted triangle. The two parity sectors meet through a shared center of 145, yielding total macro contact 290.

## What is established
- existence of a two-stage exact quotient descent
- prism support at the first quotient level
- parity stability of that support
- exact weighted triangle at the second quotient level
- shared-center count 145
- doubled macro-contact count 290
- provisional witness-bundle consistency across all four promoted checks
- symbolic prism-model agreement across even, odd, parity, and collapse artifacts
- symbolic quotient-law domain and codomain checks for the collapse map
- extracted shared prism edge law from the weighted prism source

## What remains open
- explicit carrier-level extraction proving the prism quotient directly from the full 900-cell subdivision
- explicit parity-distinguished extraction, if it differs from the current shared exported prism
- explicit extracted prism-to-triangle pushforward values beyond symbolic formulas
- concrete lower-level derivation of the 145 shared center
- concrete lower-level derivation of the 290 macro contact
- interpretation of the shared center in transport / thalion language

## Figure artifacts

The current symbolic descent figure is available as:

- `specs/paper/g60/g900_symbolic_prism.svg`
- `specs/paper/g60/g900_symbolic_prism.png`

The supporting verification and generation artifacts are:

- `specs/paper/g60/g900_descent_witness_v0_1.json`
- `src/xalchemy_lab/app/hello_g900_descent_table.py`
- `src/xalchemy_lab/app/render_g900_symbolic_prism.py`

## Figure note
The current figure is a symbolic structural rendering of the shared prism carrier and its collapse to the weighted triangle target.
It is not yet an extracted geometric embedding from the full carrier.
Its present role is to make the verified symbolic quotient law visually inspectable.

## Weight artifacts

The current prism-weight scaffold is available as:

- `specs/paper/g60/g900_prism_weight_table_v0_1.json`
- `src/xalchemy_lab/app/hello_g900_weight_table.py`

This is the current landing point for extracted edge weights on the shared symbolic prism carrier and their pushforward to the weighted triangle.

## Extracted prism weight law

The current weighted-prism export gives the first extracted numeric edge law for the symbolic prism carrier:

- top-face edges: 140
- vertical macro-rung edges: 145
- bottom-face edges: 150

Equivalently, with center weight 145:

- top-face offset = -5
- vertical offset = 0
- bottom-face offset = +5

At the current scaffold level, both even and odd slice support files inherit this same extracted weighted prism law from:

- `specs/paper/g60/g900_weighted_prism_v0_1.json`

This should be read as an extracted shared prism law.
A later parity-distinguishing extractor may refine this further, but the current checked bundle supports the uniform weighted prism:
\[
(140,145,150)
\]
across top, vertical, and bottom edge classes.

## Upstream weighted prism source

The current extracted prism weights are grounded in the upstream artifact:

- `specs/paper/g60/g900_weighted_prism_v0_1.json`

A terminal reader for this artifact is available at:

- `src/xalchemy_lab/app/hello_g900_weighted_prism.py`

This upstream artifact is the present numeric source for the shared prism law:
- bit0_face = 140
- macro_rung = 145
- bit1_face = 150

The downstream even/odd prism support files and the prism weight table currently inherit their extracted weights from this source.
