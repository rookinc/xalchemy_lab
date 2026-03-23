# G900 Centered Prism Forcing Question v0.1

## Status
Open theorem-hunt note.

The current checked bundle and centered prism lemma establish that the extracted weighted prism artifact satisfies:

- top-face weight = 140
- rung weight = 145
- bottom-face weight = 150
- midpoint law: 145 = (140 + 150) / 2
- doubled-center law: 290 = 2 * 145
- face-sum law: 290 = 140 + 150

The open question is whether these identities are merely observed in the current export, or are forced by the quotient structure itself.

## The fork

### 1. Observed-law version
The current extracted weighted prism artifact happens to satisfy:

- w_top = 140
- w_rung = 145
- w_bottom = 150

with

- w_rung = (w_top + w_bottom) / 2
- w_triangle_base = w_top + w_bottom = 290 = 2 * w_rung

Under this reading, the midpoint law is real but contingent.
It may depend on the current export, normalization choice, or present classification of the carrier.

### 2. Forced-law version
Any exact weighted triangular prism quotient compatible with the current G900 descent package must satisfy:

- rung weight = midpoint of top and bottom face weights
- descended triangle base weight = doubled center
- face layers symmetric around the center

Under this reading, the identities are not accidental.
They would follow from the structure of the quotient itself.

## Candidate forcing statement
Suppose the first exact quotient is a weighted triangular prism with:

- a top face class,
- a bottom face class,
- a rung class,
- and a second quotient to a weighted triangle,

subject to the following conditions:

1. the top and bottom face classes collapse to the same descended triangle edge class,
2. the collapse respects exact class aggregation,
3. the macro-contact law is uniform and equals the descended base edge law,
4. the rung class is the central support mediating the two face layers.

Question:
Do these conditions force

- w_rung = (w_top + w_bottom) / 2
- w_triangle_base = w_top + w_bottom = 2 * w_rung ?

## Minimal assumptions to test
The theorem hunt should isolate which assumptions are actually needed.

### A. Exact aggregation
If the triangle edge class is the recombination of the top and bottom face edge classes, then

- w_triangle_base = w_top + w_bottom

may already be forced.

### B. Macro-contact identification
If the descended edge law must equal macro contact, and macro contact is already known to be

- 290 = 2 * 145,

then the descended base edge law may force

- w_top + w_bottom = 2 * w_rung.

### C. Central support interpretation
If the rung class is the unique central mediator between the two face layers, then
there may be a natural balancing principle forcing the center to be the midpoint.

### D. Symmetry of the prism quotient
If the top and bottom layers are structurally paired by the exact prism quotient, then
the only admissible weighting compatible with a central rung may be a symmetric offset law:

- w_top = c - d
- w_rung = c
- w_bottom = c + d

for some center c and offset d.

In the current extracted artifact:

- c = 145
- d = 5

## Strong candidate theorem shape
A plausible theorem form is:

**Candidate Theorem.**
Let an exact weighted triangular prism descend to a weighted triangle by identifying paired top and bottom face edge classes.
If the descended edge law equals the uniform macro-contact law and the rung class is the central mediating support between the paired face layers, then the prism weights are centered:
- w_rung = (w_top + w_bottom) / 2
and the descended triangle edge base weight is
- w_triangle_base = w_top + w_bottom = 2 * w_rung.

## What would falsify forcing
The midpoint law is not forced if one can construct a competing exact prism quotient with:

- the same support graph,
- the same descent combinatorics,
- the same macro-contact semantics,

but with weights

- w_top, w_rung, w_bottom

not satisfying

- w_rung = (w_top + w_bottom) / 2.

So one possible next step is to search for admissible counterexamples.

## Present best judgment
At the moment, the bundle proves only the observed-law version.

However, the numerical closure is unusually tight:

- midpoint law,
- doubled-center law,
- face-sum law,
- macro-contact match,

all close on the same three numbers.

So the forcing version is now a legitimate theorem target.

## Immediate next mathematical tasks
1. State the exact assumptions of aggregation and contact matching.
2. Ask whether those assumptions already imply
   - w_top + w_bottom = 2 * w_rung.
3. Search for counterexample weighted prisms with the same combinatorics but non-centered weights.
4. Determine whether side-contribution semantics can break or preserve forcing.

