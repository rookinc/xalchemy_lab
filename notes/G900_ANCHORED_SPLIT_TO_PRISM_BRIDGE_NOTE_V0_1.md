# G900 Anchored Split to Prism Bridge Note v0.1

## Current bridge-side hard result
The current bridge witness is carried by a 7-edge anchored split core:

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

So the bridge-side witness has type:

e00 | (e05,e10,e02) | (e04,e07,e01)

Equivalently:

1 + 3 + 3

The three current specimen loops sit naturally inside this core:

- global_return uses the anchor e00
- global_square uses the anchor plus square arm
- global_twist uses the anchor plus twist arm

The full odd-support cloud is larger:

- e01
- e02
- e05
- e09
- e12
- e16
- e19
- e22
- e24
- e25

So the active bridge witness is not controlled by odd support alone.
It is carried by a smaller anchored structural core.

## Current descent-side hard result
The G900 descent artifacts now explicitly realize:

- carrier type:
  - 900-cell order-30 triangular subdivision

- first quotient:
  - exact weighted triangular prism

- second quotient:
  - exact weighted triangle

The prism quotient has weighted edge law:

- bit0_face = 140
- macro_rung = 145
- bit1_face = 150

So the prism is centered at:

145

with centered offsets:

- bit0_face = -5
- macro_rung = 0
- bit1_face = +5

The coarse triangle edge weight is:

290

and the macro contact counts are:

- (0,1) = 290
- (0,2) = 290
- (1,2) = 290

## Explicit collapse structure
The prism-to-triangle collapse artifact states:

- top and bottom prism vertices collapse to the same triangle vertices
- top and bottom horizontal edges collapse to the same triangle edges
- vertical edges collapse to triangle vertices

The current pushforward rule is:

AB = w(top_ab) + w(bottom_ab) + side contribution
BC = w(top_bc) + w(bottom_bc) + side contribution
CA = w(top_ca) + w(bottom_ca) + side contribution

The current base candidate is therefore:

140 + 150 = 290

with side contribution still unresolved.

## Strongest current bridge reading
We now have a clean structural rhyme:

### Bridge side
One shared anchor plus two three-edge branch arms:

1 + 3 + 3

### G900 prism side
One shared center plus two off-center face classes:

145 | 140,150

### Coarse collapse
The two off-center face classes collapse onto the same coarse triangle edge candidate:

140 + 150 = 290

So the bridge-side anchored split core and the G900 weighted prism now exhibit the same qualitative shape:

- one shared central/support object
- two nontrivial branch classes
- collapse of the two branch classes into one coarse contact edge

## Working identification
Best current tentative reading:

- bridge anchor e00 corresponds to the shared center/support role
- square arm (e05,e10,e02) corresponds to one off-center prism branch
- twist arm  (e04,e07,e01) corresponds to the other off-center prism branch

Then the G900 descent realizes the same pattern in scalar form:

- center = 145
- branch 1 = 140
- branch 2 = 150

and prism collapse merges the two branches into the triangle edge candidate:

290

## Honest status
This is still a bridge note, not a theorem.

What is now real:

- bridge-side anchored split core exists
- G900 centered weighted prism exists
- prism-to-triangle collapse exists
- the centered pair 140 and 150 push toward the coarse edge candidate 290

What is not yet proved:

> that the square arm and twist arm descend canonically to the two off-center prism branches.

That is the exact next bridge target.

## Next question
Does each bridge-side 3-edge arm descend to one of the two off-center prism branches around center 145?

That is now the sharp next probe.

