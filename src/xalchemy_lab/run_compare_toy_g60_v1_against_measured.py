from __future__ import annotations

from dataclasses import dataclass


STATES = [
    ("001_baseline", (0, 0, 1)),
    ("000_tau_off", (0, 0, 0)),
    ("011_sigma_on", (0, 1, 1)),
    ("010_sigma_on_tau_off", (0, 1, 0)),
    ("110_alt_preimage", (1, 1, 0)),
]

TRACES = [
    ("A", "O", "O", "O"),
    ("A", "E1", "E1", "E1"),
    ("A", "E2", "E2", "E2"),
    ("E1", "E1", "E1", "O"),
    ("E1", "E1", "E1", "E2"),
    ("D", "E1", "E1", "E2"),
    ("D", "E1", "E1", "M+"),
    ("D", "E1", "E2", "E2"),
    ("E2", "E2", "E2", "E2"),
    ("D", "E1", "O", "M+"),
    ("E1", "E1", "M+", "M+"),
    ("E1", "E2", "E2", "E2"),
    ("E1", "E2", "M+", "M+"),
    ("E1", "M+", "M+", "O"),
    ("E2", "E2", "E2", "O"),
]


@dataclass(frozen=True)
class ToyState:
    A: int
    sigma: int
    tau: int


def predict_trace_parity(s: ToyState) -> dict[tuple[str, ...], int]:
    out: dict[tuple[str, ...], int] = {}
    out[("A","O","O","O")]    = 1 if (s.tau == 1 or s.A == 1) else 0
    out[("A","E1","E1","E1")] = 1 if (s.sigma == 1 and s.A == 0) else 0
    out[("A","E2","E2","E2")] = 1 if (s.A == 1) else 0
    out[("E1","E1","E1","O")] = 1 if ((s.tau == 0 and s.sigma == 0 and s.A == 0) or (s.tau == 1 and s.sigma == 1 and s.A == 0)) else 0
    out[("E1","E1","E1","E2")] = 1 if s.sigma == 1 else 0

    out[("D","E1","E1","E2")] = 1
    out[("D","E1","E1","M+")] = 1
    out[("D","E1","E2","E2")] = 1
    out[("E2","E2","E2","E2")] = 1

    out[("D","E1","O","M+")] = 0
    out[("E1","E1","M+","M+")] = 0
    out[("E1","E2","E2","E2")] = 0
    out[("E1","E2","M+","M+")] = 0
    out[("E1","M+","M+", "O")] = 0
    out[("E2","E2","E2","O")] = 0
    return out


# Measured from your local_trace_state_machine_delta_table output
MEASURED = {
    "001_baseline": {
        ("A","E1","E1","E1"):0, ("A","E2","E2","E2"):0, ("A","O","O","O"):1,
        ("D","E1","E1","E2"):1, ("D","E1","E1","M+"):1, ("D","E1","E2","E2"):1,
        ("D","E1","O","M+"):0, ("E1","E1","E1","E2"):0, ("E1","E1","E1","O"):0,
        ("E1","E1","M+","M+"):0, ("E1","E2","E2","E2"):0, ("E1","E2","M+","M+"):0,
        ("E1","M+","M+","O"):0, ("E2","E2","E2","E2"):1, ("E2","E2","E2","O"):0,
    },
    "000_tau_off": {
        ("A","E1","E1","E1"):0, ("A","E2","E2","E2"):0, ("A","O","O","O"):0,
        ("D","E1","E1","E2"):1, ("D","E1","E1","M+"):1, ("D","E1","E2","E2"):1,
        ("D","E1","O","M+"):0, ("E1","E1","E1","E2"):0, ("E1","E1","E1","O"):1,
        ("E1","E1","M+","M+"):0, ("E1","E2","E2","E2"):0, ("E1","E2","M+","M+"):0,
        ("E1","M+","M+","O"):0, ("E2","E2","E2","E2"):1, ("E2","E2","E2","O"):0,
    },
    "011_sigma_on": {
        ("A","E1","E1","E1"):1, ("A","E2","E2","E2"):0, ("A","O","O","O"):1,
        ("D","E1","E1","E2"):1, ("D","E1","E1","M+"):1, ("D","E1","E2","E2"):1,
        ("D","E1","O","M+"):0, ("E1","E1","E1","E2"):1, ("E1","E1","E1","O"):1,
        ("E1","E1","M+","M+"):0, ("E1","E2","E2","E2"):0, ("E1","E2","M+","M+"):0,
        ("E1","M+","M+","O"):0, ("E2","E2","E2","E2"):1, ("E2","E2","E2","O"):0,
    },
    "010_sigma_on_tau_off": {
        ("A","E1","E1","E1"):1, ("A","E2","E2","E2"):0, ("A","O","O","O"):0,
        ("D","E1","E1","E2"):1, ("D","E1","E1","M+"):1, ("D","E1","E2","E2"):1,
        ("D","E1","O","M+"):0, ("E1","E1","E1","E2"):1, ("E1","E1","E1","O"):0,
        ("E1","E1","M+","M+"):0, ("E1","E2","E2","E2"):0, ("E1","E2","M+","M+"):0,
        ("E1","M+","M+","O"):0, ("E2","E2","E2","E2"):1, ("E2","E2","E2","O"):0,
    },
    "110_alt_preimage": {
        ("A","E1","E1","E1"):0, ("A","E2","E2","E2"):1, ("A","O","O","O"):1,
        ("D","E1","E1","E2"):1, ("D","E1","E1","M+"):1, ("D","E1","E2","E2"):1,
        ("D","E1","O","M+"):0, ("E1","E1","E1","E2"):1, ("E1","E1","E1","O"):0,
        ("E1","E1","M+","M+"):0, ("E1","E2","E2","E2"):0, ("E1","E2","M+","M+"):0,
        ("E1","M+","M+","O"):0, ("E2","E2","E2","E2"):1, ("E2","E2","E2","O"):0,
    },
}


def tag(x: int) -> str:
    return "ODD" if x else "EVEN"


def main() -> None:
    print("\n====================")
    print("COMPARE TOY G60 V1 AGAINST MEASURED")
    print("====================\n")

    total = 0
    mismatches = 0

    for name, (A, sigma, tau) in STATES:
        s = ToyState(A=A, sigma=sigma, tau=tau)
        pred = predict_trace_parity(s)
        print(name)
        state_mismatches = 0
        for trace in TRACES:
            p = pred[trace]
            m = MEASURED[name][trace]
            total += 1
            if p != m:
                mismatches += 1
                state_mismatches += 1
                print(f"  FAIL {trace}: predicted={tag(p)} measured={tag(m)}")
        if state_mismatches == 0:
            print("  PASS")
        print()

    print(f"total_checks = {total}")
    print(f"mismatches   = {mismatches}")
    print(f"matches      = {total - mismatches}")


if __name__ == "__main__":
    main()
