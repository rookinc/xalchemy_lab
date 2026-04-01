# Retained Substitution Closure at Slot 4

## Status
Established from extracted finite table

## Purpose
Record the finite retained-substitution closure law for normalized slot 4, as extracted directly from the actual G900 substitution grammar and bounded retention filter.

---

## 1. Actual retained substitution system

The operative move system is:

1. choose one raw position in the 6-cycle,
2. replace the symbol at that position by a different symbol from the fixed vocabulary
   \[
   V=\{o0,o1,o2,o3,o4,s0,s2,s3,s4,t0,t3,t4\},
   \]
3. dihedrally normalize the resulting cycle,
4. classify the normalized cycle,
5. retain the child only if it satisfies the bounded filter:
   - exact frame-2, or
   - best action distance \(\le 3\).

Thus the relevant dynamics are those of a bounded retained substitution automaton.

---

## 2. Extracted finite summary

From the locked frame-2 witnesses, the retained substitution extraction yields:

### Retained bounded slot-4 histogram
\[
\{o4:48,\ s0:29,\ s2:5,\ s3:31,\ s4:6,\ t0:10,\ t3:6,\ t4:33\}.
\]

### Retained bounded slot-4 alphabet
\[
A_{\mathrm{ret}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Retained frame-2 \(d_A=1\) slot-4 histogram
\[
\{o4:3,\ s0:3,\ s2:4,\ s3:3,\ s4:4,\ t0:4,\ t3:4,\ t4:3\}.
\]

### Retained frame-2 \(d_A=1\) slot-4 alphabet
\[
A_{\mathrm{seam}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

These two alphabets coincide.

---

## 3. Main closure proposition

### Proposition 3.1. Retained slot-4 closure
Under the bounded retained substitution system generated from the locked frame-2 witnesses,
every retained child has normalized slot-4 value in
\[
A_{\mathrm{seam}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Proof
This is exactly the extracted retained bounded slot-4 alphabet recorded above. No retained child falls outside this set. ∎

---

## 4. Exclusion corollary

### Corollary 4.1. Bounded slot-4 exclusion
Under the same retained substitution system,
\[
\forall c,\quad \pi_4(c)\neq t2.
\]

### Proof
The retained slot-4 alphabet is
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\},
\]
which does not contain \(t2\). ∎

---

## 5. No-closure corollary

### Corollary 5.1. Bounded no exact frame-2 closure
If exact frame-2 closure requires \(\pi_4=t2\), then no retained bounded state is exact frame 2.

### Proof
Immediate from Corollary 4.1 and the exactness necessity principle. ∎

---

## 6. Seed-generation observation

The retained seam transition summary shows that the locked slot-4 seed values
\[
A_{\mathrm{seed}}=\{t4,o4,s3,s0\}
\]
generate the full seam alphabet under retained frame-2 \(d_A=1\) substitutions.

This supports the interpretation that \(A_{\mathrm{seam}}\) is not merely observed but generated from the locked seed set by the seam-local retained substitution law.

---

## 7. Interpretation

The bounded obstruction is therefore no longer merely a negative search outcome.

It is a finite closure law for the actual retained substitution grammar:
bounded retained substitutions preserve a proper normalized slot-4 alphabet that excludes the exact frame-2 installation value \(t2\).

That is the cleanest current theorem statement.

---

## 8. Role in the paper

This proposition is the concrete finite proof certificate underlying the bounded obstruction theorem.

Together with the reduction theorem and the slot-4 exactness necessity principle, it yields the current main result:

- bounded slot-4 exclusion,
- bounded no exact frame-2 closure,
- seam alphabet generation from the locked seed set.

This is the correct theorem-facing replacement for the earlier looser “search saturation found no \(t2\)” phrasing.
