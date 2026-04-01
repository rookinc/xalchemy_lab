# ACTION_DEPTH3_UNRESOLVED_CORE_CHAMBER_SPLIT_NOTE_2026-03-31

## Status

Working computational note.

This note records the chamber structure of the unresolved depth-3 core after the exact-preference patch and the depth-3 hard-shell probe.

---

## Executive summary

The depth-3 unresolved core contains:

- 20 states total

These 20 are not diffuse. They cluster around two exact action representatives:

- 13 nearest to frame 1:
  `o3 | s3 | t1 | s1 | t4 | s4`
- 7 nearest to frame 4:
  `o1 | s1 | t4 | s4 | t2 | s2`

This shows that the residual geometry is multi-chambered.

The best current chamber picture is:

- frame 0: dominant reachable chamber, repaired by exact-preference
- frame 2: blocked near-action chamber at distance 1
- frame 1 / frame 4: deeper unresolved chamber surviving the depth-3 probe

The best current summary is:

> the residual basin is not one obstruction, but a chambered geometry with distinct reachable, blocked, and deeper unresolved sectors.

---

## 1. Background

After the exact-preference patch, the residual failure basin was:

- distance 1: 71
- distance 2: 123
- distance 3: 3

The residual distance-1 layer was entirely concentrated on frame 2 and had no exact one-edit closure.

A two-step probe of the residual distance-2 layer identified a 63-state hard shell.

A depth-3 parallel probe on that hard shell then showed:

- 43 hard-shell states open to action-cell distance 1 within depth 3
- 20 remain unresolved within depth 3
- none reaches exact closure within depth 3

Those 20 states are the current irreducible core at probe depth 3.

---

## 2. Chamber split of the unresolved 20

The unresolved 20 were classified by nearest exact action representative.

Result:

- 13 nearest to frame 1:
  `o3 | s3 | t1 | s1 | t4 | s4`
- 7 nearest to frame 4:
  `o1 | s1 | t4 | s4 | t2 | s2`

Thus the unresolved depth-3 core is concentrated in a frame-1 / frame-4 chamber pair.

This is not a continuation of the frame-2 near-action obstruction core.

It is a different residual chamber.

---

## 3. Geometric interpretation

The current geometry is now best understood as chambered.

### 3.1 Frame-0 chamber

This was the dominant reachable chamber.

Its near-action fringe was exact-reachable in one edit and was resolved by exact-preference.

### 3.2 Frame-2 chamber

This remains the blocked near-action chamber:

- distance 1
- locally non-closable in one edit

### 3.3 Frame-1 / frame-4 chamber

This is the deeper unresolved chamber:

- survives the depth-3 hard-shell probe
- does not reduce to the frame-2 obstruction
- clusters on two exact representatives only

So the residual basin is not a single nested shell around one center.

It is a multi-chamber residual geometry.

---

## 4. What is now resolved

Resolved:

- the depth-3 unresolved core contains 20 states
- those 20 cluster around frame 1 and frame 4 only
- the unresolved core is not centered on frame 2
- the residual basin is therefore structurally chambered

---

## 5. What remains open

Open:

- whether the frame-1 / frame-4 chamber opens at depth 4
- whether it opens to distance 1 only or to exactness
- whether frame 1 and frame 4 behave symmetrically
- whether the chamber supports a stronger obstruction invariant

---

## 6. Best short summary

The residual basin has at least three chambers:

- repaired frame 0
- blocked frame 2
- deeper unresolved frame 1 / frame 4

Or more compactly:

> repaired porch, blocked balcony, deeper side chambers.

