# Signed Cycle Rule Probe Note

## Status
Working probe note

## Purpose
Record the current status of the first explicit cocycle-parity probe for the sign-closing / identity-restoring doctrine.

This note does **not** claim the full theorem.
It records that the theorem bridge is now operational as a probe.

---

## 1. The doctrine being tested

The current cycle doctrine is:

\[
n_{15}=-n_0,
\qquad
n_{30}=n_0.
\]

Interpretation:

- one full G15 cycle is sign-closing,
- two full G15 cycles restore identity.

The current theorem question is whether this rule is realized by actual cocycle parity on \(G_{15}\).

---

## 2. Probe implementation

A dedicated parity probe now exists:

```text
scripts/g15_cycle_parity_probe.py
script accepts:
a chosen cocycle support on the 30 edge labels of (G_{15}),
a chosen loop written as edge labels,
and computes:
one-cycle parity,
two-cycle parity,
one-cycle sheet effect,
two-cycle sheet effect,
truth values for the checks [ n_{15}=-n_0,\qquad n_{30}=n_0. ]
So the sign-closing doctrine is now testable by explicit finite input.
3. First successful sample
A first sample probe was run with:
Cocycle support
Loop
The script returned:
one-cycle parity: (1),
two-cycle parity: (0),
one-cycle sheet effect: flip,
two-cycle sheet effect: restore.
So for this explicit sample pair, the probe agrees exactly with the intended doctrine.
4. What this establishes
The result establishes the following.
4.1
The parity-probe machinery is operational.
4.2
There exists at least one explicit cocycle-support / loop pair on (G_{15}) for which:
one pass is parity-odd,
two passes are parity-even,
matching the sign-closing / identity-restoring law.
4.3
The bridge from cocycle language to sheet language is now executable rather than merely aspirational.
This is a genuine milestone in the theorem program.
5. What this does not yet establish
This sample does not yet prove the full theorem.
What remains open is whether:
the chosen loop is the canonical full G15 host-frame loop,
the chosen cocycle support is the canonical cocycle representative coming from the relevant signed lift,
the parity result is forced by the true lift data rather than being a coincidental sample.
So this note records a successful probe, not a final theorem.
6. Current interpretation
The current best reading is:
the sign-closing doctrine is now supported by an explicit parity probe whose sample output matches the expected one-pass flip / two-pass restore pattern.
This upgrades the doctrine from pure modeling to an actual cocycle-test interface.
7. Immediate next theorem tasks
The next tasks are now sharply defined.
Task 7.1. Canonical loop identification
Identify the edge-label loop in (G_{15}) that truly represents the full host-frame G15 cycle.
Task 7.2. Canonical cocycle representative
Identify the cocycle support or signed-edge representative canonically associated with the lift under study.
Task 7.3. Re-run the probe canonically
Run the same parity probe using the canonical loop and canonical cocycle representative.
Task 7.4. Invariance check
Show that the parity result is invariant under the relevant allowable choices.
Only after these steps can the probe be promoted to theorem-level evidence.
8. Working summary
The theorem bridge is no longer blocked by missing tooling.
The current state is:
the parity probe exists,
a sample parity match has been observed,
the remaining bottleneck is mathematical identification of the canonical loop and cocycle data.
In one line:
the sign-closing rule now has an explicit cocycle-parity probe, and that probe already exhibits the correct one-pass flip / two-pass restore behavior on a successful sample.
