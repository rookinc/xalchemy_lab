# Proposition: Anchored Control Surface and Rigid Distal Backbone

## Proposition

In the current tested local neighborhood, bridge control decomposes into:

1. an **anchored control surface**, where the nearby control parameters \((A,\sigma,\tau)\) change trace parities, and
2. a **rigid distal backbone**, whose trace parities remain fixed across the tested local state transitions.

---

## Anchored control surface

The trace-state-machine delta table shows that only a small family of trace classes changes parity across the tested nearby states:
- \((0,0,1)\)
- \((0,0,0)\)
- \((0,1,1)\)
- \((0,1,0)\)
- \((1,1,0)\)

The changing trace classes are:

- \((A,O,O,O)\)
- \((A,E1,E1,E1)\)
- \((A,E2,E2,E2)\)
- \((E1,E1,E1,O)\)
- \((E1,E1,E1,E2)\)

These form the current anchored control surface.

### Control roles

#### Tau
\(\tau\) toggles the anchored odd branch:
- \((A,O,O,O)\)

When \(\tau\) turns off, oddness is transferred into:
- \((E1,E1,E1,O)\)

So \(\tau\) acts as anchor-side odd exchange activation.

#### Sigma
\(\sigma\) activates the anchored \(E1\) continuation sheet:
- \((A,E1,E1,E1)\)
- \((E1,E1,E1,E2)\)

So \(\sigma\) acts as \(E1\)-sheet activation.

#### A
The \(A\)-control performs an anchored polarity swap together with odd rearming:
- \((A,E1,E1,E1)\): odd \(\to\) even
- \((A,E2,E2,E2)\): even \(\to\) odd
- \((A,O,O,O)\): even \(\to\) odd

So \(A\) is not merely a passive anchor bit; it participates in anchored sheet-polarity control.

---

## Rigid distal backbone

Across the same tested local state transitions, the following odd trace classes remain odd:

- \((D,E1,E1,E2)\)
- \((D,E1,E1,M+)\)
- \((D,E1,E2,E2)\)
- \((E2,E2,E2,E2)\)

And the following even trace classes remain even:

- \((D,E1,O,M+)\)
- \((E1,E1,M+,M+)\)
- \((E1,E2,E2,E2)\)
- \((E1,E2,M+,M+)\)
- \((E1,M+,M+,O)\)
- \((E2,E2,E2,O)\)

These classes form the current rigid distal backbone.

---

## Meaning

The local bridge is not controlled uniformly across all trace classes.

Instead, the current local law separates into:

- a **small anchored control surface**, where nearby control flips act,
- and a **rigid distal backbone**, which remains parity-stable across those same flips.

So the local transport law has both:
- a flexible anchored control region,
- and a stable distal transport skeleton.

---

## Corollary

The bridge signature and invariant cube do not by themselves reveal this decomposition.

This anchored-surface / rigid-backbone split only becomes visible at the finer trace-catalog level.

Thus the trace-class transport law is the correct local layer at which bridge control is organized.

---

## Strongest current reading

The present local bridge law is best understood as a controlled anchored transport surface sitting on top of a rigid distal backbone.

That is the tightest dynamic local formulation obtained so far.

