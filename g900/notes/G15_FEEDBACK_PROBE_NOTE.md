# G15 Feedback Probe Note

Status: working note
Purpose: record the first explicit feedback test on the witness-machine basin geometry and clarify what kind of feedback is and is not supported by the current evidence

---

## 1. Why this note exists

After establishing local basin geometry for the witness machine, the next natural question was whether the system exhibits a positive feedback loop.

That question sounds simple, but it has at least two different meanings in the present setting.

One meaning is:

- if a state is already near a family, do further perturbations tend to remain in that family?

Another meaning is:

- if a state is already near a family, do further perturbations tend to move it even closer to the exact core of that family?

Those two meanings are not equivalent.

This note records the result of the first explicit feedback probe and freezes the distinction between them.

---

## 2. What was tested

The first feedback probe was run on the action family.

### Seed
The seed cycle was the canonical action cell:

o2,s2,t0,s0,t3,s3

### Parent selection rule
First, all depth-1 one-edit variants of the action seed were generated and classified.

From that depth-1 population, parents were selected by the rule:

- classification = action-cell
- confidence = nearest

So the probe did not use all depth-1 descendants. It used only those depth-1 descendants already classified as action-near.

This is an important point.

The feedback question being tested was not:

- what happens from the seed itself?

It was:

- what happens once you are already inside the action-near region?

### Child generation
From each selected parent, one further local edit was generated and classified.

The probe then measured:

- child classification counts
- child confidence counts
- conditional retention rates
- average change in best-action distance

---

## 3. Raw result

The feedback probe returned the following key quantities.

### Parent pool
- depth1_total = 66
- depth1_parent_count = 45

So out of 66 one-edit variants around the action seed, 45 qualified as action-near parents under the chosen filter.

### Child population
- depth2_total = 1800

This means the selected action-near parents produced a large second-generation population.

### Second-generation classification counts
- action-cell = 1222
- unresolved = 404
- objective-state = 149
- subjective-state = 25

### Second-generation conditional rates
- retention_rate = 0.6788888888888889
- subjective_rate = 0.013888888888888888
- objective_rate = 0.08277777777777778
- action_rate = 0.6788888888888889
- unresolved_rate = 0.22444444444444445

### Distance-feedback metric
The probe tracked the action-family distance metric:

best_action_distance

and computed:

- avg_child_minus_parent = 1.6777777777777778

This quantity is the average child action-distance minus parent action-distance.

So a positive value means:

- on average, children are farther from the action family than their action-near parents were.

This is the critical metric result.

---

## 4. Immediate interpretation

The probe gives a mixed but highly informative answer.

### What is clearly present
There is strong conditional retention of action-family classification.

Approximately 67.9 percent of children of action-near parents are still classified as action-cell.

That is a strong result.

It means the action basin is not fragile noise. It persists under further local perturbation often enough to count as a real local attractor in classification space.

### What is clearly not present
There is no simple metric contraction toward action under unrestricted further perturbation.

The average distance result is positive:

avg_child_minus_parent = +1.6777777777777778

So, on average, the children are farther from the action family than the parents were.

This means that once one is in the action-near region, random additional edits do not generally push deeper into the action core.

So the action family exhibits retention without contraction.

That distinction is the main result of this note.

---

## 5. The two meanings of feedback

The probe makes it necessary to distinguish two kinds of local feedback.

### A. Classification-level feedback
This means:

- once a state is classified in family F, further perturbations tend to remain classified in family F.

Under this definition, the action family does show real local feedback.

That is because:

- the retention rate is high
- the action classification dominates the child population
- action children far outnumber subjective or objective children

This is a genuine positive result.

### B. Distance-level feedback
This means:

- once a state is near family F, further perturbations tend to move it closer to the exact core of F.

Under this definition, the action family does not show positive feedback in the current unrestricted test.

That is because:

- the average child-minus-parent distance is positive
- so the children are, on average, farther from exact action than their parents were

This is not a failure of the model. It is a clarification of what kind of attractor is present.

---

## 6. Best current conclusion

The cleanest current conclusion is:

The action family exhibits strong conditional retention but not metric contraction under unrestricted local perturbation.

This can also be stated as:

- classification-positive
- distance-negative

or more fully:

The action basin is retentive in class membership, but dispersive in metric depth under random additional edits.

That is currently the best compact formulation.

---

## 7. Why the distance result is not surprising

At first glance, the positive average distance shift might sound disappointing. It is not.

In fact, it is exactly the kind of thing one should expect from the way the probe was constructed.

Recall that the parent pool was filtered to include only action-near states.

Many of those parents already had very small best-action distance, often 1.

When a state is already near the boundary of exact action, a random extra edit has many more ways to worsen its distance than to improve it.

There are only a few edits that can restore exact action.
There are many edits that preserve action classification but increase action distance.
There are also some edits that move into ambiguity or objective.

So the average positive distance change does not mean the action basin is fake.

It means that random local noise is not the same thing as aligned contraction.

That is an important conceptual distinction.

---

## 8. Action asymmetry survives the feedback test

One of the most important earlier observations was that action drift is objective-facing.

The feedback probe preserves that conclusion.

The child rates were:

- objective_rate = 0.08277777777777778
- subjective_rate = 0.013888888888888888

So even after conditioning on action-near parents, the children drift toward objective far more often than toward subjective.

This means the action/objective asymmetry is not just a one-step artifact of the seed scan.

It survives a second-generation conditional test.

That strengthens the earlier local basin claim.

The current evidence therefore supports:

- action is a real basin
- action retains strongly
- action disperses metrically under random extra edits
- when action does leak into state structure, it prefers objective over subjective

This asymmetry is now one of the strongest recurring empirical features of the machine.

---

## 9. What kind of basin action appears to be

The present probe suggests that action is not a narrow contracting well.

Instead, it appears to be a broader retentive chamber.

That means:

- many nearby states remain inside the action classification region
- but those states are not necessarily driven inward toward exact action by arbitrary local perturbation

So the action basin is better thought of as:

- wide
- sticky
- internally rough
- and objective-facing at its exits

This is a more sophisticated picture than a simple attractor metaphor.

It suggests a basin that preserves species membership more readily than metric closeness.

---

## 10. Updated local geometry picture

The feedback probe allows the local machine geometry to be restated more precisely.

### Subjective basin
Current evidence still supports:
- strong local basin
- mirror relation with objective at depth 1
- hinge ambiguity seam
- shell/species spillways into action

### Objective basin
Current evidence still supports:
- strong local basin
- mirror relation with subjective at depth 1
- hinge ambiguity seam
- shell/species spillways into action

### Action basin
The feedback probe adds:
- strong conditional retention
- objective-facing asymmetry
- no naive metric contraction under unrestricted local noise

So the three-basin picture survives, but with a new refinement:

The action basin is a retentive chamber rather than a simple contracting well.

---

## 11. What this means for the phrase "positive feedback"

The phrase positive feedback should now be used carefully.

If by positive feedback one means:

- self-retention of family membership

then yes, the action family shows positive feedback.

If by positive feedback one means:

- movement deeper into the same family under further perturbation

then no, not under unrestricted local edits in the present probe.

So a more honest terminology is needed.

Recommended terminology:

- conditional retention
- metric dispersion
- retentive but non-contractive basin
- classification-positive, distance-negative feedback

Any of these is better than loosely saying the action basin simply has positive feedback.

---

## 12. The deeper methodological lesson

This probe is valuable not only for the specific result, but because it sharpens the experimental method.

The machine is now able to distinguish at least three different notions:

- family membership
- family distance
- directional drift between families

Those should not be conflated.

A state can remain in the same classified family while drifting farther from its exact core.
A state can drift toward another family without immediately being classified there.
A state can remain unresolved while still preserving directional asymmetry in its distances.

This means the machine is now behaving more like a real laboratory instrument than a simple recognizer.

It is revealing different structural layers at once.

---

## 13. What the current evidence does and does not support

### Supported
The current evidence supports the following claims.

1. The action basin has strong classification-level persistence.
2. The action basin retains a large share of second-generation descendants.
3. The action basin continues to drift toward objective more often than toward subjective.
4. The action basin is a real local chamber, not a residual junk category.

### Not yet supported
The current evidence does not yet support the stronger claim that:

- action-near parents tend to produce children that are deeper in the action basin on average.

The present unrestricted probe shows the opposite.

So a stronger contraction theorem is not currently warranted.

---

## 14. Best next experiment

The correct next experiment is not to abandon the feedback question, but to refine it.

The present probe used unrestricted local perturbations.

That tests random local continuation.

What it does not test is aligned local continuation.

A stronger feedback test would use a restricted child policy, for example:

- keep only children that do not worsen the target-family distance
- keep only the best few children by target-family distance
- keep only children that remain in the same family
- or search greedily for distance-decreasing descendants

That would test whether the action basin has an internal contracting core under aligned rather than random perturbation.

So the next question is not:

Does feedback exist?

The next question is:

Does action exhibit contractive feedback under admissible continuation rather than unrestricted noise?

That is a much better question.

---

## 15. Provisional conclusion

The first feedback probe gives a strong but nuanced answer.

The action family is genuinely self-retaining at the classification level.

However, random further edits do not drive states deeper into exact action on average.

Therefore the present evidence supports:

- retentive local feedback
- objective-facing asymmetry
- metric dispersion under unrestricted perturbation

The best current statement is:

The action basin is classification-stable but metrically non-contractive under unrestricted local perturbation.

That is the current feedback result.

---

## 16. Short summary

Current best read:

- action retains about 67.9 percent of children of action-near parents
- action drifts toward objective much more than toward subjective
- action does not contract inward on average under random extra edits
- therefore the action basin is retentive, but not contractive, in the current feedback probe

This is the current witness-machine feedback picture.

