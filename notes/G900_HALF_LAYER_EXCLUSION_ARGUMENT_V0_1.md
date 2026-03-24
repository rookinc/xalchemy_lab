# G900 Half-Layer Exclusion Argument v0.1

## Goal
Explore the exclusion route for the final numerical step.

The target is not merely to argue that

- d = L / 2 = 5

fits the current centered prism law.

The target is to exclude competing displacement rules while preserving the current structural package.

## Current locked package

### Carrier structure
- total layer count L = 10
- midpoint layer = 5
- unique predecessor shell = 4

### Center side
- center I = 145

### Observed centered prism law
- top = 140
- mid = 145
- bottom = 150

So the observed displacement is:
- d = 5

## What must be excluded
Any rival displacement rule that claims to preserve the same story:

- midpoint supplies center
- predecessor shell supplies scale
- one-center / two-branch prism law

but yields a different value of d.

Examples of rival forms:
- d = predecessor shell index = 4
- d = midpoint index - 1 = 4
- d = shell gap = 1
- d = bit imbalance = 3
- d = local contact gap = 9, 15, or another carrier statistic
- d = arbitrary normalization constant

## Exclusion principle
A valid displacement rule must satisfy all of the following.

### 1. Carrier-derived
The rule must come from structural carrier data, not arbitrary normalization.

### 2. Center-compatible
The rule must measure off-center branch displacement relative to the midpoint regime that already carries center.

### 3. Symmetry-compatible
The rule must produce a symmetric law:
- I - d
- I
- I + d

because the current prism law is centered and two-sided.

### 4. Branch-level
The rule must describe the first visible branch departure from center, not a distal or higher-order refinement.

### 5. Quotient-compatible
The rule must reproduce the exact observed centered prism law:
- (140,145,150)

without introducing extra free choices.

## Rival candidate exclusions

### Candidate A: d = predecessor shell index = 4
This fails exact reconstruction:
- 145 - 4 = 141
- 145 + 4 = 149

So it does not recover the observed prism law.

### Candidate B: d = shell gap between predecessor and midpoint = 1
This gives:
- 144,145,146

So it is far too small and fails reconstruction.

### Candidate C: d = bit imbalance = 3
The shell probes show persistent bit imbalance 3 in many layers.
But this gives:
- 142,145,148

So it does not match the prism law.

Moreover bit imbalance is not the first branch-scale statistic of the shell ladder.
It is a local parity skew, not the centered branch displacement.

### Candidate D: d from parity gap 15
The parity-triangle refinement exhibits:
- 145 +/- 15

But this is a different quotient level.
It is not the prism branch displacement.
So it is too coarse for the first centered prism refinement.

### Candidate E: arbitrary free d
This violates carrier-derivedness and should be rejected by protocol.

## Surviving candidate
The rule

- d = L / 2

satisfies all current requirements:

- carrier-derived, since L = 10 is carrier-derived
- center-compatible, since it is measured from the midpoint regime
- symmetry-compatible
- branch-level, since it gives the first centered prism split
- quotient-compatible, since it reconstructs exactly:
  - 140,145,150

Indeed:
- d = 10 / 2 = 5

so:
- 145 - 5 = 140
- 145 + 5 = 150

## Strongest current exclusion reading
Among the currently visible shell statistics, the half-layer value is the only one that:

1. is carrier-derived,
2. is centered on midpoint structure,
3. yields a symmetric two-branch law,
4. and reconstructs the exact observed prism weights.

So the current rival candidates are excluded.

## Honest status
This is a strong exclusion argument.
It still falls slightly short of a pure first-principles derivation, because it works by eliminating competitors among currently visible structural rules.

But under the present protocol, it is the strongest available route to upgrading the half-layer step.

