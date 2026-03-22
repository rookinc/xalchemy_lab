# Framed Signature Composition Result

## Result

The framed signature `(H,S)` composes lawfully under path concatenation.

For two framed traces with signatures

- `(H1,S1)`
- `(H2,S2)`

the concatenated trace satisfies:

- `S_total = S1 + S2`
- `H_total = H1 * H2 * join_term`

where:

- `join_term = +1` if the last chart symbol of the first trace matches the first chart symbol of the second trace
- `join_term = -1` otherwise

## Observed outcome

All tested pairs matched the predicted composition law for both invariants.

## Interpretation

- `S` behaves as an additive signed framed displacement
- `H` behaves as a multiplicative flip-parity cocycle with a boundary correction term

## Strongest sentence

The framed transport layer now admits a lawful signature composition rule under concatenation.

