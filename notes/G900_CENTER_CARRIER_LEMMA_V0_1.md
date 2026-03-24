# G900 Center Carrier Lemma v0.1

## Goal
Finish the center-forcing argument by identifying which prism class is allowed to carry the shared scalar center.

## Current structural facts

### Face classes
- top face class = bit0_face
- bottom face class = bit1_face

These two classes are paired and exchanged under top/bottom face exchange.

They are also exactly the two classes whose weights aggregate to the coarse triangle edge law:
- 140 + 150 = 290

So they are not fixed center carriers.
They are the paired off-center contributors.

### Mediator class
- mediator class = macro_rung

This class is:
1. the only class joining paired top/bottom strata
2. repeated uniformly across all three macro sectors
3. fixed under top/bottom exchange
4. not itself one of the coarse descended edge classes

So the mediator is the only fixed class in the prism support that sits between the paired face layers.

## Candidate lemma
### Center Carrier Lemma
In the exact weighted prism quotient, any shared scalar center compatible with:
- paired face exchange,
- exact face aggregation,
- and the prism-to-triangle descent ladder,

must be realized on the unique fixed mediator class rather than on either exchanged face class.

Therefore the only admissible carrier of the shared scalar center is the macro_rung class.

## Consequence
If the descent ladder already determines the shared scalar center to be 145, then the mediator class must carry that value.

Hence:
- w_mid = 145

## Remaining burden
The only step still to formalize is:

> why an exchanged class cannot itself serve as the center carrier of the descent ladder

The likely answer is:
- exchanged classes occur only as paired off-center contributors,
- while the center must be invariant under the exchange that pairs them.

That is the next proof sentence to lock.

