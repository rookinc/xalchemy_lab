# Framed Signature Composition Result Template

## Goal

Test whether the framed signature `(H,S)` composes lawfully under path concatenation.

## Candidate laws

- `H_total = H1 * H2 * join_term`
- `S_total = S1 + S2`

where:

- `join_term = +1` if the last chart symbol of the first trace matches the first chart symbol of the second trace
- `join_term = -1` otherwise

## What to inspect

For each pair of traces:

- `H1`, `S1`
- `H2`, `S2`
- join term
- combined `H`, `S`
- predicted `H`, `S`
- whether the predictions match

## Strongest sentence

The next serious question for the framed signature is whether it obeys a lawful composition rule under concatenation.

