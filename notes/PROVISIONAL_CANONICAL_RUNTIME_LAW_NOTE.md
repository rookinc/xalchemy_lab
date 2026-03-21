# Provisional Canonical Runtime Law Note

## Status

The current state-sensitive routing table and sweep result are strong enough to serve as the provisional canonical runtime law for the minimal degree-3 local controller.

This means:

- the structural controller register `(A,sigma,tau)` is operational,
- the preferred exit law is explicit,
- burden-threshold override is integrated,
- transient switch memory is integrated,
- and the resulting controller behavior is auditable by artifact.

## Scope

This provisional canonical runtime law applies to the current minimal local setting:

- one incoming edge
- two candidate exits
- degree-3 controller
- explicit table-driven structural preference law

## Not yet claimed

This note does not claim that the current table is yet derived from the deepest geometric principle.

It is currently:

- explicit
- operational
- auditable
- non-collapsed
- and locally useful

So it should be treated as a provisional canonical runtime law, pending deeper derivation.

## Strongest sentence

The controller now has a provisional canonical runtime law: structural state selects the preferred local exit, burden may override it, and transient switch memory records the yield.

