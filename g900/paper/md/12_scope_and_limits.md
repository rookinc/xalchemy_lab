# Scope and Limits

## Status
Working draft

## Purpose
State precisely what the present paper claims, what it does not claim, and how the bounded frame-2 obstruction result depends on normalization and regime choice.

---

## 1. Scope of the present result

The central result of the present paper is a bounded result.

More precisely, the paper concerns the bounded escape-return regime \(B\) generated from the distinguished locked frame-2 witnesses under legal one-edit moves subject to the action-distance cutoff
\[
d_A(\,\cdot\,,F_2^{\mathrm{exact}})\le 3.
\]

Within this regime, the main computationally established claim is:

- no state in \(B\) lies in \(F_2^{\mathrm{exact}}\),
- no state in \(B\) has slot-4 value \(t2\).

This is the main theorem-shaped result currently available.

---

## 2. What is claimed

The paper claims the following.

### Claim 2.1. Baseline failure is not the whole story
The baseline two-step policy exhibits contraction without closure, but this does not by itself establish deep structural obstruction.

### Claim 2.2. Exact-preference repair sharpens the problem
Exact-preference repair recovers the dominant reachable chamber, so the remaining failure becomes more localized and more structurally meaningful.

### Claim 2.3. The residual obstruction localizes
After repair, the remaining basin funnels into the frame-2 seam and the residual mismatch localizes at slot 4.

### Claim 2.4. The bounded regime saturates
The bounded escape-return regime generated from the locked witnesses saturates computationally by depth 6.

### Claim 2.5. The exact slot-4 installation value is excluded in the bounded regime
Within that saturated bounded regime, the value \(t2\) never appears at slot 4.

These claims together support the bounded slot-4 exclusion theorem as the main current result.

---

## 3. What is not claimed

The paper does **not** currently claim the following.

### Non-claim 3.1. No global impossibility theorem
The paper does not prove that exact frame-2 closure is globally impossible in the full witness machine.

### Non-claim 3.2. No normalization-independent theorem
The paper does not prove that the obstruction persists independently of the normalization convention.

### Non-claim 3.3. No fully proved invariant yet
The paper does not yet prove a parity law, affine residue law, orbit theorem, or defect-preservation theorem explaining the exclusion of \(t2\).

### Non-claim 3.4. No universality beyond the chosen generating set
The paper does not claim that every frame-2-nearest witness exhibits the same bounded obstruction pattern as the distinguished locked set unless this is proved separately.

### Non-claim 3.5. No automatic extension beyond the stated cutoff
The paper does not yet prove that the cutoff \(d_A \le 3\) is the maximal or natural barrier for reaching \(t2\).

These omissions are deliberate and should remain explicit.

---

## 4. Dependence on normalization

The present paper is about the **normalized** witness machine.

All central objects are defined after normalization:
- the state space \(X\),
- the one-edit relation \(\to\),
- the action distance \(d_A\),
- the exact frame-2 set \(F_2^{\mathrm{exact}}\),
- the seam \(\Sigma_2\),
- the slot projection \(\pi_4\).

Accordingly, the bounded slot-4 exclusion result is a theorem about normalized representatives and normalized dynamics.

This should not be treated as an embarrassment or caveat hidden in fine print. It is part of the theorem statement itself.

A separate future problem is to compare:
- pre-normalized accessibility,
- normalized accessibility,
- quotient effects introduced by normalization.

But that comparison lies outside the scope of the present paper.

---

## 5. Why the bounded theorem is still significant

A natural concern is that a bounded theorem may be too local to matter.

The reply is that the bounded result is significant for four reasons.

### Reason 5.1. The regime is saturated
This is not a partial sample inside the bounded regime. The regime closes computationally by depth 6, with no new states at depths 7 and 8.

### Reason 5.2. The obstruction is localized
The result is not a vague absence of closure somewhere in a large space. It is a one-slot exclusion phenomenon at the exact residual obstruction coordinate.

### Reason 5.3. The excluded value is structurally distinguished
The missing value \(t2\) is the exact slot-4 installation value required for frame-2 closure.

### Reason 5.4. The result emerged after policy repair
Because exact-preference repair removes a major contingent failure mode, the surviving bounded obstruction is more likely to reflect genuine witness-machine structure.

So the bounded theorem is local in scope, but sharp in content.

---

## 6. Computational propositions versus structural conjectures

The paper should maintain a strict separation between these two levels.

### Computational propositions
These are established by the bounded saturation study:
- regime size,
- saturation depth,
- locked witness properties,
- global and seam slot-4 alphabets,
- absence of exact frame-2 closure,
- absence of slot-4 value \(t2\).

### Structural conjectures
These are the currently unproved explanations:
- seam alphabet closure from the projected transport law,
- minimality of the seam alphabet,
- affine residue exclusion,
- normalization-orbit exclusion,
- defect transport without annihilation.

The paper is stronger when it keeps this distinction explicit.

---

## 7. Why slot 4 is singled out

Slot 4 is not privileged arbitrarily.

It becomes privileged because:
1. exact-preference repair resolves the dominant chamber-level failure,
2. the residual mismatch then localizes there,
3. exact frame-2 closure requires slot 4 = \(t2\).

Thus slot 4 is the canonical residual obstruction coordinate in the repaired normalized setting.

The paper should say this plainly, because otherwise the slot-4 emphasis can look ad hoc.

---

## 8. Why the bounded claim should come first

There is a temptation to reach immediately for stronger language:
- barrier theorem,
- no-go theorem,
- global obstruction,
- impossibility of exact frame-2 closure.

That temptation should be resisted.

The bounded theorem is already mathematically interesting:
- it is precise,
- it is saturated,
- it is localized,
- it singles out a distinguished missing value.

Moreover, a strong bounded theorem is the best foundation for any later global theorem. Overclaiming too early would weaken the paper.

---

## 9. Proper statement discipline

The present paper should follow the following discipline.

### Rule 9.1
State the bounded theorem as bounded.

### Rule 9.2
State normalization dependence explicitly.

### Rule 9.3
Treat projected-transport and invariant explanations as proof-program material unless proved.

### Rule 9.4
Treat global escape or barrier claims as conjectural.

### Rule 9.5
Use the bounded slot-4 exclusion law, not mere no-closure, as the main positive statement.

This discipline will make the paper look serious and controlled.

---

## 10. Best concise scope statement

A good compact scope statement for the paper is:

> We prove a bounded computational exclusion theorem for the normalized G900 witness machine: in the saturated escape-return regime generated from the locked frame-2 seam witnesses under one-edit moves with \(d_A\le 3\), the exact slot-4 installation value \(t2\) never appears. We do not yet claim a global impossibility theorem; instead, we formulate a structural proof program based on projected slot-4 transport.

This is probably the cleanest one-paragraph summary of scope and restraint.

---

## 11. Closing remark

The right ambition for the present paper is not maximal breadth.

It is maximal sharpness within the correct regime.

At this stage, the mathematically honest achievement is the conversion of a diffuse closure failure into a saturated, localized, bounded slot-4 exclusion law, together with a credible route toward structural proof.
