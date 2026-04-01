# Candidate Invariants for the Bounded Slot-4 Exclusion Program

## Status
Working structural note

## Purpose
Record the most promising structural mechanisms explaining the bounded slot-4 exclusion law, incorporating the extracted residue evidence from the actual retained substitution dynamics.

---

## 1. Current theorem status

The bounded slot-4 exclusion theorem is already established at the finite retained-substitution level.

What remains is a deeper explanation of why the normalized slot-4 image closes on
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}
\]
and excludes \(t2\).

The strongest current explanation candidate is no longer a naive mod-5 slot-value rule. It is a seam-local \(O\)-support residue law.

---

## 2. Vocabulary support invariance

The raw substitution grammar uses the fixed vocabulary
\[
V=\{o0,o1,o2,o3,o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

Because retained descendants are obtained only by substitutions from this vocabulary, followed by normalization and filtering, no retained state can contain any symbol outside \(V\).

### Immediate consequence
Since
\[
t2\notin V,
\]
the symbol \(t2\) never appears anywhere in the retained substitution regime.

This explains the literal \(t2\)-exclusion directly.

However, it does not yet explain why the slot-4 image sharpens further to the smaller seam alphabet.

---

## 3. The failed naive residue guess

A first candidate residue law was:

> every retained bounded state has unique \(o\)-anchor \(o4\).

That is false globally.

The retained bounded residue extraction shows:
- anchors at \(0,1,2,3,4\),
- and many retained bounded states with non-unique \(o\)-support.

So unique-\(o4\)-anchor is not a valid invariant on the whole bounded retained regime.

This failure is informative: the correct residue law must be formulated on the right slice.

---

## 4. Seam-local O-support residue law

The correct slice is the retained frame-2 \(d_A=1\) seam.

On that slice, the extracted data show:

- 25 rows with a unique \(o\)-symbol, always \(o4\),
- 3 exceptional rows, all equal to the same normalized cycle
  \[
  [o4,s0,t0,s2,o4,s4],
  \]
  whose \(o\)-support is still entirely \(\{o4\}\).

This suggests the right invariant:

### Candidate invariant
For every retained frame-2 \(d_A=1\) state \(c\),
\[
\operatorname{Supp}_O(c)\subseteq \{o4\}.
\]

Equivalently, no seam-local retained state contains any of
\[
o0,o1,o2,o3.
\]

This is the strongest current residue candidate.

---

## 5. Why this explains the seam alphabet

If every seam-local retained state has
\[
\operatorname{Supp}_O(c)\subseteq \{o4\},
\]
then normalized slot 4 can never be one of
\[
o0,o1,o2,o3.
\]

Combined with vocabulary support invariance, the only possible normalized slot-4 values are
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

That is exactly the observed seam alphabet.

So the current best explanation of the seam alphabet is:

1. vocabulary support invariance excludes \(t2\),
2. seam-local \(O\)-support residue excludes \(o0,o1,o2,o3\),
3. the remaining slot-4 possibilities are exactly the observed seam alphabet.

---

## 6. Affine residue interpretation

The seam-local \(O\)-support law may itself be the visible form of a deeper affine residue law mod 5.

In that reading, the index 4 is not special accidentally; it is the residue class selected by the locked frame-2 seam geometry and preserved by the retained seam-local dynamics.

At present, however, the cleanest provable form is the support statement
\[
\operatorname{Supp}_O(c)\subseteq\{o4\},
\]
not yet a closed algebraic residue formula.

---

## 7. Normalization-orbit interpretation

The \(O\)-support residue law also fits naturally with a normalization-orbit interpretation.

Because the normalized representative is chosen by dihedral lexicographic minimization, concentration of \(O\)-support at \(o4\) forces the normalized seam states into a proper orbit slice. This provides a plausible explanation of why the seam-local normalized slot-4 image is sharply smaller than the ambient vocabulary.

So the present best reading is hybrid:

- substitution support controls what symbols can appear at all,
- seam-local \(O\)-support controls which \(o\)-symbols survive in the normalized seam slice,
- normalization then sharpens the visible slot-4 alphabet.

---

## 8. Defect-transport interpretation

The \(O\)-support residue law is also compatible with the defect-transport picture.

On that reading, the seam-local defect is transported within a class whose \(o\)-support remains anchored at \(o4\). The visible slot-4 values
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}
\]
are then the defect presentations compatible with that anchored support, while \(t2\) is excluded already at the support level.

So the defect-transport explanation and the \(O\)-support residue law may be two views of the same phenomenon.

---

## 9. Current best invariant package

The strongest current invariant package is:

### Invariant A. Vocabulary support
Every retained state uses only symbols from
\[
V=\{o0,o1,o2,o3,o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Invariant B. Seam-local O-support residue
For every retained frame-2 \(d_A=1\) state \(c\),
\[
\operatorname{Supp}_O(c)\subseteq \{o4\}.
\]

### Consequence
For every retained frame-2 \(d_A=1\) state \(c\),
\[
\pi_4(c)\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

This is the current best structural explanation of the seam alphabet.

---

## 10. What remains open

The following deeper questions remain.

### Question 10.1
Why does the seam-local \(O\)-support residue law hold?

### Question 10.2
Can the support law be upgraded to a genuine affine residue theorem mod 5?

### Question 10.3
Can the seam-local law be extended beyond the \(d_A=1\) seam slice to a larger bounded class?

### Question 10.4
Is the three-row degenerate duplicate-\(o4\) case merely a normalization overlap phenomenon, or part of a broader structural family?

---

## 11. Present working judgment

The best current explanation is no longer a naive parity or direct slot-value residue law.

It is:

> vocabulary support invariance globally, plus seam-local \(O\)-support residue at \(o4\).

That package explains the observed seam alphabet more naturally than any earlier candidate.
