# Next Step: Vertex Controller Synthesis

## Status

We now have two strong local layers:

1. a canonical local state-space law
2. a working local transport controller runtime

These should not be treated as competing descriptions.
They appear to be adjacent layers of the same machine.

---

## 1. What is already present

### Canonical local state layer

We already have a local structural register

\[
(A,\sigma,\tau)\in \mathbb Z_2^3
\]

with current meanings:

- `A` = anchored chart selector
- `sigma` = E1-sheet activation
- `tau` = odd-branch activation

This layer tells us:

- what local lawful states exist
- how the anchored chart splits
- what remains rigid
- what the quotient bridge signature is
- how the local state is projected into receipt space

### Vertex controller layer

We now also have a working local routing controller with:

- arrivals
- routing decisions
- event receipts
- local route counts
- burden-sensitive override
- cooldown / switch recovery
- deterministic local policy

This layer tells us:

- how local informative transport is routed
- how burden modifies polarity
- how local memory accumulates
- how routing receipts are logged

---

## 2. Strongest current synthesis

The current best reading is:

- the canonical local state-space describes the **structural local law**
- the vertex controller describes the **runtime local routing law**

So the system now appears to want two controller layers:

### Structural controller state
longer-lived local law

- anchored chart
- sheet activation
- odd-branch activation
- sector / face / local orientation tags

### Runtime controller state
short-horizon routing memory

- switch state
- cooldown remaining
- route counts
- recent arrivals
- coupling count
- classes seen

Canonical sentence:

The local state register determines what kind of controller the vertex is.
The runtime controller state determines how it is behaving right now.

---

## 3. What should not be done

It would be a mistake to identify `(A,sigma,tau)` directly with the current `switch_state`.

Reason:

- `(A,sigma,tau)` is structural / chart-level local law
- `switch_state` is transient routing memory

So these should remain distinct.

Do not force chart structure into the override/cooldown mechanism.

---

## 4. Proposed controller extension

The `VertexController` should eventually gain an explicit structural controller register.

Minimal proposal:

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

Suggested meanings:

- `anchored_chart` in `{0,1}` corresponds to `A`
- `sigma_state` in `{0,1}` corresponds to `sigma`
- `tau_state` in `{0,1}` corresponds to `tau`

This preserves the distinction between:

- structural controller law
- transient routing state

---

## 5. First mapping hypothesis

Current best mapping hypothesis:

### Structural fields

- `A` controls chart selection and local controller interpretation
- `sigma` controls E1-facing activation / routing openness
- `tau` controls odd-branch activation / handedness-sensitive branch openness

### Runtime fields

- `switch_state` records whether polarity has recently yielded
- `switch_cooldown_remaining` records temporary memory after override
- `route_counts` records local burden history
- `recent_arrivals` records short-horizon traffic memory
- `coupling_count` records interaction history

So the state register should sit above the current runtime controller.

---

## 6. Relation to earlier burden work

The current `polarity_under_load` controller appears to be the runtime distillation of the earlier burden / polarity / override experiments.

That is a major gain.

Current operational form:

- choose preferred exit by handedness
- compare preferred vs alternate route counts
- override polarity when imbalance exceeds threshold
- record override
- move into temporary flipped state
- recover through cooldown

Canonical sentence:

The earlier burden experiments now have a lawful runtime controller form.

---

## 7. Relation to edges

The current controller preserves the excellent separation:

- edge carries residue
- vertex decides flow

This should be retained.

However, `route_counts` is currently standing in for burden.
That is acceptable for v0.1, but later we may want distinct edge-side fields such as:

- `touch_count`
- `burden`
- `residue`
- `freshness`
- `class_presence`

because least-used and least-burdened are not always identical.

For now this simplification is acceptable.

---

## 8. What this unlocks

Once the structural state register is bound into the vertex controller, the project will have:

- a local state law
- a local routing law
- a runtime receipt system
- a local controller object that can be simulated and audited

That would mean the project has moved from:

- static local structure

to

- dynamic local transport on top of lawful local structure

This is likely the next major synthesis step.

---

## 9. Best next implementation step

The next clean implementation target is:

### v0.2 Vertex Controller
Add structural local state fields:

- `anchored_chart`
- `sigma_state`
- `tau_state`

Then allow routing rules to read both:

- structural state
- runtime state

This would allow future policies such as:

- chart-sensitive handedness
- sigma-gated E1 preference
- tau-gated odd branching
- chart-conditioned burden yielding

---

## 10. Strongest current summary

The canonical local state-space and the vertex controller now look like two halves of the same machine.

The state-space tells us what the lawful local states are.
The controller tells us how informative transport moves through them.

The next step is to bind `(A,sigma,tau)` into the controller as structural state, while preserving `switch_state` as transient routing memory.

