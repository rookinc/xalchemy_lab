# G900 prism-to-triangle descent note

## Purpose

Now that the G900 carrier has yielded:

- a coarse 6-class weighted prism quotient
- an even-layer prism slice
- an odd-layer prism slice

the next question is whether the prism itself admits a lawful descent.

The simplest candidate is a collapse along the macro rungs.

That means identifying:

- `(0,0)` with `(0,1)`
- `(1,0)` with `(1,1)`
- `(2,0)` with `(2,1)`

This should produce a 3-node quotient.

The immediate burden is to determine:

1. whether the support descends to a triangle
2. what the induced edge weights are
3. how the even and odd parity slices compare after rung collapse

## Working expectation

Since the prism support consists of:

- a bit-0 triangle
- a bit-1 triangle
- three macro rungs

collapsing each rung should yield a 3-node support triangle.

The more interesting question is the induced weights.

## Current weighted data

Coarse prism:
- bit0 face = 140
- macro rung = 145
- bit1 face = 150

Even slice:
- bit0 face = 160
- macro rung = 240
- bit1 face = 320

Odd slice:
- bit0 face = 260
- macro rung = 195
- bit1 face = 130

Under rung collapse, rung weights should disappear into vertex identification, while face-edge contributions should accumulate into the triangle.

## Next task

Construct the rung-collapsed 3-node quotient for:

- coarse prism
- even slice
- odd slice

and compare the resulting triangle weights.

