# G15 Lift Maturation Program

Status: active working note  
Scope: mature the lift-side claim of the witness machine without weakening rigor

---

## 1. Purpose

The internal witness machine is now strong enough to be treated as a real mathematical object.

What remains unresolved is the lift-side question:

> does the actual signed/cocycle structure of the relevant lift select the witness machine, and if so, in what precise way?

This note defines the program for answering that question in a disciplined way.

The main objective is to mature the lift from a suggestive bridge into a testable and falsifiable layer of the project.

---

## 2. Current position

At present, three layers must be distinguished.

### Layer A: internal machine layer
This layer is already well developed.

It includes:

- binary frame completion
- subjective/objective witness pair
- state species O-O-O-S-T-S
- action species O-S-T-S-T-S
- machine law Z5 x Z2
- scaled machine M_r = Z_(5r) x Z2
- affine orbit theorem in syndrome space

This layer is the current strongest part of the program.

### Layer B: syndrome embedding layer
This layer is also strong.

It includes:

- witness states embedded into F2^16 by syndrome
- action cells embedded as phase-separation vectors
- affine binary fibers
- transported action-vector orbit under frame shift

This layer connects the witness machine to the 16-bit ambient passage space.

### Layer C: actual lift-selection layer
This layer remains open.

This is the question of whether the real signed lift, cocycle data, or switching-class structure actually selects:

- the subjective orbit
- the objective orbit
- the whole witness machine
- the action-vector orbit
- or something nearby but not identical

This layer is the one to be matured.

---

## 3. Lift vocabulary freeze

The following vocabulary is to be treated as authoritative for this phase.

### support
A weight-6 edge subset in the ambient graph.

### syndrome
A 16-bit class obtained from the chosen cycle-basis map.

### fiber
The set of all weight-6 supports sharing the same syndrome.

### lift bit
Actual sign or cocycle data associated with the signed lift or switching class.

### machine state
A witness state of the form (i,e), with i in Z5 and e in Z2, or its scaled counterpart.

### action vector
The syndrome-space difference vector eta_i between the two phase states at frame i.

### lift selection
Any rule induced by the actual lift data that privileges, isolates, stabilizes, or reproduces a witness state, action vector, orbit, or machine structure.

### objective orbit
The witness orbit:
o_i-o_(i+1)-o_(i+2)-s_(i+3)-t_(i+3)-s_i-o_i

### subjective orbit
The witness orbit:
o_i-o_(i+1)-o_(i+2)-s_(i+2)-t_i-s_i-o_i

No claim should be made that confuses syndrome structure with actual lift selection unless explicitly stated.

---

## 4. Claims that must remain separated

The program must keep the following claims distinct.

### Claim A: internal machine theorem
The witness machine exists internally as a coherent graph-theoretic machine.

This is already strong.

### Claim B: syndrome embedding claim
The witness machine embeds into syndrome space as affine binary fibers.

This is also strong.

### Claim C: actual lift-selection claim
The real signed lift or cocycle data selects the witness machine, or a part of it.

This is not yet proven.

This separation is mandatory. Conflating A or B with C weakens rigor.

---

## 5. Formal lift objective

The lift layer should be treated as an interface problem.

The lift is to be understood as supplying data of the form:

L : graph-side input -> cocycle-side observable

where the input may be represented by one of the following:

- a signed edge assignment
- a cocycle vector
- a switching-class representative
- a selected syndrome target
- a lift-side decoding result

The purpose of the lift program is to determine how this data interacts with:

- witness states
- witness fibers
- action vectors
- affine orbit structure

---

## 6. Four core lift tests

These are the authoritative tests for the current phase.

### Test 1: selection test
Question:
Does actual lift data land on the subjective orbit, the objective orbit, both, or neither?

Target outputs:
- subjective match score
- objective match score
- best-matching witness states
- ambiguity status

This is the top-priority test.

### Test 2: fiber test
Question:
Does actual lift data prefer the cleaner 18-fibers, the broader 26-fibers, or some other syndrome region?

Target outputs:
- matched fiber sizes
- syndrome class location
- objective-versus-subjective fiber preference

This tests whether the current objective preference is externally real.

### Test 3: action-vector test
Question:
Do actual lift-side phase gaps match the action-cell syndromes eta_i?

Target outputs:
- action-vector match score
- nearest eta_i
- residual mismatch

This tests whether the state/action split survives contact with lift data.

### Test 4: transport test
Question:
Does frame transport in the actual lift induce the same affine orbit law as the internal machine?

Target outputs:
- transport consistency score
- induced T-like behavior
- orbit-stability assessment

This tests whether the Affine Orbit Theorem is lift-real or only machine-internal.

---

## 7. Lift maturity levels

The lift program should be tracked by maturity level.

### Level 0: internal machine only
Only the internal witness machine is available.

### Level 1: syndrome embedding
Witness machine embedded in F2^16 as affine fibers.

### Level 2: lift probe active
Actual lift-side inputs are tested against witness states and fibers.

### Level 3: stable orbit preference
Actual lift data stably prefers one witness orbit family.

### Level 4: affine transport match
Actual lift data reproduces transported action-vector structure.

### Level 5: lift theorem
A theorem-level statement can be made that the actual lift canonically induces the witness machine, or a specified subsystem of it.

Current estimate:
between Level 1 and Level 2.

---

## 8. Allowed falsification modes

A mature lift program must allow negative outcomes.

The lift is allowed to show any of the following.

### F1
The objective orbit is not actually selected.

### F2
The subjective orbit is not actually selected.

### F3
Neither orbit is selected cleanly.

### F4
The witness machine exists internally but the actual lift prefers a different subsystem.

### F5
The action vectors eta_i are wrong or incomplete.

### F6
The affine orbit law is only approximate or basis-dependent in a stronger way than expected.

### F7
The machine must be enlarged before the lift becomes stable.

These are all valid outcomes and must be treated as legitimate scientific results.

---

## 9. Immediate work package

The next work package is Lift Maturation v0.

### A. Authoritative note
This file is the authoritative note for the lift program.

### B. Probe script
Create a script:

`scripts/g15_lift_selection_probe.py`

Purpose:
accept a lift-side input and compare it against:

- subjective orbit
- objective orbit
- action-vector orbit
- syndrome fibers

Minimum outputs:
- best candidate matches
- match scores
- fiber alignment
- action-vector alignment
- unresolved residual

### C. Artifact format
Create an artifact shape for lift probes, for example:

- input payload
- decoded syndrome or cocycle data
- subjective match block
- objective match block
- action-vector match block
- transport match block
- comments
- final verdict status

This artifact must be machine-readable.

---

## 10. Recommended probe outputs

The lift probe should attempt to emit the following fields.

### Input block
- source type
- input identifier
- raw input payload
- decoding assumptions

### Syndrome block
- derived syndrome
- candidate fibers
- fiber sizes
- nearest witness states

### Orbit block
- subjective orbit score
- objective orbit score
- ambiguity metric
- preferred orbit if any

### Action block
- eta_i nearest match
- action-vector residual
- action-cell agreement score

### Transport block
- frame-shift consistency score
- affine-orbit consistency score

### Verdict block
One of:
- objective-selected
- subjective-selected
- mixed
- unresolved
- falsified

---

## 11. Standards for lift claims

From this point forward, the following standard should hold.

### Acceptable statement
"The internal witness machine embeds naturally in syndrome space, and current lift probes are being used to test whether actual lift data selects the objective orbit."

### Not acceptable
"The actual lift is the witness machine."

That stronger claim is not yet earned.

Any theorem-level lift claim must explicitly state whether it belongs to:
- internal machine structure
- syndrome embedding
- actual lift selection

---

## 12. Practical program summary

The witness machine is mature enough internally.

The next phase is not to invent more machine structure prematurely. The next phase is to force the actual lift to answer:

- which states it prefers
- which fibers it lands in
- whether the action vectors are real
- whether affine transport survives

The lift is now to be treated as a test interface, not a poetic destination.

---

## 13. Short operational summary

Current stance:

- the machine is real internally
- the embedding is real in syndrome space
- the lift claim is promising but unclosed

Next action:

- build the lift selection probe
- run the four core lift tests
- record results as artifacts
- advance maturity level only when the evidence justifies it

---

## 14. One-line mission statement

The next phase is to force the actual lift to answer the witness machine.

