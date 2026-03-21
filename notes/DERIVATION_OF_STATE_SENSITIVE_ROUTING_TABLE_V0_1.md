# Derivation of State-Sensitive Routing Table v0.1

## Goal

Explain the current degree-3 structural routing table as a derived local frame law, not just a lookup artifact.

## Local setting

A degree-3 controller has:
- one incoming edge: `e_in`
- two candidate exits: `e_left`, `e_right`

The structural controller register is:
- `A`
- `sigma`
- `tau`

Handedness is:
- `left`
- `right`

---

## 1. Base chart orientation

The anchored chart bit `A` chooses the local frame orientation.

Base handed routing law:

### A = 0
- left  -> `e_left`
- right -> `e_right`

### A = 1
- left  -> `e_right`
- right -> `e_left`

So `A` reverses the base handed frame.

---

## 2. Unary collapse operators

Define two chart-relative collapse actions:

- `sigma` collapses to chart-left
- `tau` collapses to chart-right

Chart-relative meaning:

### for A = 0
- chart-left  = `e_left`
- chart-right = `e_right`

### for A = 1
- chart-left  = `e_right`
- chart-right = `e_left`

So:
- `sigma=1` pulls both handed choices toward chart-left
- `tau=1` pulls both handed choices toward chart-right

This explains:
- `001`
- `010`
- `101`
- `110`

---

## 3. Mixed-state reopening rule

When `sigma=tau=1`, the controller does not remain collapsed.
Instead it reopens a handed split.

In the current v0.1 law, both mixed states use the same reopened handed split:

- left  -> `e_right`
- right -> `e_left`

So:

### for A = 0
- `011` gives:
  - left  -> `e_right`
  - right -> `e_left`

### for A = 1
- `111` gives:
  - left  -> `e_right`
  - right -> `e_left`

Thus the mixed state is a reopened split state, while `A` continues to govern the base frame and unary collapse interpretation.

---

## 4. Resulting table

- `000`: left->`e_left`,  right->`e_right`
- `001`: left->`e_right`, right->`e_right`
- `010`: left->`e_left`,  right->`e_left`
- `011`: left->`e_right`, right->`e_left`
- `100`: left->`e_right`, right->`e_left`
- `101`: left->`e_left`,  right->`e_left`
- `110`: left->`e_right`, right->`e_right`
- `111`: left->`e_right`, right->`e_left`

---

## 5. Strongest sentence

The current table is derivable from:
- a chart-oriented base handed frame,
- a sigma collapse to chart-left,
- a tau collapse to chart-right,
- and a mixed-state reopening rule that restores the split `left->e_right`, `right->e_left`.

---

## 6. Status

This is a first derivation ansatz aligned to the currently implemented runtime law.

