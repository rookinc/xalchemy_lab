# Smoke-Test To Real-Data Handoff Note

## Current checkpoint

The bridge stack now passes at three levels for the core specimens:

- local lift_bit
- stored artifact cocycle values
- computed tree-gauge loop parities

The consistency checker passes on all three core loops.

## Important honesty clause

The current tree-gauge edge values are still smoke-test values.
They were chosen to reproduce:

- global_return = 0
- global_square = 0
- global_twist = 1

So the system is computationally wired and verified,
but not yet fed by independently derived signed-lift geometry.

## Next real milestone

Replace the smoke-test edge values in:

- specs/tree_gauge_representative_v1.json

with independently obtained signed-lift/tree-gauge edge data.

Then rerun:

- run_tree_gauge_loop_parities
- run_signed_lift_artifact_consistency_check
- run_tri_patch_global_bridge_table

## Success condition

The bridge still passes after the smoke-test edge values are replaced by independently sourced data.

That will be the first actual derivation-grade checkpoint.

