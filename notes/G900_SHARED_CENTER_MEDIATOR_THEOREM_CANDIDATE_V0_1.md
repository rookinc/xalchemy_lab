# G900 Shared-Center Mediator Theorem Candidate v0.1

## Candidate theorem
Let the current G900 descent package satisfy:

1. the first exact quotient is a weighted triangular prism with weights
   - w_top
   - w_mid
   - w_bot

2. the second quotient collapses paired top and bottom face classes to a coarse triangle edge law by exact aggregation:
   - w_triangle = w_top + w_bot

3. the descended coarse edge law agrees with the uniform macro-contact law:
   - w_triangle = 290

4. the parity-triangle refinement carries a shared scalar midpoint
   - c = 145

5. the rung class is the unique central mediating support between the paired face strata, and must respect the same shared scalar center visible elsewhere in the descent ladder.

Then:
- w_mid = 145

If, further, top and bottom are symmetrically paired around the mediator, then
- w_top = 145 - d
- w_mid = 145
- w_bot = 145 + d

If, finally, shell structure forces d = 5, then:
- (w_top, w_mid, w_bot) = (140,145,150)

## Lemma chain
- Aggregation lemma: w_top + w_bot = 290
- Shared-center lemma: 145 is the common scalar midpoint of the current descent ladder
- Mediator lemma: unique central mediation forces w_mid = 145
- Symmetric pairing lemma: top and bottom occur as 145 +/- d
- Shell-offset lemma: d = 5

## Exact burden
The main open proof burden is now the mediator lemma.

Arithmetic alone does not force midpoint balance.
So the center must be forced structurally, by the role of the rung as the unique central mediator.

