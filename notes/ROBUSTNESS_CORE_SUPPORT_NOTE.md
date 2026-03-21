# Robustness Core Support Note

## Checkpoint

A single-flip robustness sweep was performed on selected odd edges of the current seeded local signed lift.

Baseline bridge signature:
- return = 0
- square = 0
- twist = 1

## Result

### Essential odd edges
Flipping any of the following destroys the bridge signature:

- e01
- e02
- e05

Observed failures:
- flip e01 -> return=0, square=0, twist=0
- flip e02 -> return=0, square=1, twist=1
- flip e05 -> return=0, square=1, twist=1

### Nonessential odd edges
Flipping any of the following preserves the bridge signature:

- e16
- e22
- e25

Observed survival:
- return=0, square=0, twist=1 remains unchanged

## Meaning

The bridge is neither arbitrary nor fully rigid.

It depends on an essential odd-edge support set in the current seeded lift.

Current essential support:
- {e01, e02, e05}

Current nonessential tested odd edges:
- {e16, e22, e25}

## Strongest reading

The local class-based bridge is robust under some odd-edge perturbations, but not under all of them.
So the present bridge signature is controlled by a smaller structural odd core.

