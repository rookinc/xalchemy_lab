# Proposition: G60 No-Go Filter v1

## Proposition

A candidate upstairs `G60` transport model is incompatible with the current local interface if, under descent to the tested local neighborhood, it exhibits any of the following behaviors:

1. the rigid distal backbone becomes control-sensitive under nearby local controls \((A,\sigma,\tau)\),
2. both anchored even sheets swap parity simultaneously under a single local control action,
3. the mixed cancellation trace
   \[
   (D,E1,O,M+)
   \]
   becomes odd without a structural change in the distal skeleton,
4. anchor odd rearming occurs without a corresponding anchored control-surface transition.

These conditions form the first no-go filter for upstairs compatibility.

---

## 1. Distal rigidity requirement

The local normal form separates into:

- an anchored control surface,
- a rigid odd backbone,
- a rigid even backbone.

So any candidate upstairs model that causes the rigid distal backbone to respond directly to nearby local controls fails to descend to the observed local law.

In particular, the following classes must remain parity-stable in the tested neighborhood:

### Rigid odd backbone
- \((D,E1,E1,E2)\)
- \((D,E1,E1,M+)\)
- \((D,E1,E2,E2)\)
- \((E2,E2,E2,E2)\)

### Rigid even backbone
- \((D,E1,O,M+)\)
- \((E1,E1,M+,M+)\)
- \((E1,E2,E2,E2)\)
- \((E1,E2,M+,M+)\)
- \((E1,M+,M+,O)\)
- \((E2,E2,E2,O)\)

---

## 2. Anchored sheet-swap constraint

The current local control law shows that anchored parity changes are structured:

- \(\sigma\) activates the anchored \(E1\) sheet,
- \(A\) swaps anchored sheet polarity together with odd rearming.

No tested local control causes both anchored even sheets
- \((A,E1,E1,E1)\)
- \((A,E2,E2,E2)\)

to swap parity simultaneously.

So any upstairs model descending to such a simultaneous swap violates the current anchored control law.

---

## 3. Mixed cancellation protection

The mixed trace
\[
(D,E1,O,M+)
\]
is stably even in the tested neighborhood.

So if a candidate upstairs model makes this class odd while leaving the distal skeleton type unchanged, it breaks the observed local cancellation law and is incompatible with the interface.

---

## 4. Anchored rearming constraint

The local control table shows that anchor odd rearming is not arbitrary.
It occurs only together with anchored control-surface changes.

So any upstairs model that produces anchor odd rearming without a corresponding anchored surface transition fails the observed local state-machine law.

---

## Meaning

This proposition upgrades the `G60` schema from a positive structural guess to a negative compatibility filter.

A viable upstairs model must not only descend to the anchored control packet and rigid transport skeleton.
It must also avoid the forbidden descent patterns above.

---

## Strongest current reading

The local law now imposes both:

- positive interface requirements,
- and negative no-go constraints.

So the search for a viable `G60` model is no longer unconstrained speculation.
It is already subject to a concrete local admissibility filter.

