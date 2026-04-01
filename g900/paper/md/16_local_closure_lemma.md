# Local Closure Lemma for Slot-4 Seam Transport

## Status
Working proof target

## Purpose
State the exact local lemma whose proof would complete the structural bounded slot-4 exclusion theorem, and organize that proof into a finite template program.

---

## 1. Position in the theorem ladder

The reduction theorem shows that the bounded slot-4 exclusion law follows once we prove a one-step closure property for slot 4 under bounded legal one-edit moves.

Thus the remaining structural bottleneck is local.

The purpose of this note is to isolate that bottleneck as a precise lemma and to organize the finite checks needed for its proof.

---

## 2. Standing notation

Let:

- \(X\) be the normalized witness-state space,
- \(\to\) be the legal one-edit move relation after normalization,
- \(F_2^{\mathrm{exact}}\subseteq X\) be the exact frame-2 set,
- \(d_A\) be normalized action distance,
- \(B\subseteq X\) be the bounded escape-return regime generated from the locked set \(L\) under the cutoff
  \[
  d_A(\,\cdot\,,F_2^{\mathrm{exact}})\le 3,
  \]
- \(\Sigma_2=\{c\in X:d_A(c,F_2^{\mathrm{exact}})=1\}\) be the frame-2 seam,
- \(\pi_4:X\to\mathcal A\) be the slot-4 projection.

Define the seam slot-4 alphabet
\[
A_{\mathrm{seam}}:=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

This is the observed slot-4 alphabet on \(B\cap\Sigma_2\).

---

## 3. Main local lemma

### Lemma 3.1. Local slot-4 closure lemma
For every bounded legal one-edit move
\[
c\to c',
\]
if
\[
\pi_4(c)\in A_{\mathrm{seam}},
\]
then
\[
\pi_4(c')\in A_{\mathrm{seam}}.
\]

Equivalently,
\[
\pi_4(c)\in\{o4,s0,s2,s3,s4,t0,t3,t4\}
\quad\Longrightarrow\quad
\pi_4(c')\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

---

## 4. Immediate consequence

By the reduction theorem already established, Lemma 3.1 implies:

### Corollary 4.1. Structural bounded slot-4 exclusion
For every \(c\in B\),
\[
\pi_4(c)\neq t2.
\]

### Corollary 4.2. Structural bounded no-closure law
If exact frame-2 closure requires \(\pi_4=t2\), then
\[
B\cap F_2^{\mathrm{exact}}=\varnothing.
\]

So Lemma 3.1 is the exact missing bridge from the reduction theorem to the full bounded structural exclusion theorem.

---

## 5. Why this lemma is plausible

The computation strongly suggests that bounded slot-4 motion is not arbitrary.

Inside the seam region, the observed slot-4 alphabet is already sharply restricted:
\[
A_{\mathrm{seam}}=\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

The missing value \(t2\) is not an arbitrary omission. It is the exact installation value required for frame-2 closure.

So the local hypothesis suggested by the data is:

- bounded legal one-edits can move slot 4,
- but only inside a proper seam-compatible transport class,
- and that class excludes the exact closure value.

Lemma 3.1 is the formal statement of this idea.

---

## 6. Template-based proof strategy

The natural proof strategy is to classify all bounded legal one-edit moves according to their effect on slot 4 after normalization.

That suggests the following program.

### Step 6.1. Identify slot-4-relevant moves
Determine which one-edit moves can affect the normalized slot-4 value at all.

### Step 6.2. Collapse into local templates
Show that every slot-4-relevant one-edit move belongs to one of finitely many local template classes, modulo normalization.

### Step 6.3. Check template outputs
For each template, compute the allowed output slot-4 values when the input lies in \(A_{\mathrm{seam}}\).

### Step 6.4. Verify closure
Show that every such output still lies in \(A_{\mathrm{seam}}\).

Once these checks are complete, Lemma 3.1 follows.

---

## 7. Expected move classes

At a minimum, the local proof should distinguish the following classes.

### Type I. Direct slot-4 edits
Moves that directly alter the local content that normalizes to slot 4.

These are the most obvious candidates for changing \(\pi_4\).

### Type II. Adjacent-frame edits
Moves that do not directly replace slot 4 but alter nearby structure so that normalization changes the slot-4 representative.

These are the most likely source of hidden slot-4 motion.

### Type III. Remote edits
Moves outside the slot-4 local frame.

These should either:
- leave \(\pi_4\) unchanged, or
- reduce after normalization to one of the already identified local effects.

A convincing proof must show that Type III does not create new slot-4 behavior outside the local template list.

---

## 8. Lemma decomposition

To prove Lemma 3.1 cleanly, it is helpful to split it into sublemmas.

### Lemma 8.1. Remote-edit inertness
If a bounded legal one-edit move is remote from the slot-4 local frame, then
\[
\pi_4(c')=\pi_4(c).
\]

Or, if exact equality is too strong, then at least:
\[
\pi_4(c')\in A_{\mathrm{seam}}
\quad\text{whenever}\quad
\pi_4(c)\in A_{\mathrm{seam}}.
\]

### Lemma 8.2. Local-template completeness
Every bounded legal one-edit move that can alter \(\pi_4\) belongs to one of finitely many local template classes, modulo normalization.

### Lemma 8.3. Template closure
Each local template maps input slot-4 values in \(A_{\mathrm{seam}}\) to output slot-4 values in \(A_{\mathrm{seam}}\).

Taken together, Lemmas 8.1 through 8.3 imply Lemma 3.1.

---

## 9. Stronger version

A slightly stronger statement than Lemma 3.1 may be more natural once the templates are explicit.

### Lemma 9.1. Local nonproduction of \(t2\)
For every bounded legal one-edit move \(c\to c'\), if
\[
\pi_4(c)\in A_{\mathrm{seam}},
\]
then
\[
\pi_4(c')\neq t2.
\]

This is weaker than full closure if one allows outputs outside \(A_{\mathrm{seam}}\) but still not equal to \(t2\). However, the observed alphabet suggests full closure is the more natural and more informative statement.

So the recommended goal remains Lemma 3.1 rather than only Lemma 9.1.

---

## 10. Candidate proof mechanisms

The proof of Lemma 3.1 may ultimately rest on one of several mechanisms.

### Mechanism A. Direct grammar restriction
The move grammar may simply forbid transitions from \(A_{\mathrm{seam}}\) to slot-4 values outside \(A_{\mathrm{seam}}\) in the bounded seam-local setting.

### Mechanism B. Normalization-orbit closure
The local grammar may allow raw moves that appear broader, but after normalization the slot-4 representative always lands back in \(A_{\mathrm{seam}}\).

### Mechanism C. Residue-class obstruction
A conserved residue, likely mod 5 or a related cyclic law, may force the slot-4 value to remain inside a proper subset of the ambient alphabet.

### Mechanism D. Defect transport
The slot-4 mismatch may be a localized defect whose visible presentations are exactly the values in \(A_{\mathrm{seam}}\). Bounded legal one-edits would then move the defect among those presentations without resolving it.

At present, the first proof should aim for closure directly from templates. Any deeper explanation can be layered on afterward.

---

## 11. What must be written next

The next proof-facing document should explicitly list the slot-4-relevant local templates.

That file should include, for each template:

1. a short name,
2. a verbal description,
3. which local part of the state it acts on,
4. how normalization affects the result,
5. the resulting slot-4 output possibilities,
6. whether the output stays in \(A_{\mathrm{seam}}\).

Without that explicit template sheet, Lemma 3.1 remains plausible but unproved.

---

## 12. Suggested next-file title

The next natural file is:

`17_slot4_templates.md`

Its purpose should be to enumerate the slot-4-affecting bounded one-edit templates and discharge Lemma 3.1 by finite case analysis.

---

## 13. Closing summary

The theorem program is now sharply focused.

The bounded structural exclusion theorem no longer depends on a large global search argument. It depends on one local claim:

> bounded legal one-edit moves preserve the seam slot-4 alphabet.

Once that local closure lemma is proved, bounded slot-4 exclusion and bounded no exact frame-2 closure follow immediately.
