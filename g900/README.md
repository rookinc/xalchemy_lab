# G900

## Status

Active project subtree for the current G900 program.

This directory now contains both:

- the witness-machine theorem cockpit
- the broader surrounding project material for artifacts, notes, scripts, specs, tests, and paper assembly

The root README is project-level.
For detailed witness-machine usage, see:

witness_machine/README.md

## What G900 is

G900 is the current project home for the local witness, lifted-sheet, bridge, and host-cycle program.

At the present stage, the subtree combines several kinds of work:

- executable witness-machine code
- theorem verification and export
- generated experiment artifacts
- paper-facing markdown
- working project notes
- bridge and transport scripts
- G15 / G30 / host-cycle / parity investigations

So G900 is not just a package and not just a paper folder.
It is the full working environment for the present program.

## Current theorem posture

The current machine-supported position is:

### Verified

- visible slot-4 machine structure
- scaffold rigidity
- socket fixation
- bounded payload alphabet
- exact payload exclusion
- rigid / variable edge split
- subjective / objective family doctrine
- G15 / G30 sign-sheet readout
- native lifted frame / family / sheet state
- visible projection forgetting sheet
- native sheet-flip operator law

### Modeled

- retained predicate
- sheet-legal predicate
- retained iff sheet-legal at the current local bridge layer
- retained as no-escape continuation
- exact forbidden state detection
- exact forbidden state is non-retained
- exact forbidden state is sheet-illegal
- failure set equals illegality set
- forbidden core plus one-step fringe
- fringe feeds exact core in one step
- puncture as derived core-plus-fringe shadow
- bridge-family robustness testing
- bridge-operator robustness testing
- unique exact core is operator-invariant
- failure = illegality is operator-invariant
- core-plus-fringe decomposition is operator-invariant
- retained iff sheet-legal is operator-invariant
- fringe size is operator-sensitive
- puncture equals sheet shadow in the current model
- failure-type exhaustion
- upstairs residual obstruction

### Open

- retained iff sheet-legal as a full causal bridge theorem
- puncture = sheet shadow beyond the current bridge model
- full causal theorem beyond the current bridge model

## Current strongest supported statement

In the current bridge model, the puncture is realized as the visible shadow of a unique illegal exact core together with a one-step causal fringe. The non-retained set, the sheet-illegal set, and the core-plus-fringe set coincide. Across the tested bridge families and operator families, the uniqueness of the exact core and the failure = illegality = core-plus-fringe structure remain stable, while the fringe size varies with the continuation law.

This statement is modeled, not yet a full beyond-model theorem.

## Directory map

The current subtree is organized as follows:

g900/
|-- README.md
|-- artifacts/
|-- notes/
|-- paper/
|   `-- md/
|-- scripts/
|-- specs/
|-- tests/
`-- witness_machine/

### README.md

This file.
Project-level overview for the full G900 subtree.

### artifacts/

Generated outputs from scripts, verifiers, and experiments.

This includes things like:

- frame-2 obstruction artifacts
- action policy and repair scans
- local basin scans
- greedy and feedback probe outputs
- G15 signed-cycle and host-cycle outputs
- theorem status exports
- witness-machine exports

Examples currently present include:

- theorem_status.json
- theorem_status.md
- g15_signed_cycle_rule_probe.json
- g15_hamiltonian_cycle_parity_sweep.json
- g15_host_cycle_edge_loop.json
- witness_machine.json

### notes/

Working notes, position reports, theory sketches, theorem-program notes, and orientation documents.

These are project memory and project reasoning aids, but they are not the same thing as machine verification.

This folder currently contains material on:

- frame-2 obstruction law
- bounded exclusion program
- G15 / G30 cycle structure
- local basin geometry
- bridge tables
- passage transducer program
- graph-theoretic status reports
- witness and transport notes

### paper/md/

Paper-facing markdown and manuscript assembly material.

This includes:

- outline and introduction material
- theorem-chain files
- local closure and slot-4 files
- subjective / objective lift files
- signed-cycle and host-cycle files
- theorem status report
- draft manuscripts

Important current files include:

- 37_sheeted_witness_machine_definition.md
- 38_signed_cycle_rule_probe_note.md
- 39_candidate_host_cycle_parity_match.md
- 40_theorem_status_report.md

### scripts/

Exploratory and batch scripts used to generate artifacts and probe the machine.

This is where much of the computational experiment layer lives.

It currently includes scripts for:

- frame-2 slot and seam analysis
- repair-radius scans
- action policy and oracle scans
- basin summaries
- subjective / objective tests
- parity probes
- host-cycle extraction
- signed-cycle verification
- passage transducer experiments

### specs/

Schemas and structured payload definitions used in the broader G900 program.

This includes examples and strict schema files.

### tests/

Project tests for the core machinery.

### witness_machine/

The actual witness-machine package.

This is the executable cockpit layer and now has its own detailed README:

witness_machine/README.md

That README should be treated as the detailed manual for:

- CLI commands
- theorem verification
- theorem exports
- socket / assembly inspection
- orbit and classification tools

## Project split

The clean split is now:

- g900/README.md
  project-level overview

- witness_machine/README.md
  machine-level manual

That split should be preserved going forward.

## Quickstart

Run from:

cd ~/dev/cori/alchemy_lab/g900

A few useful first commands are:

python3 -m witness_machine.cli show --state 0,0
python3 -m witness_machine.cli action --frame 0
python3 -m witness_machine.cli so-orbit --i 0 --pretty
python3 -m witness_machine.cli verify-theorems --pretty

For the full machine manual, use:

sed -n '1,260p' witness_machine/README.md

## Main generated reports

The current machine exports important status reports into both artifacts and paper-facing locations.

Key files include:

- artifacts/theorem_status.json
- artifacts/theorem_status.md
- paper/md/40_theorem_status_report.md

These should be understood as machine-generated status artifacts, not freehand notes.

## Interpreting the bridge result

The bridge result must be read carefully.

The machine does not yet claim that the full intended causal theory has been proved.

The current state is:

- verified for the visible machine
- verified for the lifted machine
- modeled for the current bridge law
- open for the full beyond-model causal theorem

That distinction is intentional and should not be blurred in future writing.

## Robustness picture

The current modeled bridge law survives tested perturbations in both of the following senses:

### Bridge-family robustness

The shape survives tested payload-table perturbations such as:

- pair swaps
- simultaneous swaps
- cyclic rotations
- exact-core relocation

### Operator-family robustness

The shape also survives tested continuation-operator families.

Across tested operator families, the following remain invariant:

- unique exact core
- failure = illegality
- core-plus-fringe decomposition
- retained iff sheet-legal

What changes is the fringe size.
So the obstruction shape is stable while the fringe thickness is operator-sensitive.

## Typical project workflows

### 1. Cockpit / theorem check

python3 -m witness_machine.cli verify-theorems --pretty

### 2. State and action inspection

python3 -m witness_machine.cli show --state 0,0
python3 -m witness_machine.cli action --frame 0

### 3. Export theorem posture

python3 -m witness_machine.cli export-theorem-status --out artifacts/theorem_status.json
python3 -m witness_machine.cli export-theorem-markdown --out artifacts/theorem_status.md
python3 -m witness_machine.cli export-paper-theorem-status \
  --artifacts-out artifacts/theorem_status.md \
  --paper-out paper/md/40_theorem_status_report.md

### 4. Work with the broader manuscript

See:

paper/md/

### 5. Work with the broader experiment layer

See:

scripts/
artifacts/
notes/

## Development principle

The guiding principle of this subtree is to keep a clean separation between:

- executable machine law
- machine-generated theorem ledger
- experimental artifacts
- human-facing notes
- manuscript prose

Whenever a claim can be migrated from note-form into machine-verifiable form, that is preferred.

## Summary

G900 is now the full project home for the current witness, lift, bridge, host-cycle, and manuscript program.

Inside it:

- witness_machine/ is the executable theorem cockpit
- artifacts/ stores generated outputs
- notes/ stores working reasoning and position notes
- paper/md/ stores manuscript-facing material
- scripts/ stores exploratory and batch computational tools
- specs/ stores schemas
- tests/ stores core tests

The strongest beyond-model causal theorem remains open, and the project is now organized so that the machine-supported boundary stays explicit.
