# Toy G60 Automaton v2 in Phase Form

## Anchored phase variable

Let A select one of two anchored phases.

### Phase A = 0
Anchored control laws:
- AOOO = tau
- AE1E1E1 = sigma
- AE2E2E2 = 0

Shuttle laws:
- E1E1E1O = 1 exactly when sigma = tau
- E1E1E1E2 = sigma

### Phase A = 1
Anchored control laws:
- AE2E2E2 = 1
- AE1E1E1 = 1 except at (sigma,tau) = (1,0)
- AOOO = 1 except at (sigma,tau) = (0,1)

Shuttle laws:
- E1E1E1O = 1 exactly when sigma = tau
- E1E1E1E2 = sigma

## Distal backbone

Always odd:
- DE1E1E2
- DE1E1M+
- DE1E2E2
- E2E2E2E2

Always even:
- DE1OM+
- E1E1M+M+
- E1E2E2E2
- E1E2M+M+
- E1M+M+O
- E2E2E2O

## Reading

The automaton is a two-phase anchored controller over a rigid distal backbone.

