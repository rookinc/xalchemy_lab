# Next Step: Framed Signature Composition

## Goal

Test whether the framed signature

- `(H,S)`

admits a lawful composition rule under path concatenation.

## Reason

We already have:

- `H` = parity of chart-coordinate flips
- `S` = signed chart displacement

The next natural question is:

- how do these combine when two framed paths are glued end-to-end?

## First candidate laws

### Cocycle parity
Expect:

- `H_total = H1 * H2 * boundary_term`

A boundary term may appear because the final chart symbol of the first path and the initial chart symbol of the second path contribute one extra transition at the join.

So parity is expected to be multiplicative up to a join correction.

### Signed displacement
Expect:

- `S_total = S1 + S2`

at first pass, since signed chart values simply add along concatenation.

## What to record

For two traces `T1`, `T2`:

- `H1`, `S1`
- `H2`, `S2`
- concatenated trace `T = T1 + T2`
- `H_total`, `S_total`
- predicted values
- discrepancy / join term

## Strongest sentence

Once a framed signature exists, the next serious question is whether it composes lawfully under path concatenation.

