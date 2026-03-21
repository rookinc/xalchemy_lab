# Next Step: Toy G60 Automaton

## Goal

Construct the first explicit upstairs toy mechanism that could satisfy the current G60 interface.

## Minimal components

- H  = anchor packet
- O  = odd exchange branch
- E1 = continuation sheet 1
- E2 = continuation sheet 2
- K  = rigid distal skeleton

## Control actions

- tau: toggle H <-> O coupling
- sigma: toggle H <-> E1 coupling
- A: swap E1/E2 at the anchor and rearm O

## Test

A toy automaton passes its first test only if its local descent reproduces:

- anchored control surface
- rigid distal backbone
- mixed cancellation class
- bridge-signature degeneracy between (0,0,1) and (1,1,0)

