# G900 Half-Layer Displacement Lemma v0.1

## Goal
State the exact remaining numerical lemma on the offset side.

## Locked inputs
- total layer count L = 10
- centered prism center I = 145
- observed off-center displacement d = 5
- carrier-derived audit confirms L is structural
- predecessor shell is uniquely located immediately before midpoint

## Candidate lemma
### Half-Layer Displacement Lemma
If the centered prism branch displacement is inherited from shell geometry, and the relevant shell geometry is the 10-layer midpoint/predecessor configuration, then the inherited displacement is exactly the half-layer value:

- d = L / 2

Hence in the current carrier:

- d = 10 / 2 = 5

## Consequence
Therefore the centered prism law reconstructs as:

- I - d = 145 - 5 = 140
- I     = 145
- I + d = 145 + 5 = 150

## Exact burden
The remaining proof sentence is:

> why the shell-derived displacement is measured by the half-layer count rather than by another shell statistic

That is now the narrowest open numerical step.

