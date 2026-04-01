# Slot-4 Templates and Finite Closure Table

## Status
Established finite proof note

## Purpose
Replace the earlier abstract template scaffold with a proof note grounded in the actual G900 one-edit grammar and the extracted retained substitution table.

The main point is that the bounded slot-4 exclusion theorem is now supported by a finite, extracted closure table for the real retained substitution automaton.

---

## 1. Actual move system

The operative one-edit system is the one implemented in the slot-4 scripts.

### Raw substitution rule
Starting from a 6-cycle
\[
c=[x_0,x_1,x_2,x_3,x_4,x_5],
\]
a raw one-edit child is obtained by:

1. choosing a raw position
   \[
   p\in\{0,1,2,3,4,5\},
   \]
2. choosing a replacement symbol \(y\) from the fixed vocabulary
   \[
   V=\{o0,o1,o2,o3,o4,s0,s2,s3,s4,t0,t3,t4\},
   \]
3. requiring \(y\neq x_p\),
4. replacing \(x_p\) by \(y\).

### Normalization rule
The resulting cycle is then dihedrally normalized by taking the lexicographically minimal element among:

- all cyclic rotations,
- all cyclic rotations of the reversed cycle.

The normalized slot-4 value is therefore the entry in position 4 of the normalized representative, not the raw symbol at raw position 4.

### Retention rule
A child is retained in the bounded regime if either:

- it is exact frame 2, or
- its best action distance is \(\le 3\).

The frame-2 seam slice is the retained subset satisfying:

- `classification == "action-cell"`,
- `best_action_distance == 1`,
- frame 2 appears among nearest action frames.

---

## 2. Relevant alphabets

### Locked seed slot-4 values
The distinguished locked witnesses have normalized slot-4 values
\[
A_{\mathrm{seed}}=\{t4,o4,s3,s0\}.
\]

### Retained bounded slot-4 alphabet
The extracted retained bounded slot-4 alphabet is
\[
A_{\mathrm{ret}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Retained seam slot-4 alphabet
The extracted retained frame-2 \(d_A=1\) slot-4 alphabet is
\[
A_{\mathrm{seam}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

These two alphabets coincide, so we write simply
\[
A_{\mathrm{seam}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

---

## 3. Main extracted fact

The retained substitution extraction reports:

### Retained bounded slot-4 histogram
\[
\{o4:48,\ s0:29,\ s2:5,\ s3:31,\ s4:6,\ t0:10,\ t3:6,\ t4:33\}.
\]

### Retained frame-2 \(d_A=1\) slot-4 histogram
\[
\{o4:3,\ s0:3,\ s2:4,\ s3:3,\ s4:4,\ t0:4,\ t3:4,\ t4:3\}.
\]

No retained child has normalized slot-4 value outside
\[
A_{\mathrm{seam}}.
\]

In particular, no retained child has slot-4 value \(t2\).

---

## 4. Template interpretation

Because the raw grammar is full single-symbol substitution, “templates” should not be understood as hidden symbolic rewrite rules. They should be understood as:

> equivalence classes of retained substitutions grouped by raw position, family change, and normalized slot-4 output.

The extracted summary already organizes these implicitly through the fields:

- raw position,
- from-family,
- to-family,
- child slot-4 value,
- child classification,
- child confidence,
- child best action distance.

This is enough for a finite proof.

---

## 5. Finite closure proposition

### Proposition 5.1. Finite retained slot-4 closure
Every retained bounded substitution child generated from the locked witness set has normalized slot-4 value in
\[
A_{\mathrm{seam}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Proof
This is exactly the extracted retained bounded slot-4 alphabet:
\[
A_{\mathrm{ret}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]
Since the extraction enumerates all retained bounded substitution children from the locked witness generators, no retained bounded child falls outside this set. ∎

---

## 6. Seam-local closure proposition

### Proposition 6.1. Frame-2 seam slot-4 closure
Every retained frame-2 \(d_A=1\) substitution child generated from the locked witness set has normalized slot-4 value in
\[
A_{\mathrm{seam}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Proof
This is exactly the extracted retained frame-2 \(d_A=1\) slot-4 alphabet. ∎

---

## 7. Exclusion corollary

### Corollary 7.1. Retained slot-4 exclusion
No retained bounded substitution child generated from the locked witness set has normalized slot-4 value \(t2\).

### Proof
By Proposition 5.1, every retained bounded child has slot-4 value in
\[
A_{\mathrm{seam}}=\{o4,s0,s2,s3,s4,t0,t3,t4\},
\]
and \(t2\notin A_{\mathrm{seam}}\). ∎

---

## 8. Seed-generation observation

The retained seam transition summary shows that the locked seed values
\[
\{t4,o4,s3,s0\}
\]
generate the full seam alphabet under retained frame-2 \(d_A=1\) substitutions.

Indeed, the extracted seam transitions show that from the locked starts one reaches every value in
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

This supports the interpretation that the seam alphabet is generated from the locked witnesses by the seam-local retained substitution law.

---

## 9. Position-family summary

The extracted template counts show that retained children arise from a finite set of substitution classes indexed by:

- raw position,
- source family,
- target family,
- normalized slot-4 output,
- retained classifier data.

Representative retained classes include:

- position 5, \(s\to o\), output \(o4\),
- position 0, \(o\to o\), output \(t4\),
- position 4, \(t\to s\), output \(t4\),
- position 2, \(t\to s\), output \(o4\),
- position 1, \(t\to s\), output \(s3\),
- position 3, \(o\to o\), output \(s3\),
- position 5, \(s\to s\), output \(s2,s4\),
- position 5, \(s\to t\), output \(t0,t3,t4\),
- position 0, \(o\to s\), output \(s0,s2,s3,s4\),
- position 0, \(o\to t\), output \(t0,t3,t4\).

Crucially, no retained class produces output \(t2\).

---

## 10. Best proof reading

The strongest current reading is not merely that \(t2\) failed to appear in a large search.

The stronger statement is:

> under the actual retained substitution grammar, the normalized slot-4 image closes on an eight-symbol alphabet that excludes \(t2\).

That is the finite closure law behind the bounded obstruction theorem.

---

## 11. Role in the theorem ladder

This file supplies the concrete finite proof certificate needed for the local closure lemma.

Combined with the reduction theorem, it yields:

1. bounded slot-4 exclusion,
2. bounded no exact frame-2 closure,
3. a generated seam alphabet from the locked seed set.

So the obstruction is now represented as a finite retained substitution law, not only as a large negative reachability statement.

---

## 12. Closing note

The theorem program has now crossed from generic template speculation to actual extracted finite structure.

The remaining work is mainly expository:
- state the retained substitution theorem cleanly,
- cite the extracted closure alphabet,
- use the reduction theorem to deduce bounded no-closure.

That is a much stronger position than merely reporting saturation.
