# Artifact-Driven Bridge Checkpoint Note

## Checkpoint

The bridge table is now running from artifact-backed global cocycle values for the three core bridge specimens:

- `global_return = 0`
- `global_square = 0`
- `global_twist = 1`

These values are now sourced from:

- `specs/signed_lift_actual_loop_artifacts_v1.json`

and the bridge table reports:

- `global_source = actual_signed_lift_artifact`

for the core rows.

## Result

The artifact-driven bridge rows currently match the local lift-bit values on the tested local words.

So at this checkpoint:

- local `lift_bit` agrees with artifact-backed global parity assignments
- local mismatch parity remains identically even and therefore remains the kernel channel
- the bridge is no longer relying on provisional symbolic fallback for the core named specimens

## What this means

The project has successfully crossed from:

- symbolic bridge vocabulary only

to:

- artifact-driven bridge comparison

for the current core specimen family.

## What this does not yet mean

The artifact file is still hand-populated.
So this is not yet a derived signed-lift theorem.

It is an artifact-backed checkpoint, not yet an independently computed global cocycle extraction.

## Next step

The next real mathematical upgrade is to replace hand-entered artifact cocycle values with values computed from actual signed-lift representatives.

