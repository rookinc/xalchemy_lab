# G60 First Patch Extraction Prompt

## Use

This prompt is for extracting one actual local G60 patch from your existing G60 data, notes, or construction files.

## Prompt

Take one explicit chamber-centered local neighborhood from the current G60 model and report:

1. the chamber identifier
2. the incoming oriented incidence chosen as arrival
3. the locally admissible continuation identifiers
4. a local chart convention that orders or orients those continuations
5. a proposed partition into left-like and right-like continuation classes
6. how that partition changes under chart flip
7. the nearest adjacent carriers needed for a first short return test

Return the result in a form that can be copied into:

- `specs/paper/g60/g60_first_patch_instance_v0_1.json`

## Strongest sentence

We are not asking for the whole G60 object, only one chamber-centered local patch with an explicit framed readout.

