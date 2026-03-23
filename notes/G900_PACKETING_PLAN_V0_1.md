# G900 packeting plan v0.1

## Current result

Order-30 triangular subdivision yields exactly 900 smallest triangular cells.

Treat this as the first concrete candidate carrier for G900.

## Next question

Can the 900 cells be grouped into lawful packets that expose a descent toward:

- 60 packet-nodes of size 15
- 30 packet-nodes of size 30
- 15 packet-nodes of size 60

## First packeting tests

### Test A
Partition cells by barycentric strip coordinates.

### Test B
Partition cells by mod-15 index classes.

### Test C
Partition cells by transport-compatible local neighborhoods.

### Test D
Partition cells by symmetry or orbit classes under the triangle's dihedral symmetry.

## Success criterion

A packeting is interesting only if:

1. every cell belongs to exactly one packet
2. packet adjacency is well-defined
3. the induced packet carrier is structured, not chaotic
4. some invariant survives from cell level to packet level

## First target

Test whether a 60-node packet carrier can be extracted from 900 cells using packets of size 15.

