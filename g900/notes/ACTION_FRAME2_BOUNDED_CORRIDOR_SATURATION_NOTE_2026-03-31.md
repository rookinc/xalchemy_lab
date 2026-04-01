# ACTION_FRAME2_BOUNDED_CORRIDOR_SATURATION_NOTE_2026-03-31

## Status

Working computational saturation note.

This note records the bounded escape-and-return depth sweep on the unique frame-2 witness states and states the strongest current saturation result for the frame-2 slot-4 obstruction.

---

## Executive summary

The bounded escape-and-return search regime around the frame-2 witness states appears saturated by depth 6.

Starting from the 4 unique frame-2 witness states, and allowing exploration up to:

- max action distance = 3
- depths 4, 5, 6, 7, 8

the sweep yields at every tested depth:

- `has_exact_frame2_count = 0`
- `has_frame2_d1_count = 4`
- `has_t2_anywhere_count = 0`
- `has_t2_in_frame2_d1_count = 0`

So within this bounded regime:

- exact frame-2 closure is never observed
- the exact slot value `t2` is never observed at all
- all 4 starts remain connected to the frame-2 near-action channel

The key saturation signal is the visited-state count:

- depth 4: 41086
- depth 5: 57827
- depth 6: 58624
- depth 7: 58624
- depth 8: 58624

So the explored bounded corridor closes under search by depth 6. Additional depth up to 8 produces no new reachable states in this regime.

The best current summary is:

> the bounded frame-2 escape-and-return corridor saturates by depth 6 without ever producing `t2` at normalized position 4 or exact frame-2 closure.

---

## 1. Background

Earlier stages of the computational ladder established:

1. the baseline two-step rule is monotone in normalized action distance on the sampled run but has no nontrivial exact closure
2. exact-preference repairs the dominant frame-0 reachable fringe
3. deeper side chambers feed the frame-2 near-action bottleneck by depth 4
4. the frame-2 near-action witnesses are all Hamming-1 from the exact frame-2 representative
5. every such mismatch occurs at normalized position 4
6. the exact frame-2 target requires `t2` at that slot
7. a strict corridor probe to depth 6 does not install `t2`
8. a bounded escape-and-return probe to depth 6 with allowed action distance up to 3 also does not reach exact frame-2 closure

The natural next question was:

> does the key appear at larger depth in the same bounded regime, or does the bounded regime itself saturate?

This note answers that question.

---

## 2. Depth sweep setup

A depth sweep was run on the 4 unique frame-2 witness starts using the bounded escape-and-return vessel with:

- max action distance = 3
- depths = 4, 5, 6, 7, 8

For each depth, the sweep recorded:

- whether exact frame-2 closure appeared
- whether the frame-2 near-action channel remained reachable
- whether `t2` appeared anywhere in the explored state set
- whether `t2` appeared specifically inside the frame-2 near-action channel
- total visited-state count
- slot-4 value histogram
- runtime

---

## 3. Uniform negative result across the full sweep

At every tested depth 4 through 8:

- `has_exact_frame2_count = 0`
- `has_frame2_d1_count = 4`
- `has_t2_anywhere_count = 0`
- `has_t2_in_frame2_d1_count = 0`

So across the entire bounded sweep:

- exact frame-2 closure is never observed
- `t2` never appears at all
- all 4 starts remain connected to the frame-2 near-action channel

This means the failure is not simply “we stopped too early.”

The bounded search regime has been pushed far enough to observe its stabilization behavior.

---

## 4. Saturation of the reachable bounded corridor

The decisive signal is the growth of the visited-state count.

Observed totals:

- depth 4: 41086
- depth 5: 57827
- depth 6: 58624
- depth 7: 58624
- depth 8: 58624

The state count grows significantly from depth 4 to 5, then only slightly from 5 to 6, and then remains unchanged from depth 6 onward.

So the bounded regime appears to have reached closure under exploration by depth 6.

In other words:

- depth 7 does not reveal new states
- depth 8 does not reveal new states
- deeper search in this same regime is no longer opening new geometry

This is the strongest computational sign so far that the current bounded frame-2 regime has been exhausted.

---

## 5. Slot-4 alphabet in the saturated bounded regime

Even as the bounded corridor saturates, the slot-4 alphabet remains broad but excludes the exact key value.

Observed slot-4 histograms at the saturated depths include values such as:

- `o4`
- `s0`
- `s2`
- `s3`
- `s4`
- `t0`
- `t3`
- `t4`
- `o0`
- `o1`
- `o2`
- `o3`

But never:

- `t2`

So the saturation result is not merely “no exact closure happened.”

It is stronger:

> the explored bounded regime never even generates the exact slot value required by the frame-2 target.

That is the clearest current computational expression of the slot-4 lock.

---

## 6. Runtime profile

Wall-time profile of the sweep:

- depth 4: 10.583 s
- depth 5: 19.448 s
- depth 6: 23.743 s
- depth 7: 24.979 s
- depth 8: 24.732 s

This runtime profile mirrors the state-count plateau:

- major growth to depth 5
- small additional growth to depth 6
- saturation beyond depth 6

So the computational evidence and the runtime evidence agree:

- this bounded regime is essentially exhausted by depth 6

The reported `cpu_seconds_parent_only` values are not a measure of total worker CPU and should not be used for cross-depth cost comparison. The meaningful timing metric here is wall time.

---

## 7. Best current obstruction statement

The strongest current bounded-regime obstruction statement is:

> Within the bounded escape-and-return regime defined by maximum action distance 3, the frame-2 witness dynamics saturate by depth 6. Across the saturated reachable set, exact frame-2 closure is never observed and the required slot-4 value `t2` never appears. The bounded frame-2 corridor therefore excludes the exact key within the explored regime.

This is stronger than a mere depth-limited negative search.

It is a saturation result.

---

## 8. Cube-walk translation

In walk-around-the-cube language:

- the walker can roam not just on the frame-2 balcony, but a bounded region around it
- this bounded region has now been fully explored, at least within the allowed corridor width
- the walker can return to the balcony from anywhere in that bounded region
- but nowhere in that region does the correct key appear
- the door remains shut not because the walker did not look far enough inside the bounded neighborhood, but because the bounded neighborhood itself contains no seated key

So the current reading is:

- the balcony is stable
- the local neighborhood around it has been explored
- the key is absent from that whole bounded neighborhood

---

## 9. What is now resolved

Resolved:

1. The bounded frame-2 escape-and-return regime saturates by depth 6.
2. Exact frame-2 closure is not observed anywhere in that saturated regime.
3. The exact slot value `t2` is not observed anywhere in that saturated regime.
4. The frame-2 near-action channel remains reachable throughout, so the failure is not due to loss of contact with the frame-2 side.

These points together make the bounded obstruction result much stronger than the earlier corridor-only statement.

---

## 10. What remains open

Open:

1. Whether `t2` is reachable only in a qualitatively broader regime than action distance <= 3.
2. Whether a deeper invariant forbids `t2` from normalized position 4 in the bounded frame-2 channel.
3. Whether the observed slot-4 alphabet is governed by a symbolic, parity, or orbit constraint.
4. Whether a theorem can be stated for the bounded regime itself, independent of what may happen globally.

The natural next move is no longer “search deeper in the same regime.”

The natural next move is either:

- prove the bounded-regime obstruction
or
- enlarge the regime in a qualitatively different way

---

## 11. Best theorem-shaped statement

A clean theorem-shaped formulation suggested by the evidence is:

> Let the bounded frame-2 escape-and-return regime be the set of states reachable from the unique frame-2 witness starts under the local move grammar while remaining within action distance at most 3. This regime saturates computationally by depth 6. Within that saturated regime, exact frame-2 closure is not observed, and the exact slot value `t2` required at normalized position 4 never appears. The current evidence therefore supports a bounded-regime slot-4 obstruction law for frame 2.

This is not yet a universal proof, but it is a sharply localized and computationally saturated obstruction result.

---

## 12. Best short summary

The bounded neighborhood around the frame-2 balcony has now been exhausted.

The key `t2` never appears there, and the door never opens.

Or more compactly:

> the bounded corridor saturates, and the key is nowhere inside it.

