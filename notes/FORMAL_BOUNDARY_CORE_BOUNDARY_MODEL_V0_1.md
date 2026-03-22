# Formal Boundary-Core-Boundary Model v0.1

## Goal

State the current cube/G60 cycle as a formal model class with explicit state variables, parameters, and maps.

This note does not claim the model is proved.
It defines the strongest rigorous conjectural scaffold currently supported by the work.

## Parameters

Let:

- `phi = (1 + sqrt(5)) / 2`
- `alpha = phi^3`

Let `x` be the real root of:

- `64x^3 + 63x^2 + 7x - 9 = 0`

and define:

- `beta = x^2`

## Numerical values

Using the real root:

- `x ~= 0.2918496024`
- `beta = x^2 ~= 0.0851761954`

Also:

- `alpha = phi^3 ~= 4.2360679775`

So the current candidate scales are:

- `alpha` expansive
- `beta` contractive

## State variables

At step `t`, define the system state as:

- `poke_set_t`
- `snapped_vertex_t`
- `return_path_class_t`
- `center_state_t`
- `next_face_state_t`

### Meanings

#### poke_set_t
The active set of boundary perturbations or sector excitations at time `t`.

#### snapped_vertex_t
The discrete G60 attractor vertex selected from the induced interior bias.

#### return_path_class_t
The class of the shortest admissible path from the snapped vertex back to center.

#### center_state_t
The internal state of the core after receiving the closure receipt.

#### next_face_state_t
The re-emitted face-state pattern produced by the center.

## Core maps

Define the following maps.

### 1. Snap
- `Snap(poke_set_t) -> snapped_vertex_t`

Interpretation:
Boundary perturbations induce an interior bias which is discretized by nearest-vertex snap in G60.

### 2. Return
- `Return(snapped_vertex_t) -> return_path_class_t`

Interpretation:
The snapped vertex determines a known fastest admissible path class back to center.

### 3. CenterUpdate
- `CenterUpdate(center_state_t, return_path_class_t; beta) -> center_state_{t+1}`

Interpretation:
The core integrates the closure receipt using the inward drain / collapse scale `beta = x^2`.

### 4. Emit
- `Emit(center_state_{t+1}; alpha) -> next_face_state_{t+1}`

Interpretation:
The center reissues the updated state to the boundary using the outward radiative scale `alpha = phi^3`.

## Candidate cycle law

The current candidate cycle is:

- `snapped_vertex_t = Snap(poke_set_t)`
- `return_path_class_t = Return(snapped_vertex_t)`
- `center_state_{t+1} = CenterUpdate(center_state_t, return_path_class_t; beta)`
- `next_face_state_{t+1} = Emit(center_state_{t+1}; alpha)`

A boundary-core-boundary recursion is then obtained by identifying:

- `poke_set_{t+1}` with some function of `next_face_state_{t+1}`

to be specified later.

## Interpretation of scales

### alpha = phi^3
Candidate role:

- ignition scale
- triadic packet scale
- outward radiative reissue scale

### beta = x^2
Candidate role:

- inward drain scale
- centerward collapse scale
- core resolution scale

## Minimal rigorous claims

### Claim 1
The scales are strongly asymmetric:

- `alpha >> beta`

Numerically:

- `4.2360679775 >> 0.0851761954`

### Claim 2
This asymmetry is consistent with the interpretation:

- `alpha` for excitation / launch / radiation
- `beta` for inward contraction / drain / collapse

### Claim 3
Any stronger statement, such as exact geometric derivation from the cube or G60 scaffold, remains conjectural until the maps `Snap`, `Return`, `CenterUpdate`, and `Emit` are instantiated explicitly.

## Formal conjecture

There exists a discrete boundary-core-boundary dynamical system on the anchored cube / G60 scaffold in which ignition and re-radiation are governed by `alpha = phi^3`, while centerward collapse is governed by `beta = x^2`, where `x` is the real root of `64x^3 + 63x^2 + 7x - 9 = 0`.

## Immediate next tasks

1. Define the admissible form of `poke_set`
2. Define the nearest-vertex snapping rule
3. Define the return-path-class library
4. Define the center update grammar
5. Define the face-state emission grammar

## Strongest sentence

The current rigorous scaffold is a boundary-core-boundary dynamical model with expansive scale `phi^3` and contractive scale `x^2`.

