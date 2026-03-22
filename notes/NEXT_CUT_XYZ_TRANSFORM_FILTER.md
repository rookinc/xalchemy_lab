# Next Cut: xyz Transform Filter

## Goal

Decide which transforms of ordered `xyz` are:

- admissible symmetries
- admissible physical pre-reconciliation moves
- non-admissible because they alter the state too strongly

## Decision buckets

### Bucket A: presentation symmetry
A transform changes the presentation of `xyz` but not the physical pre-reconciliation class.

### Bucket B: physical pre-reconciliation move
A transform changes the state of `xyz` in a way the kernel must treat as meaningful.

### Bucket C: forbidden / non-admissible
A transform does not belong to the pre-identification grammar.

## Most important question

Does the kernel treat:

- cyclic permutation
- adjacent swap
- reversal

as different physical inputs, or only as different presentations of the same ordered carrier?

## Strongest sentence

The next rigorous task is to filter ordered `xyz` transforms into symmetries, physical moves, and forbidden operations.

