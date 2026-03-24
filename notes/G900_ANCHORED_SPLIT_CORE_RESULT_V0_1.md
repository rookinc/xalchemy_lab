# G900 Anchored Split Core Result v0.1

## Hard result
The current bridge witness is not controlled by the full odd-support cloud alone.

Instead, it is carried by a smaller 7-edge structural core:

- e00
- e01
- e02
- e04
- e05
- e07
- e10

## Exact decomposition
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

So the structural core is:

e00 | (e05,e10,e02) | (e04,e07,e01)

Equivalently:

{e00} union {e05,e10,e02} union {e04,e07,e01}
=
{e00,e01,e02,e04,e05,e07,e10}

## Verified probe facts
The decomposition was checked directly.

Results:

- anchor union square_arm union twist_arm matches the structural core exactly
- odd edges inside the core are:
  - e01
  - e02
  - e05

- even edges inside the core are:
  - e00
  - e04
  - e07
  - e10

- odd-support edges outside the core are:
  - e09
  - e12
  - e16
  - e19
  - e22
  - e24
  - e25

So the larger 10-edge odd cloud contains spectator odd edges relative to the current bridge witness set.

## Witness interpretation
The three current bridge specimen loops sit naturally inside this anchored split core:

- global_return uses the anchor edge e00
- global_square uses the square arm together with the anchor
- global_twist uses the twist arm together with the anchor

This means the live witness geometry is:

- one shared anchor
- two three-edge branch arms

## Strongest current reading
The bridge witness currently realizes an anchored split core of type:

1 + 3 + 3

This is the first concrete bridge-side object that visibly resembles:

- a shared seed/contact
- plus two nontrivial branch realizations

## Why this matters for G900
The closure search has been looking for:

- a center / seed
- a binary split
- two branch realizations

The anchored split core is now the strongest bridge-side candidate for that pattern.

The next question is not whether a pair exists.
It does.

The next question is:

> Does the anchored 1+3+3 split descend to the G900 centered prism's one-center plus two-offset structure?

That is the next bridge target.

## Immediate next task
Test whether the two branch arms:

- square arm = (e05,e10,e02)
- twist arm  = (e04,e07,e01)

project, collapse, or descend to the two off-center G900 branches around the centered value 145.

