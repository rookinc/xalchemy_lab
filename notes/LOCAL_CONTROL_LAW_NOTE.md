# Local Control Law Note

## Checkpoint

The local trace-state-machine delta table shows that only a small subset of trace classes changes across the tested nearby states.

## Main control traces

Anchored control surface:
- (A,O,O,O)
- (A,E1,E1,E1)
- (A,E2,E2,E2)

Mixed shuttle trace:
- (E1,E1,E1,O)

## Control interpretation

### tau
Tau toggles the anchor odd branch:
- (A,O,O,O)

When tau turns off, oddness moves into:
- (E1,E1,E1,O)

### sigma
Sigma activates the anchored E1 sheet:
- (A,E1,E1,E1)
- (E1,E1,E1,E2)

### A
A swaps anchored sheet polarity and rearms the anchor odd mode:
- (A,E1,E1,E1): odd -> even
- (A,E2,E2,E2): even -> odd
- (A,O,O,O): even -> odd

## Rigid backbone

Stable odd:
- (D,E1,E1,E2)
- (D,E1,E1,M+)
- (D,E1,E2,E2)
- (E2,E2,E2,E2)

Stable even:
- (D,E1,O,M+)
- (E1,E1,M+,M+)
- (E1,E2,E2,E2)
- (E1,E2,M+,M+)
- (E1,M+,M+,O)
- (E2,E2,E2,O)

## Strongest reading

The local state machine is controlled by a small anchored parity surface sitting on top of a rigid distal backbone.

