# G60 First Explicit Patch Schema Result

## Result

A first explicit schema now exists for a chamber-centered local G60 patch.

Artifact:

- `specs/paper/g60/g60_first_explicit_patch_schema_v0_1.json`

## What the schema includes

The schema contains fields for:

- carrier
- local chart
- incoming incidence
- candidate continuations
- framed left/right-like partition
- local reversal data
- short return neighborhood
- readout targets

## Why this matters

This is the first concrete container for lifting the framed transport language into G60 without jumping straight to a full simulator.

It is now possible to instantiate one actual G60 patch and ask:

- what is the carrier?
- what are the admissible continuations?
- which are left-like and right-like?
- what changes under chart flip?
- what short return paths exist nearby?

## Strongest sentence

The first G60 lift now has an explicit local schema, so the next task is no longer to invent the container but to instantiate one real patch.

## Next step

Pick one actual chamber-centered local G60 example and fill this schema with real local data.

