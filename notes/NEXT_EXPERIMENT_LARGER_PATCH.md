# Next Experiment: Larger Local Patch

## Purpose

The current tri-turtle toy has reached a useful local threshold.

It now supports:

- hub polarity
- carried sign
- mismatch
- tensioned closure
- clean closure
- stored tension
- stress energy
- turtle-borne stress
- stress deposition
- free-flight damping

The current limitation is not the rule set.
The current limitation is the carrier.

Right now the toy lives on a very small scaffold:

- one upper hub `u1T`
- one lower hub `d1T`
- short side chains
- one direct spine

That is enough to discover local laws, but not enough to study longer transport.

We now need a slightly larger local patch so that stress can do more than:

- collide immediately
- or damp immediately

We want a patch large enough to support:

1. multi-hop transport
2. free-flight intervals
3. re-entry into a different hub
4. possible branching choices
5. repeated loading and unloading

---

## Current local toy summary

The present toy distinguishes:

- local polarity of a hub
- transported polarity on turtles
- mismatch between carried sign and site sign
- tensioned closure when mismatch is present
- clean closure when mismatch is absent
- stored hub tension
- cumulative hub stress energy
- turtle-borne carried stress
- deposited stress at later hubs
- damping during non-collision travel

This is already enough to justify expansion.

The next expansion should preserve the same laws while enlarging the carrier graph.

---

## Design goal for the larger patch

We do **not** need the full Thalean machinery yet.

We only need a bigger local patch with these properties:

- at least **4 signed hubs**
- at least **2 distinct routes** between some hubs
- at least **one route long enough** for free-flight damping to matter
- enough symmetry that mirror tests remain possible
- enough separation that transported stress can either:
  - arrive intact
  - partially damp
  - or fully damp before re-entry

The correct first question is not:
“what is the full final graph?”

The correct first question is:
“what is the smallest larger patch that can test hub-to-hub stress transport over distance?”

---

## Candidate patch shape

A good first candidate is a 4-hub ladder.

For example:

- top row hubs:
  - `u1L`
  - `u1R`

- bottom row hubs:
  - `d1L`
  - `d1R`

with side/interior connectors between them.

This does not need to be physically final.
It only needs to create a bigger transport arena.

One possible shape:

- upper left branch into `u1L`
- upper right branch into `u1R`
- lower left branch into `d1L`
- lower right branch into `d1R`
- cross-links or spine-links connecting upper and lower hubs
- optional mid-layer nodes between hubs

This gives:

- more than one hub per sign
- more than one possible destination
- actual travel distance

---

## Minimal requirements for the graph

The next patch should allow these experiment types.

### Experiment A: direct stress transfer
A stressed packet leaves one hub and reaches a neighboring hub quickly.

Question:
- does it remain strong enough to trigger tension there?

### Experiment B: delayed stress transfer
A stressed packet must travel through non-collision nodes before reaching another hub.

Question:
- does free-flight damping erase it before arrival?

### Experiment C: route competition
Two packets leave the same stressed source but take different routes.

Question:
- can one route preserve stress while another dissipates it?

### Experiment D: mirror symmetry
Repeat the same experiment in a mirrored polarity arrangement.

Question:
- are the results structurally symmetric?

### Experiment E: hub accumulation
Multiple stressed returns hit the same downstream hub over time.

Question:
- does the downstream hub become more tension-prone?

---

## Recommended new state variables

The existing state variables are still good and should remain.

### Per turtle
- `carry_sign`
- `mismatch_count`
- `carried_stress`
- `site_sign_history`

### Per hub
- `plus_arrivals`
- `minus_arrivals`
- `unsigned_arrivals`
- `mismatch_events`
- `transfers`
- `clean_closures`
- `tension_closures`
- `stored_tension`
- `stress_energy`
- `deposited_stress`

No new fields are required yet.
First enlarge the carrier.
Then only add new bookkeeping if the larger patch reveals a missing distinction.

---

## Strong working interpretation

The current toy should still be interpreted conservatively.

It is **not** electromagnetism.
It is a polarity-and-stress transport toy.

But the EM compass remains useful because the toy now clearly distinguishes:

- source polarity vs transported polarity
- local loading vs mobile load
- interaction-dense propagation vs free-flight decay
- reversible tension vs cumulative residue

That is enough to justify the next patch.

---

## Proposed implementation plan

### Step 1
Create a new file, for example:

- `src/xalchemy_lab/tri_patch_core.py`

This lets the larger patch evolve without breaking the current small toy.

### Step 2
Define a slightly larger graph with 4 hubs and intermediate transport nodes.

### Step 3
Port the current rules unchanged:
- sign carrying
- mismatch
- closure
- tension
- carried stress
- deposition
- damping

### Step 4
Create a new runner:
- `src/xalchemy_lab/run_tri_patch_test.py`

### Step 5
Implement 3 minimal scenarios:
- fast transfer
- delayed transfer
- route split

### Step 6
Compare outcomes:
- does stress survive?
- does it damp?
- does the destination hub inherit stress?
- does route length matter?

---

## Success criterion

The larger patch experiment succeeds if it can clearly show at least one of the following:

1. stress survives one route but not another
2. a downstream hub inherits stress from an upstream tension event
3. route length measurably changes closure quality
4. free-flight damping competes with deposition in a nontrivial way

If any one of those becomes visible, the larger patch is worth keeping.

---

## Bottom line

The current local toy has earned expansion.

The rules are now good enough.
The carrier is too small.

The next correct move is therefore:

**build a slightly larger local patch and keep the present rules fixed.**

That will tell us whether the current polarity–mismatch–stress machinery is merely a local curiosity or the beginning of a scalable transport system.

