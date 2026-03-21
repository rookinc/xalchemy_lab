# G60 Interface Checklist v1

Use this checklist to evaluate any proposed upstairs `G60` transport mechanism against the current local law.

---

## A. Positive interface requirements

A candidate `G60` model must reproduce all of the following under local descent.

### 1. Anchored control packet
- [ ] Descends to an anchored control surface.
- [ ] Reproduces `tau` as anchor-side odd exchange activation.
- [ ] Reproduces `sigma` as `E1`-sheet activation.
- [ ] Reproduces `A` as anchored sheet-polarity swap plus odd rearming.

### 2. Rigid transport skeleton
- [ ] Descends to a rigid odd backbone.
- [ ] Descends to a rigid even backbone.
- [ ] Preserves backbone parity stability across the tested nearby controls.

### 3. Quotient compatibility
- [ ] Descends to the invariant receipt layer `(A, sigma, tau)`.
- [ ] Descends further to the bridge quotient `(R, Q, W) = (0, A+sigma, A+tau)`.
- [ ] Allows distinct trace catalogs to share a bridge signature.

---

## B. Required local structures

A candidate `G60` model should exhibit recognizable upstairs counterparts of the following.

### 4. Packet structure
- [ ] One anchor chamber packet.
- [ ] One odd exchange branch.
- [ ] Two sibling continuation sheets.
- [ ] One rigid distal skeleton.

### 5. Local trace-law compatibility
- [ ] Supports the anchored control surface traces.
- [ ] Supports the rigid odd backbone traces.
- [ ] Supports the rigid even backbone traces.
- [ ] Supports the mixed cancellation class `(D,E1,O,M+)` as even.

---

## C. No-go filter

A candidate `G60` model fails if any of the following occur.

### 6. Distal rigidity violations
- [ ] FAIL if the rigid distal backbone becomes control-sensitive under nearby `A, sigma, tau` flips.

### 7. Anchored parity violations
- [ ] FAIL if both anchored even sheets swap parity simultaneously under a single local control.

### 8. Cancellation-law violations
- [ ] FAIL if `(D,E1,O,M+)` becomes odd without a structural change in the distal skeleton.

### 9. Rearming violations
- [ ] FAIL if anchor odd rearming occurs without a corresponding anchored control-surface transition.

---

## D. Current known local control law

Use this as the present reference when checking descent.

### 10. Anchored control surface
- [ ] `(A,O,O,O)`
- [ ] `(A,E1,E1,E1)`
- [ ] `(A,E2,E2,E2)`
- [ ] `(E1,E1,E1,O)`
- [ ] `(E1,E1,E1,E2)`

### 11. Rigid odd backbone
- [ ] `(D,E1,E1,E2)`
- [ ] `(D,E1,E1,M+)`
- [ ] `(D,E1,E2,E2)`
- [ ] `(E2,E2,E2,E2)`

### 12. Rigid even backbone
- [ ] `(D,E1,O,M+)`
- [ ] `(E1,E1,M+,M+)`
- [ ] `(E1,E2,E2,E2)`
- [ ] `(E1,E2,M+,M+)`
- [ ] `(E1,M+,M+,O)`
- [ ] `(E2,E2,E2,O)`

---

## E. Theorem-preimage check

A good candidate should also explain the known bridge-signature degeneracy.

### 13. Shared bridge class with distinct trace catalogs
- [ ] Explains how `(0,0,1)` and `(1,1,0)` both descend to bridge signature `(0,0,1)`.
- [ ] Explains why those two invariant preimages support different anchored trace behavior.
- [ ] Explains the anchored even-sheet polarity swap forgotten by the bridge signature.

---

## F. Verdict

### Pass / fail summary
- [ ] PASS: reproduces anchored control packet
- [ ] PASS: reproduces rigid transport skeleton
- [ ] PASS: respects quotient compatibility
- [ ] PASS: avoids all current no-go patterns

### Final decision
- [ ] Candidate is locally compatible with the current `G60` interface
- [ ] Candidate is locally incompatible with the current `G60` interface

