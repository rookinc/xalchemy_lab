# Predicted Framed Signature Result Template

## Goal

Test whether the framed signature `(H,S)` can be predicted directly from controller-state sequence and handedness inputs.

## Inputs

- controller sequence `(A,sigma,tau)`
- handedness sequence

## Predicted outputs

- chart trace
- transition signs
- `H`
- `S`

## Comparison

For each loop compare:

- predicted chart trace vs observed chart trace
- predicted signature vs observed signature

## Strongest sentence

The framed signature becomes structurally stronger if it can be predicted from controller-state sequence before runtime replay.

