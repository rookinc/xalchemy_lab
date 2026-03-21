# Coherent N-Way Split Law (Polarity Symmetric)

## Statement

For coherent zero-mismatch triadic closure at either hub polarity:

- positive hub: coherent +++ at u1R
- negative hub: coherent --- at d1R

replacing a one-shot event by n coherent nonzero subevents with the same total incoming load preserves deposited stress and shifts the ledger by

    (-(n-1), 0, 0, +(n-1), 0)

with ledger coordinates ordered as

    (stress_energy, stored_tension, deposited_stress, clean_closures, tension_closures)

---

## Interpretation

This means the ledger is not additive in event decomposition, even in the clean coherent sector.

What is preserved:

- total deposited stress

What changes under splitting into n coherent subevents:

- stress_energy decreases by n-1
- clean_closures increases by n-1

What remains unchanged in this sector:

- stored_tension
- tension_closures

So the hub records not only total quantity, but also the granularity of arrival history.

---

## Positive-hub law

For coherent +++ at u1R, zero mismatch:

    Delta_ledger = split ledger - one-shot ledger = (-(n-1), 0, 0, +(n-1), 0)

This was verified for nontrivial 2-way and 3-way coherent splits on representative totals, including:

- (1,1,1)
- (2,1,0)
- (2,2,2)
- (3,2,1)

---

## Negative-hub mirror

For coherent --- at d1R, zero mismatch:

    Delta_ledger = split ledger - one-shot ledger = (-(n-1), 0, 0, +(n-1), 0)

The same 2-way and 3-way split law appeared on the negative hub.

Thus the law is polarity symmetric.

---

## Consequence

The coherent clean sector obeys a hub-intrinsic granularity law:

- deposited quantity is additive
- ledger bookkeeping is affine in event count
- event decomposition leaves a receipt-level signature

Equivalently:

    same total load != same ledger

once the total load is realized through different counts of coherent subevents.

---

## Carrier versus ledger

The sweep also showed that carrier final state may or may not match the one-shot event, depending on the total load and decomposition.

But ledger equality did not occur in the tested nontrivial splits.

So the stronger invariant is ledger-side, not carrier-side.

---

## Compact theorem form

Let L_1(S) denote the ledger produced by a one-shot coherent zero-mismatch closure of total load S, and let L_n(S) denote the ledger produced by any coherent decomposition of the same total load into n nonzero coherent subevents.

Then in the tested coherent clean sector:

    L_n(S) - L_1(S) = (-(n-1), 0, 0, +(n-1), 0)

with ledger coordinates ordered as

    (stress_energy, stored_tension, deposited_stress, clean_closures, tension_closures)

---

## Summary sentence

The coherent clean manifold is polarity symmetric and nonadditive under event splitting: total deposited load is preserved, but the ledger shifts by a universal (n-1) granularity law.
