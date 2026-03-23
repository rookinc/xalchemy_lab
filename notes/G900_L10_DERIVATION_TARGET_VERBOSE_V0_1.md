# G900 L = 10 Derivation Target — Verbose Note v0.1

## Status
Verbose derivation-target note.

## Why this note exists
The current G900 package has now reached a strong internal checkpoint.

We are no longer mainly asking:

- why is the offset 5?
- what scalar explains the package?
- is there a prettier normalization?

Those questions have now been subordinated to a clearer and more disciplined upstream target.

The live derivation target is:

- why does the carrier produce L = 10?

This note records exactly why that is now the right next question, what has already been closed, what has not yet been closed, and what a real derivation of L = 10 would need to accomplish.

---

## Current checked package
The checked bundle now supports the following exported and replayable facts.

### Weighted prism source
The current weighted prism export records:

- center weight = 145
- top-face weight = 140
- rung weight = 145
- bottom-face weight = 150

with normalized offsets

- bit0_face = -5
- macro_rung = 0
- bit1_face = +5

and carrier summary

- cell_count = 900
- layer_count = 10
- macro_count = 3
- bit_count = 2

### Derived centered family
The current data can be written in centered form as:

- (I - d, I, I + d)

with

- I = 145
- d = 5

so the present extracted instance is

- (140, 145, 150).

### Quotient image
The paired face values recombine to:

- 140 + 150 = 290

which is exactly

- 2 * 145 = 290.

So the current quotient reading is:

- Q(I) = 2I.

### Half-layer law in the export
The current export also records:

- layer_count = 10
- d = 5

so that:

- d = L / 2

with

- L = 10.

### Derived closure law
Combining the centered family with the export-level band law yields:

- (I - L/2, I, I + L/2) -> Q(I) = 2I

and in the present instance:

- (140, 145, 150) -> 290.

This is now bundle-checked and replayable.

---

## What is closed now
The following are currently closed at the export-and-checker level.

### 1. Centered band form
The current preimage is centered:

- 145 = (140 + 150) / 2

so the extracted band is legitimately centered around I.

### 2. Doubled-center quotient image
The quotient image satisfies:

- Q(I) = 2I

in the current package.

That is not merely a suggestive pattern now.
It is replayed and checked.

### 3. Offset invisibility at quotient level
The extension parameter d cancels in:

- (I - d) + (I + d) = 2I

so the quotient image is insensitive to d.

This is a strong separation result.

It means:

- I is core quotient data
- d is extension data

### 4. Export-level half-layer law
The current export satisfies:

- d = L / 2

with:

- d = 5
- L = 10.

### 5. Mid-band consistency
The export is exactly consistent with a centered face-to-face band of width 10:

- top offset = -5
- bottom offset = +5
- band width = 10
- rung at midpoint

So the centered 10-layer band reading is strongly supported in the current export.

### 6. Bundle replay
The full G900 bundle now replays the entire ladder and passes.

That matters methodologically.
This is not a one-shot interpretation.
It is now an executable closure package.

---

## What has been weakened or eliminated
Several tempting explanations have already been pressure-tested and either weakened or ruled out as direct explanations.

### 1. Arithmetic alone does not force midpoint balance
Noncentered candidates survive arithmetic-only constraints.
So the centered law is not forced by face-sum arithmetic alone.

### 2. Centered-offset structure forces the center, but not the specific offset
Once the rung is treated as the true center class, the center becomes structural.
But the exact magnitude d is still not fixed by that alone.

### 3. The cubic does not directly normalize the current package
The positive root of

- 64x^3 + 64x^2 + 7x - 9 = 0

did not line up in a clean direct way with the current observed normalized G900 quantities.

So the cubic should not presently be treated as the direct normalizer of the extension layer.

### 4. Phi does not directly normalize the current package either
Phi and simple phi-derived forms also failed to cleanly match the current observed normalized extension ratios.

So phi remains, at best, a possible upstream geometric influence, not a demonstrated direct control parameter of the present G900 export.

### 5. Simple numerical fit is not enough
Several simple formulas reproduce the observed offset 5:

- layer_count / 2
- macro_count + bit_count
- layer_count / bit_count
- cell_count / 180

So arithmetic matching alone cannot identify the correct explanatory law.

This means the live explanation must be structural, not merely exact-valued.

---

## Why L = 10 is now the true upstream target
At this point, the package has compressed into a clean dependency chain:

- carrier geometry -> L = 10 -> d = 5 -> centered band -> Q(I) = 2I

That means the real explanatory bottleneck is no longer:

- why 5?

Instead it is:

- why 10?

Because once L = 10 is granted, the rest follows very cleanly:

- d = L / 2 = 5
- centered band = (140, 145, 150)
- quotient image = 290 = 2 * 145

So the live mathematical pressure is entirely on the source of the 10-layer band.

This is now the strongest and most honest derivation target.

---

## What a real derivation of L = 10 would need to show
A theorem-grade derivation of L = 10 should not merely point to metadata or restate the export.
It should explain why the carrier must yield a face-to-face separation of width 10.

At minimum, such a derivation would need to show one or more of the following.

### 1. Layer-count is intrinsic, not decorative
The value:

- layer_count = 10

must be shown to arise from the actual carrier organization, rather than being a convenient recording choice.

That means:

- derived from the classification,
- derived from adjacency traversal,
- derived from shell depth,
- derived from face-to-face separation,
- or derived from another explicit carrier construction law.

### 2. The two face strata sit at opposite ends of that band
A derivation must show that the two face families used in the centered prism law really are separated by the full band width.

In other words:

- top and bottom are not just two labeled classes
- they are opposite ends of the same extension axis or band

### 3. The rung is the true midpoint support
A derivation must show that the rung class is not merely an intermediate numerical weight, but the actual mediating midpoint between the two face strata.

That is what would upgrade the current centered band reading from “export-consistent” to “structurally forced.”

### 4. The normalization records half-thickness
A derivation must explain why the recorded offsets are:

- -L/2
- 0
- +L/2

rather than some other scaling or coordinate convention.

That is the place where the current package still depends on export-level normalization.

---

## Plausible sources of an L = 10 derivation
The next derivation may come from one or more of these.

### A. Direct carrier traversal
The most rigorous option:
show an explicit 10-step or 10-layer face-to-face traversal in the actual carrier.

This would be strong because it would directly anchor band width in the combinatorics.

### B. Macro / bit decomposition
Since the source is classified by:

- macro_count = 3
- bit_count = 2

it is possible that the 10-layer band arises from how the two bit sectors are embedded across the carrier depth.

That would be a more structural explanation than reading the layer count as raw metadata.

### C. Shell or band geometry
The 10 may be the width of the first full centered extension band around a triadic core.

This is compatible with the hypothesis that:

- the core law is triadic
- the extension law is where the 5-structured geometry enters
- the full band is doubled across the center

This is conceptually attractive, but still needs proof.

### D. Export-generation code path
There may be a concrete script or generation step where the layer count is actually constructed or inferred.

If so, the path to derivation may run through code archaeology:
find the step where the 10 enters and determine whether it is computed or declared.

---

## Current theorem-hunt split
The clean split is now:

### Closed, replayable, export-level
- centered band
- doubled-center quotient image
- d = L / 2 in the export
- derived closure law
- bundle replay

### Open, structural, theorem-level
- derivation of L = 10 from the carrier
- proof that d = L / 2 is structurally necessary
- proof that the centered band is not merely an export normalization artifact
- exact status of side-contribution semantics
- broader extension beyond this G900 package

This is now the mathematically honest frontier.

---

## Recommended next derivation question
The next question should be framed as narrowly and concretely as possible:

- What explicit carrier mechanism produces the face-to-face separation L = 10?

This is better than asking:

- why 5?
- what scalar explains this?
- is phi hiding somewhere?
- does the cubic secretly normalize the band?

Those questions may still matter later, but they are now downstream of the real issue.

The next real issue is the origin of the 10-layer band.

---

## Suggested derivation path
A disciplined path forward would be:

1. locate the exact source of `layer_count = 10`
2. determine whether it is declared or computed
3. identify the actual two face strata used as band endpoints
4. show whether the rung class is the midpoint of their separation
5. rewrite the band law as a carrier statement, not an export statement
6. only then ask whether any higher scalar or pentadic geometry belongs upstream

This keeps explanation subordinate to derivation.

---

## Honest conclusion
The current G900 package now has a strong internal mathematical spine.

That spine is:

- Q(I) = 2I
- d = L / 2 in the export
- (I - L/2, I, I + L/2) -> Q(I) = 2I

The package is now strong enough that the next task is no longer to hunt for a prettier interpretation.

The next task is to derive the single remaining upstream parameter:

- L = 10

from the carrier itself.

That is the present derivation target.

