# State-Sensitive Routing Table Result

## Result

The controller now uses an explicit table-driven structural preference law for the minimal degree-3 case:

- incoming edge = `e_in`
- candidate exits = `e_left`, `e_right`

The structural controller register is:

- `A`
- `sigma`
- `tau`

and the table assigns a preferred exit for each handedness in each of the 8 states.

## Implemented table

| state | left | right |
|------:|:-----|:------|
| 000 | e_left  | e_right |
| 001 | e_right | e_right |
| 010 | e_left  | e_left |
| 011 | e_right | e_left |
| 100 | e_right | e_left |
| 101 | e_left  | e_left |
| 110 | e_right | e_right |
| 111 | e_left  | e_right |

## Consequence

This removes the earlier excessive collapse in the structural routing law and gives a more meaningfully differentiated first-pass v0.2 controller semantics.

## Runtime meaning

- `state_sensitive` uses the table directly
- `state_sensitive_under_load` uses the table as preferred exit law, then allows burden override and cooldown memory

## Next step

Push `anchored_chart`, `sigma_state`, and `tau_state` into the walk layer so controller summaries and walk receipts are structurally auditable.

