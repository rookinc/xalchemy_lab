# Holonomy Class Map Note

## Context

The bundled locked rail supports an exact affine transport law with a semilinear defect algebra.
But once we allow admissible departures from the bundled middle route, the operator ceases to be route invariant.

The route-comparison probe already showed that two admissible histories with the same start and end hubs can produce different final stress and mismatch totals.

The holonomy class map sharpens that result:

> Admissible middle-route patterns fall into discrete correction classes.

These classes are stable across:

- positive vs negative hub launch
- clean vs defect-loaded initial states

So the correction is not a seed artifact.
It appears to be a genuine route class invariant.

---

## Baseline bundled transport

The bundled locked rail is the reference route:

- all three carriers move together through `mR`
- all three hit the opposite hub together
- all three return together

Relative to this bundled baseline, the correction vector is

\[
(\Delta \mathbf{s}, \Delta \mathbf{m}) = ((0,0,0),(0,0,0)).
\]

This is the trivial holonomy class.

---

## Holonomy classes discovered

The class map probe found six classes.

---

### Class 6: bundled rail

Route family:
- `bundled_all`

Correction:
\[
(\Delta \mathbf{s}, \Delta \mathbf{m}) = ((0,0,0),(0,0,0)).
\]

This is the exact affine rail law.

---

### Class 4: split `LR`, hold `L2`

Route family:
- `split_LR_hold_L2`

Middle event:
- dyadic `LR -> sign_transfer±`

Correction:
\[
(\Delta \mathbf{s}, \Delta \mathbf{m})
=
((-1,-1,-1),(-1,-2,-1)).
\]

Interpretation:
- all stress coordinates lose one
- mismatch loss is asymmetric, with the held `L2` channel losing two

This is the first nontrivial split class.

---

### Class 5: split `LL`, hold `R1`

Route family:
- `split_LL_hold_R1`

Middle event:
- dyadic `LL -> B±`

Correction:
\[
(\Delta \mathbf{s}, \Delta \mathbf{m})
=
((-1,-1,-1),(0,0,-2)).
\]

Interpretation:
- all stress coordinates again lose one
- mismatch penalty falls entirely on the held `R1` channel

So `LR`-type and `LL`-type splitting are different holonomy classes.

---

### Class 1: singleton `L1` advances

Route family:
- `singleton_L1_only`

Correction:
\[
(\Delta \mathbf{s}, \Delta \mathbf{m})
=
((-2,-1,-1),(-2,-2,-2)).
\]

Interpretation:
- the advancing singleton carrier `L1` loses an extra stress unit
- mismatch loses two units uniformly across all carriers

---

### Class 2: singleton `L2` advances

Route family:
- `singleton_L2_only`

Correction:
\[
(\Delta \mathbf{s}, \Delta \mathbf{m})
=
((-1,-2,-1),(-2,-2,-2)).
\]

Interpretation:
- now the extra stress loss falls on `L2`
- mismatch penalty remains uniformly `(-2,-2,-2)`

---

### Class 3: singleton `R1` advances

Route family:
- `singleton_R1_only`

Correction:
\[
(\Delta \mathbf{s}, \Delta \mathbf{m})
=
((-1,-1,-2),(-2,-2,-2)).
\]

Interpretation:
- the extra stress loss falls on `R1`
- mismatch penalty again remains uniformly `(-2,-2,-2)`

So the singleton family splits into three carrier-labeled classes.

---

## Structural observations

The class map reveals several clear patterns.

### 1. Arity matters

The correction depends strongly on the collision arity at the middle route:

- full triad closure gives zero holonomy
- dyadic routes give nontrivial corrections
- singleton routes give the strongest corrections

So the class structure is not arbitrary.
It is sensitive to how many carriers arrive together.

---

### 2. Carrier identity matters

For singleton routes, the stress correction remembers exactly which carrier advanced alone:

- `L1` singled out gives extra penalty on `L1`
- `L2` singled out gives extra penalty on `L2`
- `R1` singled out gives extra penalty on `R1`

Thus the holonomy class is not determined by arity alone.
It also depends on carrier identity.

---

### 3. Mismatch behaves differently from stress

Stress correction in singleton classes is carrier-localized:

\[
(-2,-1,-1),\quad (-1,-2,-1),\quad (-1,-1,-2).
\]

But mismatch correction there is uniform:

\[
(-2,-2,-2).
\]

So stress and mismatch respond differently to route splitting.

This reinforces the earlier theme:

- stress behaves like a transported payload
- mismatch behaves like a path/history receipt

---

### 4. Route class beats seed data

The same correction vector appears for a given route family across:

- positive rail / negative rail
- clean locked seed / defect-loaded locked seed

That means the class vectors are not sensitive to the carried additive defects already present on the rail.

So the holonomy is genuinely attached to the route pattern itself.

---

## Holonomy class table

For convenience, the current class table is:

\[
\begin{array}{c|c|c}
\text{Route family} & \Delta \mathbf{s} & \Delta \mathbf{m} \\
\hline
\text{bundled\_all} & (0,0,0) & (0,0,0) \\
\text{split\_LR\_hold\_L2} & (-1,-1,-1) & (-1,-2,-1) \\
\text{split\_LL\_hold\_R1} & (-1,-1,-1) & (0,0,-2) \\
\text{singleton\_L1\_only} & (-2,-1,-1) & (-2,-2,-2) \\
\text{singleton\_L2\_only} & (-1,-2,-1) & (-2,-2,-2) \\
\text{singleton\_R1\_only} & (-1,-1,-2) & (-2,-2,-2)
\end{array}
\]

This is the first real holonomy table of the toy patch.

---

## Interpretation

This means the tri-patch now has two distinct transport layers:

### Exact bundled layer
A preferred rail with exact affine and defect-transport laws.

### Off-rail holonomy layer
Alternative admissible histories with fixed route-class correction vectors.

So the system is not just a rail.
It is a rail inside a larger path-sensitive transport geometry.

---

## Conjecture

### Holonomy Class Conjecture

Each admissible middle-route pattern determines a discrete holonomy class

\[
H(\gamma) = (\Delta \mathbf{s}_\gamma,\ \Delta \mathbf{m}_\gamma)
\]

relative to the bundled baseline, and this class depends only on the route family \(\gamma\), not on the tested background defect load or hub sign.

---

## Immediate next question

The next natural question is composition.

If we perform two nontrivial route deviations in sequence:

- does the net correction equal the sum of their class vectors?
- or does the order matter?
- or does the second deviation see a modified state and generate a nonabelian correction?

That is the next frontier.

---

## Working summary

The turtles have now uncovered:

1. a bundled affine rail
2. a semilinear defect algebra on that rail
3. off-rail route sensitivity
4. a discrete map of holonomy classes

That is already the skeleton of a transport geometry.

