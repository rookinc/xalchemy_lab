# G60 First Patch Fill Guide

## Goal

Fill `g60_first_patch_instance_v0_1.json` with one real local G60 example.

## Fill order

### 1. Carrier
Fill these first:

- `carrier.carrier_id`
- `carrier.why_chosen`

Question:
Which exact chamber or local chamber-like object are we using as the first carrier?

### 2. Incoming incidence
Fill these second:

- `incoming_incidence.incoming_id`
- `incoming_incidence.incoming_type`
- `incoming_incidence.incoming_orientation`

Question:
What counts as arrival into this local patch?

### 3. Candidate continuations
Fill these third:

- `candidate_continuations.continuation_ids`
- `candidate_continuations.continuation_types`
- `candidate_continuations.continuation_orientations`

Minimum condition:
Name at least two locally distinct continuations.

### 4. Local chart
Fill these fourth:

- `local_chart.chart_id`
- `local_chart.chart_orientation`
- `local_chart.chart_order`
- `local_chart.chart_flip_description`

Question:
What local convention lets us read the same continuation differently under chart change?

### 5. Framed partition
Fill these fifth:

- `framed_partition.left_like_ids`
- `framed_partition.right_like_ids`
- `framed_partition.partition_note`

Minimum condition:
At least one continuation sits in each side-class.

### 6. Reversal data
Fill these sixth:

- `local_reversal_data.reversal_pairs`
- `local_reversal_data.chart_flip_action`

Question:
Which continuation classes exchange under chart flip?

### 7. Short return neighborhood
Fill these seventh:

- `short_return_neighborhood.adjacent_carrier_ids`
- `short_return_neighborhood.short_path_candidates`

Question:
What is the smallest local return-capable neighborhood around the chosen carrier?

## Success test

You are ready for the first G60 framed receipt once these are all true:

- one explicit carrier is named
- one explicit incoming incidence is named
- at least two continuations are named
- one left/right-like partition is declared
- one chart-flip effect is described

## Strongest sentence

Do not aim for full G60 yet; aim for one explicit local patch whose framed readout can be defended.

