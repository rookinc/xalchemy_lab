# G900 Noncentered Counterexample Search v0.1

## Goal
Test whether the centered prism law is forced or merely observed.

## Fixed combinatorics
Keep the same prism support shape:

- top face class
- bottom face class
- rung class
- collapse to triangle edge classes AB, BC, CA

## Fixed target laws
Keep the following as target constraints:

- triangle base candidate = 290
- macro contact = 290
- top + bottom = 290

## Question
Can one choose prism weights

- top = a
- rung = r
- bottom = b

with

- a + b = 290

but

- r != (a + b) / 2 = 145

while still preserving the same intended descent semantics?

## Current observed solution
- top = 140
- rung = 145
- bottom = 150

This is centered.

## Counterexample template
A noncentered candidate would look like:

- top = 130
- rung = 145
- bottom = 160

or

- top = 140
- rung = 144
- bottom = 150

or any other triple preserving selected constraints but breaking midpoint balance.

## What counts as failure
A candidate should be rejected if it breaks one of:

1. top + bottom = 290
2. uniform triangle base candidate
3. macro-contact match
4. central-support interpretation
5. exact symmetric prism pairing semantics

## Present status
Search not yet run.
