# G900 Offset Forcing Theorem Sketch v0.1

## Claim
The off-center displacement in the centered prism law is forced to equal 5 once the scale-inheritance and half-layer lemmas are granted.

## Lemma chain
1. midpoint shell supplies center:
   - I = 145

2. predecessor-shell uniqueness:
   - layer 4 is the unique shell immediately before midpoint layer 5

3. predecessor-shell scale inheritance:
   - branch displacement is inherited from the predecessor shell

4. half-layer displacement:
   - inherited displacement equals L / 2 = 5

## Conclusion
Therefore:

- top = 145 - 5 = 140
- mid = 145
- bottom = 145 + 5 = 150

So the full centered prism law is:

- (140,145,150)

## Honest status
The remaining proof burdens are now:

- predecessor-shell privilege implies scale inheritance
- inherited scale equals the half-layer displacement

