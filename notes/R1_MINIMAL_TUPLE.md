# r1 Minimal Tuple

## Proposal

The minimal resolved state is:

- `r1 = (localized_site, centroid_orientation, initial_grammar_state)`

## Reason

This is the smallest tuple that appears sufficient to make downstream propagation mostly deterministic.

## Meanings

- `localized_site` = where the spark resolves
- `centroid_orientation` = how the cube is oriented to that resolved spark
- `initial_grammar_state` = which propagation grammar is seeded

## Strongest sentence

r1 should be the smallest state that makes propagation deterministic.

