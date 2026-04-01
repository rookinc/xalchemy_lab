# G900 Witness Machine

## Status

Working theorem instrument and cockpit for the current G900 / G15 / lifted-bridge program.

This repository subtree contains:

- the witness machine itself
- command-line tooling for inspecting states and cycles
- a self-verifying theorem ledger
- bridge-model experiments around the frame-2 puncture
- artifact exports for both machine-facing and paper-facing reporting

The current system supports a verified visible machine, a verified lifted machine, and a modeled bridge layer with explicit robustness tests. The strongest beyond-model causal theorem remains open.

## Purpose

The purpose of the witness machine is to make the current project claims inspectable, executable, and falsifiable.

Instead of holding the local theory only in prose, the machine provides:

- explicit state and action representations
- classification and orbit tools
- local frame-2 socket / puncture inspection
- theorem verification routines
- reproducible JSON and Markdown exports

This lets the project distinguish clearly between:

1. verified laws
2. modeled bridge results
3. open statements

That distinction is a central design principle.

## High-level picture

At the current stage, the machine supports three layers.

### 1. Visible witness layer

This is the cycle-level and action-cell layer on the base machine. It includes:

- subjective and objective witness states
- action cells
- normalization and classification tools
- socket / assembly reads of frame-2 local structure

### 2. Lifted sheet layer

This is the native lifted machine whose states include:

- frame
- family
- sheet

This layer makes the sign-closing / identity-restoring doctrine explicit and machine-checkable.

### 3. Bridge layer

This is the current modeled local bridge between visible puncture behavior and lifted sheet illegality.

In the current model, the puncture is realized as the visible shadow of:

- a unique exact forbidden core
- plus a one-step causal fringe

This structure is tested under both payload-family perturbations and operator-family perturbations.

## Current theorem posture

The current machine-supported position is:

### Verified

- slot-4 machine shape
- scaffold rigidity
- socket fixation
- payload alphabet
- exact payload exclusion
- rigid / variable edge split
- subjective / objective family doctrine
- G15 / G30 sign-sheet readout
- native lifted state schema
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

## Directory layout

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

### artifacts/

Machine outputs, experiment results, theorem ledgers, and generated reports.

Examples:
- theorem JSON ledger
- theorem Markdown status report
- parity / host-cycle outputs
- bridge experiment outputs

### notes/

Working project notes and position reports.

These are often useful for human orientation but are not the same thing as machine verification.

### paper/md/

Paper-facing markdown files.

This directory may contain both hand-written drafts and machine-exported status reports.

### scripts/

Exploratory and batch scripts used to generate or inspect artifacts outside the core CLI.

### specs/

Schemas and formal payload shapes used in the broader G900 program.

### tests/

Project tests for the core system.

### witness_machine/

The actual machine package and CLI.

## Package overview

The witness_machine/ package contains the command-line interface, rendering helpers, bridge verifiers, export tools, and core machine logic.

Typical modules include:

- core.py
  Basic machine states, actions, cycle generation, normalization, classification, and family data.

- render.py
  Human-readable views for states, actions, tables, theorem reports, and cockpit output.

- cli.py
  The main command-line entrypoint.

- verify.py
  The theorem verifier and section ledger.

- lifted.py
  Lifted state machinery with frame / family / sheet coordinates.

- bridge.py
  Current local bridge logic around retained vs sheet-legal behavior.

- bridge_family.py
  Payload-family robustness tests.

- bridge_operator_family.py
  Operator-family robustness and invariant tests.

- theorem_status.py
  JSON export builder for theorem status.

- theorem_markdown.py
  Paper-facing Markdown report builder.

## Environment and usage

The current workflow assumes you run commands from:

cd ~/dev/cori/alchemy_lab/g900

Then invoke the package as a module:

python3 -m witness_machine.cli ...

This is the intended path because witness_machine/ lives inside g900/.

## CLI overview

The CLI supports cockpit inspection, cycle classification, local socket analysis, theorem verification, and export commands.

### General pattern

python3 -m witness_machine.cli <command> [options]

### Global option

Most commands support the top-level scale parameter:

--r N

Current local theory is primarily used with:

--r 1

## Core cockpit commands

### Show a state

python3 -m witness_machine.cli show --state 0,0

This displays:

- state code
- phase
- witness cycle
- species
- alignment
- spread
- fiber
- current action cell
- next tau
- next mu

### Show an action cell

python3 -m witness_machine.cli action --frame 0

### List all states

python3 -m witness_machine.cli list-states

### List all actions

python3 -m witness_machine.cli list-actions

### Table view

python3 -m witness_machine.cli table

### ASCII machine view

python3 -m witness_machine.cli ascii

### Observer views

python3 -m witness_machine.cli observe --state 0,0 --view frame
python3 -m witness_machine.cli observe --state 0,0 --view phase
python3 -m witness_machine.cli observe --state 0,0 --view output

### Basic checks

python3 -m witness_machine.cli check

This checks machine-level structural consistency such as:

- state count
- tau^(5r)
- mu^2
- tau / mu commutation
- state species
- action species
- output partition

## Orbit and word commands

These commands inspect how states move under operators and words.

### Orbit under a single operator

python3 -m witness_machine.cli orbit --state 0,0 --op tau

### Orbit under a word

python3 -m witness_machine.cli orbit --state 0,0 --word tau,mu

### Compose a word

python3 -m witness_machine.cli compose --word tau,mu

This reports:

- frame delta
- phase delta
- affine form
- orbit length
- component orders

### Compare scales

python3 -m witness_machine.cli compare --r1 1 --r2 2 --word tau,mu

## Cycle classification commands

These commands classify arbitrary cycles against the subjective / objective / action-cell families.

### Classify a cycle directly

python3 -m witness_machine.cli classify --cycle o0,o1,o2,s2,t0,s0

### Classify from JSON input

python3 -m witness_machine.cli classify --input some_cycle.json

### Batch classify

python3 -m witness_machine.cli batch-classify --input batch.json

### Report batch summary

python3 -m witness_machine.cli report-batch --input batch.json

### Explain a cycle

python3 -m witness_machine.cli explain-cycle \
  --cycle o0,o1,o2,s2,t0,s0 \
  --show-diff action:0

### Audit the one-edit neighborhood

python3 -m witness_machine.cli audit-neighborhood \
  --cycle o4,s0,t0,s2,o4,s4

or JSON mode:

python3 -m witness_machine.cli audit-neighborhood \
  --cycle o4,s0,t0,s2,o4,s4 \
  --json

## Frame-2 socket / assembly commands

These commands are central to the current local obstruction program.

### Assembly readout

python3 -m witness_machine.cli assembly --pretty

You can also specify a payload:

python3 -m witness_machine.cli assembly --t o4 --pretty

This gives an assembly-layer read in the [W,X,Y,Z,T,I] language and shows:

- scaffold
- socket
- payload
- exact payload
- rigid edges
- variable edges
- diads
- couplers

### Socket neighborhood

python3 -m witness_machine.cli socket-neighborhood --t o4 --pretty

This examines one-edit seam children and tests local closure behavior.

### Socket family

Full family:

python3 -m witness_machine.cli socket-family --pretty

Bounded family:

python3 -m witness_machine.cli socket-family --bounded --pretty

This is one of the most useful cockpit commands for seeing the punctured branch vs exact junction structure.

## Subjective / objective family commands

### Family table

python3 -m witness_machine.cli so-family --pretty

### Orbit readout

python3 -m witness_machine.cli so-orbit --i 0 --pretty

This gives the G15 / G30 sign-sheet readout and is a concise way to inspect the current subjective/objective doctrine.

## Theorem verification commands

### Full theorem verification

python3 -m witness_machine.cli verify-theorems --pretty

This is the main theorem cockpit.

It reports section-by-section status for:

- slot-4 machine
- family doctrine
- sign-sheet doctrine
- lifted machine
- bridge predicates
- causal bridge
- forbidden fringe
- fringe dynamics
- derived bridge
- bridge-family robustness
- bridge-operator family
- bridge-operator invariants
- bridge summary
- bridge statement
- ledger

### JSON theorem report

python3 -m witness_machine.cli verify-theorems --out artifacts/verify.json

## Export commands

These commands turn the live theorem state into reusable artifacts.

### Export theorem status as JSON

python3 -m witness_machine.cli export-theorem-status \
  --out artifacts/theorem_status.json

### Export theorem status as Markdown

python3 -m witness_machine.cli export-theorem-markdown \
  --out artifacts/theorem_status.md

### Export theorem status to both artifact and paper locations

python3 -m witness_machine.cli export-paper-theorem-status \
  --artifacts-out artifacts/theorem_status.md \
  --paper-out paper/md/40_theorem_status_report.md

This keeps the paper-facing status report synchronized with the machine state.

## Built-in help

The CLI uses argparse, so help is available directly.

### Top-level help

python3 -m witness_machine.cli --help

### Command help

Examples:

python3 -m witness_machine.cli show --help
python3 -m witness_machine.cli verify-theorems --help
python3 -m witness_machine.cli socket-family --help
python3 -m witness_machine.cli export-paper-theorem-status --help

## Current strongest supported statement

At the current stage, the strongest machine-supported statement is:

In the current bridge model, the puncture is realized as the visible shadow of a unique illegal exact core together with a one-step causal fringe. The non-retained set, the sheet-illegal set, and the core-plus-fringe set coincide. Across the tested bridge families and operator families, the uniqueness of the exact core and the failure = illegality = core-plus-fringe structure remain stable, while the fringe size varies with the continuation law.

This statement is modeled, not yet a full beyond-model theorem.

## Interpreting the bridge result

The bridge result should be read carefully.

The machine does not yet claim that the full intended causal theory has been proved.

It currently claims that:

- in the current bridge model
- the puncture behaves like the visible shadow of a unique illegal exact core
- with a one-step fringe
- and this bridge shape survives a substantial tested robustness family

So the correct language is:

- verified for the visible and lifted machine laws
- modeled for the current bridge theorem
- open for the full causal theorem beyond the current model

This distinction should always be preserved.

## Robustness picture

The current robustness tools show that the modeled obstruction shape survives:

### Payload-family perturbations

- pair swaps
- simultaneous swaps
- cyclic rotations
- exact-core relocations

### Operator-family perturbations

The bridge law survives the tested continuation families.

Across these operator families:

- exact core uniqueness remains invariant
- failure = illegality remains invariant
- core-plus-fringe decomposition remains invariant
- retained iff sheet-legal remains invariant
- fringe size varies with the operator family

This is one of the most important current findings.

## Typical workflows

### 1. Cockpit sanity pass

python3 -m witness_machine.cli show --state 0,0
python3 -m witness_machine.cli action --frame 0
python3 -m witness_machine.cli so-orbit --i 0 --pretty
python3 -m witness_machine.cli verify-theorems --pretty

### 2. Frame-2 local obstruction pass

python3 -m witness_machine.cli assembly --pretty
python3 -m witness_machine.cli socket-family --bounded --pretty
python3 -m witness_machine.cli socket-neighborhood --t o4 --pretty

### 3. Export theorem posture

python3 -m witness_machine.cli export-theorem-status --out artifacts/theorem_status.json
python3 -m witness_machine.cli export-theorem-markdown --out artifacts/theorem_status.md
python3 -m witness_machine.cli export-paper-theorem-status \
  --artifacts-out artifacts/theorem_status.md \
  --paper-out paper/md/40_theorem_status_report.md

## Development notes

### Running location

Use:

cd ~/dev/cori/alchemy_lab/g900

before invoking the CLI as a module.

### Style principle

The project tries to keep a strict separation between:

- executable machine law
- theorem ledger
- human-facing note / manuscript prose

### Operational principle

Whenever a claim can be moved from note-form into machine-verifiable form, that is preferred.

## Recommended next directions

The current vector is already strong. Good next directions would be:

- tightening the bridge from modeled to more causally derived
- extending paper-generation from full report export to section-level export
- connecting theorem status more directly into manuscript assembly
- expanding operator-family testing if and only if it serves a theorem question rather than tool proliferation

## Summary

This subtree is not just a notebook of ideas.

It is a working theorem cockpit.

At present it provides:

- a visible witness machine
- a native lifted sheet machine
- a modeled bridge around the frame-2 puncture
- robustness testing across payload and operator families
- reproducible theorem ledgers
- paper-facing report export

The strongest beyond-model causal theorem remains open, and the machine is designed to keep that boundary explicit.
