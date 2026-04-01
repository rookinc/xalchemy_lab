# Main Results

## Status
Working draft

## Purpose
State the current bounded computational results in proposition form, separating established statements from conjectural structural claims.

---

## 1. Standing objects

We work in the normalized witness-state space \(X\) with:

- legal one-edit move relation \(\to\),
- normalized action distance \(d_A\),
- exact frame-2 set \(F_2^{\mathrm{exact}}\),
- frame-2 seam
  \[
  \Sigma_2=\{c\in X : d_A(c,F_2^{\mathrm{exact}})=1\},
  \]
- distinguished locked witness set
  \[
  L=\{
  (o4,s0,t0,s2,t4,s4),
  (o4,s0,t0,s2,o4,s4),
  (o4,s0,t0,s2,s3,s4),
  (o4,s0,t0,s2,s0,s4)
  \},
  \]
- bounded escape-return regime \(B\), defined as the forward closure of \(L\) under legal one-edit moves subject to the cutoff
  \[
  d_A(\,\cdot\,,F_2^{\mathrm{exact}})\le 3.
  \]

We write
\[
\pi_4 : X \to \mathcal A
\]
for the slot-4 projection.

---

## 2. Baseline and repair propositions

### Proposition 2.1. Baseline contraction without closure
Under the baseline two-step policy on the sampled run, the witness machine is monotone in normalized action distance but produces no nontrivial exact closure.

### Proposition 2.2. Exact-preference repair of the dominant chamber
After exact-preference repair, the dominant reachable frame-0 chamber is recovered.

### Interpretation
Proposition 2.2 shows that a substantial part of the original baseline failure was due to policy selection rather than deep global obstruction.

---

## 3. Residual localization propositions

### Proposition 3.1. Residual funnel to the frame-2 seam
After exact-preference repair, the residual basin funnels into the frame-2 near-action seam.

### Proposition 3.2. One-slot localization of the residual mismatch
For the distinguished locked frame-2-nearest witnesses, the residual mismatch is localized at slot 4.

### Proposition 3.3. Exact frame-2 slot-4 necessity
If
\[
c\in F_2^{\mathrm{exact}},
\]
then
\[
\pi_4(c)=t2.
\]

### Interpretation
The post-repair obstruction is therefore localized: exact frame-2 closure is blocked by failure to install the required slot-4 value.

---

## 4. Locked witness propositions

### Proposition 4.1. Locked frame-2 witness set
The distinguished locked witness set is
\[
L=\{
(o4,s0,t0,s2,t4,s4),
(o4,s0,t0,s2,o4,s4),
(o4,s0,t0,s2,s3,s4),
(o4,s0,t0,s2,s0,s4)
\}.
\]

Each state in \(L\) satisfies:
1. \(d_A(c,F_2^{\mathrm{exact}})=1\),
2. the residual mismatch is at slot 4,
3. there is no exact one-edit child.

### Proposition 4.2. One-edit seam branching count
Each locked witness has exactly 7 one-edit children that remain at frame-2 action distance \(1\).

### Interpretation
These witnesses are not dead ends in the ordinary sense; they are locally mobile within the seam, but not directly repairable.

---

## 5. Bounded regime propositions

### Proposition 5.1. Bounded saturation
The bounded escape-return regime \(B\) saturates computationally by depth 6.

### Proposition 5.2. No new states after saturation
No new states appear at depths 7 or 8.

### Proposition 5.3. Bounded regime size
The total number of visited states in \(B\) is
\[
|B|=58{,}624.
\]

### Interpretation
The bounded regime is therefore computationally complete with respect to the stated generating set and cutoff.

---

## 6. Bounded exclusion propositions

### Proposition 6.1. No exact frame-2 closure in \(B\)
No state in the bounded regime \(B\) lies in the exact frame-2 set:
\[
B\cap F_2^{\mathrm{exact}}=\varnothing.
\]

### Proposition 6.2. Global slot-4 exclusion in \(B\)
For every state \(c\in B\),
\[
\pi_4(c)\neq t2.
\]

### Corollary 6.3. Bounded no-closure corollary
Because exact frame-2 closure requires \(\pi_4(c)=t2\), Proposition 6.2 implies Proposition 6.1.

### Interpretation
The bounded obstruction is stronger than a bare no-closure result: the exact installation value itself is excluded.

---

## 7. Slot-4 alphabet propositions

### Proposition 7.1. Global bounded slot-4 alphabet
The observed slot-4 alphabet in the full bounded regime is
\[
\pi_4(B)=\{o0,o1,o2,o3,o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Proposition 7.2. Seam slot-4 alphabet
The observed slot-4 alphabet on the frame-2 seam inside the bounded regime is
\[
\pi_4(B\cap\Sigma_2)=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Corollary 7.3. Seam exclusion of \(t2\)
The value \(t2\) does not occur at slot 4 on the frame-2 seam inside the bounded regime.

### Interpretation
The seam alphabet is a proper subset of the global bounded slot-4 alphabet and excludes the exact installation value \(t2\).

---

## 8. The main bounded theorem statement

### Theorem 8.1. Computational bounded slot-4 exclusion theorem
Let \(B\) be the bounded escape-return regime generated from the locked frame-2 witnesses under legal one-edit moves subject to the cutoff \(d_A \le 3\). Then:

1. \(B\) saturates by depth 6,
2. \(|B|=58{,}624\),
3. no state in \(B\) lies in \(F_2^{\mathrm{exact}}\),
4. no state in \(B\) has slot-4 value \(t2\).

### Proof status
Established computationally.

---

## 9. Structural conjectures

### Conjecture 9.1. Seam alphabet closure
The set
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}
\]
is closed under the projected slot-4 transport law induced by bounded legal one-edits and normalization.

### Conjecture 9.2. Minimal closed transport alphabet
The seam slot-4 alphabet is the minimal closed slot-4 transport set generated by the locked-seed values
\[
\{t4,o4,s3,s0\}.
\]

### Conjecture 9.3. Structural bounded slot-4 exclusion law
For every \(c\in B\),
\[
\pi_4(c)\neq t2
\]
for structural reasons derivable from the move grammar, normalization law, and induced slot-4 transport.

### Conjecture 9.4. Defect-transport interpretation
The residual slot-4 mismatch defines a localized defect that bounded legal one-edits transport but do not annihilate.

---

## 10. Summary statement

The current result can be summarized as follows.

After exact-preference repair resolves the dominant chamber-level failure, the residual obstruction localizes to slot 4 on the frame-2 seam. The bounded escape-return regime generated from the locked seam witnesses saturates completely, yet the exact slot value required for frame-2 closure never appears. This supports a bounded slot-4 exclusion law as the central theorem target of the present program.
