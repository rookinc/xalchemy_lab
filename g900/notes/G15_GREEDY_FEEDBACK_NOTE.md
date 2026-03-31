# G15 Greedy Feedback Note

Status: working note
Purpose: record the result of the greedy feedback probe and clarify how it changes the interpretation of the action basin

---

## 1. Why this note matters

The earlier unrestricted feedback probe showed an important but incomplete result.

That probe demonstrated that the action family is:

- strongly self-retaining at the level of classification
- but not metrically contractive under random further perturbation

In plain language:

- once a state becomes action-like, random nearby states are often still action-like
- but random extra edits do not, on average, push the state deeper into exact action

That result was already useful, because it distinguished:

- retention
from
- contraction

However, it also left an open question.

The unresolved question was:

Does the action basin fail to contract because it has no contracting structure, or only because random perturbation is the wrong way to test it?

The greedy feedback probe was designed to answer that question.

The answer is now much sharper.

The action basin does appear to have an internal contracting structure, but that structure is visible under aligned descent rather than under unrestricted local noise.

This note freezes that conclusion.

---

## 2. The question the greedy probe asks

The greedy probe does not ask:

What happens if we keep bumping the machine randomly?

Instead, it asks:

If a state is already action-near, and at each step we choose the child that best improves action distance, can the state be tightened back into exact action?

This is a fundamentally different experiment.

The unrestricted probe measured random continuation.
The greedy probe measures admissible or aligned continuation.

That distinction now turns out to be essential.

---

## 3. Setup of the greedy test

### Seed
The seed remained the canonical action cell:

o2,s2,t0,s0,t3,s3

### Parent rule
Parents were chosen from the one-edit neighborhood by the filter:

- classification = action-cell
- confidence = nearest

So the probe starts from states that are already known to be action-near, but not exact.

### Greedy rule
At each step:

- all one-edit children are generated
- the child with the best action-distance is selected
- ties are resolved in favor of exact target membership, then target-family membership
- the walk stops if there is no improvement or if exact action is reached

This is a local greedy repair policy.

It is not random wandering.
It is not global optimization.
It is simply the best local descent available under the target metric.

---

## 4. Main result

The greedy probe changes the interpretation of the action family in a major way.

The currently inspected walks show that many action-near parents are tightened back to:

- action-cell
- exact
- best_action_distance = 0

and in many of the displayed examples this happens in:

- one step

This is the crucial new result.

The action basin is therefore not merely:

- sticky in classification
- but metrically dispersive under random noise

It is also:

- locally repairable
- and contractive under greedy admissible descent

This is a much stronger structural statement.

---

## 5. The most important distinction

The greedy probe makes the following distinction unavoidable.

### Random probe
The random probe showed:

- action retains many descendants
- but average action distance increases under unrestricted further edits

So the action basin is not self-tightening under arbitrary local perturbation.

### Greedy probe
The greedy probe shows:

- many action-near states admit immediate local repairs
- these repairs reduce best-action distance
- many of them terminate at exact action
- often in one move

So the action basin is self-tightening under aligned local continuation.

This is a very different result.

The correct synthesis is:

The action basin is non-contractive under random noise, but contractive under greedy repair.

This is the core message of the note.

---

## 6. What the examples are showing

The displayed examples are remarkably clean.

Again and again the same pattern appears:

- a parent begins as action-cell, nearest
- its best_action_distance is often 1, sometimes 3
- the greedy move simply restores the disturbed coordinate
- the child becomes action-cell, exact
- the distance drops to 0

Examples of repair patterns visible in the output include local reversals such as:

- replacing o4 back with t0
- replacing o2 back with s0
- replacing s4 back with s0
- replacing t4 back with t3
- replacing s2 back with s3
- replacing altered fifth or sixth coordinates back to their exact action values

These are not vague classifier successes.

They are explicit local repairs.

That is why the greedy probe is so informative.

It shows that the action-near region is not only near in a statistical sense.
It is near in a repairable structural sense.

That is a much stronger claim.

---

## 7. New interpretation of the action basin

Before the greedy test, the best metaphor for the action basin was something like:

- a broad sticky swamp

That metaphor captured classification retention, but it did not capture repair.

After the greedy test, that metaphor is no longer adequate.

A better picture is:

- a broad sticky region under random perturbation
- with an internal contractive spine under aligned descent

Another way to say this is:

- the action basin has a noisy outer shell
- but inside that shell there is a recoverable repair structure

This is a major improvement in understanding.

The action family is not just stable enough to keep identity.
It is structured enough to support local recovery.

---

## 8. What this means for "positive feedback"

The phrase positive feedback now needs a refined meaning.

### Under unrestricted noise
If positive feedback means:

- random further perturbation makes action-near states more exact on average

then the answer remains no.

The random probe already showed that average action distance increases under arbitrary local continuation.

So there is no naive random contraction.

### Under admissible continuation
If positive feedback means:

- once near action, locally best moves tend to bring the state closer to exact action

then the answer is yes.

The greedy probe now supports exactly that statement.

So the right formulation is:

The action family exhibits admissible local contraction, but not random-noise contraction.

This is probably the most precise short summary.

---

## 9. Why this is exciting

This result is exciting because it means the witness machine is revealing not merely a static classification landscape, but a dynamic local repair geometry.

That is a much richer kind of structure.

The machine is now distinguishing at least three layers of behavior:

1. family membership
2. family distance
3. family repairability

The greedy probe is about the third layer.

That layer is especially valuable because it suggests the machine has something like a lawful correction mechanism.

In other words:

being near a family is not only a matter of resemblance
it is also, in many cases, a matter of recoverable deformation

That is a very strong structural signal.

---

## 10. Updated action-basin picture

The current best action-basin picture is now:

### Outer behavior under noise
- strong retention of action classification
- outward metric dispersion
- objective-facing leakage stronger than subjective-facing leakage

### Inner behavior under repair
- many action-near states tighten to exact action
- local repair often succeeds in one step
- the action core is reachable by a greedy local policy

So the action basin has both:

- persistence
and
- recoverability

Those are not the same thing, and the greedy probe is what reveals the second.

---

## 11. How this changes the global local-geometry story

The witness machine now looks more structured than before.

The previous local picture already contained:

- subjective basin
- objective basin
- action basin
- hinge ambiguity seam
- action/objective asymmetry

The greedy probe now adds:

- action has a recoverable internal core

So the updated picture is:

- subjective and objective remain the primary state chambers
- action remains a genuine third chamber
- action is sticky under noise
- action is repairable under admissible descent
- action remains objective-facing at its non-action exits

This is not yet a full global theory, but it is a very meaningful local one.

---

## 12. The best current synthesis

The correct synthesis of the random and greedy probes is now:

### Random continuation
- preserves action membership often
- but does not improve action depth on average

### Greedy continuation
- frequently improves action depth
- often restores exact action immediately

So the basin is:

- retentive under random continuation
- contractive under greedy continuation

This is the most important conclusion of the note.

The previous tension between retention and dispersion is now resolved.

There was no contradiction.
There were simply two different continuation laws.

---

## 13. What this suggests mathematically

The greedy result suggests that the action basin may contain a genuine admissible descent law.

That is stronger than mere attraction.

It suggests:

- there may be local normal forms around exact action
- many near-action states may be one-edit deformations of exact action
- action-distance may be a meaningful local Lyapunov-like guide under admissible continuation

This is still provisional language, not theorem language.

But the greedy probe now makes those questions mathematically credible.

Before the greedy probe, they were only suggestive.
Now they are experimentally motivated.

---

## 14. What remains open

Several important questions remain.

### Open question 1
Does the same greedy contraction phenomenon hold for the subjective basin?

### Open question 2
Does it hold for the objective basin?

### Open question 3
Are there action-near parents that do not greedily contract to exact action within the tested step limit?

### Open question 4
Does the objective-facing asymmetry remain visible even under greedy target-specific descent?

### Open question 5
Can one define an admissibility rule stronger than greedy local distance minimization that reveals a deeper internal geometry?

These are now good experimental questions rather than vague hopes.

---

## 15. Present working conclusion

The action family now has a much more refined interpretation.

From the unrestricted probe we learned:

- action is classification-stable but metrically dispersive under random local noise

From the greedy probe we now learn:

- action-near states often admit immediate local repair to exact action

Therefore the best current conclusion is:

The action basin is not randomly self-tightening, but it does possess a locally contractive repair structure under greedy admissible continuation.

That is the present best read.

---

## 16. Short summary

Current best read:

- random local perturbation keeps many states in the action family but does not deepen them on average
- greedy local continuation often pulls action-near states directly back to exact action
- the action basin is therefore both sticky and repairable
- its outer shell is noisy, but its inner core is contractive under aligned descent

This is the current greedy feedback picture of the witness machine.

