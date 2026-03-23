# G900 Midpoint Not Forced by Arithmetic v0.1

## Status
Result note.

## Statement
The current extracted weighted prism artifact satisfies the centered prism law:

- top = 140
- rung = 145
- bottom = 150

with midpoint identity

- 145 = (140 + 150) / 2.

However, this midpoint law is **not forced by arithmetic constraints alone**.

## Arithmetic constraints tested
The counterexample search kept only the following arithmetic conditions:

1. top + bottom = 290
2. macro-contact match = 290
3. same intended base edge law at the collapsed triangle level

Under those conditions alone, the midpoint identity

- rung = (top + bottom) / 2

is not forced.

## Surviving noncentered candidates
The search found explicit noncentered survivors such as:

- top = 140, rung = 144, bottom = 150
- top = 140, rung = 146, bottom = 150

These candidates preserve:

- top + bottom = 290
- macro-contact match = 290

but break:

- rung = (top + bottom) / 2 = 145.

## Consequence
So the centered prism law cannot be derived from arithmetic coincidence alone.

Any theorem forcing midpoint balance must use stronger structural assumptions, for example:

- the rung as unique central mediating support,
- exact symmetric pairing of top and bottom face strata,
- normalization by offsets around a true center class,
- or a stronger quotient-law constraint tying rung weight to the paired face layers.

## Present conclusion
At present, the checked bundle supports:

- the **observed** centered prism law,
- but not yet the **forced** centered prism law.

The forcing version remains open and must be proved structurally, not arithmetically.

## Next target
Find the minimal structural assumption that excludes the noncentered survivors.

