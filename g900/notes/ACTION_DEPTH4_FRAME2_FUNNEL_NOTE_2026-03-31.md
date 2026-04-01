# ACTION_DEPTH4_FRAME2_FUNNEL_NOTE_2026-03-31

## Status

Working computational note.

This note records the depth-4 result on the 20-state unresolved depth-3 core and clarifies how that core relates to the frame-2 near-action obstruction.

---

## Executive summary

The depth-4 probe completely opens the 20-state unresolved depth-3 core to the near-action fringe, but not to exact closure.

Headline result:

- unresolved depth-3 starts scanned: 20
- with any <=4-step exact hit: 0
- with any <=4-step action-cell distance-1 hit: 20
- with any <=4-step distance-1 hit nearest to frame 2: 20

So every state in the depth-3 unresolved core reaches the near-action fringe by depth 4, and every one of those routes touches the frame-2 side of the action family.

This means the frame-1 / frame-4 chamber identified at depth 3 is not a permanently isolated residual chamber.

It is a deeper feeder chamber into the frame-2 near-action obstruction.

The best current summary is:

> the depth-3 unresolved frame-1/frame-4 chamber fully funnels into the frame-2 near-action fringe by depth 4, but still does not reach exact closure.

---

## 1. Background

Before this depth-4 probe, the computational ladder had established the following:

### 1.1 Baseline two-step rule

- monotone descent in normalized action distance
- no nontrivial exact closures

### 1.2 Exact-preference patch

- resolves the dominant frame-0 reachable fringe
- produces 402 / 599 exact repairs
- preserves monotonicity

### 1.3 Residual near-action obstruction

- a 71-state residual distance-1 fringe
- all nearest to frame 2
- no exact one-edit closure

### 1.4 Hard d2 shell and depth-3 split

A depth-3 probe of the hard 63-state d2 shell showed:

- 43 states admit a <=3-step distance-1 action-cell hit
- 20 remain unresolved at depth 3
- none reaches exact closure within depth 3

Those unresolved 20 then clustered as:

- 13 nearest to frame 1
- 7 nearest to frame 4

So the depth-3 unresolved core appeared as a frame-1 / frame-4 side chamber.

---

## 2. Depth-4 result on the unresolved 20

The depth-4 parallel probe on the unresolved 20 gives:

- has_4step_exact = 0
- has_4step_d1 = 20
- to_frame2_d1 = 20

Therefore:

1. every one of the 20 unresolved states reaches an action-cell distance-1 state within depth 4
2. every one of those states reaches a distance-1 state nearest to frame 2
3. none reaches exact closure within depth 4

This is the decisive geometric clarification.

The frame-1 / frame-4 chamber is not permanently separate. It is a deeper route into the frame-2 obstruction fringe.

---

## 3. Target distribution of depth-4 distance-1 hits

The depth-4 output reports the aggregate nearest-target distribution for the newly found distance-1 hits as:

- frame 0:
  `o2 | s2 | t0 | s0 | t3 | s3`
  count = 214

- frame 2:
  `o4 | s4 | t2 | s2 | t0 | s0`
  count = 99

This tells us two things.

### 3.1 The depth-4 chamber is not rigidly single-target at the level of all discovered distance-1 hits

Even though every unresolved start reaches some frame-2 distance-1 hit, the set of all discovered depth-4 distance-1 hits also includes many frame-0-nearest hits.

So the chamber is not combinatorially collapsing onto a single unique terminal string or even a single target frame at the level of all reachable d1 states.

### 3.2 Frame 2 is still the decisive bottleneck

Despite that broader set of d1 hits, the probe-level summary shows:

- all 20 starts have at least one <=4-step d1 hit nearest to frame 2

So frame 2 remains the meaningful obstruction target.

---

## 4. Geometric interpretation

The chamber picture must now be refined.

### 4.1 Earlier picture

At depth 3, the unresolved 20 looked like a separate frame-1 / frame-4 chamber.

### 4.2 Updated picture

At depth 4, that chamber is no longer isolated.

Instead it behaves as:

- a deeper feeder chamber
- which opens into the frame-2 near-action fringe
- but still not into exact closure

So the current residual basin is better described as a layered funnel:

1. frame-0 reachable fringe, repaired by exact-preference
2. frame-2 blocked near-action fringe, still exact-resistant
3. frame-1 / frame-4 deeper feeder chamber, which enters the frame-2 fringe by depth 4

This is a much stronger structural statement than the earlier “three disjoint chambers” reading.

The deeper chamber is not independent. It feeds the blocked core.

---

## 5. Runtime note

The depth-4 probe reported:

- wall_seconds ≈ 224.753
- cpu_seconds ≈ 0.0217
- max_rss_mb ≈ 22.14

Interpretation:

- the wall time is meaningful as end-to-end elapsed time
- the cpu_seconds value is not a valid measure of total worker CPU for the whole multi-process job, because it only reflects the parent coordinator process
- the memory figure likewise reflects the parent process, not total worker memory

So for cross-depth comparison of multi-process runs, the reliable metric here is:

- wall_seconds

The depth-4 result therefore carries a concrete computational cost of roughly 225 seconds at the chosen worker count.

---

## 6. What is now resolved

The following are now resolved.

### 6.1 Fate of the unresolved 20

Resolved:

- all 20 open to action-cell distance 1 by depth 4

### 6.2 Relation to frame 2

Resolved:

- all 20 have a <=4-step route to a frame-2-nearest distance-1 state

### 6.3 Exactness

Resolved:

- none of the 20 reaches exact closure within depth 4

### 6.4 Chamber interpretation

Resolved:

- the frame-1 / frame-4 depth-3 unresolved chamber is not isolated
- it is a deeper feeder chamber into the frame-2 near-action obstruction

---

## 7. What remains open

The remaining questions are now much narrower.

### 7.1 Why is frame 2 still blocked?

We now know multiple outer chambers can feed the frame-2 near-action fringe, but exact closure is still absent.

So the real bottleneck is now unmistakably the frame-2 near-action obstruction itself.

### 7.2 Does frame 2 open at depth 5 or beyond?

We do not yet know whether the frame-2 distance-1 obstruction yields to deeper nonexpansive search, or whether it represents a more fundamental obstruction under the current move grammar.

### 7.3 Which depth-4 d1 hits are operationally useful?

The aggregate d1 target distribution includes both frame-0 and frame-2 hits.

We have not yet extracted the actual depth-4 frame-2-nearest d1 witnesses for direct inspection.

That is the next surgical target.

---

## 8. Best current theorem-shaped statement

A clean theorem-style formulation suggested by the evidence is:

> After exact-preference resolves the dominant frame-0 selection failure, the remaining residual basin funnels toward the frame-2 near-action obstruction. The depth-3 unresolved frame-1 / frame-4 chamber is not isolated; by depth 4 every one of its 20 states reaches action-cell distance 1, and every state has a route to a frame-2-nearest distance-1 witness. None reaches exact closure within depth 4.

This is not yet a universal proof, but it is now a sharply structured and layered result.

---

## 9. Best short summary

The deeper side chamber is real, but it is not separate.

It feeds the same blocked frame-2 bottleneck.

Or more compactly:

> depth 4 routes the side chamber into frame 2, but the door is still shut.

