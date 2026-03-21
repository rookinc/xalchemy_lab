# First Explicit Global Return Specimen Note

## Checkpoint

The symbolic bridge alphabet is now bound to the base-graph language of G15.

In particular:

- `q0` is the chosen base vertex
- `q1` is a neighboring vertex
- `x` is the oriented edge from `q0` to `q1`
- `x^-1` is the formal reverse traversal from `q1` back to `q0`

So the global loop

\[
\texttt{global\_return} = [x, x^{-1}]
\]

now has a fully explicit base-graph reading:

> start at `q0`, traverse the oriented edge `x` to `q1`, then return immediately along the reverse traversal `x^-1` to `q0`.

This is the first fully explicit global loop specimen in the bridge file.

## Why this matters

This does not yet define the signed lift or its cocycle value.

But it does upgrade `global_return` from:
- symbolic body with intended meaning

to:
- explicit base-graph walk with named endpoints and direction.

That is the correct first anchor for later signed-lift evaluation.

