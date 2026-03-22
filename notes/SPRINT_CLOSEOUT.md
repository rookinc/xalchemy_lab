# Sprint Closeout

## What is now defined

The sprint has reduced to a small formal stack:

- spark
- kernel
- grammar

The primary formal objects are:

- `specs/paper/g60/spark_v0_1.json`
- `specs/paper/g60/kernel_r0_r1_v0_2.json`
- `specs/paper/g60/r1_state_v0_2.json`
- `specs/paper/g60/trurtle_xyz_v0_1.json`
- `specs/paper/g60/identification_state_I_v0_1.json`
- `specs/paper/g60/reconciliation_state_v0_1.json`

The key definitions are:

- spark = minimal perturbation primitive
- kernel = `r0 -> r1`
- trurtle = ordered triadic frame `xyz`
- lift+twist = half-step reconciliation operator
- `I` = identification state
- `r1` = reconciled centroid-oriented initial state
- post-`r1` evolution = mostly grammar

## Working grammar floor

The strongest currently supported local finite grammar is:

- local four-state family modeled by `Z2 x Z2`

with:

- one binary generator corresponding to mirror-rotation
- one binary generator corresponding to diameter-flip

This is treated as the current local grammar floor.

A possible `Z5` outer layer remains open and is not part of the locked sprint core.

## What remains conjectural

The following remain live but not locked:

- spark-photon interpretation
- `phi^3 / x^2` scale split
- 8-sector signed grammar
- nearest-vertex snapping details
- multi-face interior reduction
- outer `Z5` orbit layer
- finite kernel lookup implementation

These are preserved in:

- `notes/OPEN_CONJECTURES_AND_BACKLOG.md`

## What the next sprint should do

The next sprint should focus on one task:

- define the finite values of `reconciliation_state`

A good target is to decide whether reconciliation is exactly:

- `Z2 x Z2`

or whether it is:

- a small finite refinement whose local floor is `Z2 x Z2`

After that, the next task is to determine whether `I` is:

- already a grammar seed
- or a pre-grammar intermediate state

## Success statement

This sprint is successful if future work can restart from:

- the canonical model note
- the six primary specs
- and the closeout note

without rereading the full exploration log.

## Strongest sentences

A spark is the minimal perturbation primitive.

The kernel is the map from raw perturbation to reconciled centroid-oriented initial state.

After `r1`, propagation is mostly grammar.

