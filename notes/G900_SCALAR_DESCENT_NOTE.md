# G900 scalar descent note

## Purpose

The current descent chain is now:

- 900-cell sampled carrier
- 6-class weighted prism
- 3-node exact weighted triangle

The next question is whether a single scalar survives this descent.

That means:

> after forgetting sheet split and keeping only triadic macro symmetry, what quantity remains invariant?

---

## Current exact data

### Coarse triangle
- each edge = 290

### Even parity triangle
- each edge = 160

### Odd parity triangle
- each edge = 130

and

- `160 + 130 = 290`

So the triangle quotient is already isotropic, and each parity slice contributes a uniform edge law.

---

## Candidate scalar invariants

Possible scalars to test:

1. common triangle edge weight
2. total triangle weight
3. normalized parity difference
4. parity ratio
5. centered parity offset

---

## Immediate candidates

### Edge scalar
Take the common edge weight directly.

- coarse edge scalar = 290
- even edge scalar = 160
- odd edge scalar = 130

### Total triangle weight
Since each triangle has 3 equal edges:

- coarse total = `3 * 290 = 870`
- even total = `3 * 160 = 480`
- odd total = `3 * 130 = 390`

and

- `480 + 390 = 870`

### Centered parity offset
Take the midpoint:

- midpoint = `(160 + 130)/2 = 145`

Then offsets are:

- even = `+15`
- odd = `-15`

So the triangle parity split can be written as:

- `145 + 15`
- `145 - 15`

This is very clean.

### Parity ratio
- `160 / 130 = 16 / 13`

Do not overinterpret yet, but record it.

---

## First interpretation

At the prism level, centered normalization gave:

- bit0 face = `145 - 5`
- rung      = `145`
- bit1 face = `145 + 5`

At the rung-collapsed triangle level, parity-centered normalization gives:

- odd  = `145 - 15`
- even = `145 + 15`

So the scalar `145` now appears twice:

1. as the rung-center at prism level
2. as the parity midpoint at triangle level

This is a strong clue that `145` may be the first stable scalar center of the descent.

---

## Strong candidate statement

A first scalar surviving the descent is the centered value:

`145`

with two observed refinements:

- prism refinement: `145 + {-5, 0, +5}`
- parity-triangle refinement: `145 + {-15, +15}`

---

## Next burden

Test whether `145` can be derived directly from the 900-cell carrier without passing through the quotient chain.

If yes, it becomes a real candidate invariant rather than a post hoc average.

