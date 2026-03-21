# Next Step: Local Normal Form

## Goal

Compress the local trace-state machine into a first normal form.

## Proposed split

### Anchored control surface
Trace classes whose parity changes under nearby controls:
- (A,O,O,O)
- (A,E1,E1,E1)
- (A,E2,E2,E2)
- (E1,E1,E1,O)
- (E1,E1,E1,E2)

### Rigid odd backbone
- (D,E1,E1,E2)
- (D,E1,E1,M+)
- (D,E1,E2,E2)
- (E2,E2,E2,E2)

### Rigid even backbone
- (D,E1,O,M+)
- (E1,E1,M+,M+)
- (E1,E2,E2,E2)
- (E1,E2,M+,M+)
- (E1,M+,M+,O)
- (E2,E2,E2,O)

## Desired outcome

State the local law in normal form as:

- anchored control surface
- rigid odd backbone
- rigid even backbone

This would be the cleanest static formulation before pushing upward toward G60.

