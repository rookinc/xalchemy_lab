# ACTION_FRAME2_OBSTRUCTION_LAW_POSITION_NOTE_2026-03-31

## Status

Working position note.

This note records the strongest current computational obstruction result for the frame-2 near-action bottleneck after the full ladder of baseline, exact-preference, hard-shell, depth-4 feeder, strict corridor, and bounded escape-return probes.

---

## Executive summary

The current computational evidence supports a sharp obstruction picture centered on the frame-2 near-action chamber.

The established ladder is now:

1. The baseline two-step lookahead is monotone in normalized action distance on the sampled run but produces no nontrivial exact repairs.
2. Adding exact-preference resolves the dominant frame-0 reachable fringe and produces 402 exact repairs out of 599 non-exact starts.
3. The remaining basin funnels toward a frame-2 near-action obstruction.
4. The recorded frame-2 near-action witnesses are all Hamming-1 from the exact frame-2 representative and differ only at normalized position 4.
5. The exact value required at that locked slot is `t2`.
6. A strict frame-2 corridor probe to depth 6 does not install `t2` and does not reach exact frame-2 closure.
7. A bounded escape-and-return probe to depth 6 with allowed action distance up to 3 also does not reach exact frame-2 closure.

The best current summary is:

> the frame-2 bottleneck behaves as a one-slot obstruction law: exact closure requires `t2` at normalized position 4, but the explored local dynamics do not install that value, even when bounded off-corridor escape and return are allowed.

---

## 1. Baseline result

The baseline two-step lookahead was tested on the sampled nontrivial D4 action-family.

After excluding trivial exact starts, the baseline run yielded:

- 599 non-exact starts
- 0 exact repairs

At the same time, the baseline policy was shown to be stepwise nonincreasing in normalized action distance on the realized walk set. So the baseline rule has genuine geometric directionality, but not exact closure.

This established the first structural slogan:

> contraction without closure.

---

## 2. Exact-preference resolves the dominant reachable fringe

A local analysis of the baseline distance-1 fringe showed that the dominant part of that fringe was exact-reachable in one edit but not being selected by the policy.

Adding an exact-preference rule changed the regime sharply:

- exact repairs after patch: 402 / 599
- failures after patch: 197

This demonstrated that the dominant baseline failure was not geometric impossibility. It was a policy-selection failure on the frame-0 reachable fringe.

So the reachable front porch was repaired.

---

## 3. Residual basin structure after exact-preference

After exact-preference, the residual basin split into:

- distance 1: 71
- distance 2: 123
- distance 3: 3

The residual distance-1 layer was then shown to be:

- entirely nearest to frame 2
- with no exact one-edit closure

So the remaining near-action obstruction core was concentrated on frame 2.

This was the first sign that the real bottleneck lived there.

---

## 4. Hard shell and depth structure

The residual distance-2 layer was analyzed in stages.

### 4.1 One- and two-step probes

The distance-2 layer had no one-edit route to exactness or to action-cell distance 1.

A two-step probe split it into:

- a tiny exact-reachable piece
- a larger piece with two-step routes toward frame-0 distance-1 states
- a 63-state hard shell with no <=2-step exact or action-cell distance-1 hit

### 4.2 Depth-3 probe on the hard 63

A parallel depth-3 probe on the 63-state hard shell showed:

- 43 open to action-cell distance 1 within depth 3
- 20 remain unresolved within depth 3
- none reaches exact closure within depth 3

### 4.3 Depth-4 probe on the unresolved 20

The unresolved 20 were clustered near frame 1 and frame 4 at depth 3, but a depth-4 probe showed:

- all 20 open to action-cell distance 1 by depth 4
- all 20 have a route to a frame-2-nearest distance-1 state
- none reaches exact closure within depth 4

So the frame-1 / frame-4 chamber is not isolated. It is a deeper feeder chamber into the frame-2 near-action bottleneck.

The residual geometry is therefore layered, but it converges on frame 2.

---

## 5. Frame-2 witnesses reduce the problem to one slot

The frame-2-nearest distance-1 witnesses extracted from the depth-4 feeder analysis were then compared directly to the exact frame-2 representative.

Result:

- all recorded frame-2 witnesses were Hamming-1 from the exact frame-2 target
- every mismatch occurred at normalized position 4
- the exact frame-2 target requires `t2` at that position

Observed wrong values at that slot included:

- `t4`
- `o4`
- `s3`
- `s0`

So the frame-2 bottleneck reduced to a one-slot installation question:

> why does normalized position 4 fail to become `t2`?

This is the key reduction.

---

## 6. Strict frame-2 corridor probe

A strict corridor probe was then run on the unique frame-2 witness states.

This probe explored only the frame-2 near-action corridor.

Headline result:

- start_count = 4
- visited_corridor_state_count = 8
- exact_frame2_one_edit_hits_found = 0
- corridor_t2_examples_found = 0
- off-corridor `t2` examples found inside this restricted corridor search = 0

The slot-4 values actually observed in the corridor were:

- `t4`
- `o4`
- `s3`
- `s0`
- `s2`
- `s4`
- `t0`
- `t3`

but never `t2`.

The dominant local transitions were persistence transitions that kept the current slot-4 value unchanged while remaining action-cell-nearest. Many slot-changing moves led instead to unresolved ambiguous states at much larger action distance.

So the strict corridor probe showed:

- the corridor is stable
- the locked slot cycles among several wrong values
- the exact value `t2` is not installed
- exact frame-2 closure is not locally present inside the corridor

This is the first clear experimental form of the lock law.

---

## 7. Bounded escape-and-return probe

A natural escape hypothesis remained:

> perhaps `t2` can only be installed by briefly leaving the strict frame-2 corridor and returning.

To test that, a bounded escape-and-return probe was run from the unique frame-2 witness starts with:

- max depth = 6
- allowed action distance up to 3

Result:

- `has_exact_frame2_count = 0`
- `has_frame2_d1_count = 4`

So all four unique witness starts remain connected to the frame-2 near-action channel, but none reaches exact frame-2 closure even when short off-corridor excursions are allowed.

This rules out the simplest escape-and-return explanation.

---

## 8. Best current obstruction law

The strongest current obstruction law suggested by the evidence is:

> The frame-2 near-action bottleneck is a one-slot installation obstruction. Exact frame-2 closure requires `t2` at normalized position 4. The explored local dynamics do not install `t2` there. Strict corridor dynamics overwhelmingly preserve a small alphabet of wrong slot-4 values while remaining near-action, and bounded off-corridor escape-and-return to depth 6 still does not produce exact frame-2 closure.

This is the clearest current statement of the lock.

---

## 9. Cube-walk translation

In walk-around-the-cube language:

- the walker can descend toward the lawful chamber
- the front porch on the frame-0 side was fixed by teaching the walker to use the obvious door
- the deeper side chambers eventually feed the frame-2 balcony
- on that balcony, the walker is always one lock-component short of opening the door
- the missing key is always the same: `t2` in the locked socket
- the walker can shuffle around the balcony and even take small excursions away from it
- but the key never reaches the lock, and the door never opens

So the obstruction is not just “we do not get home.”

It is:

- a stable balcony
- a locked socket
- and a missing key value that the explored dynamics do not install

---

## 10. What is now resolved

Resolved:

1. The baseline rule fails mostly because of policy selection on the frame-0 reachable fringe.
2. Exact-preference repairs that reachable frame-0 component.
3. The deeper residual geometry funnels toward frame 2.
4. The frame-2 near-action bottleneck is Hamming-1 from exactness.
5. The mismatch is localized entirely at normalized position 4.
6. The exact required value there is `t2`.
7. Strict corridor dynamics to depth 6 do not install `t2`.
8. Bounded escape-and-return dynamics to depth 6 and action distance 3 also do not reach exact frame-2 closure.

---

## 11. What remains open

Open:

1. Whether `t2` is globally reachable at normalized position 4 only through longer or more weakly constrained excursions.
2. Whether a deeper invariant of the move grammar excludes `t2` from that slot in the frame-2 channel.
3. Whether there is a symbolic or parity-like law governing the observed slot-4 alphabet.
4. Whether a stronger policy should search for an off-corridor installation route rather than a corridor-preserving route.

These are now the right theoretical questions.

---

## 12. Best theorem-shaped statement

A clean theorem-shaped formulation suggested by the evidence is:

> After exact-preference resolves the dominant frame-0 reachable fringe, the residual basin funnels toward a frame-2 near-action bottleneck. The frame-2 witnesses are all Hamming-1 from the exact frame-2 target and differ only at normalized position 4. The exact slot value required there is `t2`. Neither strict frame-2 corridor exploration nor bounded escape-and-return exploration to depth 6 produces exact frame-2 closure from the unique frame-2 witness states. The current evidence therefore supports a one-slot obstruction law centered on the non-installation of `t2` at normalized position 4.

This is not yet a universal proof, but it is a sharply localized and highly structured obstruction result.

---

## 13. Best short summary

The frame-0 porch was fixable.

The deeper side chambers feed frame 2.

The frame-2 balcony is a one-slot lock.

The missing key is `t2`, and the explored local dynamics do not put it in the lock.

Or more compactly:

> the balcony is stable, the lock is local, and the key never seats.

