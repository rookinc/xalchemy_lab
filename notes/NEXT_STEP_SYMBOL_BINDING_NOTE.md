# Next Step Symbol Binding Note

## Why this is the next move

The local side is no longer the bottleneck.

The bridge table already has:
- local lift_bit,
- stable bridge rows,
- symbolic global loop bodies.

What is still missing is a concrete reading of the symbols:
- q0
- x
- a
- b
- c
- d

So the next smallest real step is to bind those symbols to a base-graph convention.

---

## Provisional convention

For now, read the global symbolic loops in the language of the base graph G15:

- q0 = chosen base vertex
- x, a, b, c, d = oriented base edges
- s^-1 = formal reverse traversal of edge s

This does not yet define the signed lift.
It only turns the symbolic loops into actual candidate closed walks on the base side.

---

## What this buys us

After the binding is fixed, each symbolic global loop can be read as a genuine walk object:

- global_return = out-and-back edge walk
- global_square = small cycle candidate
- global_twist = two-path comparison candidate

That is the correct staging point before signed-lift cocycle evaluation is introduced.

---

## Immediate next task after binding

Once the symbol binding is frozen, choose whether:

1. q0, q1, ... will remain symbolic vertex names, or
2. they will be replaced by actual vertices from the chosen G15 model.

That is the next concrete upgrade after this note.

