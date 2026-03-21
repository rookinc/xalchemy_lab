# Next Step: Formal Lens Axiom

## Goal

Turn the relabeled cube sketch into a formal lens statement.

The sketch is no longer just an image.
It is now being treated as a projection device:

\[
G15 \;\to\; G30 \;\to\; \mathrm{Faces}(G60).
\]

The next step is to say exactly what that means.

---

## Proposed lens axiom

A local packet inserted into the carrier cell is not observed directly.
It is observed only through its projected face receipts.

So the basic axiom should be:

> A local chamber packet is visible only through weighted face receipts produced by an internal controller.

This gives the cube a precise role:
it is not the packet itself, but the visible receipt body of the packet.

---

## Formal lens shape

Define a lens

\[
\mathcal L : \mathcal P_{15} \to \mathcal O_{30} \to \mathcal F_{60}
\]

where:

- \(\mathcal P_{15}\) = packet basis from `G15`
- \(\mathcal O_{30}\) = organizer state on `G30`
- \(\mathcal F_{60}\) = 6-face receipt field on the `G60` cube

---

## Stage 1: packet basis

The current packet basis is:

\[
\mathcal P_{15} = \{H,\ O,\ E1,\ E2,\ K,\ C\}
\]

with:

- \(H\) = anchored controller
- \(O\) = odd exchange branch
- \(E1\) = continuation sheet 1
- \(E2\) = continuation sheet 2
- \(K\) = rigid distal skeleton
- \(C\) = cancellation channel

This is the content being projected.

---

## Stage 2: organizer on G30

The organizer state should specify:

- anchor phase
- branch activation
- sheet activation
- face pairings
- seam assignment
- projection weights

So `G30` is the first place where packet content becomes spatially organized.

It is the mediator, not the final display.

---

## Stage 3: face receipts on G60

The cube receives the organized packet as six face receipts:

\[
\mathcal F_{60} = \{F_1,F_2,F_3,F_4,F_5,F_6\}.
\]

A first semantic assignment is:

- \(F_1\) = anchor controller face
- \(F_2\) = anchored \(E1\) face
- \(F_3\) = anchored \(E2\) face
- \(F_4\) = distal odd backbone face
- \(F_5\) = distal even backbone face
- \(F_6\) = seam / cancellation face

So the cube is the visible receipt carrier.

---

## Weighted face law

Each face should carry a receipt weight

\[
w_i \in [0,1]
\]

or in a simpler discrete model

\[
w_i \in \mathbb Q
\]

with the interpretation:

- \(w_i\) is the fraction of the organized packet visible on face \(F_i\).

This is the natural reinterpretation of the old sketch fractions.

So the sketch placeholders become lens coefficients, not arbitrary annotations.

---

## Minimal statement

The smallest formal statement is:

> A G60 cube face field is the weighted receipt of a G15 packet after G30 organization.

That is the first true axiom-level version of the sketch.

---

## Why this matters

Once this is written down, the sketch becomes testable.

Now we can ask:

- what are the packet basis elements?
- what organizer states are allowed?
- what face weights are allowed?
- which face assignments are rigid?
- which receipts change with anchor phase?

This turns the sketch into a real interface object.

---

## Strongest current reading

The next real move is not to decorate the cube.
It is to define the lens axiom that says what the cube is *doing*:

it is receiving an organized packet and displaying its six weighted face receipts.

