# ACTION_TWO_STEP_LOOKAHEAD_POSITION_REPORT_2026-03-31

## Status

Working position note.  
This note records the current empirical status of the two-step lookahead policy on the sampled D4 action-family and clarifies what has and has not been established.

---

## Executive summary

The current two-step lookahead policy is **not** an exact repair operator on the sampled D4 action-family.

After excluding trivial exact starts, the experiment contains **599 non-exact starts** and yields **0 exact repairs**.

At the same time, the policy is very far from random. Its terminal distribution is sharply concentrated near the action target basin:

- distance 1: 473
- distance 2: 123
- distance 3: 3
- distance 0: 0 nontrivial cases

Thus the current rule exhibits strong **basin contraction** without **exact closure**.

The best current description is:

> the two-step lookahead behaves as a near-target concentrator or basin funnel, not as an exact transducer.

---

## 1. Experimental object under study

We are studying the script:

- `scripts/g15_action_two_step_policy.py`

and its action-family run on the input:

- `artifacts/repair_radius_action_d4.json`

with parameters:

- `--top-first 6`
- `--top-second 6`

The output artifact of interest is:

- `artifacts/repair_radius_action_d4_result_two_step_lookahead.json`
- `artifacts/repair_radius_action_d4_result_two_step_lookahead_nontrivial.json`

The target family is:

- `action-cell`

The sample depth is:

- `4`

The seed cycle is inherited from the input payload and the action-family starts are sampled from that payload-driven family construction.

---

## 2. Initial confusion and its resolution

An apparent contradiction first arose between the summary counts and the exported walk list.

Observed facts:

- the script summary reported:
  - `count = 600`
  - `reached_exact_count = 1`
- but the exported `walks` list appeared to contain only 50 items
- and scanning those 50 found 0 exact hits

Inspection of the script showed the cause immediately:

```python
"summary": summarize(walks),
"walks": walks[:50],
```

So the script was:

- computing the summary over **all** walks
- but exporting only the **first 50** walks in the `walks` field

That means the artifact mixed a global summary with a truncated preview list.

This was not a logic contradiction in the policy itself. It was an export semantics issue.

The script was then patched so that the output exports the full walk set:

```python
"walks": walks,
```

After rerunning, the artifact became internally consistent.

---

## 3. Full-run result before excluding trivial exact starts

With the full export fixed, the rerun yielded:

- starts = 600
- exact = 1 / 600
- failed = 599
- avg_steps = 4.360

The full walk count matched the summary count:

- `summary.count = 600`
- `len(walks) = 600`
- `exact hits in walks = 1`

This established that the previous discrepancy was due solely to truncation of the exported walk list.

However, inspection of the single exact hit showed that it was **not** a genuine repair event.

The lone exact hit had:

- `start_distance = 0`
- `end_distance = 0`
- `steps_taken = 0`
- `start_cycle == end_cycle`
- `end_classification = action-cell`
- `end_confidence = exact`

So the only exact case was already exact at initialization.

In other words:

> the observed `1/600` success rate was entirely due to a trivial exact start that was sampled into the family.

This means the full-run exact count did **not** demonstrate a nontrivial repair channel.

---

## 4. Patch to exclude trivial exact starts

To test genuine repair rather than exact membership, the script was patched to remove trivial exact starts immediately after `sample_family_starts(...)` and before the walk loop.

Conceptually, the patch was:

```python
starts = [
    s for s in starts
    if not (s["classification"] == "action-cell" and s["confidence"] == "exact")
]
```

This converts the run from a mixed sample of:

- non-exact action-family starts
- plus any exact action-family starts accidentally included by the sampler

into a strictly nontrivial test population.

This is the correct way to ask the real question:

> can the two-step lookahead take a non-exact action-family start and repair it to exactness?

---

## 5. Nontrivial-run result

After excluding trivial exact starts, the rerun yielded:

- starts = 599
- exact = 0 / 599
- failed = 599
- avg_steps = 4.367

This is the cleanest and most important result currently in hand.

It means:

> among 599 non-exact action-family starts, the current two-step lookahead produced 0 exact repairs.

Therefore the current policy is **not** an exact repair operator on this sampled D4 action-family.

This statement is now clean, direct, and free of the earlier artifact ambiguity.

---

## 6. Terminal distance structure on the nontrivial run

The nontrivial terminal histogram is:

- distance 1: 473
- distance 2: 123
- distance 3: 3

There are no nontrivial terminals at distance 0.

This is extremely informative.

### 6.1 First read

The policy overwhelmingly terminates at distance 1.

That means the policy has a strong tendency to pull trajectories into the immediate neighborhood of the target family, but it does not realize exact closure.

### 6.2 Percentages

Out of 599 non-exact starts:

- distance 1: 473 / 599 = 78.96%
- distance 2: 123 / 599 = 20.53%
- distance 3: 3 / 599 = 0.50%

So nearly four-fifths of all nontrivial trajectories terminate one action-distance unit away from exactness.

This is not the signature of a random or structureless process.

It is strong evidence of directed contraction.

### 6.3 Best current summary sentence

> The present two-step lookahead contracts the overwhelming majority of sampled non-exact action-family starts into a distance-1 terminal fringe, but never crosses into exact closure.

---

## 7. Interpretation: contraction without closure

This run separates two phenomena very clearly.

### 7.1 Basin attraction

Yes, strongly.

The terminal mass is overwhelmingly concentrated at distance 1, with very little residue at distance 2 and almost none at distance 3.

This indicates that the rule has a real directional relation to the action target family.

### 7.2 Exact closure

No.

After removing trivial exact starts, not a single trajectory reaches exactness.

So the final closure step is not being realized under the current policy.

### 7.3 Practical interpretation

The operator knows the right neighborhood.

It does not know how to complete the final exact selector.

This is why the right description is not “failed repair” in a generic sense, but rather:

- near-target concentrator
- basin funnel
- contractive but not closing
- family-seeking but not exact

---

## 8. Analysis of the distance-1 fringe

To understand whether the 473 distance-1 terminals are all variants of the same near miss or something more structured, the distance-1 subset was profiled.

Result:

- distance-1 terminals = 473

### 8.1 Steps taken

Distribution of `steps_taken` among distance-1 terminals:

- 2: 1
- 3: 38
- 4: 138
- 5: 268
- 6: 27
- 7: 1

Equivalent path lengths including the start node:

- 3: 1
- 4: 38
- 5: 138
- 6: 268
- 7: 27
- 8: 1

This means most distance-1 terminals arise after 4–5 actual moves, with 5 moves being dominant.

So the policy is not merely making one or two superficial improvements and stopping. It is walking a real path through the state space and repeatedly settling into a stable near-target shelf.

### 8.2 Most common terminal cycles

The distance-1 fringe is not diffuse. It is dominated by a small number of recurrent terminal forms.

Top observed end cycles:

1. `o2 | s2 | t0 | s0 | t3 | s4` — 100
2. `o2 | s2 | t0 | s0 | o4 | s3` — 47
3. `t0 | s2 | o2 | s3 | t3 | o3` — 28
4. `o2 | s3 | t3 | s0 | t0 | o4` — 20
5. `s0 | s2 | t0 | s0 | o4 | s4` — 19
6. `o2 | s2 | t0 | o3 | t3 | s3` — 17
7. `t0 | s2 | o1 | s3 | t3 | s0` — 15
8. `o2 | s2 | t0 | s0 | t3 | s2` — 12
9. `s0 | s4 | o4 | s0 | t0 | s2` — 10
10. `o2 | o4 | t0 | s0 | t3 | s3` — 9
11. `s0 | t0 | s2 | o2 | s3 | o4` — 9
12. `o2 | s2 | t0 | s0 | o3 | s3` — 9

This tells us that the distance-1 layer is a **small structured fringe of attractors**, not a broad scatter cloud.

That is important.

It means the failure mode is structured enough to model.

### 8.3 Most common final moves into the distance-1 fringe

Top final moves:

- `edit_pos5_s2_to_s4` — 107
- `edit_pos4_o3_to_o4` — 55
- `edit_pos5_o3_to_o4` — 53
- `edit_pos5_o2_to_o3` — 33
- `edit_pos0_o4_to_s0` — 29
- `edit_pos3_o2_to_o3` — 17
- `edit_pos2_o0_to_o1` — 15
- `edit_pos1_o3_to_o4` — 13
- `edit_pos5_s4_to_s2` — 13
- `edit_pos3_o3_to_o4` — 12
- `edit_pos4_o4_to_o3` — 10
- `edit_pos4_s2_to_s4` — 10

This is a major clue.

The last mile obstruction is not a single universal missing edit.

Instead, the policy recurrently lands on a small family of terminal substitutions, especially in positions 4 and 5, with a visible bias toward local substitutions like:

- `o3 -> o4`
- `o2 -> o3`
- `s2 -> s4`
- `o4 -> s0`

This suggests the fringe is generated by a small set of recurring local terminal adjustments.

---

## 9. Comparison against the lone exact reference cycle

The exact reference cycle from the full run was:

- `o2 | s3 | t3 | s0 | t0 | s2`

The natural question was:

> are the distance-1 terminals literally one coordinate away from this exact reference cycle?

Answer: mostly no.

When the distance-1 terminals were compared coordinatewise against that exact reference cycle, the majority were **not** Hamming-1 neighbors of it.

Observed difference counts:

- 186 terminals differ in 6 positions
- 174 terminals differ in 4 positions
- 55 terminals differ in 5 positions
- 23 terminals differ in 3 positions

Only a minority were literal single-position differences from that one exact reference, for example:

- position 5: `o4 -> s2` — 20
- position 4: `o4 -> t0` — 6
- position 5: `o3 -> s2` — 3
- position 1: `s2 -> s3` — 3

This is a decisive conceptual point.

It means:

> “distance 1” in this experiment is not the same thing as “Hamming distance 1 from one canonical exact cycle.”

So the classifier’s `best_action_distance` is measuring nearness to the **action family** or its representatives, not coordinatewise nearness to a single fixed exact target.

This matters for theory.

The right mental picture is not:

- one exact point with a literal shell around it

but rather:

- a family-relative action geometry with a codimension-1 fringe of near representatives

---

## 10. What has actually been established

The following points are now empirically established for the current sampled test.

### 10.1 Established

1. The two-step lookahead is **not** an exact repair operator on the sampled nontrivial D4 action-family.
2. The previous apparent `1/600` exact success was entirely due to a trivial exact start.
3. After removing trivial exact starts, the exact repair count is **0 / 599**.
4. The terminal distribution is sharply concentrated near the target family:
   - overwhelmingly at distance 1
   - substantially less at distance 2
   - almost none at distance 3
5. The distance-1 terminals form a **small structured fringe** of recurrent end cycles rather than a diffuse cloud.
6. The notion of “distance 1” here is **classifier-relative / family-relative**, not ordinary coordinatewise distance to the single exact reference cycle.

### 10.2 Not established

1. We have **not** established an exact repair law.
2. We have **not** identified a single universal missing final edit.
3. We have **not** shown that the distance-1 fringe is a single orbit under relabeling, rotation, or symmetry.
4. We have **not** yet unpacked the internal classifier logic behind `best_action_distance`.
5. We have **not** yet identified which action representatives certify the observed distance-1 terminals.

---

## 11. Best current theoretical framing

The current policy should be described as follows.

### 11.1 Negative statement

It is **not** an exact transducer.

That claim is now directly supported by the nontrivial run.

### 11.2 Positive statement

It is a **near-target concentrator**.

It takes a broad family of non-exact starts and drives them into a narrow terminal fringe near the action family.

### 11.3 Strongest concise formulation

> The two-step lookahead realizes family-relative contraction without exact closure.

### 11.4 Alternative formulations

- basin funnel
- codimension-1 fringe attractor
- contractive selector with terminal obstruction
- family-seeking but not exact-closing
- near-target shelf without final descent

---

## 12. What this suggests about the geometry

The empirical shape suggests a layered geometry of failure.

### 12.1 Not random wandering

The terminal mass is too concentrated for this to be interpreted as random drift.

### 12.2 Not one canonical missed target

Because most distance-1 terminals are not Hamming-1 neighbors of the lone exact reference cycle, the fringe cannot be modeled as a single exact point plus literal one-edit shell.

### 12.3 More plausible picture

The classifier is recognizing a family of action-like representatives and assigning low action distance to a structured near-family layer.

So the geometry appears to be:

- one or more exact representatives
- a structured family-relative fringe
- a policy that reliably contracts into that fringe
- an unresolved final criterion preventing exact entry

That unresolved criterion may be:

- a symmetry choice
- a local substitution obstruction
- a parity-like selector
- a seam/position coupling effect
- a lookahead horizon limitation
- or a scoring rule that undervalues the exact-closing move

---

## 13. Likely next technical blades

The next work should not begin by asking whether the rule has any structure. It clearly does.

The right next questions are finer.

### 13.1 Inspect classifier internals

We need to inspect how `best_action_distance` is computed inside `classify_cycle`.

Specifically:

- which exact or representative action-cell cycles are being matched?
- what equivalence operations are allowed?
- why can a cycle that differs from the reference exact cycle in 4–6 coordinates still be certified as distance 1?

This is the key to understanding the family-relative geometry.

### 13.2 Cluster the distance-1 terminals

The top terminal cycles already suggest a small attractor fringe.

We should:

- quotient by obvious symmetries if any
- group by shared local substitutions
- test whether the 473 terminals collapse into a small number of equivalence classes

### 13.3 Study the terminal moves

The dominant last-step labels suggest repeated local obstructions in a few positions.

We should examine:

- whether positions 4 and 5 are special
- whether the last move is often “locally best but globally blocking”
- whether the exact-closing move is systematically ranked below another move because of the two-step scoring criterion

### 13.4 Expand or alter the lookahead criterion

Because the current policy contracts but does not close, possible next experiments include:

- increasing `top_first` and `top_second`
- adding tie-breakers that prefer exactness when available
- adding a direct exactness check inside the candidate scoring loop
- allowing a distinct terminal preference for moves that preserve or improve family structure while enabling exact closure

### 13.5 Separate family distance from coordinate distance

A note or script should explicitly compare:

- classifier action distance
- Hamming distance to chosen exact representatives
- orbit/equivalence distance if symmetries are present

Right now those notions are being conflated if one is not careful.

---

## 14. Clean result statement for future use

A concise result statement suitable for reuse:

> On the sampled D4 action-family, the current two-step lookahead exhibits strong family-relative contraction but no nontrivial exact repair. After excluding trivial exact starts, 0 of 599 non-exact starts reach exact action-cell closure, while 473 terminate at action distance 1, 123 at distance 2, and 3 at distance 3. The dominant distance-1 outcomes form a small structured fringe of recurrent terminal cycles rather than a diffuse error cloud.

A slightly more interpretive version:

> The rule reliably finds the immediate neighborhood of the action family but not the final exact selector.

And the shortest version:

> contraction without closure.

---

## 15. Provisional conclusion

The present two-step lookahead has successfully revealed an important structural distinction.

It does **not** produce exact nontrivial repairs.

But it does produce a highly organized near-target fringe, demonstrating that the action-family geometry is real and that the policy is aligned with it in a nontrivial way.

So the right conclusion is not that the experiment failed.

The right conclusion is that the experiment separated:

- exact closure
- from family-relative attraction

and showed that the current policy possesses the second without the first.

That is a meaningful and useful result.
