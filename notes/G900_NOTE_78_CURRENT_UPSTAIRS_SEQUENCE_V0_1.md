# G900 Note 78 — Current Upstairs Sequence v0.1

## Current best upstairs sequence
The current extracted upstairs process is:

- r0
- Kernel(r0) -> r1
- initial_grammar_state
- A
- B
- C

## Role reading
- r0 = raw seed
- Kernel(r0) -> r1 = launch handoff
- initial_grammar_state = seeded propagation state
- A = advance
- B = bifurcate / transport-mode commitment
- C = close / return-identification / reconciliation

## Meaning
The upstairs system now has an explicit staged structure that is compatible with the current downstairs staged grammar, but shifted by one layer:

- upstairs launch occurs at kernel handoff
- downstairs launch occurs at first visible outward transport boundary

