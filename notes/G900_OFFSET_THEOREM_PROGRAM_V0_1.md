# G900 Offset Theorem Program v0.1

## Goal
Finish the centered prism forcing argument by proving that the off-center displacement is exactly:

- d = 5

## Current locked inputs
- total layer count L = 10
- midpoint layer = 5
- predecessor shell = 4
- center already isolated as 145
- observed centered prism law = (140,145,150)

## Exact burden
Still open:

> why the branch displacement equals the half-layer offset rather than some other admissible value

Arithmetic fit is not enough.
The value d = 5 must be tied to shell structure.

## Candidate theorem
### Shell-Offset Theorem
If the centered prism branches are supplied by the unique predecessor shell immediately before midpoint, and the shell-to-center displacement is governed by the half-layer law of the 10-layer carrier, then the only admissible offset is:

- d = L / 2 = 5

Hence:
- top = 145 - 5 = 140
- mid = 145
- bottom = 145 + 5 = 150

## Proof tasks

### Task 1. Positional uniqueness
Show that layer 4 is the unique shell immediately before midpoint layer 5.

### Task 2. Scale inheritance
Show that the off-center branch magnitude is inherited from predecessor-shell position, not from arbitrary normalization.

### Task 3. Half-layer law
Show that the inherited displacement is exactly:
- d = L / 2

### Task 4. Full reconstruction
Combine center forcing and offset forcing to obtain:
- (140,145,150)

## Honest status
At present:
- d = 5 is exact and strongly motivated
- but still not fully forced by a closed structural proof

