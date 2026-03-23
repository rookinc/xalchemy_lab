# G900 Note 07 — Next Quotient Map Target v0.1

## Next target
Test the first direct carrier-to-prism quotient map.

## Candidate rule
Assign each carrier cell:

- prism macro label = layer mod 3
- prism bit label = orientation bit

Then collapse cells by:

- (layer mod 3, bit)

to obtain six carrier partitions:

- (0,0), (1,0), (2,0), (0,1), (1,1), (2,1)

## Why this is the right next test
This rule uses only carrier-derived structure:

- barycentric layer
- exact macro phase law
- bit split

It does not import the prism classes from outside.

## Success condition
The resulting six-way partition should look natural, stable, and structurally consistent with the prism node order.

