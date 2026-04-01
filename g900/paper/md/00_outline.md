# Paper Outline: G900 Witness-Machine Frame-2 Obstruction

## Status
Working outline

## Provisional title
Bounded Slot-4 Exclusion at the Frame-2 Seam in the G900 Witness Machine

## Alternative titles
- Seam Without Sealing: A Bounded Obstruction Law in the G900 Witness Machine
- Contraction Without Closure, Repair Without Installation
- A One-Slot Exclusion Law at the Frame-2 Seam

---

## 1. Core thesis

After exact-preference repair removes the dominant policy-selection failure, the remaining obstruction in the G900 witness machine localizes to a one-slot frame-2 seam defect.

Within the bounded escape-return regime generated from the distinguished locked witnesses, the exact slot-4 value \(t2\) required for frame-2 closure never appears.

This supports a bounded slot-4 exclusion law and a bounded no-closure corollary.

---

## 2. Narrative arc

### Phase I. Baseline failure
- The baseline two-step policy is monotone in normalized action distance.
- It contracts toward exactness but does not achieve nontrivial exact closure.
- Slogan: contraction without closure.

### Phase II. Policy repair
- Exact-preference repair recovers the dominant reachable frame-0 chamber.
- This shows that a major part of the earlier failure was due to policy choice, not deep obstruction.

### Phase III. Residual localization
- After repair, the residual basin funnels into the frame-2 seam.
- The remaining mismatch localizes to slot 4.
- Exact frame-2 closure requires slot 4 = \(t2\).

### Phase IV. Bounded obstruction
- The bounded escape-return regime generated from the locked frame-2 witnesses saturates by depth 6.
- No exact frame-2 state appears.
- No state in the bounded regime has slot 4 = \(t2\).

### Phase V. Structural program
- The key open task is to prove that the bounded seam dynamics are confined to a proper slot-4 transport alphabet excluding \(t2\).
- Candidate explanations: projected transport closure, affine residue law, normalization orbit restriction, defect transport.

---

## 3. Main theorem ladder

### Definition layer
- normalized state space \(X\)
- one-edit move relation \(\to\)
- action distance \(d_A\)
- exact frame-2 set \(F_2^{\mathrm{exact}}\)
- seam \(\Sigma_2\)
- locked witness set \(L\)
- bounded regime \(B\)
- slot projection \(\pi_4\)

### Proposition layer
- baseline contraction without closure
- exact-preference repair of dominant chamber
- residual funnel into frame-2 seam
- bounded saturation by depth 6
- no exact frame-2 closure in \(B\)
- no slot-4 value \(t2\) in \(B\)

### Conjectural / proof-program layer
- seam alphabet closure
- bounded slot-4 exclusion law
- defect-transport interpretation
- possible affine residue or orbit obstruction

---

## 4. Proposed section order

### Section 1. Introduction
State the problem and the main bounded result.
Emphasize that exact-preference repair sharpens the obstruction rather than eliminating it.

### Section 2. Formal objects
Define the normalized witness machine, exact frame-2 set, seam, locked witnesses, bounded regime, and slot projection.

### Section 3. Computational ladder
Present:
- baseline contraction without closure,
- exact-preference repair,
- localization to the frame-2 seam,
- locked witness subset,
- bounded saturation.

### Section 4. Bounded slot-4 exclusion
State the computational bounded obstruction theorem and the slot-4 exclusion result.

### Section 5. Structural proof program
Present the projected slot-4 transport relation and candidate lemmas.
Frame the seam alphabet as a candidate closed transport subalphabet.

### Section 6. Candidate invariant explanations
Discuss:
- parity-like laws,
- affine residue laws,
- normalization-orbit restrictions,
- defect-transport formulation.

### Section 7. Objections, scope, and limits
Make clear:
- bounded versus global,
- dependence on normalization,
- computational theorem versus structural conjecture.

### Section 8. Open problems
List the next theorem targets and possible generalizations.

---

## 5. Main statements to feature early

### Statement A. Computational bounded obstruction
The bounded escape-return regime generated from the locked frame-2 witnesses saturates by depth 6 and contains no exact frame-2 state.

### Statement B. Slot-4 exclusion
Within that same bounded regime, the slot-4 value \(t2\) never appears.

### Statement C. No-closure corollary
Because exact frame-2 closure requires slot 4 = \(t2\), bounded slot-4 exclusion implies bounded no exact frame-2 closure.

---

## 6. Best slogans currently available

- contraction without closure
- seam without sealing
- local repair, residual obstruction
- one-slot exclusion after chamber repair
- the machine finds the seam without sealing it

Use sparingly. The paper should remain mathematically dry overall.

---

## 7. What the paper should not claim yet

Do not claim:
- global impossibility of exact frame-2 closure,
- a proved invariant unless one is actually derived,
- normalization-independence,
- universality beyond the bounded regime generated from the locked witnesses.

---

## 8. Current file map

- `01_formal_objects.md`
- `02_computational_results.md`
- `03_bounded_exclusion_theorem.md`
- `04_candidate_invariants.md`
- `05_referee_objections.md`
- `06_open_problems.md`

---

## 9. Immediate next writing task

The next strongest writing move is to draft a compact `07_introduction.md` that states:

1. the baseline problem,
2. the effect of exact-preference repair,
3. the localized frame-2 seam obstruction,
4. the bounded slot-4 exclusion result,
5. the structural proof program.

That file will force the paper to sound like a theorem paper rather than a lab notebook.
