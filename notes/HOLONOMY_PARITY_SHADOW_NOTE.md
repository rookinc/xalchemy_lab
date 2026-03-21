# Holonomy Parity Shadow Note

## Context

The tri-patch transport study has now revealed four distinct layers:

1. **Bundled rail law**  
   Exact affine transport on the preferred bundled route.

2. **Rail defect algebra**  
   Stable transported stress/mismatch offsets with parity-controlled flip injection.

3. **Holonomy lattice**  
   Additive route-class corrections for admissible off-rail middle-route deviations.

4. **Parity shadow**  
   A residual binary obstruction visible in the integer structure of the holonomy lattice.

This note records the fourth layer.

---

## 1. Recap: enumerated middle-route classes

The middle-route enumerator found the following eight route classes:

\[
\text{hold\_all}
\]

\[
\text{advance\_L1},\quad \text{advance\_L2},\quad \text{advance\_R1}
\]

\[
\text{advance\_L1\_L2},\quad \text{advance\_L1\_R1},\quad \text{advance\_L2\_R1}
\]

\[
\text{advance\_L1\_L2\_R1}.
\]

Relative to bundled transport, these produce holonomy vectors in

\[
\mathbb{Z}^3_s \oplus \mathbb{Z}^3_m.
\]

The zero class is the fully bundled route:

\[
\text{advance\_L1\_L2\_R1} \mapsto (0,0,0;\,0,0,0).
\]

All other route classes give nontrivial corrections.

---

## 2. Integer lattice result

The Smith-normal-form probe on the seven nonzero holonomy vectors produced:

- rank over \(\mathbb{Q}\):  
  \[
  6
  \]

- Smith invariants:  
  \[
  (1,1,1,1,1,2).
  \]

This means the observed holonomy classes generate a rank-6 lattice with a residual factor of \(2\).

Equivalently:

- the lattice spans all six ambient directions rationally
- but it does **not** fill \(\mathbb{Z}^6\) integrally
- instead it sits inside with **index 2**

So the holonomy lattice is not unimodular in the ambient integer coordinates.

This is the first precise sign that a binary obstruction is present.

---

## 3. Mod-2 reduction

The mod-2 probe reduced each holonomy vector into \((\mathbb{Z}_2)^6\).

The result was:

- mod-2 rank:
  \[
  5
  \]

- number of reachable parity vectors:
  \[
  32
  \]

- number of unreachable parity vectors:
  \[
  32
  \]

out of the total \(64\) parity vectors in \((\mathbb{Z}_2)^6\).

So the observed holonomy image mod 2 is exactly **half** of the ambient parity space.

This is the mod-2 manifestation of the index-2 Smith obstruction.

---

## 4. Interpretation: codimension-1 binary shadow

Since the mod-2 image has size \(32 = 2^5\), it is a codimension-1 subspace of \((\mathbb{Z}_2)^6\).

That means there is exactly one independent binary constraint cutting out the observed image.

In other words, the holonomy classes do not realize arbitrary parity signatures.
They are restricted to one half-space in parity space.

This is what we call the **holonomy parity shadow**.

---

## 5. Distinct observed parity classes

The probe found the following distinct parity representatives among the enumerated route classes:

\[
(0,0,0,0,0,0)
\]

\[
(0,1,1,0,0,0)
\]

\[
(1,0,1,0,0,0)
\]

\[
(1,1,0,0,0,0)
\]

\[
(1,1,1,0,0,0)
\]

\[
(1,1,1,1,0,1)
\]

\[
(1,1,1,0,1,1).
\]

These already span a 5-dimensional mod-2 space.

---

## 6. Witness of the missing coset

The probe also displayed explicit unreachable parity vectors, including for example:

\[
(0,0,0,0,0,1).
\]

This is a concrete witness that the parity image is not all of \((\mathbb{Z}_2)^6\).

That unreachable witness is important because it proves the obstruction is not an artifact of small sampling inside the enumerated class list.
It is built into the mod-2 lattice image itself.

---

## 7. Why the parity shadow matters

At the integer level, the holonomy lattice already looked a little strange:

- it was full rank
- but basis attempts gave awkward non-unimodular coordinates
- and the SNF had a final invariant factor \(2\)

The parity shadow explains that cleanly.

The lattice is not “messy by accident.”
It is missing exactly one binary degree of freedom in ambient \(\mathbb{Z}^6\).

So there is a genuine mod-2 memory baked into the holonomy structure.

---

## 8. Relation to earlier parity phenomena

This is not the first binary layer in the broader project.

Earlier signed-lift work on the quotient/lift side already revealed a nontrivial \(\mathbb{Z}_2\)-valued cocycle associated with loop holonomy in the signed chamber lift.

That earlier cocycle was global and combinatorial.
The present parity shadow is local and transport-dynamical.

They should not yet be identified as the same object.
But the resemblance is striking:

- both are loop-sensitive
- both survive after more obvious local transport data is accounted for
- both leave a binary remainder not captured by the main affine law

So the holonomy parity shadow is now the strongest local candidate for a transport-side manifestation of the broader binary structure.

---

## 9. Current conjecture

### Holonomy Parity Shadow Conjecture

The middle-route holonomy lattice on the tri-patch carries an intrinsic codimension-1 binary shadow.
Equivalently, the mod-2 reduction of the observed holonomy image occupies one 5-dimensional subspace of \((\mathbb{Z}_2)^6\), not the full parity space.

This binary shadow is the mod-2 trace of the index-2 integral obstruction seen in the Smith invariants.

---

## 10. Structural summary

The current transport geometry now looks like this:

### Bundled layer
Exact affine transport on the bundled locked rail.

### Defect layer
Additive stress/mismatch defect transport with parity flip injection.

### Holonomy layer
Additive route-class correction lattice for off-rail admissible histories.

### Parity-shadow layer
A codimension-1 binary constraint on the holonomy lattice mod 2.

This means the tri-patch is not merely an affine transport gadget.
It is an affine transport system with a nontrivial binary shadow.

---

## 11. What remains to do

The key unresolved question is:

> What is the actual linear parity functional defining the codimension-1 subspace?

That is the next concrete task.

A script should solve for the binary linear form

\[
\ell : (\mathbb{Z}_2)^6 \to \mathbb{Z}_2
\]

such that the observed holonomy classes satisfy

\[
\ell(H) = 0
\]

for all reachable parity vectors.

That will expose the exact missing bit.

After that, the real bridge question becomes:

> Does this local parity functional correspond in any clean way to the signed-lift cocycle’s global binary data?

That is the next major bridge.

---

## 12. Working summary

The transport story now has a sharp ending point for this phase:

- the bundled rail is exact
- the off-rail corrections form an additive lattice
- that lattice is full-rank but non-unimodular
- and its mod-2 image has codimension 1

So the current best description is:

> **The tri-patch holonomy lattice carries a genuine parity shadow.**

