# G900 Mediator Lemma Refinement v0.1

## Structural result
The exact weighted prism quotient now makes the class roles explicit.

### Top face class
- bit0_face edges
- weight 140
- connects only bit-0 classes across macros

### Bottom face class
- bit1_face edges
- weight 150
- connects only bit-1 classes across macros

### Mediator class
- macro_rung edges
- weight 145
- connects paired classes (m,0) to (m,1)

So the rung class is the only class directly joining the paired top and bottom strata.

## Collapse asymmetry
Under prism-to-triangle collapse:

- top and bottom face edges collapse to coarse triangle edges
- rung edges do not collapse to triangle edges
- rung edges collapse to vertex / side-support data instead

So the rung is not a third face class.
It is the unique mediating support of the paired face layers.

## Refined mediator claim
The rung class is uniquely characterized by all of the following:

1. it links paired top/bottom strata
2. it is repeated uniformly in all three macro sectors
3. it is fixed under top/bottom exchange
4. it is not identified with either face class in the coarse triangle edge law

Therefore it is the unique central mediator in the exact prism quotient.

## Forcing consequence
If the descent ladder carries a shared scalar center, then the mediator class is the only admissible carrier of that center.

This reduces the center-forcing burden to one final step:

> prove that the shared scalar center of the descent ladder must be realized on the unique fixed mediator class

That step would force:
- w_mid = 145

