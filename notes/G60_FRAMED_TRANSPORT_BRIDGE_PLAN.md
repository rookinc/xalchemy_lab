# G60 Framed Transport Bridge Plan

## Goal

Use the toy framed transport/controller layer as a local normal form, then lift only its essential framed invariants into the G60 setting.

## Principle

Do not try to port the full toy runtime upward all at once.

Instead:

- isolate what is structurally essential
- identify the corresponding G60 local objects
- test those objects on the smallest nontrivial G60 patch

## What should survive from the toy layer

The likely survivors are:

- local framed state
- chart-relative exit
- framed transition sign
- cocycle-like parity invariant `H`
- displacement-like invariant `S`
- signature composition law

## What is probably disposable

These are useful locally but should not be treated as sacred:

- toy edge names like `e_left`, `e_right`, `e_in`
- degree-3 convenience assumptions
- demo-specific CLI surfaces
- local story language around trurtles

## Correct bridge question

The right G60-facing question is not:

- "How do we run the toy controller on G60?"

The right questions are:

- What is the G60 analogue of a local framed state?
- What is the G60 analogue of a chart-relative exit?
- What is the smallest G60 patch on which chart-relative transport can be defined?
- What is the smallest G60 loop on which a framed signature can be measured?

## Roadmap

### Layer A. Local normal form
Already built:

- controller register `(A,sigma,tau)`
- chart-primary local law
- signature `(H,S)`
- composition rule
- structural predictor

### Layer B. G60 translation layer
Next:

- define the G60 counterpart of each local notion
- identify smallest valid local G60 patch
- define chart-relative exits in that patch

### Layer C. G60 receipts
Then:

- compute actual framed traces on the patch
- test candidate G60 analogues of `H` and `S`
- check whether composition survives on short G60 loops

## Strongest sentence

Use the toy controller layer as a local normal form, then lift only its framed invariants and chart law into the smallest G60 patch that can support them.

