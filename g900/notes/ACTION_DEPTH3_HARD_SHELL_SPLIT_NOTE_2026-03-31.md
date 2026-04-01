# ACTION_DEPTH3_HARD_SHELL_SPLIT_NOTE_2026-03-31

## Status

Working computational note.

This note records the depth-3 local reachability result on the 63-state hard distance-2 shell identified after the exact-preference patch.

---

## Executive summary

The 63-state hard distance-2 shell is not uniformly blocked.

A depth-3 local reachability probe shows:

- hard d2 states scanned: 63
- with any <=3-step exact hit: 0
- with any <=3-step action-cell distance-1 hit: 43
- with any <=3-step distance-1 hit nearest to frame 2: 19

So the hard shell splits into:

- 43 states that are deeper but reachable at depth 3
- 20 states that remain unresolved at depth 3

This means the residual basin is deeper, but not opaque.

The best current summary is:

> the hard d2 shell is partially penetrable at depth 3, including limited access toward the frame-2 near-action fringe, but a 20-state core remains unresolved.

---

## 1. Background

After the exact-preference patch, the residual failure basin was:

- distance 1: 71
- distance 2: 123
- distance 3: 3

The residual distance-1 core was already resolved as:

- entirely nearest to frame 2
- with no exact one-edit closure

The residual distance-2 layer was then split by a two-step local probe into:

- 2 with <=2-step exact hit
- 60 with <=2-step distance-1 action-cell hit
- 63 with no <=2-step exact hit and no <=2-step distance-1 action-cell hit

These 63 formed the hard d2 shell.

---

## 2. Depth-3 probe result on the hard d2 shell

A parallel depth-3 local reachability probe was run on the 63 hard d2 states.

Headline result:

- has_3step_exact = 0
- has_3step_d1 = 43
- to_frame2_d1 = 19

So the hard shell divides into:

### 2.1 Depth-3 reachable part

43 states admit a <=3-step action-cell distance-1 hit.

These are deeper than the earlier reachable d2 states, but not fundamentally blocked.

### 2.2 Depth-3 unresolved part

20 states admit neither:

- a <=3-step exact hit
- nor a <=3-step action-cell distance-1 hit

These 20 now form the new irreducible core at the current probe depth.

---

## 3. Exactness vs near-action access

The most important negative fact is:

- no hard d2 state has a <=3-step exact hit

So depth 3 does not yet produce closure from the hard shell.

However, the positive fact is almost as important:

- 43 / 63 do reach action-cell distance 1 within depth 3

So the hard shell is not closed off from the near-action fringe.

It is only partly closed off from exact closure.

---

## 4. Frame-2 access appears at depth 3

A new phenomenon appears here:

- 19 of the hard d2 states have a <=3-step distance-1 hit nearest to frame 2

This matters because earlier local probes on the residual d2 layer found no <=2-step distance-1 hits nearest to frame 2.

So depth 3 is the first probe depth at which the hard shell begins to connect to the frame-2 near-action fringe.

That makes the geometry more nuanced:

- frame 2 was not reachable in <=2 steps from the hard shell
- frame 2 becomes reachable in some cases at depth 3
- but still without exact closure

---

## 5. Geometric interpretation

The current post-patch geometry is now best understood as layered and partially permeable.

### 5.1 Reachable frame-0 side

The dominant frame-0 fringe was already repaired by exact-preference.

### 5.2 Blocked frame-2 near-action core

The 71-state residual distance-1 layer remains a genuine local obstruction:

- all nearest to frame 2
- no exact one-edit closure

### 5.3 Hard d2 shell

The 63-state hard shell is neither fully closed nor fully open.

It contains:

- a 43-state depth-3 reachable component
- a 20-state depth-3 unresolved component

This means the shell is deeper than the earlier reachable basin, but not a uniform wall.

---

## 6. What is now resolved

Resolved:

- the 63-state hard d2 shell is not uniformly blocked
- 43 of the 63 open to action-cell distance 1 within depth 3
- 19 of those depth-3 openings touch the frame-2 near-action side
- none reaches exactness within depth 3
- 20 states remain unresolved at the current depth

---

## 7. What remains open

Open:

- which exact representatives dominate the 43 newly reachable depth-3 distance-1 hits
- whether the 20 unresolved states open at depth 4
- whether the 20 unresolved states share a stronger invariant or obstruction pattern
- whether a modified policy can use the new depth-3 openings to close more of the residual basin

---

## 8. Best current theorem-shaped statement

A clean statement suggested by the evidence is:

> After exact-preference removes the dominant frame-0 selection failure, the remaining hard 63-state distance-2 shell is partially penetrable at depth 3: 43 states admit a <=3-step action-cell distance-1 hit, including 19 that reach the frame-2 near-action fringe, while 20 admit no <=3-step exact or distance-1 action-cell hit. No hard-shell state reaches exact closure within depth 3.

---

## 9. Best short summary

Depth 3 opens most of the hard shell, but not all of it.

Or more compactly:

> the hard shell cracks at depth 3, but a 20-state core still holds.

