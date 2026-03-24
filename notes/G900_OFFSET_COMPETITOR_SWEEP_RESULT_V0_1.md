# G900 Offset Competitor Sweep Result v0.1

## Checkpoint
The protocol-required exclusion sweep for the prism offset has now been performed against the currently visible carrier-derived competitors.

## Tested rival families

### 1. Index / adjacency statistics
Tested examples:
- predecessor shell index = 4
- midpoint-predecessor gap = 1

These fail exact reconstruction of the centered prism law:
- 145 +/- 4 gives 141,149
- 145 +/- 1 gives 144,146

So they are excluded.

### 2. Local skew statistics
Tested example:
- bit imbalance = 3

This gives:
- 145 +/- 3 = 142,148

So it does not recover the prism law.
Moreover it is a local parity skew, not the first centered branch displacement.

So it is excluded.

### 3. Higher-level quotient gaps
Tested example:
- parity-triangle gap = 15

This gives:
- 145 +/- 15 = 130,160

This is a real quantity, but it belongs to the parity-triangle refinement rather than the first centered prism refinement.

So it is excluded as an offset competitor at the prism level.

### 4. Free normalization
Arbitrary offset values without structural carrier source are excluded by protocol.

## Surviving candidate
The half-layer rule survives:

- d = L / 2 = 10 / 2 = 5

It is:
- carrier-derived
- midpoint-centered
- compatible with predecessor-shell privilege
- exact on the observed prism law
- not a higher-level quotient artifact
- not a local skew statistic

And it reconstructs exactly:
- 145 - 5 = 140
- 145 = 145
- 145 + 5 = 150

## Strongest current judgment
Among the currently visible carrier-derived statistics, the half-layer rule is the unique surviving offset law for the centered prism branch displacement.

## Honest boundary
This is a structural exclusion result over the currently visible competitor family.
It is stronger than a fit and weaker than a purely first-principles derivation.

