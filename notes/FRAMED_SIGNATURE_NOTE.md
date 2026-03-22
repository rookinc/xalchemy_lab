# Framed Signature Note

## Purpose

Provide a single canonical readout object for the current framed transport layer.

## Signature

The current framed signature is:

- `H` = parity of chart-coordinate flips
- `S` = signed chart displacement

So the combined signature is:

- `(H,S)`

## Current examples

- return_A -> `( +1, +1 )`
- return_B -> `( +1, -1 )`
- return_C -> `( +1, +3 )`
- return_D -> `( -1, -1 )`

## Strongest sentence

The runtime now supports a two-invariant framed signature `(H,S)` that is strictly richer than either invariant alone.

