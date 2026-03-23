# G900 descent summary note v0.1

## Purpose

Lock the current G900 descent chain into one compact checkpoint.

## Carrier

The current G900 candidate carrier is the 900 smallest triangular cells in the order-30 triangular subdivision.

Locked carrier facts:

- total cells = 900
- inward layers = 10
- macro sectors = 3
- live bits = 2

Macro populations are exactly balanced:

- macro 0 = 300
- macro 1 = 300
- macro 2 = 300

Bit populations are:

- bit 0 = 435
- bit 1 = 465

Macro/bit populations are:

- (m,0) = 145
- (m,1) = 155

for each macro `m`.

Cross-macro raw contact counts are exactly:

- (0,1) = 290
- (0,2) = 290
- (1,2) = 290

So the sampled carrier already contains exact triadic macro symmetry before quotienting.

## Layer law

Inward layer counts are:

- 171
- 153
- 135
- 117
- 99
- 81
- 63
- 45
- 27
- 9

So the carrier is a layered triangular field, not a flat undifferentiated tessellation.

## First quotient: weighted prism

Classifying cells by `(macro, bit)` gives six classes.

The induced support graph on these six classes is exactly the triangular prism.

Weighted prism law:

- bit-0 face = 140
- macro rung = 145
- bit-1 face = 150

Centered prism form:

- `145 + {-5, 0, +5}`

Weight-preserving automorphism count:

- 6

Interpretation:
- macro permutations survive
- bit-sheet exchange does not

## Parity refinement

Refining the prism by layer parity preserves exact prism support in both parity slices.

Even slice weights:

- bit-0 face = 160
- macro rung = 240
- bit-1 face = 320

Odd slice weights:

- bit-0 face = 260
- macro rung = 195
- bit-1 face = 130

So the prism support is stable under parity refinement, but the weights alternate strongly by parity.

Interpretation:

- even layers favor the bit-1 sheet
- odd layers favor the bit-0 sheet

Layer is therefore a phase coordinate, not merely radial depth.

## Triangle descent

Collapsing the three macro rungs of the prism yields an exact triangle.

Triangle edge weights:

- coarse = 290
- even = 160
- odd = 130

with exact relation:

- `160 + 130 = 290`

Interpretation:

- the prism remembers the split
- the triangle remembers only exact triadic symmetry

## Shared centers

Current scalar centers observed in the chain:

- macro/bit population center = 150
- prism center = 145
- triangle parity center = 145
- macro contact center = 290

and

- `290 = 2 * 145`

So the same center `145` appears independently at prism and triangle parity levels.

This is the first shared scalar center visible across the current descent chain.

## Current descent chain

- 900-cell sampled carrier
- 6-class weighted prism
- 3-node exact weighted triangle

## Current strongest statement

The quotient chain is not inventing symmetry.

It is exposing symmetry already present in the sampled carrier.

The carrier is layered.
The split alternates by parity.
The first coarse quotient is a weighted prism.
The next quotient is an exact triangle.
The current chain is organized around the shared center 145.

