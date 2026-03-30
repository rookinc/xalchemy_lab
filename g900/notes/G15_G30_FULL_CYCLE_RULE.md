# G15 / G30 Full-Cycle Rule

## Status
Locked working note

## Purpose

This note records the now-locked cycle rule for the G15 host-frame walk and the doubled G30 return.

This is not a tentative metaphor.
This is the current structural rule for the project.

---

## Core locked statement

One full G15 walk is **sign-closing**, not identity-closing.

Thus:

\[
n_{15} = -\,n_0
\]

Walking the same cycle a second time restores identity.

Thus:

\[
n_{30} = n_0
\]

This is the full-cycle rule.

---

## Short interpretation

A single full G15 circuit returns to the same host site, but not to the same side of the sheet.

It returns with reversed sidedness.

So the first cycle does not close as identity.
It closes as a **sign flip**.

The second cycle flips that sign again and therefore restores the original state.

So the system behaves as:

- one cycle: sign reversal
- two cycles: identity restoration

---

## Operational form

Let \(W\) denote the operator corresponding to one full G15 cycle.

Then the rule is:

\[
W(n) = -n
\]

and therefore

\[
W^2(n) = n
\]

This should be regarded as the cycle law of the current host-frame model.

Equivalently:

- \(W\) is not the identity
- \(W\) is an orientation-reversing return on one pass
- \(W^2\) is the identity restoration on two passes

---

## What the minus sign means

The symbol

\[
-n
\]

does **not** mean arithmetic negation in the ordinary scalar sense.

It means:

> same host landing, same structural role, opposite sheet side or opposite sided orientation

So if a state carries sidedness, parity, or sheet polarity, then the minus sign flips that component while preserving the underlying host placement.

At minimum, the intended meaning is:

- same place
- same lawful role in the walk
- opposite side of the sheet

This is the sense in which

\[
n_{15} = -n_0
\]

must be read.

---

## Why this matters

This rule resolves the earlier ambiguity about closure.

At first glance, one might try to write:

\[
n_{15} = n_0
\]

But that is too strong and does not match the lived geometry of the walk.

When the walk is performed in the intended cubical host setting, one full circuit does not return the walker to the same sided state.
It returns the walker to the opposite side of the same host position.

So the true closure is not identity closure.
It is **signed closure**.

This is not a defect in the system.
It is part of the structure of the system.

---

## Geometric reading

The walk is imagined as follows.

You begin inside the cube.
You double-lift to stand on top of it and onto the exterior traversal regime.
From there you walk around the outside.

As you move from a face centroid toward an edge center and continue, you do not stop at the edge.
You wrap around the corner by precessional continuity and enter the adjacent face.
Your path continues in the neighboring face chart automatically.

Under one full circuit, the walk returns to the same host site, but on the opposite side of the sheet from where it began.

Hence:

\[
n_{15} = -n_0
\]

A second full circuit wraps again and restores the original sidedness.

Hence:

\[
n_{30} = n_0
\]

---

## Discrete-geometric reading

This rule says the cycle is not merely a combinatorial loop on a flat graph.

It is a discrete geometric transport process with sidedness.

The walk therefore carries more than position.
It carries orientation and sheet state.

So the cycle has two distinct closure levels:

### 1. One-pass closure
The path returns to the same host site but with sign reversed.

\[
n_{15} = -n_0
\]

### 2. Two-pass closure
The path returns to the same host site with original sign restored.

\[
n_{30} = n_0
\]

Thus the natural full identity period is not 15 but 30.

This is the project meaning of G30 in the present context.

---

## Consequence for G15

G15 should now be interpreted as the **sign-closing host cycle**.

That means:

- G15 gives a complete positional circuit
- but not yet full identity restoration
- it closes only up to sheet reversal

So G15 is a lawful complete walk, but not the full identity period.

The one-pass cycle is complete in a positional sense, yet incomplete in a sidedness sense.

This is why G15 is structurally real and yet not the whole story.

---

## Consequence for G30

G30 should now be interpreted as the **identity-restoring doubled cycle**.

That means:

- G30 is not merely a larger count
- G30 is the completion of the two-pass return law
- G30 is what restores the original state after the sign reversal of G15

So G30 is best understood as:

> the doubled host traverse required for full state recovery

In that sense, G30 is not an arbitrary extension.
It is the natural second half of the sign-closing law.

---

## Thesis-level significance

This rule strengthens the host-frame thesis.

It shows that the host is not merely supporting an arbitrary decorative path.
It is supporting a transport law with nontrivial closure behavior.

The closure is subtle:

- not flat identity after one cycle
- but lawful sign inversion after one cycle
- and lawful identity restoration after two cycles

That is stronger than ordinary loop closure because it distinguishes place from sidedness.

So the host frame is not just a graph of locations.
It is a scaffold of oriented transport.

---

## Relation to pathing

This full-cycle rule must be treated as part of the pathing law.

The path is not fully characterized by where it lands.
It must also record on which side of the sheet it arrives.

So any future state model should include a sign, side, parity, or sheet component.

A minimal symbolic form would be:

\[
s = (x,\varepsilon)
\]

where:

- \(x\) is the underlying host state or landing
- \(\varepsilon \in \{+,-\}\) is sheet side

Then one full G15 walk acts by:

\[
W(x,\varepsilon) = (x,-\varepsilon)
\]

and two walks act by:

\[
W^2(x,\varepsilon) = (x,\varepsilon)
\]

This is the simplest formal expression of the locked rule.

---

## Strong form of the cycle law

The strong form is:

> The primitive host cycle is not identity-closing. It is sign-closing.
> Its square is identity-restoring.

Or symbolically:

\[
W = \text{sign-reversing return}
\]
\[
W^2 = \text{identity return}
\]

Or in state language:

\[
n_{15} = -n_0,\qquad n_{30} = n_0
\]

This should now be regarded as fixed for the current project thread.

---

## Implications for notation

Any notation that writes

\[
n_{15}=n_0
\]

without qualification should now be treated as obsolete for this project context.

The corrected notation is:

\[
n_{15}=-n_0
\]

and the doubled-cycle completion is:

\[
n_{30}=n_0
\]

This is the notation that should appear in future notes unless explicitly discussing an earlier draft intuition.

---

## Implications for testing

Future tests should distinguish three different closure notions:

### Ambient landing closure
Returns to the same host landing site.

### Signed closure
Returns to the same host landing site with opposite sheet side.

### Full identity closure
Returns to the same host landing site with the original sheet side restored.

The locked rule says:

- G15 gives signed closure
- G30 gives full identity closure

So future scripts and schemas should be prepared to record sign state explicitly.

---

## Suggested formalism going forward

Let the walk state include a sign component:

\[
s = (v,f,h,\varepsilon)
\]

or, if the model is simplified,

\[
s = (x,\varepsilon)
\]

where \(\varepsilon\) records sheet side.

Then the cycle operator \(W\) should satisfy:

\[
W(s) = \overline{s}
\]

where \(\overline{s}\) denotes sign-flipped state, and

\[
W^2(s) = s
\]

This is the cleanest way to carry the rule into later formal development.

---

## Plain-language summary

You go around once and come back underneath yourself.
You go around twice and come back to yourself.

That is the whole rule in plain English.

More formally:

- one G15 cycle flips side
- two G15 cycles restore identity

---

## Locked formulation

For this project, the cycle law is fixed as:

\[
n_{15} = -n_0
\]
\[
n_{30} = n_0
\]

Interpretation:

- one full G15 cycle returns to the same host site with reversed sheet side
- two full G15 cycles restore the original state

This is the meaning of the full cycle.
This is the current project meaning of G30.
This should be treated as locked.

