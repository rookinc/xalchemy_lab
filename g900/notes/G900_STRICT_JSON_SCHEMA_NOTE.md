# G900 Strict JSON Schema Note

## Purpose

This note records a strict JSON-schema framing for the proposed G900 binning system.

The intent is to preserve two distinct but related layers:

1. a **meta-schema** describing the structure of the G900 binning framework itself
2. an **instance schema** describing actual G900 bin-data payloads

This separation is useful because the project is doing two things at once:

- defining the lawful categories by which a G900 object may be binned
- defining the concrete data objects that will later hold measurements, counts, overlaps, role distributions, and related observables

The meta-schema is therefore the schema of the **binning language**.
The instance schema is the schema of the **binning record**.

---

## Design posture

The design assumes the following.

- G900 should not be treated as a flat bag of vertices.
- Binning is layered.
- Radial shell structure is primary but not sufficient.
- Growth history matters.
- Transport role matters.
- Pair-distance law matters.
- Quotient-aware structure may matter.
- Spectral organization may matter.
- Strictness is useful because this object is likely to evolve quickly, and schema drift should be caught early.

For that reason, these schemas use:

- `draft/2020-12`
- `additionalProperties: false` almost everywhere
- explicit `required` lists
- enumerated role classes where appropriate
- strict default blocks
- machine-facing field discipline

---

## File 1: strict meta-schema

Saved as:

`./specs/g900-binning-schema-strict.json`

This file defines the structure of the G900 binning framework itself.

Key sections:

- `metadata`
- `bin_families`
- `indices`
- `observables`
- `storage_layout`
- `example_defaults`

This is the schema of the **binning language**.

---

## File 2: strict instance schema

Saved as:

`./specs/g900-binning-instance-strict.json`

This file defines actual G900 payloads containing binned measurements.

Current required top-level fields:

- `model_id`
- `root_id`
- `shell_bins`
- `generation_bins`
- `pair_distance_bins`
- `transport_role_bins`

This is the schema of the **binning record**.

---

## Validation workflow

A practical workflow is:

1. validate the framework object against `./specs/g900-binning-schema-strict.json`
2. validate actual measurement payloads against `./specs/g900-binning-instance-strict.json`
3. freeze schema versions whenever theorem-facing data formats change
4. only relax strictness when the object genuinely requires a new lawful extension

---

## Why this matters for G900

Strict schema discipline is not just software hygiene here.

It is also a way to preserve separation between distinct mathematical layers such as:

- shell law
- growth law
- transport law
- quotient law
- overlap law
- cocycle memory
- spectral closure behavior

If those layers begin to blur in the data model, the object becomes harder to read.

That is the real value of keeping this strict.

---

## Current normalized file layout

```text
.
├── notes
│   └── G900_STRICT_JSON_SCHEMA_NOTE.md
└── specs
    ├── g900-binning-instance-strict.json
    └── g900-binning-schema-strict.json
