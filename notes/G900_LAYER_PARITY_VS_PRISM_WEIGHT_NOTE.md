# G900 layer parity vs prism weight note

## Purpose

Test whether the weighted prism law

- bit-0 face edges = 140
- macro rungs = 145
- bit-1 face edges = 150

is the aggregate shadow of an alternating layer law.

The contact-surface data already suggests that inward layers do not behave uniformly.
Instead, bit contacts alternate between two regimes as layer increases.

So the next question is:

> do even and odd layers contribute differently to the weighted prism totals?

If yes, then the prism weights may not be primitive.
They may be the accumulated result of a deeper layer-parity alternation.

---

## Current clue

Earlier layer-conditioned bit contacts showed alternating dominance:

- layer 0: bit-1-heavy
- layer 1: bit-0-heavy
- layer 2: bit-1-heavy
- layer 3: bit-0-heavy
- ...

This suggests that layer parity may carry a phase.

If true, then the normalized prism law

- `140 -> -5`
- `145 -> 0`
- `150 -> +5`

may be the coarse sum of alternating parity contributions rather than a single uniform edge law.

---

## Probe target

Split prism-support contacts by:

- even layer contribution
- odd layer contribution

Then measure separately:

1. bit-0 face edges
2. macro rung edges
3. bit-1 face edges

---

## Success criterion

Interesting outcomes include:

1. exact parity alternation
2. stable sign bias by parity
3. rung neutrality across parity
4. cancellation pattern producing the coarse `140 / 145 / 150` law

A flat parity split would weaken the hypothesis.
A strong alternating split would support it.

---

## Immediate hypothesis

Candidate:

- even layers favor bit-1 face support
- odd layers favor bit-0 face support
- rung edges act as parity-neutral bridge terms

Do not assume this until measured.

