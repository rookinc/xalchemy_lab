# G900 Offset Forcing Refinement v0.1

## Checkpoint
The offset side of the G900 forcing program is now sharply reduced.

## Locked inputs

### 1. Carrier-derived layer count
The layer audit confirms:

- total cells = 900
- computed layers = 10
- exported layer count = 10

So L = 10 is carrier-derived.

### 2. Exact observed offset
The half-layer offset probe confirms:

- center I = 145
- offset d = 5
- d = L / 2

and reconstructs:

- 145 - 5 = 140
- 145 = 145
- 145 + 5 = 150

So the observed centered prism law is exactly compatible with the half-layer law.

### 3. Unique predecessor shell
The predecessor-shell selection probe confirms:

- midpoint layer = 5
- predecessor shell = 4
- layer 4 is the unique shell immediately before midpoint

So there is a uniquely privileged shell candidate for supplying scale.

## Strongest current mechanism reading
The best current mechanism is now:

- midpoint shell supplies center
- predecessor shell supplies scale

This is stronger than a generic arithmetic fit because:

- the center is tied to the midpoint regime,
- the scale candidate is tied to a unique carrier-derived shell position,
- and the resulting offset matches exactly:
  - d = L / 2 = 5

## Exact remaining burden
Still open:

> why predecessor-shell privilege forces scale inheritance,
> and why that inherited scale must equal the half-layer displacement L/2

## Refined theorem target
### Shell-Offset Theorem
If the off-center prism branches inherit their scale from the unique predecessor shell immediately before midpoint, then the only admissible displacement is:

- d = L / 2 = 5

Hence the exact centered prism law is:

- (145 - 5, 145, 145 + 5) = (140,145,150)

## Honest status
The mechanism is now very tight.
The forcing proof is not yet closed.

