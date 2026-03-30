# G900 First Paired Scales
## Basecamp note for the first lawful scale pairs to test on the G900 carrier

Date: 2026-03-29

---

## 0. Why this note exists

The bridge program now has a table.
The Binary row is frozen.
The Thalean row is frozen.
The next real move is to define the first natural paired scales for G900.

This note is that move.

The purpose is not to prove anything yet.
The purpose is to identify the first lawful scale pairs through which the same G900 generator output may be viewed.

This matters because the Binary rung already showed that exact law can appear in the relation between two natural normalizations of one lawful stream.
The Thalean rung showed that lawful transport can become exact only after compression into the right image.
G900 now needs its own first scale pair candidates.

The rule here is:

- keep it small
- keep it computable
- keep it lens-relevant
- do not multiply candidate scales faster than the data can support

---

## 1. What a paired scale is

A paired scale is two natural measurement frames applied to the same lawful output.

The pair should satisfy most of the following:

- both scales arise naturally from the carrier or generator
- both scales are meaningful at each tick, shell, or depth
- the same output can be normalized against both
- comparing the resulting images is mathematically sensible
- one has at least a plausible boundary/frontier flavor and the other a bulk/capacity flavor, or something structurally analogous

The whole point is not just to count more things.
The point is to compare the same lawful output under two disciplined frames.

---

## 2. The first candidate family

At current scope, the first G900 paired scales should probably come from three candidate families:

1. shell occupancy vs bulk capacity
2. frontier occupancy vs chamber capacity
3. upstairs occupancy vs quotient-visible occupancy

These are not yet laws.
They are search handles.

---

## 3. Candidate Pair A: shell occupancy vs bulk capacity

### 3.1 Intuition

This is the cleanest first candidate.

One scale measures how much lawful mass or occupancy appears at a given shell.
The other measures how much total capacity is available up to or within that shell band.

So the pair is:

- **local shell occupancy**
- **available bulk capacity**

This is the closest G900 analogue to the Binary boundary/bulk split.

### 3.2 Suggested definitions

Let \(N_k\) be the observed occupancy in shell \(k\).

Let \(C_k\) be the cumulative or modeled capacity associated with shell \(k\).
There are several possible choices for \(C_k\), and that choice will matter:

- cumulative reachable node capacity up to shell \(k\)
- modeled chamber capacity up to shell \(k\)
- geometric shell-capacity estimate from the generator grammar
- empirical maximum support size observed across comparison runs

At first, keep this simple and explicit.
Do not hide scale choice.

### 3.3 Candidate lens pair

Define two first-pass images:

- shell image:
  \[
  \rho_{\mathrm{shell}}(k) = \frac{N_k}{S_k}
  \]
  where \(S_k\) is a shell-local reference scale, possibly just raw shell capacity or shell size

- bulk image:
  \[
  \rho_{\mathrm{bulk}}(k) = \frac{N_k}{C_k}
  \]

This may later be converted to logarithmic potentials if multiplicative scaling appears useful.

### 3.4 Why it matters

If this pair is real, it may reveal:

- whether shell growth is saturating
- whether the object is filling inward capacity or merely extending outward
- whether a perspective identity exists between shell-local and bulk-normalized views
- whether a gradient emerges when shell-normalized occupancy stabilizes

### 3.5 Status

**Best first candidate.**

---

## 4. Candidate Pair B: frontier occupancy vs chamber capacity

### 4.1 Intuition

This pair is more transport-flavored.

Instead of treating a shell as the primary visible unit, it treats the active frontier as one scale and the total chamber-completion opportunity as the other.

This may be more faithful if G900 growth is not best described radially but by lawful completion opportunities.

### 4.2 Suggested definitions

Let \(F_t\) be frontier occupancy at tick \(t\), meaning the count of currently active growth sites, attachment sites, or outward-exposed lawful action sites.

Let \(K_t\) be chamber capacity at tick \(t\), meaning the count of currently available chamber completions, latent chamber slots, or bounded closure opportunities.

Then define:

- frontier-normalized image:
  \[
  \rho_{\mathrm{front}}(t) = \frac{I_t}{F_t}
  \]

- chamber-capacity image:
  \[
  \rho_{\mathrm{chamber}}(t) = \frac{I_t}{K_t}
  \]

Here \(I_t\) can be chosen as the primary lawful count under observation:
- active carriers
- occupied cells
- admissible placements realized
- or some other first conserved quantity

### 4.3 Why it matters

This pair may capture something the shell pair misses:

- whether the generator is still expanding frontier
- whether it is entering closure-dominant behavior
- whether chamber completion acts like a bulk phase relative to frontier activity
- whether boundary equilibrium induces interior tendency, as in the binary prototype

### 4.4 Risk

This pair may be harder to define cleanly at first.
“Frontier” and “chamber capacity” need to be made precise enough that the pair is not hand-wavy.

### 4.5 Status

**Strong second candidate, but needs better formal definitions.**

---

## 5. Candidate Pair C: upstairs occupancy vs quotient-visible occupancy

### 5.1 Intuition

The Thalean rung teaches that some exact laws become visible only after quotienting.

So G900 should probably include a scale pair that compares:

- what is present upstairs in the full carrier
- what remains visible after quotient compression

This is not exactly a boundary/bulk pair.
It is a **visibility/compression pair**.

### 5.2 Suggested definitions

Let \(U_t\) be a chosen upstairs observable:
- raw active count
- raw shell occupancy
- raw overlap count
- raw incidence support

Let \(Q_t\) be the corresponding quotient-visible observable:
- quotient shell occupancy
- quotient overlap count
- effective core occupancy
- fiber-collapsed support size

Then the first-pass pair is:

- upstairs image
- quotient image

and the first invariant to search is not necessarily a ratio but perhaps:

- exact difference
- bounded quotient loss
- affine offset
- asymptotic compression factor
- or operator closure visible only downstairs

### 5.3 Why it matters

This pair may be the most Thalean-faithful of all the G900 candidates.

If G900 has a true effective core, this pair may be the way you find it.

### 5.4 Risk

This pair depends on having a candidate quotient map.
If quotienting is not ready, this pair stays schematic.

### 5.5 Status

**Essential medium-term candidate, but not the very first computation.**

---

## 6. Candidate Pair D: local transport activity vs overlap image

### 6.1 Intuition

This pair is closer to the Thalean \(M \to Q\) story.

One scale is transport-local:
- move counts
- local incidence participation
- action-site activity

The other is overlap-global:
- support overlap
- pairwise incidence compression
- aa image

This pair would ask whether G900 has a comparable bridge from local incidence trace to global overlap image.

### 6.2 Why it matters

If this pair becomes clean, it may directly connect the G900 lens scaffold to the Thalean pattern where \(M\) acts as the bridge and \(Q=MM^T\) becomes the main image.

### 6.3 Risk

This is probably too high-level for first-light unless the transport trace matrix is already defined.

### 6.4 Status

**High-value later candidate.**

---

## 7. Recommended order of attack

The first-pass order should be:

### First
**shell occupancy vs bulk capacity**

Because it is the easiest to compute and the closest to the Binary pattern.

### Second
**frontier occupancy vs chamber capacity**

Because it may better respect the generator’s actual lawful action structure.

### Third
**upstairs occupancy vs quotient-visible occupancy**

Because it may reveal the first descent where G900 becomes algebraically legible.

### Fourth
**local transport activity vs overlap image**

Because it is closest to the Thalean aa architecture, but likely requires more machinery first.

---

## 8. What to compute first

For the first candidate pair, compute the following per shell or per tick.

### For shell occupancy vs bulk capacity
- raw shell occupancy \(N_k\)
- cumulative occupancy up to shell \(k\)
- shell-local capacity estimate \(S_k\)
- cumulative bulk capacity estimate \(C_k\)
- ratios \(N_k/S_k\) and \(N_k/C_k\)
- optionally log-ratios if the scaling looks multiplicative

Then inspect:
- difference between the two images
- whether the difference is stable
- whether it is affine in shell index
- whether it changes regime at closure thresholds

### For frontier vs chamber capacity
- frontier count \(F_t\)
- chamber-opportunity count \(K_t\)
- active lawful count \(I_t\)
- ratios \(I_t/F_t\) and \(I_t/K_t\)
- differences over tick

Then inspect:
- whether frontier stabilization induces chamber-gradient behavior
- whether closure causes regime change
- whether the two images separate cleanly in time

---

## 9. What would count as a hit

A candidate pair becomes important if it yields any of the following:

- an exact identity
- a stable affine difference
- a bounded difference with interpretable residue
- an asymptotic linear slope
- a quotient-visible simplification
- a low-complexity recurrence
- a polynomial reduction after descent
- or a repeatable regime transition across runs

Without one of these, it remains only a descriptive pair.

That is fine.
But the project should know the difference.

---

## 10. What not to do

Do not do these too early:

- define ten different capacities with no canonical reason
- log-transform everything just because the Binary note did
- declare a perspective identity before comparing rerooted or rerun data
- force a quotient before a visible compression candidate appears
- confuse visual roundness with scale-law evidence

The aim is not to manufacture analogy.
The aim is to discover whether a real bridge invariant exists.

---

## 11. First formal recommendation

The first formal recommendation from Basecamp is:

> Adopt shell occupancy vs bulk capacity as the first G900 paired-scale experiment.

Use shell index if the object is being analyzed radially.
Use tick if the generator chronology is cleaner than the shell chronology.
But do not mix the two in the first pass.

Once that experiment is stable, frontier vs chamber capacity should follow immediately.

---

## 12. Working summary

At first light, G900 does not need all possible scales.
It needs the first lawful pair.

That pair should probably be:

- shell occupancy
- versus
- bulk capacity

with frontier/chamber capacity as the second pair and upstairs/quotient-visible occupancy as the third.

This is enough to begin the actual bridge search.

