# Next Step: Predict Signature from Controller Sequence

## Goal

Predict the framed signature `(H,S)` directly from a sequence of controller states and handedness inputs, before running the full transport simulation.

## Reason

The current system now supports:

- chart-primary controller semantics
- a native framed accumulator
- a runtime-derived framed signature `(H,S)`

So the next stronger question is:

- can the signature be predicted structurally?

That means using only:

- controller sequence `(A,sigma,tau)`
- handedness sequence

to predict:

- chart trace
- `H`
- `S`

without depending on the full post-hoc runtime receipt.

## Strongest sentence

The next step is to turn the framed signature from a transported runtime state into a structurally predictable quantity.

## Prediction target

Given a sequence:

- `(A_1,sigma_1,tau_1), ..., (A_n,sigma_n,tau_n)`

and a handedness sequence:

- `h_1, ..., h_n`

predict:

- chart exits `c_1, ..., c_n`
- cocycle parity `H`
- signed displacement `S`

## Expected pipeline

1. local controller state predicts chart-relative exit
2. predicted chart exits determine transition signs
3. transition signs accumulate to `H`
4. chart exits sum to `S`

## Why this matters

If successful, this means the framed signature is not only observable in runtime receipts.
It is also derivable from structural controller data.

That would be a stronger step toward a true framed transport calculus.

