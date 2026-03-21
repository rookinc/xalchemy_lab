# Next Symbolic Bridge Stress Test Note

## Goal

The current bridge table matches on the core named rows.

Before attempting a true signed-lift evaluator, the next safe step is to stress-test the provisional symbolic evaluator on nearby local words already present in the repo.

## Diagnostic rows to add

- `w_single_L1`
- `w_single_L2`
- `w_single_R1`
- `w_hold_then_LR`
- `w_LR_then_hold`
- `w_LL_then_LR`
- `w_two_LR`

## Provisional symbolic role assignments

- `w_single_L1` -> `global_square`
- `w_single_L2` -> `global_square`
- `w_single_R1` -> `global_square`
- `w_hold_then_LR` -> `global_return`
- `w_LR_then_hold` -> `global_return`
- `w_LL_then_LR` -> `global_twist`
- `w_two_LR` -> `global_return`

## What to look for

- Does local `lift_bit` still match the assigned symbolic global parity?
- Do composition-like words behave mod 2 the way the current lift law predicts?
- Are there rows that force a rethink of the symbolic role vocabulary?

## Why this matters

If the symbolic evaluator survives these extra rows, then the bridge vocabulary is likely coherent enough to justify a later upgrade to actual signed-lift data.

