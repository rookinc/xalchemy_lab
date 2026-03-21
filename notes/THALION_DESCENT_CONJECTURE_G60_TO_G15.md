# Thalion Descent Conjecture: G60 -> G30 -> G15

## Conjecture

There exists a local chamber-transport packet on G60 consisting of:

- one anchor channel H
- one square-side packet {S1,S2,S3}
- one twist-side packet {T1,T2,T3}

such that:

1. G60 carries the native transport/closure law;
2. G30 carries the signed-sheet shadow of that law;
3. G15 carries the parity-class quotient of that shadow.

## Downstairs receipts

The current local G15 cluster invariants are interpreted as receipts of the upstairs packet:

- A     = receipt of the anchor channel H
- sigma = receipt of the square-side packet {S1,S2,S3}
- tau   = receipt of the twist-side packet {T1,T2,T3}

with the current local quotient law

    R = 0
    Q = A + sigma
    W = A + tau

over Z2.

## First toy dictionary

Current working receipt dictionary:

- H              -> e00
- {S1,S2,S3}     -> {e02,e05,e10}
- {T1,T2,T3}     -> {e01,e04,e07}

This dictionary is not yet asserted to be canonical upstairs.
It is the first descent ansatz from the observed local bridge core.

## Native G60 reading

Working guess:
- in-phase closure against the anchor descends to the even family
- exchanged closure against the anchor descends to the odd family

So the current even square family and odd twist family on G15 are interpreted as quotient shadows of two distinct closure sectors on G60.

## Expected break points

This conjecture is expected to fail or need refinement if:
- the 3-and-3 packets are not canonical upstairs,
- the native G60 law is ternary or sectoral before mod-2 collapse,
- different G60 transport sectors descend to the same odd class on G15,
- the missing invariant state (1,1,0) is forbidden by upstairs admissibility.

