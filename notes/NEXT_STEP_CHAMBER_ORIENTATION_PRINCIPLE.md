# Next Step: Chamber-Orientation Principle

## Goal

Replace the charted anchored rules of Toy G60 Automaton v2 with a single structural principle.

The target is a principle that explains:

- why there are exactly two anchored charts,
- why `A` selects between them,
- why `E2` is locked on in the `A=1` chart,
- why the distal backbone remains rigid,
- and why the mixed cancellation class stays even.

---

## Proposed direction

Treat the anchor packet as a **two-orientation chamber** rather than as a generic control node.

In this picture, the anchor has:

- one odd exchange corridor,
- two continuation corridors,
- one local chamber orientation bit,
- and one attached distal locking skeleton.

The key claim would be:

> the bit `A` does not directly control parity;
> it selects the active chamber orientation of the anchor packet.

Then the two anchored charts become the local receipts of two chamber orientations.

---

## Orientation 0

In chamber orientation 0:

- the odd corridor and `E1` corridor are the live anchored controls,
- the `E2` corridor is passive,
- `tau` governs odd exchange activation,
- `sigma` governs `E1` activation.

This matches the observed `A=0` chart.

---

## Orientation 1

In chamber orientation 1:

- the `E2` corridor is geometrically privileged,
- the odd corridor and `E1` corridor become complementary controls around that privileged corridor,
- `E2` remains locked on,
- the anchored parity grammar changes accordingly.

This matches the observed `A=1` chart.

---

## Why this is promising

This is the first idea that makes the `A` split feel geometric instead of ad hoc.

It explains why:

- `A` behaves like a chart selector,
- the two charts are not symmetric,
- and the `A=1` chart is naturally E2-dominant.

So it is a plausible structural source of the anchored phase split.

---

## Distal backbone interpretation

Under this same view, the distal backbone is not part of the anchor controller.

It is a **locking skeleton** attached downstream of the chambered anchor packet.

That explains why, in the current data, it remains rigid across the full realized local cube.

So the local law may separate into:

- a chambered anchor packet,
- a passive but structured distal locking skeleton.

---

## Mixed cancellation interpretation

The mixed cancellation class

- `(D,E1,O,M+)`

would then be read as a local interference pattern between:

- one branch contribution arriving from the odd corridor,
- one continuation contribution arriving through the chamber,
- one locked distal contribution arriving from the skeleton.

Its evenness would be structural cancellation, not an arbitrary exception.

That would be the right kind of explanation.

---

## What must be shown next

A real derivation from this principle would need to show:

1. two chamber orientations exist intrinsically,
2. their local receipts are exactly the observed `A=0` and `A=1` charts,
3. the distal skeleton is automatically rigid,
4. the mixed cancellation law appears without hand tuning.

Until that happens, this remains a working principle, not a proved mechanism.

---

## Strongest current reading

The best next move is to reinterpret the anchor packet as a two-orientation chamber whose local receipts generate the full anchored grammar, while the distal backbone descends from a separate locking skeleton.

That is the most promising path from fitted automaton to geometric principle.

