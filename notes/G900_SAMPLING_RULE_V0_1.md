# G900 sampling rule v0.1

## Purpose

Propose the first explicit testable sampling rule for the conjecture that `G900` is a dense sampled presentation of one upstream triangular closure law.

This note does **not** claim success yet.

It only defines the first candidate rule tightly enough to test.

---

## Working position

Test Candidate B:

> `G900` is a dense sampled presentation of one upstream triangular closure law.

The immediate burden is to define:

1. the seed domain
2. the subdivision rule
3. the count rule
4. the adjacency or incidence rule
5. the descent relation to lower graph levels

---

## Seed domain

Take an oriented triangular seed cell.

Call its vertices:

- `A`
- `B`
- `C`

Treat this seed triangle as the minimal closure region for the sampling rule.

At this stage, the seed is geometric, not yet graph-theoretic.

---

## First sampling hypothesis

Let each side of the seed triangle be subdivided into `n` equal segments.

Use the induced triangular lattice inside the seed.

The total number of smallest triangular cells in a standard order-`n` triangular subdivision is:

`n^2`

The total number of lattice points is:

`(n+1)(n+2)/2`

The total number of upward-pointing unit triangles is:

`n(n+1)/2`

The total number of downward-pointing unit triangles is:

`n(n-1)/2`

So the total unit-triangle count is:

`n^2`

---

## Immediate observation

If `900` is the total count of smallest triangular cells, then the simplest match is:

`n^2 = 900`

hence

`n = 30`

This is the first clean candidate:

> `G900` may arise from an order-30 triangular subdivision.

This is attractive because it is exact and simple.

---

## Candidate interpretation

### Candidate B1
`900` counts smallest triangular cells in an order-30 triangular subdivision.

In this reading:

- the upstream law is triangular closure
- `30` is the side subdivision order
- `900` is the dense cell count

This is the best current first hypothesis.

---

## Why this is promising

It naturally links:

- triangle seed
- triangular series
- dense finite presentation
- a visible nested closure intuition

and it gives an exact appearance of `900` without forcing numerology.

---

## But do not overclaim

This does **not** yet explain:

- why `30` should also appear as `G30`
- how `60` emerges
- how `15` emerges
- whether the sampled object is a graph, a cell complex, or a pre-graph presentation
- what adjacency / transport rule lives on the 900 cells

So the equality

`900 = 30^2`

is only a first clue, not a proof of ladder membership.

---

## Second sampling hypothesis

Maybe `900` does not count cells but directed or oriented cells.

If the underlying undirected cell count were `450`, then an orientation doubling would give `900`.

This suggests a second branch:

### Candidate B2
`900` counts oriented triangular cells rather than bare cells.

Do not prefer this yet.
Test B1 first because it is simpler.

---

## Third sampling hypothesis

Maybe `900` counts boundary-to-boundary transport links rather than cells.

For example, if an order-30 boundary sampling produced roughly 30 choices on one edge and 30 on another, then a `30 x 30 = 900` pairing count could appear.

### Candidate B3
`900` counts pairings or transport channels, not cells.

This is plausible but should be secondary until the geometric cell count is tested.

---

## First test target

Test B1 first:

> order-30 triangular subdivision
> 900 smallest triangular cells

Questions to answer:

1. can this be rendered cleanly?
2. can the cells be organized into a lawful transport sampling?
3. is there a natural quotient or identification that produces 60, 30, or 15?
4. do invariants survive under that descent?

---

## Relation to the current browser renderer

The current xyzti browser sketch already privileges:

- one triangular frame
- one loop parameter
- one continuation direction
- one local center / seed law

That makes it a suitable visual laboratory for testing whether a triangular closure sampling story feels natural.

But the current renderer is still continuous and symbolic.

To test the G900 conjecture, it must grow a discrete mode.

---

## Minimal next experiment

Build a discrete triangular subdivision mode with parameter:

- `n = 30`

and compute:

- vertices
- edges
- smallest triangular cells
- optional oriented cell doubling

The first expected number to confirm is:

- smallest cells = `900`

If that fails, reject B1 quickly.

---

## First conjectural ladder sketch

Possible interpretation:

- seed triangle = upstream law domain
- order-30 subdivision = dense sampled presentation
- transport quotient on sampled cells = candidate route toward `G60`
- deeper quotient = candidate route toward `G30`
- core quotient = candidate route toward `G15`

This is only a roadmap, not a result.

---

## Immediate deliverable

Create one browser or Python prototype that renders an order-30 triangular subdivision and reports:

- lattice point count
- edge count
- upward triangle count
- downward triangle count
- total cell count

with special attention to the value `900`.

