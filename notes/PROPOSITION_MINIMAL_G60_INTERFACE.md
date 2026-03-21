# Proposition: Minimal G60 Interface Determined by the Local Normal Form

## Proposition

Any candidate upstairs `G60` transport model compatible with the current local results must reproduce, at minimum, the following two pieces of descended data:

1. an **anchored control packet**,
2. a **rigid transport skeleton**.

These two components form the minimal `G60` interface determined by the local normal form.

---

## 1. Anchored control packet

The anchored control packet is the upstairs object whose local receipt is the anchored control surface

- \((A,O,O,O)\)
- \((A,E1,E1,E1)\)
- \((A,E2,E2,E2)\)
- \((E1,E1,E1,O)\)
- \((E1,E1,E1,E2)\)

This packet must account for the local control actions of the invariant register \((A,\sigma,\tau)\), namely:

- \(\tau\): anchor-side odd exchange activation,
- \(\sigma\): \(E1\)-sheet activation,
- \(A\): anchored sheet-polarity swap together with odd rearming.

So any viable upstairs model must contain a local transport packet whose descent supports exactly this anchored control behavior.

---

## 2. Rigid transport skeleton

The rigid transport skeleton is the upstairs object whose local receipt is the parity-stable backbone.

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

These classes remain parity-stable across the tested nearby local controls, so they are not part of the flexible local control layer.
They must therefore be reproduced upstairs as part of the stable transport skeleton rather than as control-surface effects.

---

## Meaning

The local normal form already constrains what an upstairs `G60` model must look like.

A viable upstairs model cannot merely reproduce:
- the bridge signature,
- or the invariant cube.

It must also reproduce the split between:

- a small flexible anchored control packet,
- and a larger rigid transport skeleton.

That split is the minimal interface any `G60` transport law must satisfy.

---

## Corollary

The local normal form is not only a local classification result.
It is already an upstairs compatibility filter.

Any candidate `G60` transport model that fails to descend to:

1. the anchored control packet, and
2. the rigid transport skeleton

is incompatible with the current local law.

---

## Strongest current reading

The local normal form determines the smallest nontrivial data that the upstairs transport law must carry.

So the next stage is no longer to guess freely about `G60`.
It is to search for a `G60` packet-and-skeleton mechanism whose local receipt matches this minimal interface.

