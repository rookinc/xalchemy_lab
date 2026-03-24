# G900 Coarse Collapse Law Locked v0.1

## Hard result
The G900 descent now gives an exact centered prism with weights:

- top face = 140
- vertical / center = 145
- bottom face = 150

So the first quotient is centered at 145 with offsets:

- top face = -5
- center = 0
- bottom face = +5

## Coarse collapse law
The prism-to-triangle pushforward probe shows that each coarse triangle edge already has base candidate:

140 + 150 = 290

for all three edge classes:

- AB = 290
- BC = 290
- CA = 290

So the coarse collapse law is now locked in the form:

coarse edge = top branch + bottom branch = 290

## Symmetry at coarse level
The exact weighted triangle has uniform edge law:

- (0,1) = 290
- (0,2) = 290
- (1,2) = 290

So after collapse, the coarse triangle no longer distinguishes the three edge classes.

## Parity refinement
The same coarse law admits a parity refinement:

- even triangle edge = 160
- odd triangle edge = 130

and:

160 + 130 = 290

So the coarse contact law is stable under parity splitting.

## Strongest current reading
The following is now hard:

- the G900 descent realizes a centered weighted prism
- the two off-center branch weights collapse to the coarse edge law 290
- the coarse law is uniform across the triangle
- the coarse law also splits as even + odd = 160 + 130

## Exact open question
What is not yet proved is which fine binary split is the true bridge:

- bridge-side square arm vs twist arm
- prism-side top face vs bottom face
- parity-side even vs odd

The next task is to determine which of these pairings actually align.

