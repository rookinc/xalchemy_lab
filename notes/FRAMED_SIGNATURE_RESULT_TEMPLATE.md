# Framed Signature Result Template

## Goal

Combine the first two framed invariants into a single signature object.

## Definition

For each chart trace, compute:

- `H` = parity of chart-coordinate flips
- `S` = signed framed displacement

Then define the framed signature:

- `(H,S)`

## Interpretation

- `H` gives the coarse closure / flip-parity class
- `S` gives finer signed chart displacement inside or across `H` classes

## What to inspect

For each loop:
- chart trace
- chart values
- transition signs
- `H`
- `S`
- signature tuple `(H,S)`

## Strongest sentence

The framed transport law now admits a two-invariant signature `(H,S)` combining cocycle parity and signed chart displacement.

