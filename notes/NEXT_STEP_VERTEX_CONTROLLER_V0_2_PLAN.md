# Next Step: Vertex Controller v0.2 Plan

## Goal

Move from:

- runtime-only local routing controller

to:

- local routing controller with explicit structural state.

That means the controller should carry both:

1. structural local law
2. transient routing memory

---

## 1. New structural fields

Extend the controller with:

- `anchored_chart` in `{0,1}`
- `sigma_state` in `{0,1}`
- `tau_state` in `{0,1}`

These correspond to the canonical local state register:

\[
(A,\sigma,\tau)
\]

and should be treated as controller-law state, not transient switch memory.

---

## 2. Keep runtime fields separate

Retain the current runtime layer:

- `switch_state`
- `switch_cooldown_remaining`
- `route_counts`
- `recent_arrivals`
- `classes_seen`
- `coupling_count`
- `controller_events`

Canonical sentence:

Structural state says what kind of controller this vertex is.
Runtime state says how it is behaving right now.

---

## 3. First routing-law integration targets

The first controller laws that should become structural-state aware are:

### A-sensitive routing
Let `anchored_chart` alter local handedness interpretation or candidate preference ordering.

### sigma-sensitive routing
Let `sigma_state` favor or enable E1-oriented exits.

### tau-sensitive routing
Let `tau_state` favor or enable odd-branch exits.

### burden interaction
Let burden override still operate, but within the chart-conditioned exit ordering.

So the controller becomes:

- chart-aware
- branch-aware
- sheet-aware
- burden-aware

---

## 4. Minimal v0.2 object shape

    VertexController
      vertex_id
      incident_edges
      routing_bias
      load_override_threshold

      anchored_chart
      sigma_state
      tau_state

      switch_state
      switch_cooldown_remaining
      route_counts
      recent_arrivals
      classes_seen
      coupling_count
      controller_events
      tags

---

## 5. Event log upgrade

When structural state matters, event receipts should also record it.

Suggested additions to controller events:

- `anchored_chart`
- `sigma_state`
- `tau_state`

That way route receipts can be audited against controller-law state.

---

## 6. First implementation sequence

### Step 1
Extend the dataclass with:
- `anchored_chart`
- `sigma_state`
- `tau_state`

### Step 2
Emit these values in controller events.

### Step 3
Add one new routing mode:

- `chart_sensitive`

### Step 4
Define the first chart-sensitive preference law:
- `A=0` favors odd/E1 interpretation
- `A=1` favors E2-dominant interpretation

### Step 5
Keep `polarity_under_load` as the burden override layer on top of that chart-sensitive preference.

---

## 7. Strongest current implementation target

The first real synthesis target is:

> a vertex controller whose routing decisions depend both on transient burden memory and on the canonical structural local register `(A,sigma,tau)`.

That would be the first controller that genuinely unifies the local state-space work with the trurtle runtime.

