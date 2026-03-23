# G900 layer structure note v0.1

## Current computation result

The order-30 triangular subdivision produces exactly 900 smallest triangular cells.

A barycentric inward-layer probe yields the layer counts:

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

This is an arithmetic descent by 18.

Equivalently:

- 171 = 9 * 19
- 153 = 9 * 17
- 135 = 9 * 15
- 117 = 9 * 13
- 99  = 9 * 11
- 81  = 9 * 9
- 63  = 9 * 7
- 45  = 9 * 5
- 27  = 9 * 3
- 9   = 9 * 1

So:

`900 = 9 * (19 + 17 + 15 + 13 + 11 + 9 + 7 + 5 + 3 + 1)`

Since the sum of the first ten odd numbers is 100:

`900 = 9 * 100`

## Immediate significance

The G900 candidate carrier is not just a flat 900-cell object.

It has a clean inward layer structure with:

- 10 layers
- odd-number descent
- persistent factor 9

## Next question

Does each layer admit a natural partition into 9 coherent sectors or packets?

If yes, then the residual per-layer counts are:

- 19, 17, 15, 13, 11, 9, 7, 5, 3, 1

and the full carrier may factor as:

- 9-sector shelling
- over a 10-step odd descent

## Next experiment

Test whether each cell can be assigned both:

1. a layer index
2. a sector index modulo 9

in a way that is geometrically coherent and compatible with adjacency.

