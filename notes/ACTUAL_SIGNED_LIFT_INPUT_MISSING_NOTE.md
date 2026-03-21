# Actual Signed-Lift Input Missing Note

## Checkpoint

The local/global bridge table is now in an honest bridge-ready state.

The canonical script is:

- `src/xalchemy_lab/run_tri_patch_global_bridge_table.py`

It now reports:

- local holonomy deltas,
- local mismatch parity,
- local lift bit,
- and `PENDING_ACTUAL_SIGNED_LIFT` on the global side when no actual signed-lift representative is present.

---

## What is now settled

### 1. Local state
The current augmented local state is

\[
(\Delta s,\Delta m;\lambda).
\]

### 2. Kernel channel
The mismatch sector obeys

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

In the bridge table this remains identically zero on all tested rows.
So it is a kernel condition only, not the active bridge observable.

### 3. Bridge candidate channel
The lift register \(\lambda=\texttt{lift\_bit}\) is the current best local bridge candidate.

In the current bridge table:

- `w_bundled` -> `lift_bit = 0`
- `w_hold` -> `lift_bit = 1`
- `w_LR_1` -> `lift_bit = 1`
- `w_LR_2` -> `lift_bit = 1`
- `w_LL` -> `lift_bit = 0`

and this pattern is polarity-stable on both `u1R` and `d1R`.

---

## What is not yet present

The repo still does not contain actual signed-lift loop representatives or an actual global \(\mathbb Z_2\) parity evaluator wired into the bridge table.

So the current global fields remain:

- `loop_repr = None`
- `cocycle = None`

and the bridge status correctly prints:

- `PENDING_ACTUAL_SIGNED_LIFT`

This is now the honest state of the project.

---

## Correct reading

The bridge checkpoint is no longer:

> local lift bit matches placeholder global bits

but rather:

> local lift bit is ready to be compared against actual signed-lift loop parity once that input layer is provided.

That is a stronger and cleaner checkpoint.

---

## Immediate next requirement

The next nonlocal ingredient required is:

1. an explicit signed-lift loop representative for each intended global bridge row,
2. a true evaluator returning its global \(\mathbb Z_2\) cocycle value,
3. insertion of those objects into `GLOBAL_LOOPS`.

Only then can the bridge table become a real signed-lift/local-transport comparison.

---

## Practical conclusion

Further local brute-force probing is not the priority now.

The bottleneck has moved.

The missing ingredient is no longer a local law.
The missing ingredient is actual global signed-lift input.

