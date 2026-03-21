# Order Defect Classification Table

Let:

- `C` = clean triadic closure
- `T` = tension triadic closure

Compare the two composites:

- `C -> T`
- `T -> C`

Observables:

- `S` = final carrier stress
- `L` = final ledger state

Legend:

- `Y` = commutes
- `N` = does not commute

| case | initial stress | zero lane present? | carrier commutes? | ledger commutes? | class |
|---|---:|---:|---:|---:|---|
| s000 | (0,0,0) | yes | N | N | boundary order defect |
| s100 | (1,0,0) | yes | N | N | boundary order defect |
| s210 | (2,1,0) | yes | N | N | boundary order defect |
| s321 | (3,2,1) | no | Y | N | interior ledger path dependence |

## Class I. Boundary order defect

A state belongs to **Class I** when at least one stress lane is zero and the two-event composites `C -> T` and `T -> C` produce different final carrier stress.

Empirically:

- `s000`
- `s100`
- `s210`

This is the support-boundary noncommutativity class.

## Class II. Interior ledger path dependence

A state belongs to **Class II** when all lanes are strictly positive and the two-event composites `C -> T` and `T -> C` produce the same final carrier stress but different final ledger state.

Empirically:

- `s321`

This is the ledger-only noncommutativity class.

## Proposition

In the present tri-patch closure algebra, the operators `C` and `T` do not commute in general.

More precisely:

1. On the zero-support boundary of carrier stress space, noncommutativity is visible in both:
   - final carrier stress
   - final ledger state

2. Off the zero-support boundary, carrier stress may commute while ledger state remains noncommutative.

## Compact notation

Let:

- `S_X(s)` denote the final carrier stress after operator word `X`
- `L_X(s)` denote the final ledger state after operator word `X`

Then the current observations are:

- for `s000, s100, s210`:
  - `S_CT(s) != S_TC(s)`
  - `L_CT(s) != L_TC(s)`

- for `s321`:
  - `S_CT(s) = S_TC(s)`
  - `L_CT(s) != L_TC(s)`

## Summary

The closure algebra exhibits a **two-tier order defect**:

- carrier-level noncommutativity is concentrated on zero-support lanes
- ledger-level noncommutativity persists even where carrier stress itself commutes
