# First Explicit Global Twist Specimen Note

## Checkpoint

The symbolic bridge alphabet is now explicit enough to read `global_twist` as a two-path comparison on the base-graph side.

The provisional edge reading is:

- `a : q0 -> q1`
- `b : q1 -> q2`

so path 1 is

\[
[a,b] : q0 \to q1 \to q2
\]

and

- `c : q0 -> q3`
- `d : q3 -> q2`

so path 2 is

\[
[c,d] : q0 \to q3 \to q2
\]

Therefore `global_twist` is now read as:

> two different directed paths from the same start `q0` to the same endpoint `q2`.

This is the first fully explicit two-path comparison specimen for the bridge file.

## Why this matters

This still does not assign a signed-lift cocycle value.

But it upgrades `global_twist` from:
- symbolic two-path loop with intended meaning

to:
- explicit provisional path comparison on the base-graph side.

So the bridge vocabulary now has three explicit specimen types:

- `global_return` = out-and-back
- `global_square` = small closed cycle
- `global_twist` = two-path comparison

That completes the first explicit symbolic bridge vocabulary.

