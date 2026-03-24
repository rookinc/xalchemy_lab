# G900 Note 77 — Upstairs Launch Is Kernel Handoff v0.1

## Result
The current upstairs launch role is best read as the kernel handoff:

- r0 -> r1

rather than as a standalone visible A-move.

## Supporting evidence
The refined r1 state explicitly contains:

- localized_site
- centroid_orientation
- reconciliation_state
- initial_grammar_state

with the description:

- initial_grammar_state = seed grammar state for downstream deterministic propagation

## Interpretation
This suggests the upstairs sequence is:

- r0 = raw seed
- Kernel(r0) -> r1 = privileged launch handoff
- initial_grammar_state in r1 = seeded downstream grammar
- A = first propagated advance
- B = bifurcate / mode commitment
- C = close / reconcile

## Bridge consequence
Upstairs launch and downstairs launch are not identical in form.

- upstairs launch = kernel-to-grammar handoff
- downstairs launch = first visible outward boundary

This is still compatible with the bridge, but it means the upstairs/downstairs correspondence is shifted by one abstraction layer.

