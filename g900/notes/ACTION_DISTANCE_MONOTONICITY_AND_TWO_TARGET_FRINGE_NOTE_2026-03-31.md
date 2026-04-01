# ACTION_DISTANCE_MONOTONICITY_AND_TWO_TARGET_FRINGE_NOTE_2026-03-31

## Status

Working computational note.

This note records the current status of the two-step lookahead policy after clarifying the classifier geometry, excluding trivial exact starts, and probing both stepwise action-distance behavior and the structure of the terminal distance-1 fringe.

---

## Executive summary

The present two-step lookahead is **not** an exact repair operator on the sampled nontrivial D4 action-family.

After excluding trivial exact starts, the run contains:

- 599 non-exact starts
- 0 exact repairs
- average steps = 4.367

At the same time, the policy exhibits strong and highly structured contraction toward the action family.

Three facts are now established for the sampled run:

1. The realized walk is **stepwise nonincreasing** in normalized action distance.
2. The overwhelming majority of terminals lie in the **distance-1 fringe**.
3. That distance-1 fringe collapses onto exactly **two nearest exact action representatives**.

The best current description is:

> monotone descent into a two-target codimension-1 fringe, without exact closure.

---

## 1. Background

The relevant policy is the current two-step lookahead in:

- `scripts/g15_action_two_step_policy.py`

The classification and family-distance logic are defined in:

- `witness_machine/core.py`

The relevant output artifact is:

- `artifacts/repair_radius_action_d4_result_two_step_lookahead_nontrivial.json`

This run excludes trivial exact starts before the walk loop.

---

## 2. Clarified meaning of action distance

The key conceptual ambiguity has now been resolved.

`best_action_distance` is not distance to one fixed exact target.

Instead, `classify_cycle(cycle, r)` computes the minimum normalized coordinate distance from the input cycle to the full action-cell family over all frames.

For action-cells, this is:

- compute `action_cell(i, r)` for each frame `i`
- normalize both cycles by cyclic rotation and reversal
- compare the normalized cycles coordinatewise
- take the minimum mismatch count across all action representatives

Thus the operative action distance is:

> family-relative normalized distance to the action-cell family

not:

> raw Hamming distance to one canonical exact action cycle.

This resolves the earlier apparent contradiction in which many distance-1 terminals were far from a single exact reference cycle in direct coordinate comparison.

They are not required to be close to one chosen exact representative. They are only required to be close to **some** normalized action representative.

---

## 3. Classification semantics

The classifier distinguishes:

- `subjective-state`
- `objective-state`
- `action-cell`
- `mixed`
- `unresolved`

The confidence field distinguishes:

- `exact`
- `nearest`
- `ambiguous`

For action-cells, this means:

- `classification = "action-cell", confidence = "exact"`  
  the cycle exactly matches some normalized action-cell representative and is not simultaneously an exact subjective/objective state

- `classification = "action-cell", confidence = "nearest"`  
  the cycle is not exact, but action-cell is the uniquely closest family under the normalized family-distance metric

- `classification = "unresolved", confidence = "ambiguous"`  
  there is a tie for best distance among families

This matters because the terminal fringe observed in the run consists overwhelmingly of:

- `classification = "action-cell"`
- `confidence = "nearest"`

So the observed fringe is a genuine family-relative near-target layer.

---

## 4. Nontrivial run result

After excluding trivial exact starts, the run yields:

- starts = 599
- exact = 0 / 599
- failed = 599
- avg_steps = 4.367

This settles the main negative claim:

> the present two-step lookahead does not produce nontrivial exact repairs on the sampled D4 action-family.

The earlier apparent `1 / 600` exact success was entirely due to a trivial exact start already at distance 0 with zero steps taken.

---

## 5. Terminal distance distribution

The terminal histogram on the nontrivial run is:

- distance 1: 473
- distance 2: 123
- distance 3: 3

Percentages:

- distance 1: 473 / 599 = 78.96%
- distance 2: 123 / 599 = 20.53%
- distance 3: 3 / 599 = 0.50%

So the process is strongly contractive toward the action family, and overwhelmingly settles one unit away in family-relative normalized action distance.

This is not the signature of random drift.

It is evidence of a sharply organized attractor structure.

---

## 6. Stepwise monotonicity probe

A direct probe of realized transitions over all paths gives:

- walk count: 599
- total realized transitions: 2616
- up steps: 0
- flat steps: 1117
- drop steps: 1499

Delta histogram for `new_distance - old_distance`:

- `-4`: 2
- `-3`: 8
- `-2`: 52
- `-1`: 1437
- `0`: 1117

Most common strict drops:

- `3 -> 2`: 550
- `2 -> 1`: 467
- `4 -> 3`: 417
- `4 -> 2`: 25
- `5 -> 3`: 23
- `5 -> 2`: 8
- `3 -> 1`: 4
- `5 -> 4`: 3
- `5 -> 1`: 2

The critical point is:

> there are no realized increasing steps.

So on the sampled nontrivial run, the present two-step lookahead is empirically **nonexpansive** in normalized action distance.

More strongly, it is usually strictly descending, with the dominant drops occurring in the ladder:

- `4 -> 3`
- `3 -> 2`
- `2 -> 1`

This is the strongest structural result obtained so far.

---

## 7. Structure of the distance-1 fringe

The 473 distance-1 terminals were originally seen as a small set of recurring terminal strings.

A stronger probe now shows that these terminals collapse onto exactly **two nearest exact action representatives**.

Nearest exact action representatives for the distance-1 terminals:

1. frame 0  
   `o2 | s2 | t0 | s0 | t3 | s3`  
   count: **402**

2. frame 2  
   `o4 | s4 | t2 | s2 | t0 | s0`  
   count: **71**

Thus:

- 402 / 473 distance-1 terminals are nearest to the frame-0 action representative
- 71 / 473 distance-1 terminals are nearest to the frame-2 action representative

This means the distance-1 fringe is not merely a collection of common strings.

It is more precisely:

> a codimension-1 fringe around exactly two exact action representatives.

This is a major sharpening of the geometric picture.

---

## 8. Consequence for the geometry

The observed geometry is now much clearer.

The current process does not wander randomly in state space.

Instead, it behaves like a descent process in the family-relative normalized action distance, and its terminal mass is funneled into a narrow fringe supported on two action targets.

So the geometry appears to consist of:

- the action-cell family as the exact target set
- a highly populated `d_A = 1` fringe around two dominant action representatives
- smaller residue at distances 2 and 3
- no nontrivial exact closure under the present rule

The correct mental picture is not:

- one exact point with a literal Hamming shell around it

but rather:

- a normalized family geometry with a two-target near-action fringe

---

## 9. What has now been resolved

The following are now resolved for the sampled nontrivial run.

### 9.1 Exact repair question

Resolved:

- there are 0 nontrivial exact repairs

### 9.2 Distance semantics

Resolved:

- `best_action_distance` is family-relative normalized distance to the action-cell family
- it is not coordinatewise distance to a single chosen exact target

### 9.3 Stepwise behavior

Resolved:

- the realized two-step policy never increases normalized action distance on the sampled run

### 9.4 Terminal structure

Resolved:

- the dominant terminal set is a structured distance-1 fringe
- that fringe collapses onto two exact action representatives
- the frame-0 representative dominates strongly

---

## 10. What remains open

Several important questions remain.

### 10.1 Last-mile obstruction

We still do not know why exact closure is never taken.

Possible explanations include:

- the exact-closing move is unavailable from the dominant fringe states
- it is available but loses under the current two-step ranking
- it ties and loses under lexicographic tie-break
- exact closure would require a temporary increase elsewhere in the local search tree, which the current rule forbids

The last possibility is especially plausible because the chooser refuses candidates that worsen the current distance.

### 10.2 Local exact reachability from the fringe

We have not yet tested the decisive local question:

> from a dominant distance-1 terminal, does there exist any one-edit child that is exact?

This is the next clean split:

- if no, then the fringe is a genuine one-step obstruction
- if yes, then the current rule is failing because of scoring or tie-break behavior rather than local impossibility

### 10.3 Symmetry/orbit structure inside the fringe

We know the fringe collapses onto two nearest representatives, but we have not yet fully quotient-structured the raw terminals into symmetry or orbit classes beyond the classifier’s normalization.

### 10.4 Universal vs sampled statement

The current result is computationally established on the sampled nontrivial run.

A universal theorem would require a proof not restricted to this sample.

---

## 11. Best current theorem-shaped statement

A clean formal-style statement suggested by the evidence is:

> Let \( d_A(c) \) be the minimum normalized coordinate distance from cycle \( c \) to the action-cell family. On the sampled nontrivial D4 action-family, the present two-step lookahead produces trajectories for which \( d_A \) is empirically nonincreasing at every realized step. All terminal states lie in the fringe \( d_A \in \{1,2,3\} \), with the overwhelming majority at \( d_A = 1 \), and the \( d_A = 1 \) mass is concentrated around two exact action representatives. No nontrivial trajectory reaches \( d_A = 0 \).

This is not yet a universal proof, but it is now a sharply defined theorem target.

---

## 12. Best short summary

The present two-step lookahead is not an exact transducer.

It is an empirically monotone descent process in normalized action distance that funnels the sampled nontrivial D4 action-family into a two-target codimension-1 fringe without exact closure.

Or more compactly:

> monotone descent into a two-target fringe, without closure.

---

## 13. Next blade

The next decisive test is:

> For the dominant distance-1 fringe states, check whether any one-edit child is exact.

That test will tell us whether the obstruction is:

- local impossibility
or
- policy-selection failure

That is the next clean hinge on the path toward a theorem.

