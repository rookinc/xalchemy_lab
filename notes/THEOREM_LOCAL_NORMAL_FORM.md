# Theorem: Local Normal Form

## Theorem

In the current tested local neighborhood, the exact local trace law admits a normal-form decomposition into:

1. an **anchored control surface**,
2. a **rigid odd backbone**,
3. a **rigid even backbone**.

Equivalently, the local trace-state machine splits as

\[
\mathcal L_{\text{local}}
=
\mathcal S_{\text{anchor}}
\;\sqcup\;
\mathcal B_{\text{odd}}
\;\sqcup\;
\mathcal B_{\text{even}}.
\]

---

## 1. Anchored control surface

The trace classes whose parity changes across the tested nearby states are:

- \((A,O,O,O)\)
- \((A,E1,E1,E1)\)
- \((A,E2,E2,E2)\)
- \((E1,E1,E1,O)\)
- \((E1,E1,E1,E2)\)

These form the current anchored control surface
\[
\mathcal S_{\text{anchor}}.
\]

This is the flexible part of the local law.

### Control meaning

Within this anchored control surface:

- \(\tau\) controls anchor-side odd exchange activation,
- \(\sigma\) controls \(E1\)-sheet activation,
- \(A\) controls anchored sheet-polarity swapping together with odd rearming.

So the invariant cube acts here as a local control register.

---

## 2. Rigid odd backbone

The trace classes that remain odd across the tested nearby states are:

- \((D,E1,E1,E2)\)
- \((D,E1,E1,M+)\)
- \((D,E1,E2,E2)\)
- \((E2,E2,E2,E2)\)

These form the rigid odd backbone
\[
\mathcal B_{\text{odd}}.
\]

This is the parity-stable odd transport skeleton in the currently tested neighborhood.

---

## 3. Rigid even backbone

The trace classes that remain even across the tested nearby states are:

- \((D,E1,O,M+)\)
- \((E1,E1,M+,M+)\)
- \((E1,E2,E2,E2)\)
- \((E1,E2,M+,M+)\)
- \((E1,M+,M+,O)\)
- \((E2,E2,E2,O)\)

These form the rigid even backbone
\[
\mathcal B_{\text{even}}.
\]

This is the parity-stable even transport skeleton in the currently tested neighborhood.

---

## Proof sketch

The local trace-state-machine delta table was computed across the nearby realized states

- \((0,0,1)\)
- \((0,0,0)\)
- \((0,1,1)\)
- \((0,1,0)\)
- \((1,1,0)\)

together with their corresponding bridge signatures and trace catalogs.

Inspection of the pairwise deltas shows:

- only a small family of trace classes ever changes parity,
- all remaining odd classes stay odd throughout,
- all remaining even classes stay even throughout.

Therefore the local trace-state machine decomposes into a changing anchored sector and a parity-rigid distal backbone. ∎

---

## Corollary

The invariant cube does not act uniformly on the local trace law.

Instead, in the tested neighborhood, it acts only on the anchored control surface:

\[
(A,\sigma,\tau)\curvearrowright \mathcal S_{\text{anchor}}
\]

while the distal backbones remain fixed.

So the local invariant cube is best interpreted as a control register for the anchored surface, not for the entire trace law.

---

## Meaning

This is the first clean static normal form for the local bridge law.

The local structure is now best read as:

- a small flexible anchored layer where the nearby controls operate,
- sitting on top of a rigid odd/even distal transport skeleton.

That is much sharper than:
- raw loop parity,
- raw bridge representatives,
- or even the invariant cube alone.

---

## Strongest current reading

The current local bridge law is a controlled anchored surface over a rigid distal backbone.

This is the cleanest local normal form obtained so far.

