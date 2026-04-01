# Theorem Status Report

- Scale: `1`
- Overall status: **verified-with-modeled-bridge**

## Current strongest supported statement

In the current bridge model, the puncture is realized as the visible shadow of a unique illegal exact core together with a one-step causal fringe. The non-retained set, the sheet-illegal set, and the core-plus-fringe set coincide. Across the tested bridge families and operator families, the uniqueness of the exact core and the failure = illegality = core-plus-fringe structure remain stable, while the fringe size varies with the continuation law.

## Verified laws

- slot4 machine shape
- scaffold rigidity
- socket fixation
- payload alphabet
- exact payload exclusion
- rigid/variable edge split
- subjective/objective family doctrine
- G15/G30 sign-sheet readout
- native lifted state schema
- visible projection forgetting sheet
- native sheet flip operator law

## Modeled bridge laws

- retained predicate
- sheet-legal predicate
- retained iff sheet-legal local layer
- retained as no-escape continuation
- exact forbidden state detection
- exact forbidden state is non-retained
- exact forbidden state is sheet-illegal
- failure set equals illegality set
- forbidden core plus one-step fringe
- fringe feeds exact core in one step
- puncture as derived core-plus-fringe shadow
- bridge-family robustness testing
- bridge-operator robustness testing
- unique exact core is operator-invariant
- failure equals illegality is operator-invariant
- core-plus-fringe decomposition is operator-invariant
- retained iff sheet-legal is operator-invariant
- fringe size is operator-sensitive
- puncture equals sheet shadow in current model
- failure-type exhaustion
- upstairs residual obstruction

## Operator and robustness findings

- Unique exact core is operator-invariant: **yes**
- Failure = illegality is operator-invariant: **yes**
- Core-plus-fringe decomposition is operator-invariant: **yes**
- Fringe size is operator-sensitive: **yes**
- Bridge-family robustness section passed: **yes**

## Section status table

| Section | Status | Passed |
|---|---|---|
| `slot4_machine` | `verified` | `True` |
| `family_doctrine` | `verified` | `True` |
| `so_doctrine` | `verified` | `True` |
| `lifted_machine` | `verified` | `True` |
| `bridge_predicates` | `modeled` | `True` |
| `causal_bridge` | `modeled` | `True` |
| `forbidden_fringe` | `modeled` | `True` |
| `fringe_dynamics` | `modeled` | `True` |
| `derived_bridge` | `modeled` | `True` |
| `bridge_family` | `modeled` | `True` |
| `bridge_operator_family` | `modeled` | `True` |
| `bridge_operator_invariants` | `modeled` | `True` |
| `bridge_summary` | `modeled` | `True` |
| `bridge` | `modeled` | `True` |

## Bridge summary

- **puncture_equals_sheet_shadow_in_current_model**: yes — In the current bridge model, the puncture is the visible shadow of the illegal exact core and its one-step fringe.
- **full_causal_theorem_still_open**: yes — This stronger statement has not yet been derived for the full intended bridge dynamics.

## Derived bridge statement in the current model

- **unique_exact_core**: yes — The bridge has a unique exact forbidden t2 core.
- **core_is_illegal_and_non_retained**: yes — The exact core is both non-retained and sheet-illegal.
- **failure_equals_illegality**: yes — Failure and illegality sets coincide at the current bridge layer.
- **failure_equals_core_plus_fringe**: yes — The common failure/illegality set is exactly the exact core plus its one-step fringe.
- **puncture_equals_sheet_shadow_modeled**: yes — At the current bridge model, the puncture is realized as the visible shadow of the illegal core, with fringe determined by one-step continuation.

## Open statements

- retained iff sheet-legal as causal bridge theorem
- puncture = sheet shadow beyond the current bridge model
- full causal theorem beyond the current bridge model

## Note

This report is generated directly from the witness-machine verifier and is intended to summarize the current machine-supported theorem posture without overstating beyond-model claims.

