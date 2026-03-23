# G900 Half-Layer Law Needs Geometric Justification v0.1

## Status
Method note.

## Current situation
The extracted offset magnitude is

- d = 5

and several simple formulas recover this same value from the exported source data, including:

- layer_count / 2
- macro_count + bit_count
- layer_count / bit_count
- cell_count / 180

So arithmetic matching alone does **not** identify the correct explanatory law.

## What is still true
Among the currently matching candidates, the half-layer expression

- d = layer_count / 2

remains the leading structural candidate because it fits the geometric centered-gap picture:

- (I - d, I, I + d)

with I as the midpoint and d as half-thickness.

In the current export:

- I = 145
- layer_count = 10
- d = 5 = 10 / 2

so the extracted prism law becomes:

- (145 - 5, 145, 145 + 5)
- (140, 145, 150)

## Why this is not yet a theorem
This is still not proved.

To justify the half-layer law rigorously, one would need a geometric or combinatorial argument showing that:

1. the two face strata are separated by a band of thickness equal to layer_count,
2. the rung is the true midpoint of that band,
3. the normalization records half-thickness on each side of the center.

Without that kind of argument, the half-layer law is only a promising fit, not a forced derivation.

## Honest conclusion
The current state is:

- Q(I) = 2I is strongly supported,
- the centered preimage picture is strongly supported,
- d = 5 is real,
- but the explanation of d = 5 remains open.

The half-layer law is currently the best geometric candidate, but it still needs geometric justification.

