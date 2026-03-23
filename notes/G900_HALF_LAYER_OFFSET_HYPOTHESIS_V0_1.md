# G900 Half-Layer Offset Hypothesis v0.1

## Status
Hypothesis note.

## Core question
What extension law selects the offset magnitude d in the centered prism family

- (I - d, I, I + d) ?

## Current extracted data
From the weighted prism source:

- center I = 145
- top = 140
- bottom = 150
- offset magnitude d = 5
- layer count = 10

## Hypothesis
The offset is half the layer count:

- d = layer_count / 2

so that in the current extracted artifact:

- d = 10 / 2 = 5.

## Consequence
If this is correct, then the centered prism law can be written as

- (I - L/2, I, I + L/2)

where L is the layer count.

For the current artifact:

- (145 - 10/2, 145, 145 + 10/2)
- (140, 145, 150).

## Why this is attractive
This would explain the offset using a visible parameter already present in the exported source, rather than treating 5 as a mysterious free constant.

It would also fit the current separation:

- core quotient law fixes I and Q(I)=2I,
- extension law fixes d,
- and d may come from layer thickness.

## Still open
This is only a hypothesis.
It does not yet explain why layer count should enter as a half-gap normalization.

