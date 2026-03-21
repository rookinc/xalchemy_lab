from __future__ import annotations

from dataclasses import dataclass


STATES = [
    ("000", (0, 0, 0)),
    ("001", (0, 0, 1)),
    ("010", (0, 1, 0)),
    ("011", (0, 1, 1)),
    ("100", (1, 0, 0)),
    ("101", (1, 0, 1)),
    ("110", (1, 1, 0)),
    ("111", (1, 1, 1)),
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
    out: dict[tuple[str, ...], int] = {}

    # Anchored grammar
    if s.A == 0:
        out[("A","O","O","O")]     = s.tau
        out[("A","E1","E1","E1")]  = s.sigma
        out[("A","E2","E2","E2")]  = 0
    else:
        out[("A","E2","E2","E2")]  = 1
        out[("A","E1","E1","E1")]  = 1 if (s.sigma, s.tau) in {(0,0), (0,1)} else 0
        out[("A","O","O","O")]     = 1 if (s.sigma, s.tau) in {(0,0), (1,0)} else 0

    # Shuttle / mixed anchored continuation
    if s.A == 0:
        out[("E1","E1","E1","O")]  = 1 if (s.sigma, s.tau) in {(0,0), (1,1)} else 0
    else:
        out[("E1","E1","E1","O")]  = 1 if (s.sigma, s.tau) in {(0,0), (1,1)} else 0

    out[("E1","E1","E1","E2")]     = s.sigma

    # Rigid odd backbone
    out[("D","E1","E1","E2")]      = 1
    out[("D","E1","E1","M+")]      = 1
    out[("D","E1","E2","E2")]      = 1
    out[("E2","E2","E2","E2")]     = 1

    # Rigid even backbone
    out[("D","E1","O","M+")]       = 0
    out[("E1","E1","M+","M+")]     = 0
    out[("E1","E2","E2","E2")]     = 0
    out[("E1","E2","M+","M+")]     = 0
    out[("E1","M+","M+","O")]      = 0
    out[("E2","E2","E2","O")]      = 0

    return out


def tag(x: int) -> str:
    return "ODD" if x else "EVEN"


def main() -> None:
    print("\n====================")
    print("TOY G60 AUTOMATON V2")
    print("====================\n")

    header = "trace".ljust(24) + "  " + "  ".join(name.ljust(8) for name, _ in STATES)
    print(header)
    print("-" * len(header))

    predicted_by_state: dict[str, dict[tuple[str, ...], int]] = {}
    for name, (A, sigma, tau) in STATES:
        predicted_by_state[name] = predict_trace_parity(ToyState(A=A, sigma=sigma, tau=tau))

    for trace in TRACE_ORDER:
        row = [str(trace).ljust(24)]
        for name, _ in STATES:
            row.append(tag(predicted_by_state[name][trace]).ljust(8))
        print("  ".join(row))

    print("\n====================")
    print("STATE SUMMARY")
    print("====================\n")
    for name, (A, sigma, tau) in STATES:
        s = ToyState(A=A, sigma=sigma, tau=tau)
        print(f"{name}  inv={(A, sigma, tau)}  bridge={bridge_signature(s)}")


if __name__ == "__main__":
    main()
