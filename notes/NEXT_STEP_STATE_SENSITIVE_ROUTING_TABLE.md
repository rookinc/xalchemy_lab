# Next Step: State-Sensitive Routing Table

## Goal

Replace the current coarse `_state_sensitive_choice()` rule with an explicit local routing table that makes the structural controller register

- `A`
- `sigma`
- `tau`

matter in a clearer and more inspectable way.

This is not yet the final law.
It is the first table-driven semantic refinement.

---

## 1. Design principle

The controller should choose an outgoing edge using four inputs:

- incoming edge
- handedness
- anchored chart `A`
- structural bits `sigma` and `tau`

Canonical sentence:

Handedness orients the choice, chart selects the local frame, and sigma/tau perturb that frame lawfully.

---

## 2. Minimal test setting

For the first table, use the smallest meaningful controller:

- one incoming edge: `e_in`
- two legal exits: `e_left`, `e_right`

This is enough to expose:

- chart reversal
- sigma bias
- tau bias
- override under burden

---

## 3. Proposed interpretation of the bits

### A = anchored chart selector
This chooses the base orientation of the local controller.

- `A = 0` = odd / E1 chart
- `A = 1` = E2-dominant chart

### sigma = E1-sensitive bias
This perturbs the chart toward E1-style continuation.

### tau = odd-branch-sensitive bias
This perturbs the chart toward odd-branch continuation.

### handedness
This resolves local orientation inside the current chart.

---

## 4. First explicit routing table

For the degree-3 controller with exits `{e_left, e_right}`:

### Chart A = 0

#### State 000
- left  -> `e_left`
- right -> `e_right`

#### State 001
- left  -> `e_right`
- right -> `e_right`

Interpretation:
- odd branch is dominant

#### State 010
- left  -> `e_left`
- right -> `e_left`

Interpretation:
- E1 bias dominates local continuation

#### State 011
- left  -> `e_right`
- right -> `e_left`

Interpretation:
- sigma and tau compete, producing a handed split

---

### Chart A = 1

#### State 100
- left  -> `e_right`
- right -> `e_left`

Interpretation:
- chart reversal relative to 000

#### State 101
- left  -> `e_left`
- right -> `e_left`

Interpretation:
- odd-branch bias perturbs the reversed chart

#### State 110
- left  -> `e_right`
- right -> `e_right`

Interpretation:
- E2-dominant continuation remains strong

#### State 111
- left  -> `e_left`
- right -> `e_right`

Interpretation:
- symmetric mixed state in the A=1 chart

---

## 5. Why this table is useful

This table is not claimed as final truth.

It is useful because it guarantees that the eight structural states do not collapse trivially.

In particular, it makes all of the following visibly distinct:

- `001` vs `011`
- `100` vs `111`
- `A=0` vs `A=1`

That is exactly what the first-pass rule failed to do.

---

## 6. Table form

Compactly:

| state | left  | right |
|------:|:------|:------|
| 000 | e_left  | e_right |
| 001 | e_right | e_right |
| 010 | e_left  | e_left |
| 011 | e_right | e_left |
| 100 | e_right | e_left |
| 101 | e_left  | e_left |
| 110 | e_right | e_right |
| 111 | e_left  | e_right |

---

## 7. Operational use

The controller should use this table as the base preference law when:

- `routing_bias = state_sensitive`

Then:

- `state_sensitive_under_load` should use the same table for preferred exit selection,
- but allow burden override to divert to the alternate when imbalance exceeds threshold.

So the order becomes:

1. structural state chooses preferred exit
2. burden law may override that choice
3. runtime switch state records whether yielding occurred

---

## 8. Strongest consequence

Once this table is used, the controller becomes:

- structurally stateful
- visibly nontrivial across all 8 states
- still local
- still deterministic
- still compatible with burden override

That is the next real semantic refinement.

