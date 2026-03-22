# G60 Local Dictionary v0.1

## Goal

Bridge the toy framed transport/controller layer to the G60 setting by identifying the smallest corresponding local objects.

## Principle

This is a translation layer, not yet a simulator design.

The purpose is to identify what from the toy layer survives structurally in G60.

## Toy-to-G60 dictionary

### 1. Local carrier

- Toy:
  - vertex controller
- G60 candidate:
  - local incidence site
  - oriented chamber
  - flag-neighborhood carrier
  - small local adjacency packet

Question:
Which G60 local object best plays the role of a site that receives an incoming oriented continuation and chooses among local continuations?

### 2. Incoming incidence

- Toy:
  - incoming edge `e_in`
- G60 candidate:
  - incoming oriented adjacency
  - incoming chamber-to-chamber continuation
  - incoming local flag transition

Question:
What is the cleanest G60 notion of “arrival” at a local site?

### 3. Local chart

- Toy:
  - chart selector `A`
- G60 candidate:
  - local chamber orientation choice
  - local sector orientation
  - local ordered incidence frame

Question:
What is the minimal local G60 chart choice that reverses the readout of continuation classes?

### 4. Continuation classes

- Toy:
  - `chart_left`, `chart_right`
- G60 candidate:
  - two local oriented continuation classes
  - two local branch types
  - two local side classes relative to a chosen chart

Question:
What are the first two chart-relative continuation classes in the minimal G60 patch?

### 5. Structural local bits

- Toy:
  - `sigma`, `tau`
- G60 candidate:
  - local asymmetry bits
  - local continuation-bias markers
  - local collapse/reopen selectors

Question:
What local G60 data behaves like chart-relative collapse operators?

### 6. Mixed reopening

- Toy:
  - mixed reopened split state
- G60 candidate:
  - local bifurcated continuation pattern
  - local non-collapsed two-way readout after combined structural activation

Question:
What is the smallest G60 local phenomenon corresponding to mixed reopening?

### 7. Parity-like invariant

- Toy:
  - `H`
- G60 candidate:
  - parity of local framed reversals
  - short-path cocycle sign
  - local continuation-flip parity

Question:
What is the smallest G60 parity-like framed quantity on a short local path?

### 8. Displacement-like invariant

- Toy:
  - `S`
- G60 candidate:
  - signed local continuation bias
  - net framed side displacement
  - local oriented accumulation quantity

Question:
What is the smallest G60 displacement-like framed quantity on a short local path?

## Strongest sentence

The next task is to identify the G60 local incidence object on which chart-relative continuations, parity-like flips, and displacement-like accumulation can all be defined.

