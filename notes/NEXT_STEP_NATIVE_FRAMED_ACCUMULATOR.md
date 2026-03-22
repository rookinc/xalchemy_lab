# Next Step: Native Framed Accumulator

## Goal

Make the framed signature `(H,S)` an online transported state rather than only a quantity recovered from completed chart traces.

## Reason

The current pipeline is:

- controller runs
- chart trace is recorded
- `(H,S)` is computed from the trace

The next stronger form is:

- controller runs
- a local accumulator updates at each step
- `(H,S)` is carried natively through the transport process

## Accumulator fields

A minimal framed accumulator should carry:

- `prev_chart`
- `H`
- `S`

## Update law

At each step:

1. read current chart symbol
2. update signed displacement:
   - `chart_left  -> S += -1`
   - `chart_right -> S += +1`
3. update cocycle parity:
   - if previous chart exists:
     - same chart symbol -> `H *= +1`
     - flipped chart symbol -> `H *= -1`
4. set `prev_chart = current_chart`

## Strongest sentence

The next test is whether the framed signature can be carried as an intrinsic transported state rather than reconstructed afterward from a trace.

