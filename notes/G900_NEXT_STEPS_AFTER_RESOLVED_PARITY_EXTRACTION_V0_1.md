# G900 Next Steps After Resolved Parity Extraction v0.1

## Current hard result
We now have a resolved parity check on the bridge specimen loops:

- global_return = 0
- global_square = 0
- global_twist = 1

This is not symbolic guesswork.
It follows from the resolved edge assignments and the resolved edge cocycle.

Resolved data used:

- global_return:
  - resolved_base_walk = [e00, e00^-1]
  - parity = 0

- global_square:
  - resolved_base_walk = [e00, e05, e10, e02^-1]
  - parity = 0 + 1 + 0 + 1 = 0 mod 2

- global_twist:
  - resolved_path_1 = [e00, e04]
  - resolved_path_2 = [e01, e07]
  - path parities = 0 and 1
  - comparison parity = 1

So the current binary split is real:

- untwisted return-like loops are even
- the twist witness is odd

## What this means
The construction genuinely carries binary holonomy memory.

This strengthens the stage-5 split interpretation.
It does not yet finish the 900 closure theorem, because we still need a complementary branch pair and then a seed-enclosing realization argument.

## Exact blocker just found
The parity scripts fail because they read symbolic loop fields such as:

- path
- path_1
- path_2

instead of the resolved fields already present in the resolved loop artifact:

- resolved_base_walk
- resolved_path_1
- resolved_path_2

So the current blocker is tooling, not theory.

## Immediate code patch target
Patch these scripts:

- src/xalchemy_lab/paper/bridge/run_tree_gauge_loop_parities.py
- src/xalchemy_lab/paper/bridge/run_actual_cocycle_from_artifact.py

Required behavior:

For symbolic_closed_walk:
- prefer resolved_base_walk
- fallback to path

For symbolic_two_path_loop:
- prefer resolved_path_1 and resolved_path_2
- fallback to path_1 and path_2

## Minimal intended helper shape
Suggested helper logic:

def get_closed_walk(loop):
    return loop.get("resolved_base_walk", loop.get("path"))

def get_two_path(loop):
    p1 = loop.get("resolved_path_1", loop.get("path_1"))
    p2 = loop.get("resolved_path_2", loop.get("path_2"))
    return p1, p2

Then branch on representation_type.

## First rerun after patch
Run:

PYTHONPATH=src python -m xalchemy_lab.paper.bridge.run_tree_gauge_loop_parities
PYTHONPATH=src python -m xalchemy_lab.paper.bridge.run_actual_cocycle_from_artifact

Goal:
confirm the resolved parity outputs now run cleanly without alias failures.

## Next extraction target
After patching, inspect whether there is a richer loop basis than:

- global_return
- global_square
- global_twist

Primary files to inspect next:

- specs/paper/bridge/signed_lift_actual_loop_artifacts_v1.json
- specs/paper/bridge/tree_gauge_representative_import_v1.json
- specs/paper/bridge/tree_gauge_representative_v1.json

Question:
do these artifacts already expose additional active cycles or support classes beyond the three named bridge specimens?

## Mathematical target after patch
We need to test whether the cocycle support organizes into:

1. one distinguished odd twist class
2. and, ideally, a complementary pair of active branch classes

The desired chain is:

plus/minus 5
to two distinguished holonomy classes
to two seed-enclosing minimal cycles
to winding number 1 each
to 900

## Strongest current theorem-grade statement
The actual signed-lift data distinguishes the twist witness from the return and square witnesses by odd holonomy parity.

That is the current locked result.

## What still needs to be finished
To close the 900 theorem we still need:

1. a complementary pair, not just a single odd witness
2. a geometric/topological identification of those classes with seed-enclosing branch completions
3. then the winding-1 argument giving 360 per branch

## Practical order of operations
1. patch resolved-loop parity scripts
2. rerun parity extraction cleanly
3. inspect actual loop artifacts for richer basis/support
4. isolate active complementary classes
5. test whether they project to seed-enclosing loops
6. only then return to the final 900 closure claim

