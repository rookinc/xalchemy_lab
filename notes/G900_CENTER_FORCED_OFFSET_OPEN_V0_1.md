# G900 Center Forced, Offset Still Open v0.1

## Status
Result note.

## What is now forced
From the current tests, the following are forced once we require:

- base edge sum = 290
- macro-contact match = 290
- rung as true center class

Then:

- rung = 145
- top + bottom = 290
- top and bottom are symmetric around 145

So the remaining admissible family is:

- top = 145 - d
- rung = 145
- bottom = 145 + d

for some offset d.

## What is not yet forced
The current tests do **not** force the specific extracted split

- 140, 145, 150

They only force the centered family

- (145 - d, 145, 145 + d).

So the offset magnitude d remains open.

## Current extracted artifact
The present weighted prism export gives:

- top = 140
- rung = 145
- bottom = 150

which corresponds to

- d = 5.

## New theorem target
Find the additional structural assumption that fixes

- d = 5.

Possible sources of forcing:

1. layer-count normalization,
2. macro/bit classification geometry,
3. exact support-edge census,
4. parity-layer transport symmetry,
5. a quotient normalization rule already implicit in the export.

## Honest current conclusion
The center is forced.
The symmetry is forced.
The offset magnitude is still open.
