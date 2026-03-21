from __future__ import annotations

from dataclasses import dataclass


STATES = [
    ("001_baseline", (0, 0, 1)),
    ("000_tau_off", (0, 0, 0)),
    ("011_sigma_on", (0, 1, 1)),
    ("010_sigma_on_tau_off", (0, 1, 0)),
    ("110_alt_preimage", (1, 1, 0)),
]


TRACE_ORDER = [
    ("A","O","O","O"),
    ("A","E1","E1","E1"),
    ("A","E2","E2","E2"),
    ("E1","E1","E1","O"),
    ("E1","E1","E1","E2"),
    ("D","E1","E1","E2"),
    ("D","E1","E1","M+"),
    ("D","E1","E2","E2"),
    ("E2","E2","E2","E2"),
    ("D","E1","O","M+"),
    ("E1","E1","M+","M+"),
    ("E1","E2","E2","E2"),
    ("E1","E2","M+","M+"),
    ("E1","M+","M+","O"),
    ("E2","E2","E2","O"),
]


@dataclass(frozen=True)
class ToyState:
    A: int
    sigma: int
    tau: int


def bridge_signature(s: ToyState) -> tuple[int, int, int]:
    return (0, (s.A + s.sigma) % 2, (s.A + s.tau) % 2)


def predict_trace_parity(s: ToyState) -> dict[tuple[str, ...], int]:
    """
    Toy G60 Automaton v1 descent rules.

    Control interpretation:
      tau   = anchor odd activation
      sigma = E1-sheet activation
      A     = anchored E1/E2 polarity swap + odd rearm

    Local laws encoded from the derived notes:
      - anchored odd trace depends on tau, but A can rearm it
      - anchored E1 trace depends on sigma, unless A swaps it away
      - anchored E2 trace turns on only in the swapped anchored state
      - distal odd backbone is rigid
      - rigid even backbone stays even
      - one mixed shuttle trace depends on tau off + sigma off
      - mixed cancellation trace stays even
    """
    out: dict[tuple[str, ...], int] = {}

    # Anchored control surface
    out[("A","O","O","O")]   = 1 if (s.tau == 1 or s.A == 1) else 0
    out[("A","E1","E1","E1")] = 1 if (s.sigma == 1 and s.A == 0) else 0
    out[("A","E2","E2","E2")] = 1 if (s.A == 1) else 0

    # Mixed shuttle / anchored-adjacent traces
    out[("E1","E1","E1","O")]  = 1 if (s.tau == 0 and s.sigma == 0 and s.A == 0) or (s.tau == 1 and s.sigma == 1 and s.A == 0) else 0
    out[("E1","E1","E1","E2")] = 1 if s.sigma == 1 else 0

    # Rigid odd backbone
    out[("D","E1","E1","E2")] = 1
    out[("D","E1","E1","M+")] = 1
    out[("D","E1","E2","E2")] = 1
    out[("E2","E2","E2","E2")] = 1

    # Rigid even backbone
    out[("D","E1","O","M+")] = 0
    out[("E1","E1","M+","M+")] = 0
    out[("E1","E2","E2","E2")] = 0
    out[("E1","E2","M+","M+")] = 0
    out[("E1","M+","M+","O")] = 0
    out[("E2","E2","E2","O")] = 0

    return out


def tag(x: int) -> str:
    return "ODD" if x else "EVEN"


def main() -> None:
    print("\n====================")
    print("TOY G60 AUTOMATON V1")
    print("====================\n")

    header = "trace".ljust(24) + "  " + "  ".join(name.ljust(22) for name, _ in STATES)
    print(header)
    print("-" * len(header))

    predicted_by_state: dict[str, dict[tuple[str, ...], int]] = {}

    for name, (A, sigma, tau) in STATES:
        s = ToyState(A=A, sigma=sigma, tau=tau)
        predicted_by_state[name] = predict_trace_parity(s)

    for trace in TRACE_ORDER:
        row = [str(trace).ljust(24)]
        for name, _ in STATES:
            row.append(tag(predicted_by_state[name][trace]).ljust(22))
        print("  ".join(row))

    print("\n====================")
    print("STATE SUMMARY")
    print("====================\n")
    for name, (A, sigma, tau) in STATES:
        s = ToyState(A=A, sigma=sigma, tau=tau)
        print(f"{name}")
        print(f"  invariants       = {(A, sigma, tau)}")
        print(f"  bridge_signature = {bridge_signature(s)}")
        print()

    print("Expected checks:")
    print("  001 baseline      -> anchored odd on, E1 anchor off, E2 anchor off")
    print("  000 tau off       -> anchored odd off, shuttle odd on")
    print("  011 sigma on      -> anchored odd on, E1 anchor on")
    print("  010 sigma/tau     -> anchored odd off, E1 anchor on")
    print("  110 alt preimage  -> anchored odd on, E2 anchor on, same bridge as 001")
    print()


if __name__ == "__main__":
    main()
