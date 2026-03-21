# Stateful Controller Synthesis Result

## Result

The controller now carries explicit structural local state:

- anchored_chart = A
- sigma_state = sigma
- tau_state = tau

and preserves transient runtime state separately:

- switch_state
- cooldown
- route counts
- recent arrivals
- coupling history

This confirms the correct architectural split between:

- structural controller law
- transient routing memory

## Demonstrated gain

Event receipts now explicitly record:

- A
- sigma
- tau

So controller behavior can now be audited against canonical local structural state.

## Runtime result

The stateful controller demo shows:

- structural-state-dependent routing differences
- burden override still functioning under structural control
- transient flipped state preserved as runtime memory

In particular, the `(1,1,1)` example demonstrates:

- structural state present
- state-sensitive routing
- burden-triggered override
- switch-to-flipped transition

## Limitation

The current `_state_sensitive_choice()` is still a coarse first-pass rule.

Observed issue:
- `(0,0,1)` and `(0,1,1)` currently collapse to the same preferred exit behavior

So the structural binding is successful, but the state-sensitive routing semantics remain too weak.

## Next step

Refine the state-sensitive routing law so that:

- A selects chart orientation
- sigma produces a genuine E1-sensitive bias
- tau produces a genuine odd-branch-sensitive bias
- handedness resolves orientation within that chart

That is the next true semantic refinement step.

