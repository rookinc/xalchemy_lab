# G900 Weight Extraction Notes v0.1

## First target
- edge: top_ab

## Update targets
- specs/paper/g60/even_slice_prism_support_v0_1.json
- specs/paper/g60/odd_slice_prism_support_v0_1.json
- specs/paper/g60/g900_prism_weight_table_v0_1.json

## Goal
Replace symbolic placeholders with the first extracted concrete value(s), then determine whether:
- even/odd exact equality holds, or
- only symbolic-shape agreement holds

## Current search result
Concrete prism weights were found in:

- `src/xalchemy_lab/app/hello_g900_prism_export.py`
- `specs/paper/g60/g900_weighted_prism_v0_1.json`

The exported weighted prism gives:
- bit0_face = 140
- macro_rung = 145
- bit1_face = 150

Current symbolic identification:
- top face -> bit0_face
- bottom face -> bit1_face
- vertical edges -> macro_rung

## Record
- even top_ab = 140
- odd top_ab = 140
- verdict = equal in current shared exported prism artifact
