# G15 Thesis Test Plan

## Status
Working test plan

## Thesis under test

We are testing the claim that **G15 is a rigid host frame**: a lawful chambered scaffold with a deterministic transport grammar capable of housing and rendering legible richer constructions such as G30, AT4val[60,6], and G900.

This does **not** yet claim full embedding or full derivation.

The immediate claim is narrower:

> There exists a deterministic oriented state grammar on G15, together with a nontrivial pathing system, such that the proposed walk closes exactly and induces a meaningful family of lawful related traversals.

---

## Core emphasis: pathing matters

The thesis is not only about static adjacency.

It is also about **pathing**.

A host frame must support:

- lawful local motion
- coherent orientation
- repeatable path composition
- closure of selected words
- meaningful variation of nearby words

So every test below should be read as both:

- a structural test of G15
- and a pathing test of the motion grammar carried by G15

The key question is:

> Does G15 support a stable, deterministic, and reusable pathing regime?

---

## Objects under test

### 1. Host frame
- **G15**

### 2. Candidate occupants
- **G30**
- **AT4val[60,6]**
- **G900**

### 3. Primitive motion operators
- `lift`
- `left`
- `right`
- `move`

These operators are treated as native host actions, not merely drawing instructions.

---

## State model

We take a traversal state to be:

\[
s = (v,\sigma,h)
\]

where:

- \(v\) = ambient host location
- \(\sigma\) = layer, sheet, sign, or register
- \(h\) = heading or local facing

This is necessary because pathing depends on more than bare vertex identity.

In particular:

- `left` and `right` require heading
- `lift` may require a layer/register distinction
- `move` requires an oriented local rule

---

## Host operators

Let:

- \(U\) = `lift`
- \(L\) = `left`
- \(R\) = `right`
- \(M\) = `move`

acting on traversal states.

Intended meanings:

- \(L(v,\sigma,h)\): same location, turn left
- \(R(v,\sigma,h)\): same location, turn right
- \(M(v,\sigma,h)\): advance along the current heading
- \(U(v,\sigma,h)\): lift to the corresponding state in the next register

These must be made explicit enough to test path closure and path variation.

---

## Anchor walk under test

The current anchor walk is:

\[
\begin{aligned}
n_0 &= \text{chosen start state} \\
n_1 &= U(n_0) \\
n_2 &= U(n_1) \\
n_3 &= M(R(M(L(n_2)))) \\
n_4 &= M(M(R(n_3))) \\
n_5 &= M(M(R(n_4))) \\
n_6 &= M(M(R(n_5))) \\
n_7 &= M(L(M(R(n_6)))) \\
n_8 &= M(M(R(n_7))) \\
n_9 &= M(M(n_8)) \\
n_{10} &= M(M(n_9)) \\
n_{11} &= M(L(M(R(n_{10})))) \\
n_{12} &= M(M(n_{11})) \\
n_{13} &= M(M(n_{12})) \\
n_{14} &= M(M(n_{13})) \\
n_{15} &= M(L(M(n_{14}))) = n_0
\end{aligned}
\]

This is the primary pathing witness.

If this fails, the host claim weakens immediately.

---

## Pathing questions

The thesis depends on answers to the following pathing questions.

### Q1. Determinism
Does each admissible state have a unique result under each primitive operator?

### Q2. Coherence
Do repeated compositions of the primitive operators remain interpretable without ad hoc relabeling?

### Q3. Closure
Does the anchor walk return exactly to the chosen start state?

### Q4. Transportability
Can nearby lawful path variants be defined and classified?

### Q5. Host reuse
Can richer objects be interpreted through the same pathing grammar, rather than through unrelated static descriptions?

---

## Experiment ladder

## Test 0 — Lock the state grammar

### Goal
Define the state space and operator actions precisely enough that the pathing system is executable in principle.

### What to specify
- admissible state format
- allowed layer values
- allowed headings
- action of `lift`
- action of `left`
- action of `right`
- action of `move`

### Pass condition
- the pathing grammar is deterministic
- no operator depends on hidden intuition

### Fail condition
- any operator requires visual guessing or informal repair

### Deliverable
- one note defining state and operators
- one machine-readable example instance

---

## Test 1 — Verify anchor path closure on G15

### Goal
Check whether the anchor walk closes exactly.

### Claim under test
\[
n_{15} = n_0
\]

### What to record
- start state
- full operator word
- landing sequence
- final state
- whether equality is exact or only visually suggested

### Pass condition
- exact closure on the intended start state

### Stronger pass
- closure on a symmetry class of start states

### Fail condition
- closure only appears because of drawing conventions

### Deliverable
- closure log
- state trace table
- pathing verdict

---

## Test 2 — Landing map and path trace

### Goal
Separate full pathing state from ambient landing location.

Define a projection:

\[
\pi(s) = v
\]

which forgets layer and heading.

### What to record
- full state trace \(n_0,\dots,n_{15}\)
- landing trace \(\pi(n_0),\dots,\pi(n_{15})\)
- layer trace
- heading trace

### Pathing relevance
This is the first place where pathing becomes inspectable rather than merely narrated.

### Pass condition
- the path trace is stable and readable
- repeated ambient locations, if any, are explained by layer/heading rather than confusion

### Deliverable
- state table
- landing table
- path diagram

---

## Test 3 — Nearby lawful path family

### Goal
Determine whether G15 supports only one decorative path or a reusable pathing regime.

### Variants to test
- reverse path
- mirror path
- one-turn perturbation
- shortened path
- extended path
- alternate start heading
- alternate start layer

### Classification outcomes
- closes
- remains admissible but does not close
- leaves admissibility
- collapses into ambiguity

### Pass condition
- a small but nontrivial lawful family of related paths exists

### Fail condition
- only one hand-tuned path works

### Deliverable
- path family table
- admissibility and closure classification

---

## Test 4 — G30 as pathing extension

### Goal
Test whether G30 inherits or extends G15 host pathing.

### Question
Can G30 local motion be interpreted as extended host pathing rather than unrelated adjacency?

### What to look for
- doubled circulation
- path lifts or paired chambers
- multiple G30 states projecting to common G15 host roles
- local transport words expressible in G15 grammar

### Pass condition
- at least one coherent transport/pathing correspondence from G30 into G15 is found

### Deliverable
- G30-to-G15 path correspondence note
- sample transport dictionary

---

## Test 5 — AT4val[60,6] chamber and path legibility

### Goal
Test whether AT4val[60,6] can be read through host pathing roles.

### Immediate candidate data
Shell structure:
\[
(1,4,8,16,24,6,1)
\]

### Pathing question
Do shell transitions or transport classes correspond to recurring G15-style host words?

### Pass condition
- some shell or chamber transitions admit a host-legible path interpretation

### Deliverable
- shell-to-host path notes
- candidate chamber path classes

---

## Test 6 — G900 lens-visible pathing

### Goal
Test whether G900 legibility depends on host-governed pathing plus lens compression.

### Existing project distinction
- admissibility belongs to the generator
- legibility belongs to the lens

### Pathing question
Do lawful path populations remain visible after lens compression?

### What to compare
- raw generated action
- strict-schema visibility
- lens-visible signature \(Q = MM^T\)

### Pass condition
- host-relevant path bands, shells, or clusters become legible through the lens

### Deliverable
- G900 path visibility note
- comparison tables for raw versus lens-visible outputs

---

## Pass/fail summary

The thesis gains support if all of the following become true:

1. G15 supports deterministic pathing
2. the anchor path closes exactly
3. landing and layer traces are readable
4. nearby lawful path variants exist
5. G30 admits host pathing correspondence
6. AT4val[60,6] admits host-legible path roles
7. G900 becomes path-legible through the lens

The thesis weakens if:

- pathing is ambiguous
- closure is only visual
- no nearby lawful variants exist
- larger objects require abandoning the host path grammar

---

## Immediate next artifacts

### Note
`notes/G15_STATE_AND_OPERATOR_NOTE.md`

Purpose:
- define state space
- define headings
- define layer/register behavior
- define primitive operator actions

### Example artifact
`specs/examples/g15-host-walk-test.json`

Purpose:
- serialize the start state
- serialize the anchor path word
- serialize expected closure

### Optional helper
`scripts/test_g15_host_walk.py`

Purpose:
- load a path word
- execute the path
- emit final state, trace, and closure verdict

---

## Immediate next theorem-sized claim

The next hard claim worth testing is:

> There exists a deterministic oriented pathing grammar on G15 for which the anchor walk closes exactly and generates a nontrivial family of lawful related traversals.

That is the first strong stone in the foundation.

