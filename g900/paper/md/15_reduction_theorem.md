# Reduction Theorem for Bounded Slot-4 Exclusion

## Status
Working proof draft

## Purpose
Prove that the bounded slot-4 exclusion theorem reduces to a one-step closure statement for the slot-4 projection under bounded legal one-edit moves.

---

## 1. Setup

Let:

- \(X\) be the normalized witness-state space,
- \(\to\) the legal one-edit move relation after normalization,
- \(d_A\) the normalized action distance,
- \(F_2^{\mathrm{exact}}\subseteq X\) the exact frame-2 set,
- \(L\subseteq X\) the distinguished locked witness set,
- \(B\subseteq X\) the bounded escape-return regime generated from \(L\) under legal one-edit moves with cutoff
  \[
  d_A(\,\cdot\,,F_2^{\mathrm{exact}})\le 3,
  \]
- \(\pi_4:X\to\mathcal A\) the slot-4 projection.

Define the locked slot-4 seed set
\[
A_{\mathrm{seed}}:=\{\pi_4(\ell):\ell\in L\}.
\]

In the present program,
\[
A_{\mathrm{seed}}=\{t4,o4,s3,s0\}.
\]

Define the candidate seam alphabet
\[
A_{\mathrm{seam}}:=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

Note that
\[
A_{\mathrm{seed}}\subseteq A_{\mathrm{seam}}.
\]

---

## 2. Projected transport relation

Define the projected slot-4 transport relation
\[
\rightsquigarrow_4 \subseteq \mathcal A\times\mathcal A
\]
by
\[
a\rightsquigarrow_4 b
\]
if and only if there exist states \(c,c'\in B\) such that

- \(c\to c'\),
- \(\pi_4(c)=a\),
- \(\pi_4(c')=b\).

This is the slot-4 shadow of the bounded one-edit dynamics.

---

## 3. Main reduction theorem

### Theorem 3.1. Reduction of bounded exclusion to one-step slot-4 closure
Assume the following two hypotheses.

#### (H1) Seed inclusion
For every locked witness \(\ell\in L\),
\[
\pi_4(\ell)\in A_{\mathrm{seam}}.
\]

#### (H2) One-step slot-4 closure
For every bounded legal one-edit move \(c\to c'\), if
\[
\pi_4(c)\in A_{\mathrm{seam}},
\]
then
\[
\pi_4(c')\in A_{\mathrm{seam}}.
\]

Then for every state \(c\in B\),
\[
\pi_4(c)\in A_{\mathrm{seam}}.
\]

### Proof
By definition, \(B\) is the smallest set containing \(L\) and closed under bounded legal one-edit moves.

Therefore every \(c\in B\) lies on some finite bounded legal path
\[
c_0\to c_1\to\cdots\to c_n,
\]
where
- \(c_0\in L\),
- \(c_n=c\),
- each step \(c_i\to c_{i+1}\) is a legal one-edit move,
- each intermediate state lies in the bounded regime allowed by the cutoff.

We prove by induction on \(n\) that
\[
\pi_4(c_n)\in A_{\mathrm{seam}}.
\]

#### Base case
If \(n=0\), then \(c=c_0\in L\). By (H1),
\[
\pi_4(c)\in A_{\mathrm{seam}}.
\]

#### Inductive step
Assume
\[
\pi_4(c_n)\in A_{\mathrm{seam}}.
\]
Since \(c_n\to c_{n+1}\) is a bounded legal one-edit move, hypothesis (H2) yields
\[
\pi_4(c_{n+1})\in A_{\mathrm{seam}}.
\]

Thus the statement holds for all \(n\), and hence for all \(c\in B\). ∎

---

## 4. Exclusion corollary

### Corollary 4.1. Bounded slot-4 exclusion from seam closure
Assume the hypotheses of Theorem 3.1. Since
\[
t2\notin A_{\mathrm{seam}},
\]
it follows that for every \(c\in B\),
\[
\pi_4(c)\neq t2.
\]

### Proof
By Theorem 3.1, every state \(c\in B\) satisfies
\[
\pi_4(c)\in A_{\mathrm{seam}}.
\]
Because \(t2\notin A_{\mathrm{seam}}\), the conclusion follows immediately. ∎

---

## 5. No-closure corollary

### Corollary 5.1. Bounded no exact frame-2 closure
Assume in addition the exactness necessity principle:
\[
c\in F_2^{\mathrm{exact}} \implies \pi_4(c)=t2.
\]

Then, under the hypotheses of Theorem 3.1,
\[
B\cap F_2^{\mathrm{exact}}=\varnothing.
\]

### Proof
Suppose for contradiction that some \(c\in B\cap F_2^{\mathrm{exact}}\). By exactness necessity,
\[
\pi_4(c)=t2.
\]
But Corollary 4.1 says that no state in \(B\) has slot-4 value \(t2\). Contradiction. Therefore
\[
B\cap F_2^{\mathrm{exact}}=\varnothing.
\]
∎

---

## 6. Finite-template refinement

Theorem 3.1 shows that the whole bounded exclusion theorem reduces to proving the one-step closure hypothesis (H2).

That hypothesis can be reduced further if the slot-4-affecting bounded legal one-edit moves admit a finite template classification.

### Theorem 6.1. Finite-template reduction
Assume:

1. every bounded legal one-edit move that can affect slot 4 after normalization belongs to one of finitely many slot-4 effect templates
   \[
   T_1,\dots,T_m,
   \]
2. every bounded legal one-edit move not represented by those templates leaves \(\pi_4\) unchanged,
3. each template \(T_i\) maps input values in \(A_{\mathrm{seam}}\) to output values in \(A_{\mathrm{seam}}\).

Then the one-step closure hypothesis (H2) holds, hence Theorem 3.1 and Corollaries 4.1 and 5.1 hold.

### Proof
Take any bounded legal one-edit move \(c\to c'\) with
\[
\pi_4(c)\in A_{\mathrm{seam}}.
\]

If the move does not affect slot 4 except trivially, then by assumption (2),
\[
\pi_4(c')=\pi_4(c)\in A_{\mathrm{seam}}.
\]

If the move does affect slot 4 after normalization, then it is represented by some template \(T_i\). By assumption (3), the output slot-4 value still lies in \(A_{\mathrm{seam}}\).

Thus every bounded legal one-edit move preserves \(A_{\mathrm{seam}}\) at slot 4, so (H2) holds. The rest follows from Theorem 3.1 and its corollaries. ∎

---

## 7. Interpretation

The main significance of the reduction theorem is that it collapses the bounded exclusion problem from a large state-space question to a local transport question.

Instead of proving directly that no state in a 58,624-state bounded regime has slot-4 value \(t2\), it is enough to prove the following:

1. the locked seeds begin inside the seam alphabet,
2. every bounded legal one-edit move preserves that alphabet at slot 4.

So the real proof burden is local, not global.

---

## 8. The actual remaining lemma

The decisive missing ingredient is now clear.

### Local closure lemma
For every bounded legal one-edit move \(c\to c'\), if
\[
\pi_4(c)\in\{o4,s0,s2,s3,s4,t0,t3,t4\},
\]
then
\[
\pi_4(c')\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

Once this lemma is proved from the move grammar and normalization law, the bounded slot-4 exclusion theorem follows immediately.

---

## 9. Immediate next task

The next theorem-facing task is therefore not further global search.

It is to classify the bounded legal one-edit templates that can affect slot 4 after normalization and verify that each such template preserves the seam alphabet.

That is now the entire structural bottleneck.
