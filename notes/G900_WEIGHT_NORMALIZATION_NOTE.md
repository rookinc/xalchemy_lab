# G900 weight normalization note

## Purpose

Record the first normalized edge law for the weighted prism quotient extracted from the G900 carrier.

## Raw weighted prism law

The six-class `(macro, bit)` quotient support is the triangular prism with three edge families:

- bit-0 face edges: `140`
- macro-pair rung edges: `145`
- bit-1 face edges: `150`

So the weighted support is:

- top triangle = `140`
- vertical rungs = `145`
- bottom triangle = `150`

## First normalization

Take the rung weight as the center value:

`145`

Subtract this from all edge weights:

- `140 -> -5`
- `145 -> 0`
- `150 -> +5`

This yields a signed three-level law:

- bit-0 face edges: `-5`
- macro rungs: `0`
- bit-1 face edges: `+5`

## Interpretation

This is the cleanest first symbolic normalization of the weighted prism.

Possible readings:

1. paired-sheet offset
2. signed lift bias
3. two-layer face asymmetry separated by neutral rungs
4. coarse lift profile on the first quotient support

Do not overclaim yet.

The only locked result at this stage is:

- the support is exactly the triangular prism
- its edge weights admit the centered normalization `-5 / 0 / +5`

## Immediate significance

The first coarse quotient extracted from the G900 carrier is not just combinatorially prism-shaped.

It is also weighted by a symmetric signed three-level edge law.

That makes the quotient a better candidate for comparison with existing lift / sheet / paired-channel language in the project.

## Next burden

Test whether this normalized law is:

- stable under automorphisms of the prism
- recoverable from layer-conditioned contact data
- interpretable as a lift-like or sheet-like invariant rather than a presentation accident

