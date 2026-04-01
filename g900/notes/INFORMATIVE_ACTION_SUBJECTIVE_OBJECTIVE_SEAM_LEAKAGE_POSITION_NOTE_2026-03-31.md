# INFORMATIVE_ACTION_SUBJECTIVE_OBJECTIVE_SEAM_LEAKAGE_POSITION_NOTE_2026-03-31

## Status

Working synthesis note.

This note gathers the current computational findings into a single conceptual position statement connecting:

- informative action
- the subjective / objective gap
- objective seam leakage
- the repaired frame-0 chamber
- the residual frame-2 bottleneck
- the slot-4 lock
- and the bounded-corridor saturation result

The purpose of this note is not merely to summarize logs, but to state what the current experiments now allow us to say in a coherent thesis-facing way.

---

## Executive summary

The current computational ladder supports a strong and now fairly localized thesis.

The sampled action-family dynamics are not random and do not merely wander. They exhibit:

- monotone descent in normalized action distance
- strong contraction toward the action family
- a dominant reachable chamber that can be repaired by an exact-preference policy
- a deeper residual basin that funnels into a specific frame-2 near-action bottleneck
- and a sharply localized local obstruction at normalized position 4

The strongest current result is this:

> exact frame-2 closure requires the value `t2` at normalized position 4, but the explored local dynamics do not install that value.

This remains true even after:

- repairing the dominant frame-0 reachable fringe
- tracing deeper feeder chambers into frame 2 by depth 4
- exploring the strict frame-2 corridor to depth 6
- and performing a bounded escape-and-return sweep to depth 8 with action distance capped at 3

Within that bounded regime, the reachable set saturates by depth 6 and still does not produce:

- exact frame-2 closure
- or the exact slot value `t2`

This means the current residual problem is no longer diffuse. It is highly structured and local.

The cleanest current synthesis is:

> informative action can find the objective seam without yet sealing it. The remaining subjective–objective gap is not primarily global directionality but local installation. Objective seam leakage is the observable failure mode of a one-slot lock centered on normalized position 4.

---

## 1. Informative action: what the experiments now show

The experiments clarify that informative action is not just any movement through state space.

At minimum, informative action in the present setting has two separable aspects:

1. **Directional informativeness**
2. **Closure-sufficient informativeness**

### 1.1 Directional informativeness

The baseline two-step policy already showed monotone descent in normalized action distance on the sampled run.

That means the dynamics were not arbitrary.

They were already:

- basin-seeking
- lawful in the lens
- contractive toward the action family
- and geometrically informative about where the correct chamber lies

In other words, the system already knew something real about the target.

It could find the correct neighborhood.

This is the first sense in which the action is informative:
it reduces uncertainty and narrows the region of plausible closure.

### 1.2 Closure-sufficient informativeness

But the frame-2 bottleneck shows that finding the right neighborhood is not the same as closing.

The system can:

- reach the correct near-action fringe
- remain highly structured there
- preserve contact with the frame-2 side
- and still fail to install the exact missing local content needed for closure

So informative action must be refined.

It is not enough for action to be globally aligned or locally lawful in a weak sense.
To be closure-sufficient, action must actually carry the missing local content into the closure site.

That is the crucial distinction.

### 1.3 Best current formulation

The cleanest formulation is:

> informative action can be geometrically correct without yet being closure-sufficient.

Or more concretely:

> informative action can find the lock without yet carrying the key.

That is now one of the strongest conceptual lessons of the whole ladder.

---

## 2. What we have learned about the subjective / objective gap

The experiments have also sharpened the meaning of the gap between the subjective and objective.

The main discovery is that this gap is **layered**.

It is not one undifferentiated “distance from truth.”

### 2.1 The gap is not pure randomness

The baseline dynamics already showed monotone descent toward the action family.

So the subjective side is not pure drift.
It can move lawfully toward objective structure.

This means the subjective–objective gap is not sheer separation.
There are real transport channels.

### 2.2 Much of the gap is procedural, not essential

The frame-0 chamber is the clearest example.

There, exact-preference repaired the dominant reachable fringe immediately.
That means a large part of what first looked like a deep subjective–objective separation was actually a policy-selection defect.

The walker reached the correct porch but did not take the available exact-closing step.

So part of the gap was not metaphysical.
It was procedural.

### 2.3 The final gap is local, not global

Frame 2 is different.

There the system reaches the correct near-action chamber and still does not close.
By that point, the global directional gap has already been substantially reduced.
What remains is local:

- one normalized slot
- one missing exact value
- one unsatisfied installation

So the final subjective–objective gap is not “being in the wrong world.”
It is “being in the right neighborhood without the right local content.”

### 2.4 Best current formulation

The cleanest statement is:

> the subjective–objective gap is stratified. Lawful descent and improved policy can reduce most of it, but the final gap can persist as a sharply localized closure obstruction.

Or even shorter:

> the final gap is not one of direction anymore; it is one of installation.

---

## 3. Objective seam leakage: what it now means

The phrase “objective seam leakage” now has a much sharper computational meaning.

Earlier it could have sounded metaphorical or impressionistic.
Now it has a concrete operational reading.

### 3.1 The seam is real

The system does reach the frame-2 objective-adjacent seam.
This is not a fake or imagined structure.
The residual basin funnels there repeatedly, and even deeper feeder chambers connect to it by depth 4.

So the seam is not merely a narrative device.
It is computationally visible.

### 3.2 The seam does not seal

Despite reaching that seam, exact closure still fails.

The system is Hamming-1 from the exact frame-2 target.
The exact requirement is extremely local:
normalized position 4 must become `t2`.

But that installation does not occur in the bounded explored regime.

So the seam is present but unsealed.

### 3.3 Leakage is the observable failure mode

What happens instead?

The transition-law analysis shows two dominant patterns:

1. slot-4 persistence within the frame-2 corridor
2. slot-changing moves that spill into unresolved / ambiguous states at larger action distance

That is exactly what seam leakage means here.

The system presses against the objective seam, but without the exact local key, its edits either:

- keep circulating in a stable near-action corridor,
or
- leak sideways into ambiguous neighboring regions

rather than producing exact closure.

### 3.4 Best current formulation

The cleanest statement is:

> objective seam leakage is the observable failure mode of a local closure obstruction.

And even more concretely:

> the system reaches the seam, but without `t2` in the locked slot, local edits leak into ambiguity instead of sealing objective closure.

That is now a computational statement, not just a metaphor.

---

## 4. The ladder that got us here

To understand the thesis-level meaning, it helps to state the ladder cleanly.

### 4.1 Baseline two-step policy

After excluding trivial exact starts, the baseline policy gave:

- 599 non-exact starts
- 0 exact repairs

But it also gave monotone descent in normalized action distance.

This established:
- strong contraction
- real geometry
- no nontrivial exact closure

### 4.2 Exact-preference patch

Adding exact-preference changed the regime sharply:

- exact repairs jumped to 402 / 599

This showed that the dominant frame-0 fringe was not a deep obstruction.
It was a selection bug.

So the front porch was fixable.

### 4.3 Residual frame-2 core

After the patch, the residual near-action fringe at distance 1 was:

- entirely frame-2-nearest
- with no exact one-edit closure

This identified frame 2 as the real bottleneck.

### 4.4 Deeper chambers

The depth-3 and depth-4 probes then showed that what initially looked like a separate frame-1 / frame-4 unresolved chamber actually feeds into the frame-2 near-action fringe.

So the geometry is layered, but convergent.
The deeper side chambers do not stay independent forever.
They flow into the same frame-2 bottleneck.

### 4.5 Hamming-1 reduction

The extracted frame-2 witnesses were all Hamming-1 from the exact frame-2 target.

The mismatch was always:

- one coordinate
- normalized position 4
- exact target value `t2`

At that point the entire obstruction problem reduced to a one-slot lock.

### 4.6 Strict corridor probe

A strict frame-2 corridor probe out to depth 6 showed:

- no exact frame-2 closure
- no observed `t2`
- stable cycling among wrong slot-4 values

### 4.7 Bounded escape-and-return sweep

A widened escape-and-return sweep with action distance <= 3 showed:

- no exact frame-2 closure through depth 8
- no `t2` anywhere in the explored bounded regime
- saturation of the reachable bounded state set by depth 6

That last point is particularly strong.
It means the bounded regime appears computationally exhausted, yet still lacks the key.

---

## 5. The one-slot lock

This is the real centerpiece now.

### 5.1 The exact requirement

For exact frame-2 closure, the exact normalized target requires:

- position 4 = `t2`

### 5.2 What we actually see

Instead of `t2`, the observed frame-2 near-action witnesses and corridor states exhibit a stable alphabet of wrong values at that slot, including values such as:

- `t4`
- `o4`
- `s3`
- `s0`
- `s2`
- `s4`
- `t0`
- `t3`

But never `t2`.

### 5.3 Persistence and leakage

The local transition law then shows:

- strong slot-value persistence while remaining near-action
- many slot-changing moves ejecting the state into unresolved / ambiguous regions at larger action distance

So the lock has two visible behavioral properties:

1. **the wrong values are locally stable**
2. **attempts to change them often break corridor membership instead of sealing closure**

That is why this is properly described as a lock, not just a generic failure.

### 5.4 Best current obstruction law

The strongest current experimental law is:

> the frame-2 near-action bottleneck is a one-slot installation obstruction centered on normalized position 4, where the exact value `t2` is required but not produced by the explored local dynamics.

---

## 6. What this means for the thesis

This changes the thesis, but in a good way.

The thesis is no longer best stated as:

> the present dynamics achieve exact closure.

That claim is too strong.

Instead, the thesis now becomes sharper and more believable:

### 6.1 Positive claim

The action geometry is real.

The system exhibits:
- monotone descent
- chamber structure
- funneling behavior
- and partial repair under a principled intervention

### 6.2 Negative / obstruction claim

Exact closure is blocked by a structured local obstruction.

After repairing the reachable chamber, the residual basin funnels into frame 2, where closure requires a one-slot installation that the bounded dynamics do not realize.

### 6.3 Strong bounded-regime thesis

A strong current thesis statement is:

> The sampled action-family dynamics admit monotone descent and partial repair, but exact closure is blocked by a local frame-2 obstruction. Within the bounded escape-and-return regime, the reachable set saturates without ever producing the exact slot value `t2` required at normalized position 4.

That is already thesis-grade.

It is not vague, and it is not merely descriptive.
It is structured, falsifiable, and computationally saturated in the bounded regime.

---

## 7. The thesis in cube-walk language

If we say it in the walk-around-the-cube language:

- the walker does know downhill toward home
- the front porch on the frame-0 side was repaired by teaching the walker to step through the obvious door
- the deeper side chambers eventually feed the frame-2 balcony
- once on that balcony, the walker is always one lock-component short of exact entry
- the missing key is always the same: `t2` in the locked socket
- the walker can move around the balcony and even make bounded excursions nearby
- but within that whole bounded neighborhood, the key never appears and the door never opens

That is the embodied version of the obstruction result.

---

## 8. What is now resolved

The following are now firmly resolved.

### 8.1 About informative action

Resolved:

- informative action is not identical with exact closure
- action can be globally and geometrically informative without being closure-sufficient
- closure requires local installation of the missing content

### 8.2 About the subjective / objective gap

Resolved:

- the gap is layered
- much of it is reducible by lawful descent and better policy
- the final gap can persist as a sharply localized obstruction

### 8.3 About objective seam leakage

Resolved:

- seam leakage is not just a metaphor for drift
- it is the observable failure mode of the frame-2 local obstruction
- edits near the seam tend either to preserve wrong slot-4 values or spill into ambiguous neighboring regions

### 8.4 About the frame-2 lock

Resolved:

- exact frame-2 closure requires `t2` at normalized position 4
- strict corridor search does not install `t2`
- bounded escape-and-return search saturates without installing `t2`
- the bounded regime therefore excludes the exact key

---

## 9. What remains open

The remaining open questions are now much narrower.

### 9.1 Global reachability of `t2`

Is `t2` globally reachable at normalized position 4 only through a qualitatively broader regime than the bounded one explored here?

### 9.2 Invariant explanation

Does a deeper invariant of the move grammar explain why the bounded frame-2 regime excludes `t2`?

### 9.3 Symbolic law of the slot-4 alphabet

Is there a parity-like, orbit-like, or symbolic conservation law governing the observed slot-4 alphabet?

### 9.4 Formal theorem

Can the bounded-regime obstruction be promoted from a computational saturation result to a formal theorem?

These are the right next theoretical questions.

---

## 10. Best current theorem-shaped statement

A clean theorem-shaped formulation suggested by the evidence is:

> After exact-preference resolves the dominant frame-0 reachable fringe, the residual basin funnels toward a frame-2 near-action bottleneck. The frame-2 witnesses are Hamming-1 from the exact frame-2 target and differ only at normalized position 4. The exact slot value required there is `t2`. Within the bounded escape-and-return regime of action distance at most 3, the reachable set saturates computationally by depth 6 without ever producing `t2` or exact frame-2 closure. The current evidence therefore supports a bounded-regime one-slot obstruction law for frame 2.

This is not yet a universal proof, but it is now a sharply localized, layered, and computationally saturated obstruction result.

---

## 11. Best short summary

Informative action can find the objective seam without yet sealing it.

The subjective–objective gap is now localized to a one-slot lock.

Objective seam leakage is what happens when the system reaches that seam without the key.

And within the bounded frame-2 neighborhood, the key is nowhere to be found.

Or more compactly:

> monotone descent, partial repair, local obstruction, bounded saturation.

