# Next Step: Bind Structural State Into Controller

## Goal

Extend the vertex controller so that it carries both:

1. structural local state
2. transient routing memory

This is the first direct synthesis step between the canonical local state-space and the trurtle runtime.

## Structural controller state

Add:

- `anchored_chart` in `{0,1}`
- `sigma_state` in `{0,1}`
- `tau_state` in `{0,1}`

These correspond to the canonical local register:

\[
(A,\sigma,\tau)
\]

They are controller-law state, not transient runtime state.

## Runtime controller state

Keep separate:

- `switch_state`
- `switch_cooldown_remaining`
- `route_counts`
- `recent_arrivals`
- `classes_seen`
- `coupling_count`
- `controller_events`

Canonical sentence:

Structural state says what controller law is active.
Runtime state says how that controller is behaving right now.

## First v0.2 routing interpretation

### anchored_chart = 0
Odd / E1 chart

- left-handed preference should favor odd / E1-style local ordering
- `sigma_state = 1` may strengthen E1-like preference
- `tau_state = 1` may strengthen odd-branch preference

### anchored_chart = 1
E2-dominant chart

- right face / E2-oriented continuation becomes privileged
- `sigma_state` still matters for E1 mixed behavior
- `tau_state` still matters for odd-branch activation

## Minimal implementation strategy

Do not redesign the whole controller yet.

### Step 1
Add structural fields to `VertexController`.

### Step 2
Add these fields to emitted events and summaries.

### Step 3
Add a new routing bias:

- `state_sensitive`

### Step 4
Implement a minimal state-sensitive ordering rule:
- chart 0: left preference picks lowest candidate, right picks highest
- chart 1: reverse that base preference
- sigma / tau may optionally perturb the preferred edge rank

### Step 5
Allow `polarity_under_load` to operate on top of the state-sensitive preference.

## Strongest next target

A controller should make routing decisions using:

- incident edge structure
- burden memory
- handedness
- canonical structural local state `(A,sigma,tau)`

That will be the first true local synthesis of state law and runtime law.

