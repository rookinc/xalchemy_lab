# O-Support Residue Law on the Frame-2 Seam

## Status
Working structural theorem note

## Purpose
Record the seam-local residue law suggested by the extracted frame-2 \(d_A=1\) data and show how it explains the observed slot-4 seam alphabet.

---

## 1. Empirical structural fact

The extracted frame-2 \(d_A=1\) residue summary shows:

- 25 seam-local retained rows have a unique \(o\)-symbol, and it is always \(o4\),
- the remaining 3 seam-local retained rows are all the same degenerate normalized cycle
  \[
  [o4,s0,t0,s2,o4,s4],
  \]
  whose \(o\)-support is still entirely \(\{o4\}\).

Thus every retained frame-2 \(d_A=1\) state has normalized \(o\)-support contained in \(\{o4\}\).

---

## 2. Seam-local residue law

### Proposition 2.1. O-support residue law
For every retained frame-2 \(d_A=1\) state \(c\),
\[
\operatorname{Supp}_O(c)\subseteq \{o4\}.
\]

Equivalently, no normalized seam-local retained state contains any of
\[
o0,o1,o2,o3.
\]

### Proof status
Established by extracted frame-2 \(d_A=1\) residue table.

---

## 3. Slot-4 alphabet corollary

Because the retained substitution vocabulary is
\[
V=\{o0,o1,o2,o3,o4,s0,s2,s3,s4,t0,t3,t4\},
\]
and Proposition 2.1 excludes \(o0,o1,o2,o3\) from seam-local normalized support, the only possible normalized slot-4 values on the seam are
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

This is exactly the observed seam alphabet.

### Corollary 3.1. Seam slot-4 closure
For every retained frame-2 \(d_A=1\) state \(c\),
\[
\pi_4(c)\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

---

## 4. Exclusion consequence

Since \(t2\notin V\), it follows immediately that
\[
\pi_4(c)\neq t2
\]
for every seam-local retained state \(c\).

Thus the seam-local obstruction is explained by two ingredients:

1. vocabulary support invariance,
2. seam-local \(O\)-support residue.

---

## 5. Interpretation

The slot-4 seam alphabet is not arbitrary.

It is the alphabet compatible with:
- the retained substitution vocabulary,
- and the seam-local law that all normalized \(o\)-support is concentrated at \(o4\).

So the seam obstruction is governed by an \(o4\)-anchored residue law rather than by a generic mod-5 slot value rule.

