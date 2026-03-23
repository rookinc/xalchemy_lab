# G900 prism quotient note v0.1

## Current result

The order-30 triangular subdivision carrier yields a 900-cell candidate presentation with:

- 10 inward layers
- 3 macro sectors
- 2 live-bit classes

A contact-surface probe on cell adjacency gives a highly structured class interaction law.

---

## Bit contact totals

- `(0,0) = 420`
- `(0,1) = 435`
- `(1,1) = 450`

These are all present and differ by a constant step of 15.

So the bit split is real and globally active.

---

## Macro contact totals

Same-macro contacts:

- `(0,0) = 145`
- `(1,1) = 145`
- `(2,2) = 145`

Cross-macro contacts:

- `(0,1) = 290`
- `(0,2) = 290`
- `(1,2) = 290`

So macro symmetry is exact, and cross-macro contact is exactly double same-macro contact.

---

## Combined `(macro, bit)` contact law

The six class nodes are:

- `(0,0)`
- `(0,1)`
- `(1,0)`
- `(1,1)`
- `(2,0)`
- `(2,1)`

Observed nonzero contacts are:

- `((0,0),(0,1)) = 145`
- `((1,0),(1,1)) = 145`
- `((2,0),(2,1)) = 145`

and

- `((0,0),(1,0)) = 140`
- `((0,0),(2,0)) = 140`
- `((1,0),(2,0)) = 140`

and

- `((0,1),(1,1)) = 150`
- `((0,1),(2,1)) = 150`
- `((1,1),(2,1)) = 150`

No opposite-bit cross-macro contacts appear.
No same-bit same-macro self-contacts appear at the class-pair level.

---

## First quotient support

Ignoring weights and keeping only nonzero support, the 6-class contact graph has:

- one triangle on the bit-0 classes
- one triangle on the bit-1 classes
- three vertical macro-pair links joining `(m,0)` to `(m,1)`

This is exactly the triangular prism graph.

So the current candidate statement is:

> the first class-contact quotient support of the G900 carrier is the triangular prism on 6 class nodes

This is not yet a theorem about the final graph ladder.
It is a theorem candidate about the first coarse quotient support induced by the sampled carrier.

---

## Why this matters

This is the first small finite support graph extracted from the G900 candidate carrier.

So the G900 conjecture has now advanced from:

- count
- layer law
- macro/bit law

to:

- an explicit 6-node quotient support

That is a real structural milestone.

---

## Layer-conditioned clue

Layer-conditioned bit contacts alternate between two regimes.

Examples:

- layer 0: `(0,0)=56`, `(0,1)=84`, `(1,1)=112`
- layer 1: `(0,0)=100`, `(0,1)=75`, `(1,1)=50`
- layer 2: `(0,0)=44`, `(0,1)=66`, `(1,1)=88`
- layer 3: `(0,0)=76`, `(0,1)=57`, `(1,1)=38`

This suggests that layer may carry an alternating phase rather than mere radial depth.

Do not overclaim yet, but record this as a live clue.

---

## Next burden

Make the prism support explicit by constructing the 6x6 weighted class adjacency matrix and its unweighted support matrix.

Then test:

1. whether the support graph is exactly the triangular prism
2. whether the weights admit a meaningful normalization
3. whether layer parity induces a refinement of the prism support

