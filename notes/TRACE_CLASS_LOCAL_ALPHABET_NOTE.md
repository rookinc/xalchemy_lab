# Trace-Class Local Alphabet Note

## Checkpoint

The local 4-cycle parity field is exactly predicted by a sector-trace rule, but not by a sparse low-degree polynomial on unordered sector-presence bits.

Therefore the correct local state space is not:

- unordered sector occupancy

but:

- cyclic sector trace class

for each supported 4-cycle.

## Local alphabet

Current sector symbols:

- A   = anchor
- O   = odd branch
- E1  = even sheet 1
- E2  = even sheet 2
- M+  = merged even continuation
- D   = distal defect carrier

A supported 4-cycle is therefore assigned a cyclic word in this alphabet, modulo:

1. cyclic rotation
2. reversal

So the local parity law should now be read as a function on trace classes

    [trace] -> parity in Z2

rather than as a function on unordered sector sets.

## Currently observed trace classes

### Even classes
- [A,E1,E1,E1]
- [A,E2,E2,E2]
- [E1,E1,E1,E2]
- [E1,E1,M+,M+]
- [E1,E2,M+,M+]
- [E1,M+,M+,E2]
- [E2,E1,E2,E2]
- [E2,O,E2,E2]
- [M+,O,E1,D]
- [M+,O,E1,M+]
- [O,E1,E1,E1]
- [O,E2,E2,E2]

### Odd classes
- [A,O,O,O]
- [E1,E1,E2,D]
- [E1,M+,E1,D]
- [E2,E2,E2,E2]

## Strongest current reading

The local transport law is now best understood as a parity law on cyclic trace classes.

This is stronger than a bag-of-sectors model and is the right local object for an order-sensitive continuation law.

