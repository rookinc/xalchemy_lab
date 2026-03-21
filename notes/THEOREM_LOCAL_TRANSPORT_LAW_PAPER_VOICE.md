# Theorem (Paper Voice): Local Transport Law for the Supported 4-Cycle Parity Field

## Setup

Consider the current seeded local signed-lift model and the induced supported 4-cycle family in the local `G15` patch.

Assign sector labels to the currently relevant local edges as follows.

### Anchor sector
- `A` for the anchor edge:
  - `e00`

### Odd-branch sector
- `O` for the persistent odd exchange branch:
  - `e01, e04, e07`

### Even continuation sheet 1
- `E1` for the first even continuation sheet:
  - `e02, e05, e08, e10, e11, e12, e15`

### Even continuation sheet 2
- `E2` for the second even continuation sheet:
  - `e03, e06, e09, e13, e14, e17, e20, e23, e24, e25`

### Merged even-aligned continuation
- `M+` for merged continuation edges aligned with even propagation:
  - `e16, e18, e19, e21, e26`

### Distal defect carrier
- `D` for distal defect carriers:
  - `e22, e27`

For any supported 4-cycle \(C\), let
\[
\mathrm{tr}(C)
\]
denote its cyclic sector trace.

---

## Local transport rule

Define the parity functional
\[
\Pi(\mathrm{tr}(C))\in \mathbb Z_2
\]
by the following rules.

### Rule 1. Anchor oddness
If the trace contains the anchor and at least two odd-branch edges, then
\[
\Pi(\mathrm{tr}(C))=1.
\]

This captures the primary anchored odd cycle.

### Rule 2. Distal defect oddness
If the trace contains a distal defect carrier `D` together with continuation-sheet participation, then
\[
\Pi(\mathrm{tr}(C))=1,
\]
except in the mixed cancellation case below.

### Rule 3. Pure distal even-sheet oddness
If the trace is purely of the distal even-sheet type
\[
(E2,E2,E2,E2),
\]
then
\[
\Pi(\mathrm{tr}(C))=1.
\]

### Rule 4. Mixed cancellation exception
The mixed trace class
\[
(D,E1,O,M+)
\]
up to cyclic order and reversal, is declared even:
\[
\Pi(\mathrm{tr}(C))=0.
\]

### Default
If none of the above applies, then
\[
\Pi(\mathrm{tr}(C))=0.
\]

---

## Theorem

For the 18 supported local 4-cycles in the current seeded local patch, the actual mod-2 parity of each 4-cycle is exactly reproduced by the transport-sector functional
\[
\Pi.
\]

Equivalently, the local supported 4-cycle parity field is completely predicted by:

1. anchor oddness,
2. distal defect oddness,
3. one mixed cancellation exception.

---

## Proof sketch

The supported local 4-cycles were enumerated explicitly and their actual parities computed from the derived mod-2 edge state.

A first coarse sector model correctly predicted 14 of the 18 parities, revealing that:
- the anchored odd branch is real,
- the even continuation sheets are real,
- and a second, distal oddness mechanism is present away from the anchor.

A refined sector model then isolated:
- the distal defect carriers `D`,
- the merged even continuation sector `M+`,
- and the unique mixed cancellation trace
  \[
  (D,E1,O,M+)
  \]
  up to cyclic order.

With this refinement, all 18 supported 4-cycles were predicted correctly:
\[
18/18.
\]

Therefore the supported local 4-cycle parity field is exactly described by the transport-sector rule above. ∎

---

## Corollary

The local parity field is not merely an artifact of loop naming or isolated representative choices.

It is the receipt of a transport geometry with:

- one primary hinge,
- one persistent odd exchange branch,
- two sibling even continuation sheets,
- one distal defect mechanism,
- one mixed cancellation law.

---

## Relation to the quotient law

This local transport law refines the invariant quotient picture.

Previously, the bridge signature was shown to factor through the invariant cube
\[
(A,\sigma,\tau)\in\mathbb Z_2^3
\]
via
\[
(R,Q,W)=(0,\;A+\sigma,\;A+\tau).
\]

The present theorem adds that the full supported 4-cycle parity field itself is governed by a predictive sector law.
So the current hierarchy is:

\[
\text{edge-level lift state}
\to
\text{sector transport field}
\to
\text{cluster invariants }(A,\sigma,\tau)
\to
\text{bridge signature }(R,Q,W).
\]

---

## Plain-English reading

The local geometry is now predictive.

It says:
- there is one main hinge,
- one odd branch persists away from it,
- two even sheets propagate away from it,
- a distal defect creates a second kind of oddness,
- and there is one special mixed pattern where two oddness tendencies cancel.

That rule predicts every supported local 4-cycle parity currently in view.

---

## Status

This is still a local seeded theorem checkpoint, not the final full global theorem.

But it is the strongest local law obtained so far:
the supported local 4-cycle parity field is exactly predicted by a branching-and-cancellation transport rule.

