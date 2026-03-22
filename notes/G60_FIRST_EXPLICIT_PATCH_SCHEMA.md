# G60 First Explicit Patch Schema

## Goal

Turn the chamber-centered G60 patch idea into an explicit schema that can host the first framed readout.

This is still a local description layer, not yet a full simulator.

## Patch object

The first explicit G60 patch should be described by a record with the following fields.

### 1. Carrier

- `carrier_id`
- `carrier_type`

Working choice:
- `carrier_type = oriented_chamber`

Purpose:
Identify the single local chamber-centered site that anchors the patch.

### 2. Local chart

- `chart_id`
- `chart_orientation`
- `chart_order`

Purpose:
Specify the local chart convention used to read continuations.

This is the G60 analogue of the toy chart selector.

### 3. Incoming incidence

- `incoming_id`
- `incoming_type`
- `incoming_orientation`

Purpose:
Specify what counts as arrival into the patch.

This is the G60 analogue of the toy incoming edge.

### 4. Candidate continuations

- `continuation_ids`
- `continuation_types`
- `continuation_orientations`

Purpose:
List the locally admissible oriented continuations from the carrier.

This is the local continuation menu.

### 5. Framed continuation partition

- `left_like_ids`
- `right_like_ids`

Purpose:
Record the chart-relative partition of local continuations.

This is the first G60 framed readout target.

### 6. Local reversal data

- `reversal_pairs`
- `chart_flip_action`

Purpose:
Record which continuation classes exchange under chart reversal.

This is the first place where a parity-like quantity may arise.

### 7. Short return neighborhood

- `adjacent_carrier_ids`
- `short_path_candidates`

Purpose:
Record the smallest neighboring sites needed to test a short framed return.

This prepares the first G60 parity/displacement receipts.

## Minimal schema sketch

A first patch record may look like:

- `carrier_id`
- `chart_id`
- `incoming_id`
- `continuation_ids`
- `left_like_ids`
- `right_like_ids`
- `reversal_pairs`
- `adjacent_carrier_ids`

## Success condition

The schema is good enough if one explicit G60 patch can be filled out with:

- one carrier
- one incoming oriented incidence
- at least two continuation classes
- one chart-relative partition
- one visible chart flip effect

## Immediate next step

Instantiate this schema on one actual local G60 example.

## Strongest sentence

The first explicit G60 patch schema should make chart-relative continuation classes visible on a single oriented chamber-centered local neighborhood.

