# G900 Passage Transducer Prototype Runbook

## Purpose
Run the prototype cube-host passage transducer and inspect whether the first nontrivial base-closed words produce cycle-like or path-like reduced supports.

## Script
`scripts/g900_passage_transducer_proto.py`

## Default initial state
- face: `U`
- heading: `0`
- sheet: `0`

## Default seed words
- `FXFXFX`
- `FRXFLXFX`

## First runs

### Console run
```bash
python3 scripts/g900_passage_transducer_proto.py --max-length 8
EOF
