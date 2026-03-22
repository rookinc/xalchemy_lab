# G60 Core Restart Cycle

## Cycle

A coherent runtime picture is now:

1. boundary faces or sectors are perturbed
2. the induced interior bias snaps to a nearest G60 vertex
3. a trurtle is emitted from the snapped vertex
4. the trurtle follows lawful local continuations
5. it maps a shortest return path back to the cube center
6. the core vertex applies the update rules
7. trurtles restart from the center for the next cycle

## Interpretation

This gives a recursive boundary-to-core-to-boundary transport engine.

- boundary perturbations provide input
- G60 nearest-vertex snap provides discrete activation
- trurtle motion explores lawful continuation and closure
- the center acts as rule application and restart site

## Strongest sentence

Boundary pokes resolve to a discrete G60 vertex, transport runs until shortest closure to center is mapped, and the core reissues the next generation from center.

## Roles

### Faces
Provide perturbing inputs.

### Snapped G60 vertex
Provides the first discrete resolved activation.

### Trurtles
Carry framed transport and closure information.

### Cube center
Acts as closure reference, rule application site, and restart source.

## Next step

Define the smallest explicit state machine for this cycle:

- input poke set
- snapped active vertex
- trurtle path state
- closure receipt
- core update
- restart emission

