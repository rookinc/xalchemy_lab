# Candidate Invariants for the Bounded Slot-4 Exclusion Program

## Status
Working scratch file

## Purpose
Record the most promising structural mechanisms that could explain why the bounded frame-2 regime never produces slot-4 value \(t2\).

This file is exploratory but theorem-facing. It should distinguish weak observations from candidate invariant laws.

---

## 1. Problem statement

The bounded regime \(B\), generated from the locked frame-2 witnesses under legal one-edit moves with action-distance cutoff \(d_A \le 3\), satisfies:

- no state in \(B\) lies in \(F_2^{\mathrm{exact}}\),
- no state in \(B\) satisfies \(\pi_4(c)=t2\),
- the seam slot-4 alphabet is
  \[
  \{o4,s0,s2,s3,s4,t0,t3,t4\}.
  \]

The goal is to explain this structurally.

---

## 2. Desired shape of explanation

The strongest kind of explanation would be:

1. define a quantity or defect type preserved by bounded legal one-edits,
2. show the locked witnesses all share that quantity or defect type,
3. show any state with \(\pi_4=t2\) has a different value or defect status,
4. conclude that \(t2\) cannot occur in \(B\).

This could take one of several forms:
- parity-like law,
- affine residue law,
- orbit/normalization obstruction,
- local defect transport law.

---

## 3. Candidate A: parity-like law

### Idea
There may exist a \(\mathbb{Z}/2\)-valued invariant preserved by legal one-edits and normalization in the bounded regime.

Possible sources of parity:
- parity of slot indices,
- parity of family changes,
- parity of total transport count,
- parity of normalization shifts,
- parity of defect orientation.

### Current assessment
A naive even/odd index parity appears too weak, because the observed seam alphabet contains both even and odd subscripts:
- even: \(o4,s0,s2,s4,t0,t4\),
- odd: \(s3,t3\).

So if a parity law exists, it must combine family and index, or include normalization data.

### Working conclusion
Ordinary index parity alone is not the explanation, but a more refined parity law remains possible.

---

## 4. Candidate B: affine residue law modulo 5

### Idea
Because the machine uses indexed symbol families and normalization appears cyclic, there may exist a conserved affine residue modulo 5.

A model form would be
\[
R(c) \equiv \sum_{j=0}^{5} \alpha_j \,\mathrm{ind}(x_j) + \beta_j \,\mathrm{fam}(x_j) \pmod 5,
\]
where:
- \(\mathrm{ind}(x_j)\) is the numeric subscript,
- \(\mathrm{fam}(x_j)\) encodes whether \(x_j\) is of type \(o,s,t\).

### Desired theorem use
If:
- \(R\) is preserved by bounded legal one-edits,
- all locked witnesses share the same \(R\)-value,
- any state with \(\pi_4=t2\) on the relevant seam has a different \(R\)-value,

then slot-4 exclusion follows.

### Why this is promising
The obstruction seems too structured to be accidental. The singled-out exclusion of \(t2\) suggests not random absence, but a residue-class obstruction or orbit-coset omission.

### Working conclusion
This is one of the most promising invariant candidates.

---

## 5. Candidate C: normalization-orbit exclusion

### Idea
A raw edit may appear locally to create or approach \(t2\), but after normalization the resulting representative is reindexed to another seam value, or else leaves the bounded regime.

Thus \(t2\) may be excluded not because it is impossible pre-normalization, but because it is not represented in the normalized bounded orbit generated from the locked witnesses.

### Model statement
There exists a normalization group or quotient action such that:
- the bounded regime stays inside a proper orbit family,
- \(t2\) belongs to a different representative class or orbit slice,
- bounded legal edits never cross between these classes.

### Why this is plausible
The normalized machine already privileges a repaired frame and a distinguished slot. It is natural that some formally possible local values are absent after quotienting.

### Working conclusion
This explanation could coexist with the affine residue interpretation.

---

## 6. Candidate D: defect-transport law

### Idea
The residual mismatch at slot 4 is not merely a wrong symbol. It is a localized defect of a specific installation type.

Bounded legal one-edits can:
- move the defect,
- re-present the defect,
- circulate the defect among seam-compatible values,

but cannot annihilate the defect.

Under this view:
- the observed seam alphabet is the orbit of visible defect presentations,
- \(t2\) is excluded because it corresponds to exact installation, i.e. absence of the defect.

### Why this matches the evidence
This interpretation fits the current slogan:
the machine finds the seam without sealing it.

It also fits the observation that exact-preference repair fixes chamber-level failure first, leaving a sharply localized residual defect.

### Working conclusion
This is probably the best conceptual explanation, even if the eventual proof is implemented via a projected transport relation.

---

## 7. Candidate E: grammar-induced slot-4 admissibility restriction

### Idea
The one-edit grammar may impose a direct admissibility restriction on slot 4 near the frame-2 seam.

A possible theorem form is:

For every \(c \in B \cap \Sigma_2\),
\[
\pi_4(c)\in\{o4,s0,s2,s3,s4,t0,t3,t4\},
\]
and \(t2\) is not grammatically admissible there.

### Strength
If true, this is a very strong local theorem:
it explains the seam alphabet directly from legal edit templates and normalization, without needing a more abstract invariant.

### Weakness
It may be less conceptually satisfying than a true conserved quantity, unless tied to a deeper transport law.

### Working conclusion
This is the best route for a first proof, even if a deeper invariant is later found.

---

## 8. Relation between the candidate mechanisms

These candidate explanations are not mutually exclusive.

A plausible hierarchy is:

1. the move grammar induces a projected slot-4 transport law;
2. that transport law closes on the observed seam alphabet;
3. the closure is explained by a normalization orbit or affine residue law;
4. conceptually, the whole phenomenon is a localized defect-transport obstruction.

So the immediate proof may be combinatorial, while the deeper explanation may be invariant-theoretic.

---

## 9. Immediate theorem-facing tasks

### Task 9.1. Projected slot-4 transport extraction
Derive the induced transition relation on slot-4 symbols from legal one-edits and normalization.

### Task 9.2. Seam alphabet closure proof
Show that the seam alphabet
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}
\]
is closed under the projected transport law in the bounded regime.

### Task 9.3. Nonproduction of \(t2\)
Show that \(t2\) is not in the image of any legal bounded slot-4 transport from the observed seam alphabet.

### Task 9.4. Test affine residue candidates
Attempt to fit a conserved residue mod 5 or related cyclic law to the observed slot-4 transitions.

### Task 9.5. Separate bounded theorem from global conjecture
Keep bounded exclusion as the theorem target and treat any global obstruction statement as conjectural until proved.

---

## 10. Present working judgment

At present, the most promising route is:

- first prove a projected slot-4 transport closure theorem from the move grammar,
- then search for the deeper reason that this closure excludes \(t2\).

So:

### Working judgment
The first proof should likely be combinatorial and grammar-based.
The deeper explanation will likely be orbit-theoretic, affine-residue-based, or defect-transport-based.
