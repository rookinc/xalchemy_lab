# Bounded Slot-4 Exclusion at the Frame-2 Seam

## Status
Working theorem note

## Purpose
Organize the bounded frame-2 obstruction result in theorem form using the actual retained substitution dynamics implemented in the G900 slot-4 scripts.

---

## 1. Goal

The main target is to state the bounded slot-4 exclusion law in the correct engine language.

The operative dynamics are not an abstract hidden local rewrite system. They are:

1. single-symbol substitutions from a fixed vocabulary,
2. dihedral normalization,
3. classification against subjective/objective/action-cell families,
4. retention by bounded action-distance and exact frame-2 filters.

Within that retained bounded regime, the exact slot value \(t2\) never appears at normalized slot 4.

---

## 2. Definitions in force

We work with the following objects:

- \(X\): normalized witness-state space,
- \(F_2^{\mathrm{exact}}\): exact frame-2 set,
- \(\Sigma_2\): frame-2 seam,
  \[
  \Sigma_2=\{c\in X : d_A(c,F_2^{\mathrm{exact}})=1\},
  \]
- \(L\): distinguished locked witness subset,
- \(B\): bounded retained substitution regime generated from \(L\),
- \(\pi_4\): normalized slot-4 projection.

The raw one-edit grammar is single-symbol substitution from the fixed vocabulary
\[
V=\{o0,o1,o2,o3,o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

Retention keeps children that are either exact frame 2 or satisfy best action distance \(\le 3\).

---

## 3. Computationally established facts

The following facts are established.

### Fact 3.1. Exact-preference repair
Exact-preference repair recovers the dominant reachable frame-0 chamber.

### Fact 3.2. Residual funnel
After exact-preference repair, the residual basin funnels into the frame-2 near-action seam.

### Fact 3.3. Locked one-slot defect
The distinguished locked frame-2 witnesses all lie at normalized action distance one from exact frame 2, with a single residual mismatch at slot 4.

### Fact 3.4. Bounded saturation
The bounded regime saturates computationally by depth 6, with no new states at depths 7 and 8.

### Fact 3.5. Bounded size
The total number of visited states in the bounded regime is
\[
58{,}624.
\]

### Fact 3.6. No exact frame-2 closure in the bounded regime
No state in the bounded regime belongs to \(F_2^{\mathrm{exact}}\).

### Fact 3.7. Retained slot-4 closure alphabet
The retained bounded slot-4 alphabet is
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Fact 3.8. Retained seam slot-4 alphabet
The retained frame-2 \(d_A=1\) slot-4 alphabet is also
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

### Fact 3.9. Global slot-4 exclusion
No retained bounded state has normalized slot-4 value \(t2\).

---

## 4. Main bounded theorem

### Theorem 4.1. Bounded slot-4 exclusion theorem
Let \(B\) be the bounded retained substitution regime generated from the locked frame-2 witnesses under single-symbol substitutions from the fixed vocabulary, dihedral normalization, and retention by the bounded action-distance filter. Then every retained state \(c\in B\) satisfies
\[
\pi_4(c)\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]
In particular,
\[
\pi_4(c)\neq t2.
\]

### Proof status
Established by extracted finite retained-substitution closure table together with the bounded retained slot-4 alphabet summary.

---

## 5. No-closure corollary

### Corollary 5.1. Bounded no exact frame-2 closure
If exact frame-2 closure requires \(\pi_4(c)=t2\), then no retained bounded state is exact frame 2:
\[
B\cap F_2^{\mathrm{exact}}=\varnothing.
\]

---

## 6. What remains conjectural

What remains conjectural is not the bounded exclusion itself, but its deeper explanation.

Candidate deeper explanations include:

1. affine residue obstruction,
2. normalization-orbit restriction,
3. localized defect transport.

So the theorem is now established at the finite retained-substitution level, while the invariant explanation remains open.
