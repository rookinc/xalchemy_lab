# Local–Global Z2 Bridge Note

## Context

Two different binary structures have now appeared in the project.

### Local side
In the tri-patch transport system, the holonomy lattice carries an explicit parity law:

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

Equivalently:

> odd total mismatch parity is forbidden.

This is a local transport statement. It arose from:
- bundled vs off-rail route comparison,
- holonomy class enumeration,
- Smith-normal-form analysis,
- and explicit solution of the mod-2 annihilating functional.

---

### Global side
In the Thalean / signed-lift machinery, a nontrivial \(\mathbb Z_2\)-valued cocycle already appears on the quotient/lift side.

That structure is global and loop-sensitive:
- it is not visible from the main scalar overlap law alone,
- it survives at the level of signed lift / chamber transport,
- and it records a binary obstruction associated with traversing loops.

So both sides now carry a real \(\mathbb Z_2\) trace.

---

## What is the same

At the highest level, the two binary structures rhyme strongly.

### 1. Both are history-sensitive
Neither binary object is a static label on a point.
Both arise from transport / traversal / loop behavior.

### 2. Both survive after the main affine law is understood
On the local side, the bundled rail and additive holonomy lattice were already known before the parity shadow became visible.

On the global side, the main combinatorial and quadratic transport structure was already in place before the cocycle appeared as an additional binary invariant.

### 3. Both are genuinely \(\mathbb Z_2\)-valued
Neither is just a real-valued correction that happens to be small.
Each is a strict binary remainder.

### 4. Both behave like memory
They do not look like ordinary payload quantities.
They look like residual bookkeeping of route class.

That is already enough to justify taking the bridge seriously.

---

## What is different

The two structures are not yet the same object.

### Local parity law
The tri-patch law is:

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

This is phrased in terms of local mismatch corrections on a small transport patch.

It is:
- local,
- explicit,
- coordinate-level,
- and currently attached to admissible middle-route holonomy classes.

### Global cocycle
The signed-lift cocycle lives on loop classes in the larger Thalean / lift geometry.

It is:
- global,
- loop-defined,
- not phrased directly in local mismatch coordinates,
- and attached to the signed chamber lift rather than directly to turtle stress/mismatch variables.

So at present the two objects live in different languages.

That matters.

---

## Minimal bridge hypothesis

The safest connection is not identity.
It is shadowing.

### Minimal conjecture
The local even-mismatch parity law is the **transport-side shadow** of the global signed-lift \(\mathbb Z_2\) cocycle.

In words:

- the signed-lift cocycle is the global binary invariant,
- the tri-patch parity law is what that invariant looks like when projected down into local defect transport coordinates.

That is the right strength of claim right now.

It says:
- related, not yet equal,
- structurally analogous, not yet formally identified.

---

## Candidate correspondence

A plausible bridge picture is:

### Global layer
A loop in the signed lift carries cocycle value
\[
\omega(\gamma)\in \mathbb Z_2.
\]

### Local layer
A corresponding local transport history produces mismatch correction
\[
\Delta m=(dm_{L1},dm_{L2},dm_{R1}),
\]
with binary readout
\[
\pi(\Delta m)=dm_{L1}+dm_{L2}+dm_{R1}\pmod 2.
\]

### Bridge question
Does
\[
\omega(\gamma)=\pi(\Delta m(\gamma))
\]
hold for corresponding loop classes?

That is the clean testable form.

---

## Why this would be important

If the bridge holds, then the local turtle transport model is not merely an isolated toy.

It would mean:

1. the local defect-holonomy system is seeing the same binary obstruction that appears in the signed Thalean lift,

2. the mismatch sector is the correct local carrier of that obstruction,

3. the tri-patch really is a valid local chart for the larger geometry.

That would be a major conceptual consolidation.

---

## Immediate caution

There are at least three reasons to stay careful.

### 1. Coordinate dependence
The local parity law is currently expressed in one specific carrier coordinate system:
\[
(L1,L2,R1).
\]

We do not yet know its invariant form under all relevant relabelings.

### 2. Projection ambiguity
Even if the global cocycle and local parity law are related, there may be more than one plausible projection from global loop data to local mismatch data.

### 3. Scope
The current local law was derived on the tri-patch and its admissible middle-route classes.
We have not yet shown it survives unchanged on larger graph neighborhoods.

So the bridge is promising, but not automatic.

---

## Concrete next test

The next meaningful test is loop comparison.

### Goal
Construct a small family of corresponding loops on both sides and compare:

- global signed-lift cocycle value,
- local mismatch-parity value.

### Desired outcome
For each tested loop class,
\[
\omega(\gamma)=\pi(\Delta m(\gamma)).
\]

### Failure modes
Even if exact equality fails, informative outcomes remain possible:
- equality up to relabeling,
- equality after a fixed affine offset,
- equality on a restricted loop family,
- or total mismatch of the frameworks.

Any of those would still teach us something real.

---

## Suggested workflow

### Step 1
Freeze the two binary laws side by side.
This note does that.

### Step 2
Define a candidate loop dictionary:
- what local transport history corresponds to what global loop/lift path?

### Step 3
Run a comparison probe on a handful of explicit examples.

### Step 4
Only after that, decide whether the bridge is:
- exact,
- partial,
- or only metaphorical.

---

## Working bridge conjecture

### Local–Global Z2 Bridge Conjecture
The tri-patch even-mismatch parity law is the local transport projection of the signed-lift \(\mathbb Z_2\) cocycle on the larger Thalean graph/lift system.

Equivalently, the mismatch parity shadow detected in local holonomy is the local binary trace of the global signed transport obstruction.

That is the right conjecture to test next.

---

## Working summary

We now have:

### Local binary law
\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0\pmod 2.
\]

### Global binary law
A nontrivial \(\mathbb Z_2\)-valued cocycle on signed lift loops.

### Bridge idea
The local law may be the projected transport shadow of the global cocycle.

That is the next bridge to test.

