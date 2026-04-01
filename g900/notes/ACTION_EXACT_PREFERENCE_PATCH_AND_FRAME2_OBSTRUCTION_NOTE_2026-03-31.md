# ACTION_EXACT_PREFERENCE_PATCH_AND_FRAME2_OBSTRUCTION_NOTE_2026-03-31

## Status

Working computational note.

This note records the effect of adding exact-preference to the two-step lookahead policy and identifies the remaining obstruction core after that patch.

---

## Executive summary

The exact-preference patch resolves the dominant failure mode of the baseline two-step lookahead.

On the sampled nontrivial D4 action-family:

- total starts: 599
- exact repairs after patch: 402
- failures after patch: 197
- exact repair rate after patch: 402 / 599 = 67.11%

The patched rule preserves monotone descent in normalized action distance:

- up steps: 0
- flat steps: 430
- drop steps: 1896

The residual failures split as:

- distance 1: 71
- distance 2: 123
- distance 3: 3

The residual distance-1 fringe is completely concentrated on the frame-2 action representative and admits no exact one-edit closure.

Thus the geometry now separates cleanly into:

1. a **frame-0 reachable fringe** that was blocked only by policy selection
2. a **frame-2 obstruction fringe** that is locally non-closable in one edit

The best current description is:

> exact-preference resolves the dominant selection bug and exposes a genuine frame-2 obstruction core.

---

## 1. Background

The baseline result had already established:

- the original two-step lookahead was nonexpansive in normalized action distance
- it terminated overwhelmingly in a distance-1 fringe
- that fringe collapsed onto two exact action representatives:
  - frame 0
  - frame 2

A direct local probe of the baseline distance-1 fringe then showed:

- 402 of 473 distance-1 terminals had exactly one exact one-edit child
- 71 of 473 had no exact one-edit child

This implied that the dominant baseline obstruction was not local impossibility. It was policy selection failure.

To test that directly, the chooser was patched to immediately select a first-step child if that child was already an exact action-cell.

---

## 2. Patched exact-preference run

After adding exact-preference, the run yielded:

- starts = 599
- exact = 402 / 599
- failed = 197
- avg_steps = 3.883

This is the decisive regime change.

Compared with the baseline nontrivial run:

- baseline exact repairs: 0 / 599
- patched exact repairs: 402 / 599

Therefore the patch converted 402 previously non-exact trajectories into exact closures.

This exactly matches the earlier count of distance-1 fringe states that possessed a unique exact one-edit child.

That match is the key causal confirmation:

> the dominant baseline failure mode was a chooser defect, not absence of local exact reachability.

---

## 3. Patched run preserves monotonicity

A step-delta probe on the patched run gives:

- up steps = 0
- flat steps = 430
- drop steps = 1896

Delta histogram:

- -4: 2
- -3: 8
- -2: 57
- -1: 1829
- 0: 430

So the patch does not break the descent structure.

Instead, it preserves nonexpansiveness and makes the process more aggressively descending than before.

This is important.

The patched rule is not “cheating” by allowing distance increases. It remains a monotone descent process in normalized action distance while unlocking exact closure on the reachable fringe.

---

## 4. Residual failure set after exact-preference

After patching, the remaining failures are:

- total failures = 197

Residual terminal histogram:

- distance 1: 71
- distance 2: 123
- distance 3: 3

So the patch removes the dominant distance-1 reachable fringe but leaves a smaller hard core.

This residual set is now the meaningful obstruction set.

---

## 5. Residual distance-1 fringe

The residual distance-1 failures were probed exactly as before.

Result:

- residual distance-1 failures: 71

Nearest exact action representative for all 71:

- frame 2  
  `o4 | s4 | t2 | s2 | t0 | s0`

Count:

- 71 / 71 nearest to frame 2

So after exact-preference, the distance-1 fringe is no longer split across two targets.

It is concentrated entirely on the frame-2 representative.

This is a strong structural simplification.

---

## 6. Local exact reachability of the residual distance-1 fringe

The decisive local test asked:

> does a residual distance-1 terminal have any exact one-edit child?

Result:

- residual distance-1 terminals with at least one exact one-edit child: 0
- residual distance-1 terminals with zero exact one-edit child: 71

Exact-child-count histogram:

- 0: 71

So the surviving distance-1 fringe is a genuine local obstruction layer.

Unlike the frame-0 fringe in the baseline run, these states do not sit one edit away from exact closure.

This is the core result of the patched analysis.

---

## 7. Geometric interpretation

The exact-preference patch cleanly separates two distinct geometric phenomena.

### 7.1 Frame-0 fringe

This fringe was exact-reachable in one edit.

It survived in the baseline run only because the chooser failed to select the exact-closing move.

So this component was not a true geometric obstruction.

It was a policy-selection obstruction.

### 7.2 Frame-2 fringe

This fringe remains after exact-preference.

It admits no exact one-edit closure.

So this component is a genuine local obstruction layer in the present geometry.

This is now the true hard core of the problem.

---

## 8. What is now resolved

The following are now resolved for the sampled nontrivial run.

### 8.1 Baseline failure mode

Resolved:

- the dominant baseline failure was a policy-selection bug

### 8.2 Exact-preference effect

Resolved:

- exact-preference converts the entire reachable frame-0 fringe into exact repairs

### 8.3 Monotonicity after patch

Resolved:

- the patched rule remains nonexpansive in normalized action distance
- there are still no increasing steps

### 8.4 Residual distance-1 geometry

Resolved:

- the surviving distance-1 fringe is concentrated entirely on frame 2
- none of those frame-2 distance-1 terminals has any exact one-edit child

---

## 9. What remains open

The following questions remain open.

### 9.1 Residual distance-2 layer

There are still 123 failures at distance 2.

We do not yet know whether these:

- have distance-1 children
- funnel deterministically into the frame-2 obstruction fringe
- or require a deeper policy modification to close

### 9.2 Nature of the frame-2 obstruction

We do not yet know why frame 2 is locally non-closable in one edit.

Possible explanations include:

- a true combinatorial obstruction
- an orbit / normalization asymmetry
- a chamber distinction inside the action-family geometry
- a deeper-but-still-reachable exact path requiring more than one nonincreasing step

### 9.3 Stronger policy patches

We have not yet tested whether the residual obstruction can be overcome by:

- deeper lookahead
- exact-preference propagated into second-step scoring
- tie-break changes
- explicit preference for distance-1 states nearest to frame 2 closures
- temporary plateau navigation designed to search for two-step exact entry

---

## 10. Best current theorem-shaped statement

A clean theorem-style formulation suggested by the evidence is:

> On the sampled nontrivial D4 action-family, the baseline two-step lookahead is a monotone descent process in normalized action distance that funnels trajectories into a two-target distance-1 fringe without exact closure. Adding exact-preference resolves the dominant frame-0 fringe, converting 402 trajectories into exact repairs while preserving monotonicity. The remaining distance-1 fringe is concentrated entirely on the frame-2 action representative and has no exact one-edit closure, thereby exposing a genuine local obstruction core.

This is not yet a universal proof, but it is now a sharply structured result.

---

## 11. Best short summary

The baseline rule stalled mostly because it refused reachable exact closures.

The exact-preference patch fixes that entire dominant component.

What remains is a smaller, cleaner, genuinely hard obstruction set centered on frame 2.

Or more compactly:

> exact-preference resolves frame 0 and exposes frame 2.

---

## 12. Next blade

The next decisive test is to profile the residual 123 distance-2 failures.

We should ask:

1. which exact action representatives they are nearest to
2. whether they admit any distance-1 children
3. whether those distance-1 children lie entirely in the frame-2 obstruction fringe

That will tell us whether the remaining problem is:

- a deeper funnel into the same frame-2 obstruction basin
or
- a more complicated residual geometry

