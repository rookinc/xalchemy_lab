# Trurtle xyz Admissible Transforms

## Goal

List the first candidate transformations that may act on the ordered trurtle frame `xyz` before identification.

## Principle

The trurtle frame is ordered.

So a transform acting on `xyz` is meaningful only if it respects the role of order in the pre-reconciliation stage.

## Input object

- `xyz`

interpreted as an ordered triadic frame.

## Candidate transform family

### 1. identity
- `xyz -> xyz`

Meaning:
No pre-identification rearrangement.

### 2. cyclic shift forward
- `xyz -> yzx`

Meaning:
Order rotates forward.

### 3. cyclic shift backward
- `xyz -> zxy`

Meaning:
Order rotates backward.

### 4. adjacent swap
- `xyz -> xzy`
- `xyz -> yxz`

Meaning:
Two adjacent entries exchange while one entry stays fixed.

### 5. full reversal
- `xyz -> zyx`

Meaning:
Order is reversed.

### 6. lift
- `xyz -> Lift(xyz)`

Meaning:
A transform that raises or reindexes the frame without yet identifying it.

Status:
Interpretive placeholder; needs concrete rule.

### 7. twist
- `xyz -> Twist(xyz)`

Meaning:
A transform that reorients the frame by local twisting without yet identifying it.

Status:
Interpretive placeholder; needs concrete rule.

### 8. lift+twist
- `xyz -> I`

Meaning:
The half-step reconciliation operator that sends the ordered frame into identification state `I`.

Status:
Current leading candidate for the pre-r1 reconciliation move.

## First conservative distinction

The permutation-like transforms:

- identity
- cyclic shifts
- adjacent swaps
- reversal

should be treated separately from the structural transforms:

- lift
- twist
- lift+twist

The first family rearranges the ordered frame.
The second family reconciles it.

## Strongest sentence

Ordered permutations act on `xyz`, but lift+twist is the candidate reconciliation operator that sends `xyz` into `I`.

## Next step

Determine which permutation-like transforms are admissible as pre-reconciliation symmetries, and which change the physical state rather than merely its presentation.

