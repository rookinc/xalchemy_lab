# G900 series boot note

## Purpose

Open the conjecture that `G15`, `G30`, `G60`, and `G900` are not unrelated named objects, but finite realizations, quotients, or sampled presentations of one upstream law.

This note does **not** assume that claim is already proven.

Its purpose is to define the first disciplined questions.

---

## Working conjecture

There exists one upstream generating law such that:

- `G15` is a tight core realization
- `G30` is an intermediate quotient / lift-aware realization
- `G60` is a chamber-carrier realization
- `G900` is a denser sampled or expanded realization

The intended claim is **not**:

> these are all literally the same graph

The intended claim is:

> these may be different realizations of one common generating law

---

## Immediate discipline

Before proving anything, distinguish:

- law
- seed
- realization
- quotient
- presentation

Do not collapse these.

---

## Question 1: what is G900?

Candidate possibilities:

1. a graph with 900 vertices
2. a dense sampled presentation of an upstream triangular closure law
3. a shell or boundary sampling object
4. a transport-event carrier
5. not a graph at all, but a higher presentation object that later descends to graph form

This must be decided explicitly.

---

## Question 2: what does 900 count?

Possible meanings:

- vertices
- oriented chambers
- flags
- transport events
- sample points
- boundary points
- triangle subdivision cells
- packet states

Until this is fixed, `G900` is only a label.

---

## Question 3: object-type table

We need a typed table for the current series candidates.

| label | object type | count meaning | current role |
|------|-------------|---------------|--------------|
| G0   | unknown     | unknown       | possible null / law-only seed |
| G1   | unknown     | unknown       | possible first closure seed |
| G15  | graph       | 15 vertices   | established quotient core |
| G30  | graph       | 30 vertices   | established intermediate quotient |
| G60  | graph       | 60 vertices   | established chamber carrier |
| G900 | unknown     | unknown       | candidate dense realization |

---

## Question 4: realization ladder

Candidate ladder:

1. upstream law
2. seed closure
3. dense realization / sampled presentation
4. chamber carrier
5. quotient lift level
6. algebraic core

Open placement guess:

- `G900` belongs near level 3
- `G60` belongs near level 4
- `G30` belongs near level 5
- `G15` belongs near level 6

This is a conjectural placement only.

---

## Question 5: triangular series clue

A live clue is the appearance of triangular accumulation:

`R(n) = n(n+1)/2`

Need to test whether this belongs to:

- shell growth
- boundary sampling
- triangle subdivision
- packet accumulation
- transport closure count

Do not assume relevance until matched to an actual construction.

---

## First proof burden

To advance the conjecture, produce:

1. a precise definition of `G900`
2. a precise statement of what 900 counts
3. a candidate realization map from `G900` downward
4. at least one invariant that survives descent

---

## Claim hygiene

### Established
- `120 -> 60 -> 30 -> 15`
- `G15 ≅ L(Petersen)`

### Supported conjecture
- one upstream law may underlie several finite realizations

### Open speculation
- `G0`, `G1`, `G15`, `G30`, `G60`, `G900` are one strict series in the same sense

---

## Next action

Produce one concrete candidate definition of `G900` and reject at least two weaker ones.

