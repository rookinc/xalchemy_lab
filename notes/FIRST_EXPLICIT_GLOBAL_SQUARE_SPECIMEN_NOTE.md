# First Explicit Global Square Specimen Note

## Checkpoint

The symbolic bridge alphabet is now explicit enough to read `global_square` as a concrete base-graph walk.

The provisional vertex/edge reading is:

- `a : q0 -> q1`
- `b : q1 -> q2`
- `c : q2 -> q3`
- `d : q3 -> q0`

So the loop

\[
\texttt{global\_square} = [a,b,c,d]
\]

now has the explicit base-graph reading:

> start at `q0`, traverse `a` to `q1`, then `b` to `q2`, then `c` to `q3`, then `d` back to `q0`.

This is the first fully explicit small-cycle specimen for the bridge file.

## Why this matters

This still does not define the signed lift or assign a cocycle value.

But it upgrades `global_square` from:
- symbolic closed walk with intended meaning

to:
- explicit provisional 4-step closed walk on the base-graph side.

So the bridge vocabulary now has two explicit specimens:

- `global_return` = out-and-back along `x`
- `global_square` = 4-step closed cycle along `a,b,c,d`

That is a real staging point for later signed-lift evaluation.

