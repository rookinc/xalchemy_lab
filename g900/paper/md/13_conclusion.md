# Conclusion

## Status
Working draft

The present paper isolates a sharply localized obstruction phenomenon in the normalized G900 witness machine.

The baseline two-step policy already showed that the machine can contract toward exactness without achieving nontrivial exact closure. On its own, however, that behavior did not determine whether the failure was fundamentally structural or merely a consequence of policy choice. The introduction of exact-preference repair changed that situation. Once the dominant reachable chamber-level failure is repaired, the remaining obstruction becomes much easier to read: the residual basin funnels into the frame-2 seam, and the unresolved mismatch localizes to slot 4.

That localization is the paper’s main conceptual gain. After repair, the problem is no longer best understood as a diffuse failure of global organization. It becomes a one-slot installation problem at a distinguished seam coordinate. In the normalized frame-2 setting studied here, exact closure requires slot 4 to take the value \(t2\). The bounded escape-return regime generated from the locked frame-2 witnesses then provides a natural test domain for the residual dynamics.

Within that domain, the behavior is strikingly rigid. The bounded regime saturates computationally by depth 6, contains 58,624 visited states, and produces no exact frame-2 closure. More strongly, it never produces the exact slot-4 value \(t2\). On the frame-2 seam itself, the observed slot-4 alphabet is
\[
\{o4,s0,s2,s3,s4,t0,t3,t4\},
\]
again excluding \(t2\). The current evidence therefore supports a bounded slot-4 exclusion law and, through the slot-4 exactness requirement, a bounded no-closure corollary.

This is the main mathematical contribution of the current stage of the program: a broad closure failure has been sharpened into a saturated bounded exclusion phenomenon at a single normalized coordinate. That sharpening matters. It means that the witness machine is not simply wandering without structure. It reaches the correct seam. It explores a nontrivial local neighborhood around that seam. But in the bounded regime studied here, it does not install the exact value required to seal the seam.

The next task is therefore clear. The problem should now be attacked as a projected transport problem on slot 4, not as a larger brute-force search. The most promising route is to derive the slot-4 transport relation induced by the one-edit grammar and normalization law, prove closure of the reachable seam alphabet, and show that \(t2\) lies outside that closed transport set. If successful, this would turn the present computational exclusion theorem into a structural one.

Several deeper explanations remain possible. The exclusion may arise from a direct grammar-level admissibility restriction, from an affine residue obstruction, from a normalization-orbit restriction, or from a defect-transport law in which bounded one-edits move a localized seam defect without annihilating it. At present, these remain conjectural. The paper has therefore deliberately kept its scope bounded and explicit.

That restraint is not a weakness. It is part of the result’s strength. Rather than overclaiming a global impossibility theorem, the present work identifies the smallest sharp statement that the current evidence justifies and places it in a form suitable for proof development.

In the shortest formulation, the conclusion is this:

> after chamber-level repair, the residual frame-2 obstruction becomes a bounded one-slot exclusion law.

Or, in the geometric slogan that first made the phenomenon legible:

> the machine finds the seam without sealing it.

That is where the theorem program now stands.
