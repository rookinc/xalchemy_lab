# G900 / G15 Witness Machine Lab

This repository is the current working lab for the G15 witness-machine program and its immediate graph-theoretic environment.

It now contains three tightly linked layers:

1. mathematical notes and theorem-stack work
2. brute-force and support scripts for G15 exploration
3. a working headless simulator for the witness machine

The important thing is that the witness machine is no longer only a conceptual object. It is now represented in notes, in derived formulas, and in executable code.

---

## Core result

The working machine is the witness machine

Z5 x Z2

with:

- frame coordinate in Z5
- phase coordinate in Z2
- subjective phase = 0
- objective phase = 1

The base operators are:

- tau: frame transport
- mu: phase flip

with laws:

- tau^5 = id
- mu^2 = id
- tau mu = mu tau

The machine has:

- state species: O-O-O-S-T-S
- action species: O-S-T-S-T-S

The action cell at frame i is the difference between the subjective and objective witness states at that frame.

---

## Repository layout

### `witness_machine/`
Headless simulator and machine lab.

Files:

- `core.py`
  Core machine logic, scaling law, operators, codes, exports, and word algebra.

- `render.py`
  Human-readable rendering for tables, summaries, ASCII graph, orbit traces, comparisons.

- `cli.py`
  Command-line interface for inspecting, stepping, exporting, comparing, and analyzing the machine.

- `repl.py`
  Interactive REPL for moving around inside the machine.

This is the main executable assembly for the witness machine.

### `scripts/`
Graph and syndrome support tooling.

Important files include:

- `g15_graph.py`
- `g15_c6_species.py`
- `g15_cocycle_decode.py`
- `g15_subjective_objective_test.py`
- `g15_syndrome_bruteforce.py`
- `g15_syndrome_bruteforce_weight6.py`
- `g900_passage_transducer_proto.py`

These are the lower-level support scripts used to derive, test, and inspect G15 structure and witness candidates.

### `artifacts/`
Generated outputs and machine exports.

Important current artifacts include:

- `g15_subjective_objective_test.json`
- `g15_subjective_objective_test.pretty.json`
- `witness_machine.json`
- `witness_machine_r2.json`

These are current machine-facing outputs and should be treated as generated data products, not hand-edited source.

### `notes/`
Working notes, theorem notes, position reports, and graph-theoretic development documents.

This directory is the written intellectual scaffold for the project.

### `specs/`
Schemas and structured experimental payload definitions related to the broader G900 environment.

### `tests/`
Machine tests.

Currently includes:

- `test_core.py`

---

## What exists now

At the time of this README, the following is live and working.

### 1. Fixed witness machine
The base machine `M1` is implemented as:

Z5 x Z2

with 10 total states.

### 2. Scaled witness machine
The scaled machine is implemented as:

M_r = Z_(5r) x Z2

This is a dimensionless scaling of the frame cycle while preserving binary phase structure.

### 3. Bit model
For scale parameter `r`:

- frame count = 5r
- state count = 10r
- frame bits = ceil(log2(5r))
- total bits = ceil(log2(10r))

The simulator exposes canonical state codes directly.

### 4. Orbit algebra
Words in `tau`, `tau_inv`, and `mu` are normalized to affine actions of the form:

(i, e) -> (i + delta_i mod 5r, e + delta_e mod 2)

with closed-form orbit-length calculation.

This means the machine is now algebraically inspectable through the CLI.

### 5. JSON export
The machine can be exported as structured JSON for later UI or downstream tooling.

---

## CLI quickstart

All commands are run from the repo root.

### Machine info
```bash
python3 -m witness_machine.cli info
python3 -m witness_machine.cli --r 2 info

Show a state

python3 -m witness_machine.cli show --state 0,0
python3 -m witness_machine.cli --r 2 show --state 7,1

Step the machine

python3 -m witness_machine.cli step --state 0,0 --op tau
python3 -m witness_machine.cli step --state 0,0 --op mu
python3 -m witness_machine.cli step --state 3,1 --op tau_inv

List states and actions

python3 -m witness_machine.cli list-states
python3 -m witness_machine.cli list-actions
python3 -m witness_machine.cli action --frame 2

Table and ASCII graph

python3 -m witness_machine.cli table
python3 -m witness_machine.cli ascii

python3 -m witness_machine.cli --r 2 table
python3 -m witness_machine.cli --r 2 ascii

Observer views

python3 -m witness_machine.cli observe --state 3,1 --view frame
python3 -m witness_machine.cli observe --state 3,1 --view phase
python3 -m witness_machine.cli observe --state 3,1 --view output

Theorem sanity checks

python3 -m witness_machine.cli check
python3 -m witness_machine.cli --r 2 check

Orbit tracing

python3 -m witness_machine.cli orbit --state 0,0 --op tau
python3 -m witness_machine.cli orbit --state 0,0 --op mu
python3 -m witness_machine.cli orbit --state 0,0 --word tau,mu
python3 -m witness_machine.cli orbit --state 0,0 --word tau,mu,tau

Word composition algebra

python3 -m witness_machine.cli compose --word tau
python3 -m witness_machine.cli compose --word mu
python3 -m witness_machine.cli compose --word tau,mu
python3 -m witness_machine.cli compose --word tau,mu,tau
python3 -m witness_machine.cli --r 4 compose --word tau,mu,tau

Scale comparison

python3 -m witness_machine.cli compare --r1 1 --r2 2
python3 -m witness_machine.cli compare --r1 1 --r2 3 --word tau --word mu --word tau,mu,tau

Export

python3 -m witness_machine.cli export --kind machine
python3 -m witness_machine.cli export --kind state --state 2,1
python3 -m witness_machine.cli export --kind action --frame 3
python3 -m witness_machine.cli export --kind machine --out artifacts/witness_machine.json


---

REPL quickstart

Run:

python3 -m witness_machine.repl

or scaled:

python3 -m witness_machine.repl --r 2

Useful REPL commands:

show

tau

back

mu

goto i,p

frame

phase

output

action

ascii

info

help

quit



---

Current mathematical status

The following is now effectively locked as the working witness-machine structure.

Binary witness machine

The witness system is organized as a binary lifted machine over a cyclic frame base.

State/action split

states live in species O-O-O-S-T-S

actions live in species O-S-T-S-T-S


Affine orbit form

The syndrome-space witness machine is treated as generated by:

one base point Phi(0,0)

one action vector eta0

one frame-shift operator T


with:

Phi(i,0) = T^i Phi(0,0)

eta_i = T^i eta_0

Phi(i,1) = Phi(i,0) + eta_i


This is the current locked affine working structure.

Orbit separation

The subjective and objective families separate uniformly by:

alignment

spread

fiber class


Working signatures:

subjective = return / 4 / 26

objective = forward / 5 / 18



---

What this repository is for

This repo is for:

deriving and testing witness-machine structure

comparing graph-theoretic candidate forms

executing the machine headlessly

scaling the machine dimensionlessly by r

preparing later visualization without changing core logic


It is not yet a browser app, and it is not yet a physics engine. It is a graph-theoretic machine lab with a live executable core.


---

Suggested workflow

A good normal workflow is:

1. use notes to refine theorem statements and architectural language


2. use scripts to test graph-level and syndrome-level questions


3. use witness_machine.cli to inspect machine behavior


4. use check, orbit, compose, and compare to verify algebraic claims


5. export machine snapshots to artifacts/




---

Baseline commands

If you want to quickly confirm that the machine is alive, run:

python3 -m witness_machine.cli check
python3 -m witness_machine.cli table
python3 -m witness_machine.cli ascii
python3 -m witness_machine.cli orbit --state 0,0 --word tau,mu
python3 -m witness_machine.cli compose --word tau,mu,tau

For scaled confirmation:

python3 -m witness_machine.cli --r 2 check
python3 -m witness_machine.cli --r 2 info
python3 -m witness_machine.cli compare --r1 2 --r2 4 --word tau,mu --word tau,mu,tau


---

Current practical conclusion

This repository now contains a real witness-machine MVP:

mathematically motivated

executable in CLI and REPL

scalable in r

exportable as machine JSON

algebraically inspectable by word composition


That means the project has crossed from speculative note-work into reproducible machine form.

