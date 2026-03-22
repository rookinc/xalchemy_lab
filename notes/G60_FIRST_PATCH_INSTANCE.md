# G60 First Patch Instance

## Goal

Instantiate one actual chamber-centered local G60 patch using the schema:

- `specs/paper/g60/g60_first_explicit_patch_schema_v0_1.json`

This note is the first concrete bridge from the toy framed transport layer into an actual G60 local neighborhood.

---

## Chosen local carrier

### carrier_id
- `TODO`

### carrier_type
- `oriented_chamber`

### why this carrier was chosen
- `TODO`

Questions to answer here:

- What exactly is this chamber in the current G60 model?
- Why is it the right first local site?
- What local adjacencies make it useful for a first framed readout?

---

## Local chart choice

### chart_id
- `TODO`

### chart_orientation
- `TODO`

### chart_order
- `TODO`

Questions to answer here:

- What local ordering or orientation convention is being used?
- What does a chart flip mean on this patch?
- Which local data are held fixed, and which are re-read under chart change?

Canonical target sentence:

The local chart is the convention that lets the same raw continuation be read in chart-relative terms.

---

## Incoming incidence

### incoming_id
- `TODO`

### incoming_type
- `TODO`

### incoming_orientation
- `TODO`

Questions to answer here:

- What counts as “arrival” into this patch?
- Is arrival best represented as an oriented adjacency, flag transition, chamber transition, or something else?
- What is the smallest meaningful incoming datum for framed continuation?

---

## Candidate continuations

### continuation_ids
- `TODO`

### continuation_types
- `TODO`

### continuation_orientations
- `TODO`

Questions to answer here:

- What are the locally admissible outgoing continuations from the chosen carrier?
- How many are there?
- Which of them are the first serious candidates for a left-like / right-like partition?

Minimum success condition here:

- at least two locally distinct continuations can be named explicitly

---

## First framed partition

### left_like_ids
- `TODO`

### right_like_ids
- `TODO`

### partition_note
- `TODO`

This is the heart of the first framed readout.

Questions to answer here:

- Which local continuations are read as left-like in the chosen chart?
- Which are read as right-like?
- Is this partition exhaustive, or only a first distinguished subpartition?
- What raw local feature justifies the partition?

Canonical target sentence:

The local framed readout assigns admissible continuations into chart-relative classes.

---

## Local reversal data

### reversal_pairs
- `TODO`

### chart_flip_action
- `TODO`

Questions to answer here:

- What happens to the partition if the local chart is flipped?
- Which continuation classes exchange?
- Which, if any, remain fixed?

This section should make visible the first G60 analogue of the toy chart-flip effect.

Canonical target sentence:

A chart flip changes the framed readout of local continuations.

---

## Short return neighborhood

### adjacent_carrier_ids
- `TODO`

### short_path_candidates
- `TODO`

Questions to answer here:

- What neighboring carriers are closest to supporting a first short framed return?
- What are the smallest path candidates through this neighborhood?
- Which of these are plausible first tests for parity-like or displacement-like quantities?

This does not need to be global.
It only needs to identify the first local return-capable neighborhood.

---

## First readout targets

### chart_relative_exit
- `TODO`

### parity_like_quantity
- `TODO`

### displacement_like_quantity
- `TODO`

Interpretation:

- `chart_relative_exit = yes` means the patch already supports a first framed continuation readout
- `parity_like_quantity = yes` means a first flip-like quantity can be defined on a short local path
- `displacement_like_quantity = yes` means a first signed accumulation-like quantity can be defined on a short local path

---

## First comparison to toy layer

This section should explicitly compare the chosen G60 patch to the toy local normal form.

### local carrier
- toy: vertex controller
- G60: `TODO`

### incoming incidence
- toy: incoming edge
- G60: `TODO`

### chart selector
- toy: `A`
- G60: `TODO`

### chart-relative continuation classes
- toy: `chart_left`, `chart_right`
- G60: `TODO`

### parity-like quantity
- toy: `H`
- G60: `TODO`

### displacement-like quantity
- toy: `S`
- G60: `TODO`

Strong target sentence:

The point is not to force the toy model onto G60 verbatim, but to identify the smallest local G60 objects playing the same structural roles.

---

## What will count as success

This first patch instance is successful if it gives:

- one explicit chamber-centered carrier
- one explicit incoming oriented incidence
- at least two explicit candidate continuations
- one explicit chart-relative left/right-like partition
- one explicit chart-flip effect on that partition

That is enough to begin the first genuine G60 framed receipts.

---

## Immediate next step after this note

Once this note is filled with real local data, the next artifact should be an actual instantiated JSON object, for example:

- `specs/paper/g60/g60_first_patch_instance_v0_1.json`

That will be the first concrete G60 framed patch receipt.

