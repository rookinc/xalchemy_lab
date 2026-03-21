# Even Mismatch Parity Law Note

## Context

The holonomy study on the tri-patch has now progressed through several layers:

1. **Bundled rail law**  
   Exact affine transport on the preferred bundled route.

2. **Defect algebra**  
   Stable transported stress and mismatch offsets on the bundled rail, with parity-based sign-flip injection into mismatch.

3. **Holonomy lattice**  
   Additive route-class corrections for admissible off-rail middle-route deviations.

4. **Parity shadow**  
   A codimension-1 binary obstruction in the integer holonomy lattice.

This note records the final explicit form of that parity shadow.

---

## 1. The parity question

The Smith-normal-form probe showed:

- rank over \(\mathbb{Q}\):  
  \[
  6
  \]

- Smith invariants:  
  \[
  (1,1,1,1,1,2).
  \]

So the observed holonomy lattice is full rank in the ambient six coordinates, but has an index-2 obstruction integrally.

That guarantees a residual mod-2 shadow.

The next question was:

> What is the actual binary law cutting out the reachable image mod 2?

---

## 2. Mod-2 image

The mod-2 probe showed:

- mod-2 rank:
  \[
  5
  \]

- reachable parity vectors:
  \[
  32
  \]

- unreachable parity vectors:
  \[
  32
  \]

inside the total parity space \((\mathbb{Z}_2)^6\).

So the observed holonomy classes occupy exactly one codimension-1 subspace mod 2.

---

## 3. Solving the parity functional

The parity-functional probe searched for nonzero binary linear forms

\[
\ell : (\mathbb{Z}_2)^6 \to \mathbb{Z}_2
\]

that vanish on all reachable parity classes.

It found exactly one nonzero annihilator:

\[
w=(0,0,0,1,1,1).
\]

In coordinate form, this is the law

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

This annihilator was unique among all nonzero binary linear functionals.

So the parity shadow is now completely explicit.

---

## 4. Final law

### Even Mismatch Parity Law

For every observed reachable middle-route holonomy class,

\[
\Delta m_{L1}+\Delta m_{L2}+\Delta m_{R1}\equiv 0 \pmod 2.
\]

Equivalently:

> the total mismatch correction always has **even parity**.

That is the full binary obstruction.

No stress coordinate appears in the parity law.

---

## 5. What is excluded

The parity law immediately excludes any correction vector whose mismatch part has odd total parity.

Examples of forbidden parity signatures include:

\[
(0,0,0,0,0,1)
\]

\[
(0,0,0,0,1,0)
\]

\[
(0,0,0,1,0,0)
\]

\[
(0,0,0,1,1,1)
\]

because each has odd mismatch parity.

These were explicitly listed by the probe as unreachable parity vectors.

So the missing half of \((\mathbb{Z}_2)^6\) is exactly the odd-total-mismatch half.

---

## 6. Why this is striking

This result is much cleaner than expected.

The binary shadow could in principle have mixed:

- stress parity,
- mismatch parity,
- left/right coupling,
- or stress–mismatch cross terms.

Instead, the actual law depends only on mismatch coordinates.

So the local transport geometry is telling us:

- stress participates in the additive holonomy lattice,
- but the binary obstruction lives entirely in the mismatch/receipt sector.

That strongly reinforces the emerging interpretation:

> **stress behaves like transported payload, mismatch behaves like route receipt.**

---

## 7. Relation to earlier route structure

This parity law fits everything already observed.

### Bundled rail
Bundled transport has zero holonomy:
\[
(0,0,0;\,0,0,0),
\]
so mismatch parity is even.

### Singleton classes
Singleton routes all carry mismatch correction
\[
(-2,-2,-2),
\]
whose total parity is also even.

### Dyadic classes
The dyadic classes `A`, `B`, and `advance_L2_R1` all have mismatch corrections whose mod-2 sums vanish.

So the new law is not an extra patchwork rule.
It is the clean global summary of the mod-2 behavior already hidden inside all observed classes.

---

## 8. Transport interpretation

The parity shadow is now concrete:

- route deviations may change mismatch coordinates
- but they must do so in such a way that the total mismatch change is even

That means mismatch can be redistributed, but not created in odd total parity.

So the admissible transport histories appear to conserve a binary mismatch parity charge.

This is the first precise local binary conservation law in the tri-patch transport system.

---

## 9. Comparison to the broader project

This is especially interesting because the broader Thalean / signed-lift side already contains a \(\mathbb{Z}_2\)-valued cocycle associated with loop holonomy.

The present parity law is not yet identified with that cocycle.
But it is now a serious candidate for a local transport-side analogue:

- there: a binary loop-memory invariant in the signed chamber lift
- here: a binary even-parity law in the mismatch holonomy sector

Both are:

- loop/history sensitive
- invisible from the main affine transport law alone
- genuinely \(\mathbb{Z}_2\)-valued

That makes the comparison unavoidable.

---

## 10. Current conjecture

### Even Mismatch Parity Conjecture

The tri-patch middle-route holonomy lattice satisfies an intrinsic binary conservation law:
the total mismatch correction is always even mod 2.

Equivalently, the mod-2 image of the holonomy lattice is the kernel of the unique linear functional

\[
\ell(ds_{L1},ds_{L2},ds_{R1},dm_{L1},dm_{L2},dm_{R1})
=
dm_{L1}+dm_{L2}+dm_{R1}.
\]

---

## 11. Structural summary

The transport geometry now looks like this:

### Bundled rail
Exact affine transport.

### Defect layer
Stable transported stress/mismatch defect modes.

### Holonomy layer
Additive off-rail route-class correction lattice.

### Parity shadow
A binary constraint:
\[
\Delta m_{L1}+\Delta m_{L2}+\Delta m_{R1}\equiv 0 \pmod 2.
\]

So the current best description is:

> **The tri-patch holonomy lattice carries an even-total-mismatch parity law.**

---

## 12. Next bridge question

The next real question is not whether the parity law exists.
It does.

The question is:

> Is this local even-mismatch law the transport-side shadow of the broader signed-lift \(\mathbb{Z}_2\) cocycle?

That is the bridge to test next.

A comparison note should now be written that places these two binary structures side by side without prematurely identifying them.

---

## 13. Working summary

We now know the explicit missing bit:

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

So the binary shadow of the tri-patch holonomy lattice is not mysterious anymore.

It is simply:

> **odd total mismatch parity is forbidden.**

