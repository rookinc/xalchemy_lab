# Symbolic Global Loop Roles Note

## Checkpoint

The bridge table now contains symbolic global loop bodies with role-level meaning.

Current intended roles:

### global_return
Representation:
- symbolic closed walk
- start at `q0`
- path `["x", "x^-1"]`

Meaning:
- simplest out-and-back loop
- leave the base quotient object by one admissible step
- return immediately by the formal reverse step

Bridge role:
- current global partner for local `w_LL`
- expected to be the cleanest even-sector candidate

---

### global_square
Representation:
- symbolic closed walk
- start at `q0`
- intended as a small ordinary cycle

Meaning:
- candidate untwisted small loop in the quotient picture
- one ordinary closed cycle around a local face / small cycle analogue

Bridge role:
- current global partner for local `w_bundled`

---

### global_twist
Representation:
- symbolic two-path loop
- start at `q0`
- path_1 and path_2 give two distinct symbolic routes

Meaning:
- comparison loop formed from two different ways of relating the same endpoints
- intended as the first natural odd-sector candidate family

Bridge role:
- current global partner for local `w_hold`, `w_LR_1`, and `w_LR_2`

---

## What is now true

The global bridge slots are no longer empty names.

They now have:
- symbolic bodies,
- intended loop roles,
- and human-readable interpretations.

What is still missing is:
- actual quotient/lift incidence data,
- actual signed-lift representatives,
- and actual cocycle evaluation.

---

## Current bridge reading

The bridge table now compares:

- local lift-bit values
against
- symbolic global loop specimens with stated intended meaning

This is stronger than placeholder labels, but still weaker than evaluated signed-lift data.

