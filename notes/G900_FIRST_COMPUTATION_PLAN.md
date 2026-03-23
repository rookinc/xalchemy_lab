# G900 first computation plan

## Goal

Turn the first G900 sampling hypothesis into a computable object.

Working hypothesis under test:

> G900 may be an order-30 triangular subdivision presentation, with 900 smallest triangular cells.

This note defines the first computation burden.

---

## Object under test

Seed domain:

- one oriented triangle

Sampling parameter:

- `n = 30`

Subdivision rule:

- divide each side into 30 equal segments
- induce the standard triangular lattice

---

## Counts to compute

We need the following exact counts:

1. lattice points
2. lattice edges
3. upward-pointing smallest triangles
4. downward-pointing smallest triangles
5. total smallest triangles

Expected formulas:

- lattice points = `(n+1)(n+2)/2`
- upward smallest triangles = `n(n+1)/2`
- downward smallest triangles = `n(n-1)/2`
- total smallest triangles = `n^2`

At `n = 30`, expected total smallest triangles:

- `900`

---

## Why this matters

If the count does not come out cleanly, reject the current sampling hypothesis quickly.

If the count does come out cleanly, the next question becomes:

- what structure on those 900 cells could descend toward `G60`, `G30`, and `G15`?

---

## Required outputs

For `n = 30`, compute and record:

- point count
- smallest-cell count
- coordinate representation
- adjacency relation between smallest cells
- optional orientation doubling

---

## Strict caution

Even if the total is 900, that does **not** yet prove:

- that the object is a graph
- that it deserves the label `G900`
- that it descends to `G60`

It only validates the first sampling count.

---

## Immediate next experiment

Implement one prototype that:

1. enumerates all smallest triangles in the order-30 subdivision
2. assigns each a unique ID
3. computes cell adjacency by shared edge
4. reports the total cell count

That prototype should be treated as the first candidate pre-graph presentation for the G900 conjecture.

