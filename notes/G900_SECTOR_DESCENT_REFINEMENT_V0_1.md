# G900 Sector Descent Refinement v0.1

## Correction
The bridge should now be read at sector level, not packet level.

Old wording:
- square packet
- twist packet

Improved wording:
- rigid anchor
- even-family sector
- unique odd-branch sector

## Bridge-side structure
Current anchored fan at e00:

- anchor:
  - e00

- unique odd arm:
  - {e04,e07,e01}

- even-arm family:
  - {e05,e10,e02}
  - {e06,e13,e03}

So the local geometry is:

- one hinge
- one persistent odd exchange branch
- two sibling even continuation sheets

## Receipt law
Current quotient receipt law:

R = 0
Q = A + sigma
W = A + tau

with:

- A     = anchor receipt
- sigma = even-family receipt
- tau   = odd-branch receipt

## G900-side target
Current centered prism:

- 140
- 145
- 150

So the improved descent target is:

- anchor -> 145
- even-family -> one off-center branch
- odd-branch -> the other off-center branch

## Exact frontier
Still open:

> whether the two sibling even arms merge canonically into one even-family sector before or during descent to the G900 centered prism

This is now the sharpest bridge question.

## Updated theorem frontier
### Anchored Sector Descent Theorem
Under the G900 descent, the rigid anchor descends to the centered rung 145, the sibling even arms descend as one even-family sector to one off-center branch, and the unique odd exchange arm descends to the other off-center branch.

If proved, this upgrades the current bridge proposition from packet language to sector language.

