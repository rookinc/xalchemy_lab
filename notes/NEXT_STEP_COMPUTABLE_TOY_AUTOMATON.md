# Next Step: Computable Toy Automaton

## Goal

Turn Toy G60 Automaton v1 into a computable descent simulator.

## Inputs

Controls:
- A
- sigma
- tau

## Internal state

- anchor/odd coupling
- anchor/E1 coupling
- anchor/E2 coupling
- distal defect channel
- merged distal channel

## Outputs

- anchored control surface trace parities
- rigid odd backbone trace parities
- rigid even backbone trace parities
- invariant receipt (A, sigma, tau)
- bridge signature (R, Q, W)

## Pass condition

The simulator must reproduce the known 5-state local control law:
- (0,0,1)
- (0,0,0)
- (0,1,1)
- (0,1,0)
- (1,1,0)

