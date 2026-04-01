# ACTION_RESIDUAL_BASIN_DECOMPOSITION_NOTE_2026-03-31

## Status

Working computational note.

This note records the decomposition of the residual failure basin after the exact-preference patch and clarifies which parts of the remaining geometry are reachable, blocked, or still deeper than a two-step local probe can resolve.

---

## Executive summary

The exact-preference patch resolved the dominant baseline selection failure and raised the exact repair count to:

- 402 / 599 exact repairs
- 197 residual failures

The residual failure set decomposes into:

- distance 1: 71
- distance 2: 123
- distance 3: 3

The residual distance-1 layer is a genuine obstruction core:

- all 71 are nearest to the frame-2 exact action representative
- none has an exact one-edit child

The residual distance-2 layer is not a simple outer shell of that frame-2 core.

A two-step local reachability probe on the 123 residual distance-2 failures shows:

- 2 have a <=2-step exact hit
- 60 have a <=2-step action-cell distance-1 hit
- 0 have a <=2-step distance-1 hit nearest to frame 2
- 63 have no <=2-step exact hit and no <=2-step distance-1 action-cell hit at all

Thus the post-patch residual geometry is stratified and asymmetric:

1. a blocked frame-2 distance-1 core
2. a mixed distance-2 layer with some two-step routes back toward frame 0
3. a hard 63-state distance-2 shell unresolved within two steps

The best current summary is:

> exact-preference resolves frame 0, exposes frame 2, and reveals a deeper residual shell beyond both.

---

## 1. Background

The baseline two-step lookahead exhibited:

- monotone descent in normalized action distance
- termination in a two-target distance-1 fringe
- no nontrivial exact closures

A local one-edit probe of the baseline distance-1 fringe showed:

- 402 of 473 distance-1 terminals had exactly one exact one-edit child
- 71 had none

This implied that the dominant baseline failure mode was policy-selection failure rather than lack of local exact reachability.

After adding exact-preference, the patched run produced:

- 402 / 599 exact repairs
- 197 failures
- no increasing steps

So the patch resolved the reachable fringe while preserving monotonicity.

---

## 2. Residual failure histogram after exact-preference

Residual failures after patch:

- total failures: 197

Residual terminal distance histogram:

- distance 1: 71
- distance 2: 123
- distance 3: 3

So the patch removes the dominant reachable component but leaves a smaller structured obstruction basin.

---

## 3. Residual distance-1 core

The residual distance-1 failures were classified by nearest exact action representative.

Result:

- 71 / 71 nearest to frame 2:
  `o4 | s4 | t2 | s2 | t0 | s0`

A direct one-edit closure probe showed:

- residual distance-1 terminals with >=1 exact one-edit child: 0
- residual distance-1 terminals with 0 exact one-edit child: 71

Therefore the residual distance-1 fringe is a genuine local obstruction layer.

This sharply contrasts with the baseline frame-0 fringe, which was exact-reachable in one edit and was repaired by exact-preference.

---

## 4. Residual distance-2 layer

The residual distance-2 failures were first classified by nearest exact action representative.

Counts:

- 53 nearest to frame 3:
  `o0 | s0 | t3 | s3 | t1 | s1`
- 45 nearest to frame 1:
  `o3 | s3 | t1 | s1 | t4 | s4`
- 25 nearest to frame 4:
  `o1 | s1 | t4 | s4 | t2 | s2`

So the residual distance-2 layer is already structured and multi-target, not diffuse.

A direct one-edit local probe showed:

- residual distance-2 states with any action-cell distance-1 child: 0
- residual distance-2 states with any exact one-edit child: 0

Thus the distance-2 layer is not immediately adjacent, in one edit, to either exact closure or the action-cell distance-1 fringe.

This means it is not merely a trivial outer shell around the frame-2 distance-1 core.

---

## 5. Two-step local reachability of the residual distance-2 layer

A local two-step reachability probe was then applied to all 123 residual distance-2 failures.

Results:

- residual d2 with any <=2-step exact hit: 2
- residual d2 with any <=2-step action-cell distance-1 hit: 60
- residual d2 with any <=2-step distance-1 hit nearest to frame 2: 0

Histogram of (found_d1_count, found_exact_count):

- (0, 0): 63
- (1, 0): 51
- (2, 0): 7
- (13, 1): 2

This is the key decomposition.

It shows that the residual distance-2 layer is not uniform.

Instead it contains three subpopulations:

### 5.1 Two-step exact-reachable residue

There are 2 residual distance-2 states with a two-step exact hit.

Both exact hits land in:

- frame 0:
  `o2 | s2 | t0 | s0 | t3 | s3`

So even after the exact-preference patch, there remains a tiny amount of exact-reachable mass outside the main repaired set.

### 5.2 Two-step distance-1 reachable residue

There are 60 residual distance-2 states with a <=2-step action-cell distance-1 hit.

Crucially, all of these distance-1 hits point to:

- frame 0

and none points to frame 2.

So these states do not funnel into the frame-2 obstruction core within two steps.

They still geometrically point back toward the frame-0 side of the action family.

### 5.3 Hard residual shell

There are 63 residual distance-2 states with:

- no <=2-step exact hit
- no <=2-step action-cell distance-1 hit

This is the deepest unresolved part of the current post-patch basin.

These states are not locally connected, within two edits, to either exactness or the distance-1 action-cell fringe.

---

## 6. Geometric interpretation

The post-patch residual basin is not radial and not centered in a naive way on the frame-2 obstruction core.

Instead it is stratified and asymmetric.

### 6.1 Inner blocked core

The inner blocked core is:

- distance 1
- concentrated entirely on frame 2
- locally non-closable in one edit

This is the clearest genuine obstruction layer currently identified.

### 6.2 Mixed outer d2 layer

The distance-2 layer is split:

- some states still possess two-step routes toward frame 0 distance-1 or exactness
- some have no two-step route to either

So the distance-2 shell is not simply “the outer shell of frame 2.”

It contains both:

- a still-reachable component
- and a harder unresolved component

### 6.3 Tiny distance-3 residue

A 3-state distance-3 residue remains beyond that, but it has not yet been locally profiled.

---

## 7. What is now resolved

The following are now resolved.

### 7.1 Baseline dominant failure mode

Resolved:

- the dominant baseline failure was policy-selection failure on the frame-0 reachable fringe

### 7.2 Effect of exact-preference

Resolved:

- exact-preference converts the full frame-0 reachable fringe into exact repairs
- the patch preserves monotone descent

### 7.3 Nature of the residual distance-1 core

Resolved:

- the residual distance-1 core is concentrated entirely on frame 2
- it has no exact one-edit closure

### 7.4 Nature of the residual distance-2 layer

Resolved:

- the residual distance-2 layer has no one-edit route to exactness or action-cell distance 1
- within two steps it splits into:
  - a tiny exact-reachable piece
  - a larger distance-1-reachable piece pointing to frame 0
  - a 63-state hard shell with no <=2-step exact or distance-1 hit

---

## 8. What remains open

The main open questions are now sharply defined.

### 8.1 Why is frame 2 blocked?

We still do not know why the frame-2 distance-1 fringe is locally non-closable in one edit while the frame-0 fringe was exact-reachable.

### 8.2 Why does the residual d2 layer point to frame 0 and not frame 2?

The 60 residual d2 states with <=2-step action-cell distance-1 hits all point to frame 0 and none to frame 2.

This asymmetry is not yet explained.

### 8.3 What is the true depth of the 63-state hard shell?

The hardest unresolved set is the 63 residual distance-2 states with no <=2-step exact or action-cell distance-1 hit.

We do not yet know whether they become reachable at depth 3, 4, or only under a stronger policy change.

### 8.4 What is the role of the 3-state distance-3 residue?

This residue has not yet been separately analyzed.

---

## 9. Best current theorem-shaped statement

A clean theorem-style formulation suggested by the evidence is:

> On the sampled nontrivial D4 action-family, the exact-preference patch resolves the dominant frame-0 selection failure while preserving monotone descent in normalized action distance. The remaining residual basin is stratified: a frame-2 distance-1 obstruction core with no exact one-edit closure, a distance-2 layer with no one-edit route to either exactness or action-cell distance 1, and a 63-state hard sublayer with no exact or distance-1 action-cell hit within two steps.

This is not yet a universal proof, but it is now a very sharp structural result.

---

## 10. Best short summary

The patch fixes the reachable fringe.

What remains is not one simple obstruction, but a layered residual basin:

- blocked frame-2 core
- mixed d2 outer layer
- hard 63-state shell

Or more compactly:

> exact-preference resolves frame 0, exposes frame 2, and leaves a deeper d2 shell.

---

## 11. Next blade

The next decisive test is a 3-step local reachability probe on the 63 hard distance-2 states.

We should ask:

1. whether any have a <=3-step exact hit
2. whether any have a <=3-step action-cell distance-1 hit
3. whether any newly reached distance-1 hits point to frame 2 or remain frame-0 biased

That will determine whether the hard shell is merely deeper or genuinely separated under the current descent regime.

