# ACTION_FRAME2_SLOT4_LOCK_NOTE_2026-03-31

## Status

Working obstruction note.

This note records the current local transition-law result for the frame-2 near-action corridor and states the strongest current obstruction law suggested by the evidence.

---

## Executive summary

The frame-2 near-action bottleneck is now sharply localized.

The exact frame-2 target requires:

- normalized position 4 = `t2`

The recorded frame-2 near-action witnesses are all Hamming-1 from the exact frame-2 representative and differ only at that slot. A focused transition-law probe inside the frame-2 near-action corridor then shows:

- visited corridor states: 8
- exact frame-2 one-edit hits found: 0
- corridor `t2` examples found: 0
- off-corridor `t2` examples found: 0

The slot-4 values actually observed inside the corridor are:

- `t4`
- `o4`
- `s3`
- `s0`
- `s2`
- `s4`
- `t0`
- `t3`

but never `t2`.

The best current summary is:

> the frame-2 near-action corridor enforces a slot-4 lock: the exact-closing value `t2` at normalized position 4 is not observed under the explored corridor-preserving local dynamics.

---

## 1. Background

The current ladder already established:

1. baseline two-step lookahead gives monotone descent but no nontrivial exact repair
2. exact-preference resolves the dominant frame-0 reachable fringe
3. deeper chambers funnel into the frame-2 near-action fringe by depth 4
4. the frame-2 near-action witnesses are Hamming-1 from the exact frame-2 target and differ only at normalized position 4

So the active bottleneck was reduced to a one-slot question:

> why does normalized position 4 fail to become `t2` inside the frame-2 near-action channel?

---

## 2. Transition-law probe setup

A focused transition-law probe was run on the unique frame-2 Hamming-1 witnesses.

The probe:

- started from the 4 unique normalized frame-2 witness states
- explored only the frame-2 near-action corridor
- tracked slot-4 values under one-edit transitions
- recorded whether any move produced:
  - exact frame-2 closure
  - slot-4 = `t2` while staying in the frame-2 corridor
  - slot-4 = `t2` off-corridor inside this corridor-restricted exploration

---

## 3. Main result

Headline result:

- start_count = 4
- visited_corridor_state_count = 8
- exact_frame2_one_edit_hits_found = 0
- corridor_t2_examples_found = 0
- off_corridor_t2_examples_found = 0

So within the explored frame-2 corridor dynamics:

- exact frame-2 closure is not observed
- slot 4 never becomes `t2`
- not even a `t2` example that leaves the corridor is observed inside this restricted search

This is a strong negative result.

---

## 4. Slot-4 values observed in the corridor

Observed slot-4 values among visited corridor states:

- `t4`
- `o4`
- `s3`
- `s0`
- `s2`
- `s4`
- `t0`
- `t3`

Not observed:

- `t2`

So the corridor supports a small alphabet of stable or recurrent wrong values at the locked slot, but excludes the exact one.

---

## 5. Dominant local transition pattern

The most common transitions inside the explored corridor are persistence transitions that keep the current slot-4 value unchanged while remaining action-cell-nearest at distance 2.

Examples:

- `t4 -> t4`, action-cell, nearest, `d_A = 2`, count 27
- `t0 -> t0`, action-cell, nearest, `d_A = 2`, count 27
- `t3 -> t3`, action-cell, nearest, `d_A = 2`, count 27
- `s3 -> s3`, action-cell, nearest, `d_A = 2`, count 25
- `s2 -> s2`, action-cell, nearest, `d_A = 2`, count 25
- `s4 -> s4`, action-cell, nearest, `d_A = 2`, count 25
- `o4 -> o4`, action-cell, nearest, `d_A = 2`, count 24
- `s0 -> s0`, action-cell, nearest, `d_A = 2`, count 24

So the corridor exhibits strong slot-value persistence.

---

## 6. What happens when the slot value changes

When the slot value is pushed toward alternatives such as `s2`, the resulting transitions are typically not exact-closing and do not remain cleanly in the corridor.

Typical examples:

- `t4 -> s2`, unresolved, ambiguous, `d_A = 5`, count 13
- `s3 -> s2`, unresolved, ambiguous, `d_A = 5`, count 11
- `s4 -> s2`, unresolved, ambiguous, `d_A = 5`, count 10
- `t0 -> s2`, unresolved, ambiguous, `d_A = 5`, count 10
- `t3 -> s2`, unresolved, ambiguous, `d_A = 5`, count 10
- `o4 -> s2`, unresolved, ambiguous, `d_A = 5`, count 9

So attempts to alter the slot toward nearby alternatives tend to eject the state into unresolved ambiguous regions at larger action distance rather than into exact frame-2 closure.

This is the central local mechanism currently visible.

---

## 7. Best current obstruction law

The strongest current experimental obstruction law is:

> In the frame-2 near-action corridor, normalized position 4 behaves as a locked slot. The exact-closing value `t2` is not observed. Corridor-preserving local dynamics overwhelmingly retain the current wrong slot-4 value, while many slot-changing moves lead out of the corridor into unresolved ambiguous regions at substantially larger action distance rather than toward exact frame-2 closure.

This is the clearest current explanation of why the frame-2 door remains shut.

---

## 8. Cube-walk translation

In walk-around-the-cube language:

- the walker can move around the frame-2 balcony
- that balcony admits several stable foot placements
- but the one exact foot placement needed to open the door, `t2` in the locked socket, never appears
- when the walker shifts weight toward nearby alternatives, it usually slips off the balcony into a confused region rather than stepping through the door

So the obstruction is no longer just “there is no closure.”

It is:

- a stable balcony
- a locked socket
- and a missing key value

---

## 9. What is now resolved

Resolved:

- the frame-2 bottleneck is a slot-4 installation problem
- the exact-closing value required there is `t2`
- the explored corridor dynamics do not produce `t2`
- the corridor supports a small stable alphabet of wrong slot-4 values instead
- many slot-changing moves increase disorder and leave the clean near-action regime rather than producing exact closure

---

## 10. What remains open

Open:

- whether `t2` at slot 4 is globally reachable only by leaving the frame-2 corridor first
- whether a deliberate escape-and-return policy can install `t2`
- whether the slot-4 lock is enforced by a deeper invariant of the move grammar
- whether a larger but targeted search can find a controlled off-corridor route back into exact frame-2 closure

---

## 11. Best short summary

The frame-2 door is now a one-slot lock.

The missing key is `t2` at normalized position 4, and the local corridor dynamics do not install it.

Or more compactly:

> the balcony is stable, but the key never reaches the lock.

