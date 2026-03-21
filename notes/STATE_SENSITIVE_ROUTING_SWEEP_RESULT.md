# State-Sensitive Routing Sweep Result

## Goal

Audit the current table-driven structural routing law across all 8 controller states.

## Artifact

- `specs/app/state_sensitive_routing_sweep_v0_1.json`

## What it records

For each state `(A,sigma,tau)`:

- base `state_sensitive` left/right preferred exits
- `state_sensitive_under_load` 3-arrival behavior
- final route counts
- final switch state
- override trace events

## Why it matters

This is the compact audit object for the current controller law.

It tells us whether the state-sensitive table is:

- sufficiently non-collapsed
- operational under burden
- stable enough to keep
- or still obviously provisional

## Next question

After reviewing the sweep, decide whether:

1. the table should be frozen as provisional canonical runtime law, or
2. the table should be revised toward a more geometric derivation.

