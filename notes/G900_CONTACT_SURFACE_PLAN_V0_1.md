# G900 contact surface plan v0.1

## Current position

The order-30 triangular subdivision carrier has now been probed in three distinct ways:

1. layer structure
2. macro structure
3. live-bit structure

Visible results so far:

- 900 smallest triangular cells
- 10 inward layers
- 3 macro classes
- 2 live-bit classes

So the current candidate object is no longer just a count.
It is a classified carrier.

---

## Next question

How do these classes touch?

We now want to measure the contact surface of the carrier under cell adjacency.

Meaning:

- which bit classes touch which bit classes
- which macro classes touch which macro classes
- which combined `(macro, bit)` classes touch which others
- how contact frequencies vary by inward layer

This is the first step toward a quotient candidate.

---

## Target outputs

We want the following adjacency summaries:

1. bit-to-bit contact table
2. macro-to-macro contact table
3. `(macro, bit)` to `(macro, bit)` contact table
4. optional layer-conditioned versions of the same

---

## Why this matters

If a quotient toward a smaller carrier exists, it will likely emerge through repeated contact regularities.

The most important question is not only:

> what classes exist?

but also:

> how do they interact?

A good quotient candidate should preserve a lawful contact structure, not merely a coloring.

---

## Immediate experiment

Build one probe that:

- enumerates all cell adjacencies
- assigns each cell:
  - layer
  - macro
  - bit
  - orient
- counts adjacency edges by class-pair

and prints:

- bit contact table
- macro contact table
- `(macro, bit)` contact histogram

---

## Success criterion

The probe is interesting if the contact tables are:

- sparse
- regular
- repeated
- symmetric in a meaningful way

A chaotic full-contact table would weaken the quotient hope.
A sparse patterned table would strengthen it.

