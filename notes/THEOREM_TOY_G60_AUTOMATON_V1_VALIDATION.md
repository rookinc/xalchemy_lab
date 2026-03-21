# Theorem: Toy G60 Automaton v1 Passes the Current Local Interface

## Theorem

Toy G60 Automaton v1 reproduces the measured local trace-state machine exactly on the current 5-state test neighborhood.

Result:
- total checks = 75
- mismatches   = 0
- matches      = 75

So the toy automaton passes the current local interface test in full.

## Covered features

The successful match includes:

- anchored odd exchange control
- anchored E1-sheet activation
- anchored E2-sheet polarity swap
- the E1 shuttle trace
- the E1/E2 mixed anchored continuation trace
- the rigid odd backbone
- the rigid even backbone
- the mixed cancellation class
- bridge-signature degeneracy between (0,0,1) and (1,1,0)

## Meaning

This is the first explicit upstairs candidate mechanism that is not merely compatible in prose, but validated against the measured local trace-control law.

## Strongest current reading

A controlled packet automaton on the upstairs side is sufficient, at least locally, to generate the observed bridge behavior under descent.

