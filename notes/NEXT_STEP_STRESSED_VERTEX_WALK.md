# Next Step: Stressed Vertex Walk

## Status

The current vertex walk demo proves that the runtime stack is alive:

- trurtles move
- controllers route locally
- edges accumulate transport history
- controller route counts update
- export is written successfully

However, the current demo does **not** yet exercise the most distinctive controller feature:

- burden-sensitive polarity override

In the current run:

- all routes completed with `override=false`
- all controllers remained in `switch_state=neutral`
- no cooldown recovery sequence was triggered from a real override

So the runtime is alive, but the burden-yielding controller has not yet been forced to reveal itself.

---

## Goal

Construct a stressed local walk that forces a `polarity_under_load` controller to:

1. build imbalance on the preferred exit,
2. exceed the burden threshold,
3. reroute through the alternate edge,
4. enter `switch_state=flipped`,
5. emit override receipts,
6. recover through cooldown.

This would be the first full demonstration of the controller's distinctive runtime behavior.

---

## Minimal target behavior

At least one controller event log should show:

- `override`
- `switch_to_flipped`
- `cooldown_tick`
- `switch_to_neutral`

And at least one trurtle route note should show:

- `override=true`

---

## Best test shape

The cleanest first stress test is not a large network.

It is a small hand-driven controller stress sequence at one vertex.

### Preferred target vertex shape

A degree-3 controller is ideal:

- one incoming edge
- two legal outgoing candidates
- handedness chooses one preferred exit
- repeated traffic loads the preferred exit
- threshold eventually forces diversion

This is the smallest setting where `polarity_under_load` can visibly differ from `handedness_first`.

---

## First experiment design

Use one controller:

- `routing_bias = polarity_under_load`
- `load_override_threshold = 1`
- `yield_cooldown_ticks = 2`

Then repeatedly feed arrivals that:

- enter on the same incoming edge
- carry the same handedness
- therefore keep preferring the same exit

As route counts build, the preferred exit should become overloaded relative to the alternate.

At that point the controller should yield and route to the alternate.

---

## Expected sequence

### Phase 1: baseline polarity loyalty
- preferred exit chosen
- no override
- switch state remains neutral

### Phase 2: threshold breach
- preferred exit is now sufficiently more burdened
- controller selects alternate
- `override=true`
- switch state becomes `flipped`

### Phase 3: cooldown recovery
- idle ticks decrement cooldown
- controller emits `cooldown_tick`
- controller returns to `neutral`

---

## Why this matters

This is not just a runtime curiosity.

It is the first concrete operational test of the burden / polarity / override logic that earlier existed only in experimental probe form.

Canonical sentence:

The earlier burden experiments become real once the controller is forced to yield under local imbalance.

---

## Best next step after this

Once a stressed vertex-walk demo successfully shows override and recovery, the next synthesis step is:

- bind `(A,sigma,tau)` into the controller as structural controller state

So the order should be:

1. prove burden-yielding runtime behavior
2. then synthesize canonical structural state into the controller

