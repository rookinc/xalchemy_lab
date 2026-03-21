# Ledger Additivity Probe

## Question

Does the hub ledger behave additively under split triadic input?

Equivalently:

- is one large coherent closure equivalent to two smaller coherent closures with the same total incoming stress?
- or does the ledger preserve path-sensitive memory beyond total deposited quantity?

## Test design

For a fixed coherent +++ triad at u1R with zero mismatch:

- Path A: apply one triadic closure with stress vector S
- Path B: apply two triadic closures with stress vectors A and B such that A + B = S componentwise

Compare:

- final carrier stress
- final ledger tuple:
  - stress_energy
  - stored_tension
  - deposited_stress
  - clean_closures
  - tension_closures

## Interpretation target

If Path A and Path B differ, then the ledger is not merely additive.
It is path-dependent under decomposition of the same total incoming load.

That would mean the ledger records more than quantity:
it records structure of arrival history.
