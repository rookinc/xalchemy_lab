# Projected Slot-4 Transport Program

## Status
Working structural follow-up

## Purpose
Explain the already established bounded slot-4 exclusion theorem at a deeper structural level.

The bounded exclusion itself is now supported by the extracted finite retained-substitution closure table. What remains is to understand why this closure law holds.

---

## 1. What is already established

The following is already in hand.

### Established theorem
Under the actual retained substitution dynamics:
- single-symbol substitution from the fixed vocabulary,
- dihedral normalization,
- retention by bounded action-distance / exact-frame-2 filters,

the normalized slot-4 image closes on
\[
A_{\mathrm{seam}}=\{o4,s0,s2,s3,s4,t0,t3,t4\},
\]
and therefore excludes \(t2\).

So the bounded slot-4 exclusion theorem is no longer merely conjectural.

---

## 2. What remains to explain

The remaining question is structural:

> why does the retained substitution automaton close on this eight-symbol slot-4 alphabet?

That is the real role of the projected transport program.

---

## 3. Projected transport relation

Define the projected slot-4 transport relation
\[
a \rightsquigarrow_4 b
\]
iff there exist retained bounded states \(c,c'\) such that

- \(c\to c'\) by one retained substitution step,
- \(\pi_4(c)=a\),
- \(\pi_4(c')=b\).

Then the extracted theorem says the reachable projected alphabet is
\[
A_{\mathrm{seam}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

---

## 4. Structural questions

The main structural questions are now:

### Question 4.1
Why is \(A_{\mathrm{seam}}\) closed under retained projected transport?

### Question 4.2
Why do the locked seeds
\[
\{t4,o4,s3,s0\}
\]
generate the full seam alphabet?

### Question 4.3
Why is \(t2\) excluded specifically?

These are now explanation questions, not existence questions.

---

## 5. Candidate explanation routes

### Route 5.1. Affine residue law
There may be a mod-5 or related affine residue invariant governing retained projected transport.

### Route 5.2. Normalization-orbit restriction
The raw substitution grammar may be broader than the retained normalized dynamics, which could be trapped in a proper dihedral-normalized orbit slice excluding \(t2\).

### Route 5.3. Defect-transport law
The slot-4 mismatch may define a localized defect whose visible presentations are exactly the values in
\[
A_{\mathrm{seam}}.
\]
Then retained substitutions would transport the defect without annihilating it.

---

## 6. Best current formulation

The projected transport program should now be stated as:

> explain the finite retained-substitution closure law on normalized slot 4.

That is more accurate than treating closure itself as still unproved.

---

## 7. Immediate next theorem task

The next structural task is to compress the extracted substitution classes into a smaller conceptual law, ideally one of:

- a residue law,
- an orbit law,
- a defect law.

That is now the proper next horizon.
