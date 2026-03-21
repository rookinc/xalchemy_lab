# Next Step: G60 Interface Test

## Goal

Turn the minimal G60 interface into an operational pass/fail test.

## A candidate upstairs G60 model must reproduce:

### 1. Anchored control packet descent
It must descend to local control actions matching:

- tau toggles anchor odd exchange
- sigma toggles E1-sheet activation
- A swaps anchored sheet polarity and rearms the anchor odd mode

### 2. Rigid transport skeleton descent
It must also preserve the parity stability of the rigid backbone classes across the tested nearby controls.

## Pass condition

A candidate G60 model passes the interface test only if it reproduces both:

- the anchored control surface
- the rigid odd/even backbone

under descent.

## Meaning

This converts the current local normal form into an upstairs compatibility test.

