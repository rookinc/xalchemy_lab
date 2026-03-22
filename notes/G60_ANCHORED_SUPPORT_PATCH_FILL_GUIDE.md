# G60 Anchored Support Patch Fill Guide

## Goal

Fill the anchored support patch schema with one real anchor-centered local example.

Artifact to fill:

- `specs/paper/g60/g60_anchored_support_patch_schema_v0_1.json`

## Recommended first carrier choice

Start with a:

- face-center anchor

Reason:
A face center naturally mediates between:
- nearby corners
- the cube center

That makes it the best first candidate for:
- incoming incidence
- two or more continuation classes
- local chart-relative readout
- short anchored return paths

## Fill order

### 1. Choose one actual anchor
Fill:
- `carrier_id`
- `anchor_role`
- `why_chosen`

### 2. Name one incoming anchored incidence
Fill:
- `incoming_id`
- `incoming_type`
- `incoming_orientation`

### 3. Name at least two candidate continuations
Fill:
- `continuation_ids`
- `continuation_anchor_targets`

### 4. Declare a local chart
Fill:
- `chart_id`
- `chart_orientation`
- `chart_order`
- `chart_flip_description`

### 5. Declare the first framed partition
Fill:
- `left_like_ids`
- `right_like_ids`
- `partition_note`

### 6. Record chart-flip effect
Fill:
- `reversal_pairs`
- `chart_flip_action`

### 7. Name the shortest anchored neighborhood
Fill:
- `adjacent_anchor_ids`
- `adjacent_anchor_roles`
- `short_path_candidates`

## Success condition

The first anchored patch is good enough once it shows:

- one explicit anchor-centered carrier
- one incoming anchored incidence
- at least two candidate continuations
- one chart-relative left/right partition
- one chart-flip effect

## Strongest sentence

Do not try to fill the whole 15-anchor cube at once; fill one defensible anchor-centered patch first.

