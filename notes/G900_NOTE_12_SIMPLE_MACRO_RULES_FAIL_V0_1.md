# G900 Note 12 — Simple Macro Rules Fail v0.1

## Result
The tested simple macro rules do not recover the triangular prism support graph.

## Rules tested
- min_x mod 3
- min_y mod 3
- min_k mod 3
- layer mod 3
- argmin sector

## Outcome
None of these rules gives the desired prism face support.
Some recover part of the vertical structure, but they miss the triangular face edges.

## Conclusion
The prism macro classes do not arise from a naive single-cell 3-class label.

