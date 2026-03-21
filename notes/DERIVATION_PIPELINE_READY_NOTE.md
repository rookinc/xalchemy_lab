# Derivation Pipeline Ready Note

## Checkpoint

The project now has a complete derivation pipeline for the bridge layer.

Current pipeline:

1. define explicit global loop specimens
2. define a tree-gauge cocycle on base-edge symbols
3. compute loop holonomy parity from the tree-gauge file
4. promote computed loop parities into the artifact file
5. run a consistency check between computed and stored values
6. feed the artifact-backed values into the bridge table

## What is now true

The bridge is no longer only:

- symbolic,
- hand-labeled,
- or note-level.

It is now executable as a reproducible computation pipeline.

## Current files

Core files now in place:

- `specs/signed_lift_symbol_bindings_v1.json`
- `specs/signed_lift_bridge_loops_v1.json`
- `specs/signed_lift_actual_loop_artifacts_v1.json`
- `specs/tree_gauge_representative_v1.json`

Core scripts now in place:

- `run_tree_gauge_loop_parities.py`
- `run_signed_lift_artifact_consistency_check.py`
- `run_promote_tree_gauge_to_artifacts.py`
- `run_tri_patch_global_bridge_table.py`

## Current status

The current tree-gauge edge values are still smoke-test values.

So the pipeline is ready,
but not yet fed by independently derived signed-lift geometry.

## Next real milestone

Replace the smoke-test values in `tree_gauge_representative_v1.json`
with independently obtained signed-lift/tree-gauge edge data.

Then rerun, in order:

1. `run_tree_gauge_loop_parities.py`
2. `run_promote_tree_gauge_to_artifacts.py`
3. `run_signed_lift_artifact_consistency_check.py`
4. `run_tri_patch_global_bridge_table.py`

## Success condition

The bridge still passes after the smoke-test edge values are replaced
by independently sourced signed-lift data.

That will be the first actual derivation-grade checkpoint.

