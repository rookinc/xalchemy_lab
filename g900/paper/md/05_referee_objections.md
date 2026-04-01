# Referee Objections and Replies

## Status
Working draft

## Purpose
Collect the most likely referee objections to the bounded frame-2 obstruction result and prepare precise replies.

---

## 1. Objection: this is only a bounded computational statement

### Objection
The argument only concerns a bounded escape-return regime with action-distance cutoff \(d_A \le 3\). Why should this be read as mathematically significant rather than merely local?

### Reply
The bounded nature of the claim should be stated explicitly and not overstated. The significance is that:

1. the bounded regime is not sampled loosely; it is saturated,
2. the residual obstruction localizes sharply after exact-preference repair,
3. the exclusion concerns the exact slot value required for frame-2 closure,
4. the proof program aims to derive the bounded exclusion structurally from the move grammar.

So the theorem claim is local but exact within its stated regime.

---

## 2. Objection: this may just be a search artifact

### Objection
The missing value \(t2\) may simply not have appeared in the explored region by chance.

### Reply
The bounded regime saturates computationally by depth 6, with no new states at depths 7 and 8. Thus the exclusion is complete within the stated bounded regime. The next step is not more brute-force search but structural explanation via projected transport and invariant analysis.

---

## 3. Objection: why is slot 4 privileged?

### Objection
The argument seems to single out slot 4 without justification.

### Reply
Slot 4 is not privileged arbitrarily. After exact-preference repair, the residual mismatch localizes there in the normalized frame-2 seam. Moreover, exact frame-2 closure requires slot 4 to take the value \(t2\). So slot 4 is the canonical residual obstruction coordinate in the repaired normalized setting.

---

## 4. Objection: no-closure is weaker than what you claim

### Objection
The absence of exact closure does not by itself justify a strong obstruction interpretation.

### Reply
Agreed. That is why the slot-4 exclusion law is the stronger target statement. It is not merely that exact closure fails; it is that the precise installation value required for closure never appears at the distinguished obstruction coordinate.

Thus the proposed theorem is stronger and more informative than a bare no-closure claim.

---

## 5. Objection: exact-preference repair may have changed the problem

### Objection
Perhaps the repaired policy defines a different dynamics, making the residual obstruction less meaningful.

### Reply
Exact-preference repair is introduced precisely to separate policy-selection failure from genuine residual obstruction. The result is not that the problem changed arbitrarily, but that one major contingent failure mode was removed. What remains is therefore more sharply attributable to the machine’s underlying seam dynamics.

---

## 6. Objection: why should the seam alphabet matter?

### Objection
The observed seam slot-4 alphabet may be an incidental finite list with no deeper meaning.

### Reply
The seam alphabet matters because:
- it is much smaller than the ambient slot-4 alphabet,
- it is observed after bounded saturation,
- it excludes the exact installation value \(t2\),
- it suggests a closed transport subalphabet.

The proof program is designed to test whether this list is a true grammar-induced closure set rather than an incidental observation.

---

## 7. Objection: the claim depends on normalization

### Objection
The entire obstruction may be an artifact of the normalization convention.

### Reply
The normalized setting must indeed be stated explicitly. But this is not a weakness; it is part of the theorem statement. The machine is being studied as a normalized witness machine. If normalization is structurally essential, then the theorem is a theorem about the normalized dynamics. A later paper may compare normalized and pre-normalized formulations, but that is a separate question.

---

## 8. Objection: no invariant has yet been proved

### Objection
At present, the argument offers computational evidence and heuristic invariant ideas, but no proved structural mechanism.

### Reply
Correct. The paper should separate:
- definitions,
- computationally established propositions,
- structural conjectures,
- proof program.

This separation is a strength, not a weakness. The current computational result is already theorem-shaped, and the next task is to prove the bounded slot-4 exclusion law via projected transport closure or invariant theory.

---

## 9. Objection: the result may not globalize

### Objection
Even if \(t2\) is excluded in the bounded regime, it might appear outside that regime.

### Reply
Yes. That is why global impossibility should not yet be claimed. The clean current theorem is bounded. A stronger conjecture is that any path to \(t2\) must cross beyond action distance 3, but that belongs in the open-problems or conjectures section until proved.

---

## 10. Objection: negative results are hard to interpret

### Objection
A nonappearance result can be mathematically thin unless attached to a positive structure.

### Reply
The present result is not merely negative. It has a positive structural shape:
- chamber-level repair succeeds,
- residual flow localizes to a seam,
- the seam obstruction becomes one-slot,
- the bounded regime saturates,
- the exact installation value remains excluded.

So the result identifies a sharply localized obstruction geometry, not just an absence.

---

## 11. Objection: the locked witness subset may be too special

### Objection
Why should four locked witnesses support a general obstruction statement?

### Reply
Because the bounded regime is defined as the closure generated from those witnesses under the legal move grammar with a fixed cutoff. The theorem claim is exactly about that generated regime. No broader universality is claimed without proof.

---

## 12. Objection: the observed alphabet may be overfit to computation

### Objection
The exact list
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\}
\]
may be a contingent output list rather than a mathematically meaningful object.

### Reply
This is the central structural question. The paper should therefore present the list first as a computationally established alphabet and only then promote its closure and minimality to conjectures or lemmas under investigation.

---

## 13. Best concise reply strategy

If a referee presses hard, the cleanest response is:

### Concise reply
We make a bounded claim, not a global one.
Within the saturated bounded escape-return regime generated from the locked frame-2 witnesses, the exact slot-4 value required for frame-2 closure never appears.
The next proof step is to derive this as a closed projected transport law on slot 4.

---

## 14. Paper discipline reminder

The paper should maintain the following discipline:

- Do not oversell bounded results as global impossibilities.
- Do not blur computational propositions and structural conjectures.
- Do not hide dependence on normalization.
- Do emphasize the localization and sharpening produced by exact-preference repair.
- Do frame slot-4 exclusion as stronger than mere no-closure.

That discipline will make the theorem program look serious and defensible.
