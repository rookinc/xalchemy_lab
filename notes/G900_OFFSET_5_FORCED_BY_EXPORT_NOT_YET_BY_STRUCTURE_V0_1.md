# G900 Offset 5 Forced by Export, Not Yet by Structure v0.1

## Status
Result note.

## Current position
The current extracted weighted prism artifact does not merely list the weights

- top = 140
- rung = 145
- bottom = 150

It also encodes them through a normalized edge law:

- center weight = 145
- bit0_face offset = -5
- macro_rung offset = 0
- bit1_face offset = +5

So the extracted prism law is explicitly represented as center-plus-offset data:

- top = 145 - 5
- rung = 145 + 0
- bottom = 145 + 5

## What is now established
The value d = 5 is not only visible in the recovered weights.
It is built directly into the exported normalized edge law.

So, relative to the current exported artifact, the offset magnitude is fixed:

- d = 5

## What is not yet established
This does **not** yet prove that d = 5 is forced by deeper carrier structure.

At present, the chain of justification is:

1. the export defines a normalized edge law,
2. that normalized law fixes offsets -5, 0, +5,
3. those offsets recover the observed prism weights 140, 145, 150.

What remains open is whether the normalized edge law itself is derived from deeper structural necessity, or is still a chosen normalization packaged by the export.

## Comparison with earlier results
Earlier tests established:

- arithmetic alone does not force midpoint balance,
- centered-offset structure forces the center but not the offset magnitude,
- the exported normalized law fixes the remaining freedom by selecting d = 5.

So the present state is:

- center 145: structurally forced under the centered-offset assumption,
- offset magnitude 5: forced by the export normalization,
- theorem-level structural forcing of offset 5: still open.

## Honest conclusion
The current bundle supports the statement:

- offset 5 is forced by the exported normalization,
- but not yet proved to be forced by deeper carrier structure.

## Next theorem target
Derive the normalized edge law itself from one or more deeper ingredients, such as:

- layer-count normalization,
- macro/bit carrier geometry,
- support-edge census,
- parity transport symmetry,
- exact quotient normalization.

