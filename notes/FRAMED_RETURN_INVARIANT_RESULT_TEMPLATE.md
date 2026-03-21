# Framed Return Invariant Result Template

## Goal

Compute a derived framed return invariant from the chart trace rather than using only initial and final frame labels.

## Definition

For a chart trace

- `c_1, ..., c_n`

define transition signs by:

- `+1` if consecutive chart symbols are the same
- `-1` if consecutive chart symbols differ

Then define the framed return invariant

- `H = product of transition signs`

## Interpretation

- `H = +1` means an even number of chart flips
- `H = -1` means an odd number of chart flips

## What to inspect

For each loop:
- chart trace
- transition signs
- `H`

## Strongest sentence

The first derived framed return invariant is the parity of chart-coordinate flips along the transport trace.

