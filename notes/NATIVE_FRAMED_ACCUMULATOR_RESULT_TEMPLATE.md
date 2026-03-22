# Native Framed Accumulator Result Template

## Goal

Test whether the framed signature `(H,S)` can be carried online as a transported state.

## Accumulator

The accumulator carries:

- `prev_chart`
- `H`
- `S`

and updates at each step.

## What to inspect

For each loop:

- per-step `chart_exit`
- per-step `transition_sign`
- per-step `running_H`
- per-step `running_S`
- final accumulator state
- final signature `(H,S)`

## Strongest sentence

The framed signature becomes stronger if it can be carried online as a transported local state rather than only reconstructed from completed traces.

