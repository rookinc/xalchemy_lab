# G900 Mediator Lemma Program v0.1

## Goal
Prove the missing center-forcing step:

> the rung weight is forced to equal the shared scalar center 145 because the rung is the unique central mediator between the paired face strata.

## Current inputs already locked

### Shared-center data
- prism midpoint = 145
- triangle parity midpoint = 145
- macro-contact law = 290 = 2 * 145

### Aggregation data
- coarse triangle edge law = top + bottom = 290

### Structural data
- prism support is fixed
- top and bottom are paired face strata
- rungs are the only edges joining corresponding top/bottom macro-bit classes

## Exact burden
Arithmetic does not force:

- w_mid = (w_top + w_bottom)/2

So the missing step must be structural.

## Candidate structural claim
The rung class is the only quotient class that is:

1. incident to both paired face layers,
2. macro-preserving across the bit split,
3. repeated uniformly in all three macro sectors,
4. and unchanged by the top/bottom face exchange.

If this is true, then the rung is the unique fixed class under face-layer pairing, and is therefore the only admissible carrier of the shared center.

## Theorem target
### Mediator Lemma
In the exact weighted prism quotient, the rung class is the unique class fixed by paired face exchange and mediating between the paired face strata.
Therefore it must carry the shared scalar center of the descent ladder.

Hence:
- w_mid = 145

## Proof tasks

### Task 1. Fixed-class characterization
Show that under top/bottom pairing:
- face classes are exchanged
- rung class is fixed

### Task 2. Uniqueness
Show there is only one support class with this fixed mediator role.

### Task 3. Center inheritance
Show that any shared scalar center compatible with the paired descent must sit on the fixed mediator class.

## Honest status
This lemma is not yet proved.
But it is now the exact missing step for center forcing.

