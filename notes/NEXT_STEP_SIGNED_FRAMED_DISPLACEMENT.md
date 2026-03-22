# Next Step: Signed Framed Displacement

## Goal

Introduce a second framed invariant that distinguishes loops which share the same cocycle invariant `H`.

## Reason

The current cocycle invariant

- `H`

already separates:

- `return_D`

from

- `return_A`
- `return_B`
- `return_C`

But it does not distinguish the loops inside the `H=+1` class.

So a finer framed quantity is needed.

## Candidate invariant

Define a signed chart displacement:

- `chart_left  = -1`
- `chart_right = +1`

For a chart trace

- `c_1, ..., c_n`

define

- `S = sum of signed chart values`

So:

- `return_A = chart_right, chart_left, chart_right` gives `S = +1`
- `return_B = chart_left, chart_right, chart_left` gives `S = -1`
- `return_C = chart_right, chart_right, chart_right` gives `S = +3`
- `return_D = chart_right, chart_left, chart_left` gives `S = -1`

## Interpretation

`H` detects parity of framed flips.

`S` detects signed framed displacement.

Together they give a richer framed trace classification.

## Strongest sentence

The next invariant should distinguish loops inside the same cocycle class by measuring signed displacement in chart coordinates.

