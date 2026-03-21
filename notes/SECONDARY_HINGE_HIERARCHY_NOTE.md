# Secondary Hinge Hierarchy Note

## Checkpoint

Secondary hinge scans were performed for:

- e02
- e01

## Result for e02

The edge `e02` lies in exactly three supported 4-cycles, and all three are even.

Packets:
- [e00,e05,e10]
- [e01,e08,e11]
- [e12,e15,e03]

So `e02` behaves as an even-family continuation hinge, not as a bifurcation hinge.

## Result for e01

The edge `e01` lies in exactly three supported 4-cycles, split as:

- two even
- one odd

Packets:
- even: [e08,e11,e02]
- even: [e09,e14,e03]
- odd:  [e00,e04,e07]

So `e01` behaves as a twist-side boundary hinge: it still touches the unique odd sector, but it is not the primary bifurcation hinge.

## Hierarchy

Current local hinge hierarchy:

1. Primary bifurcation hinge
   - e00
   - one odd arm + two even arms
   - two-sided and orientation-stable

2. Twist-boundary hinge
   - e01
   - one odd arm + two even arms
   - asymmetrically adjacent to the odd sector

3. Even-family continuation hinge
   - e02
   - three even arms
   - no odd branch

## Strongest current reading

The local bridge geometry is not uniform.
It is organized around a privileged hinge structure:

- one central bifurcation hinge
- one odd-side boundary hinge
- one even continuation hinge

