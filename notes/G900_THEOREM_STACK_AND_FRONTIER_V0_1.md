# G900 Theorem Stack and Frontier v0.1

## Locked theorem stack

### Theorem 1. Bridge parity witness theorem
For the resolved bridge specimen set:

- global_return = 0
- global_square = 0
- global_twist = 1

So twist is odd, while return and square are even.

### Theorem 2. Anchored split core theorem
The current bridge witness is carried by the 7-edge structural core:

- e00
- e01
- e02
- e04
- e05
- e07
- e10

This core decomposes exactly as:

- anchor:
  - e00

- square arm:
  - e05
  - e10
  - e02

- twist arm:
  - e04
  - e07
  - e01

So the live bridge witness has type:

1 + 3 + 3

### Theorem 3. Centered prism theorem
The G900 first quotient is an exact weighted triangular prism with centered law:

- 140
- 145
- 150

So the prism is centered at 145 with offsets:

- -5
- 0
- +5

### Theorem 4. Coarse collapse theorem
The prism-to-triangle collapse yields coarse triangle edge law:

140 + 150 = 290

on all three edge classes.

So the coarse triangle is uniform with edge weight 290.

### Theorem 5. Parity-stable carrier theorem
Even and odd slices share the same triangular-prism support, but carry different kind totals.

Even:
- bit0_face = 160
- macro_rung = 240
- bit1_face = 320

Odd:
- bit0_face = 260
- macro_rung = 195
- bit1_face = 130

So parity is a redistribution layer on a fixed prism carrier.

## Corollary
There are currently two distinct binary layers:

### Branch layer
The coarse centered prism:
- 140 | 145 | 150
with collapse:
- 140 + 150 = 290

### Parity layer
The even/odd redistribution on the same prism support:
- (160,240,320)
- (260,195,130)

So branch split and parity split are not the same binary layer.

## Strongest current bridge proposition
The bridge-side anchored split core

e00 | (e05,e10,e02) | (e04,e07,e01)

and the descent-side centered prism

145 | 140,150

share the same qualitative structure:

- one shared central/support object
- two nontrivial branch classes
- collapse of the two branch classes into one coarse edge law

This is now the strongest bridge statement.

## Exact frontier
Still open:

> the square arm and twist arm descend canonically to the two off-center prism branches 140 and 150, with anchor descending to the centered rung 145

That is the next theorem target.

## Next theorem target
### Anchored Arm Descent Theorem
Under the G900 descent, the two bridge-side 3-edge arms descend to the two off-center prism branches of weights 140 and 150, and the shared anchor descends to the centered rung 145.

If proved, the bridge becomes theorem-grade.

