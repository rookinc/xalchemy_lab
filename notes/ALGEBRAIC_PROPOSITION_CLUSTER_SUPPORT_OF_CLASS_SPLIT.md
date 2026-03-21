# Algebraic Proposition: Cluster Support of the Local Class Split

## Proposition

In the current seeded local signed-lift model, the observed bridge signature

- return = 0
- square = 0
- twist = 1

is controlled by a clustered mod-2 support consisting of:

- a rigid anchor edge
  - e00
- a twist-side cluster
  - {e01, e04, e07}
- a square-side cluster
  - {e02, e05, e10}

with the following experimentally established properties.

### 1. Rigid anchor
The edge `e00` is rigid in the tested local bridge signature:
flipping `e00` destroys the theorem and does not participate in any observed restoring double-flip pair.

### 2. Twist cluster law
The set
\[
T = \{e01,e04,e07\}
\]
acts as the local support cluster for the twist-type class.

Observed behavior:
- single flips in `T` destroy the theorem
- some double flips in `T` restore the theorem
- the full triple flip of `T` sends
  \[
  (\text{return},\text{square},\text{twist})=(0,0,1)\mapsto(0,0,0)
  \]
  and therefore destroys the twist sector

So the twist class depends on the mod-2 state of the cluster `T`.

### 3. Square cluster law
The set
\[
S = \{e02,e05,e10\}
\]
acts as the local support cluster for the square-type class.

Observed behavior:
- single flips in `S` destroy the theorem
- some double flips in `S` restore the theorem
- the full triple flip of `S` sends
  \[
  (\text{return},\text{square},\text{twist})=(0,0,1)\mapsto(0,1,1)
  \]
  and therefore destroys the square sector

So the square class depends on the mod-2 state of the cluster `S`.

### 4. Boundary spectators
The following tested nearby edges are not essential to the bridge signature:
- e03
- e06
- e11
- e12
- e13
- e14
- e15
- e16
- e22
- e25

Flipping them changes the even/odd 4-cycle counts, but leaves the bridge signature unchanged.

### 5. Current support principle
Therefore, the present local bridge signature is not carried by arbitrary 4-cycles one by one, but by a smaller structural support pattern:
- rigid anchor `e00`
- twist cluster `T`
- square cluster `S`

---

## Corollary

The current local theorem should be read class-theoretically:

- return-type is anchored by the rigid return edge-state
- square-type is controlled by the square support cluster
- twist-type is controlled by the twist support cluster

So the observed local/global class split is governed by clustered mod-2 support, not merely by isolated loop labels.

---

## Plain-English reading

The important thing is not just that some loops are even and some are odd.

The stronger thing is:

- one edge behaves like a rigid anchor
- one three-edge packet controls the twist side
- another three-edge packet controls the square side
- surrounding edges can wiggle without destroying the bridge

That is why the bridge now looks like a real local structure instead of a coding accident.

---

## Status

This is still a local seeded proposition, not yet the final full global theorem.
But it is the strongest current algebraic summary of the actual-edge robustness results.

