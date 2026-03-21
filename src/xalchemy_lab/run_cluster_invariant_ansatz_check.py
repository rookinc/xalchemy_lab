from __future__ import annotations

import json
from copy import deepcopy
from itertools import combinations
from pathlib import Path


SINGLE_CORE = ["e00", "e01", "e02", "e04", "e05", "e07", "e10"]
SINGLE_BOUNDARY = ["e03", "e06", "e11", "e12", "e14", "e15"]
SINGLE_SPECTATOR = ["e13", "e16", "e22", "e25"]
TRIPLE_SETS = [
    ("twist_cluster", ["e01", "e04", "e07"]),
    ("square_cluster", ["e02", "e05", "e10"]),
]


def load_json(path: str):
    return json.loads(Path(path).read_text())


def sheet(v: str) -> str:
    if v.endswith("+"):
        return "+"
    if v.endswith("-"):
        return "-"
    raise ValueError(f"bad lift vertex: {v}")


def flip_lift_pair(rows, edge_label: str):
    out = []
    seen = 0
    for row in rows:
        label, u, v = row
        if label != edge_label:
            out.append(row)
            continue
        if "TBD" in u or "TBD" in v:
            raise ValueError(f"cannot flip unfilled edge {edge_label}")
        new_v = v[:-1] + ("-" if v.endswith("+") else "+")
        out.append([label, u, new_v])
        seen += 1
    if seen != 2:
        raise ValueError(f"edge {edge_label} appears {seen} times, expected 2")
    return out


def derive_edge_cocycle(data):
    lift_edges = {}
    for label, u, v in data["lift_edges"]:
        if "TBD" in u or "TBD" in v:
            continue
        lift_edges.setdefault(label, []).append((u, v))

    result = {}
    for label, _u0, _v0 in data["base_edges"]:
        pairs = lift_edges.get(label, [])
        if len(pairs) == 0:
            continue
        if len(pairs) != 2:
            raise ValueError(f"base edge {label} has partial lift data")
        crossed0 = sheet(pairs[0][0]) != sheet(pairs[0][1])
        crossed1 = sheet(pairs[1][0]) != sheet(pairs[1][1])
        if crossed0 != crossed1:
            raise ValueError(f"inconsistent lift type for {label}")
        result[label] = 1 if crossed0 else 0
    return result


def actual_bridge_signature(edge_cocycle):
    r = (edge_cocycle["e00"] + edge_cocycle["e00"]) % 2
    q = (edge_cocycle["e00"] + edge_cocycle["e05"] + edge_cocycle["e10"] + edge_cocycle["e02"]) % 2
    w = (edge_cocycle["e00"] + edge_cocycle["e04"] + edge_cocycle["e07"] + edge_cocycle["e01"]) % 2
    return r, q, w


def ansatz_invariants(edge_cocycle):
    A = edge_cocycle["e00"] % 2
    sigma = (edge_cocycle["e02"] + edge_cocycle["e05"] + edge_cocycle["e10"]) % 2
    tau = (edge_cocycle["e01"] + edge_cocycle["e04"] + edge_cocycle["e07"]) % 2
    return A, sigma, tau


def ansatz_signature(edge_cocycle):
    A, sigma, tau = ansatz_invariants(edge_cocycle)
    return 0, (A + sigma) % 2, (A + tau) % 2


def run_trial(label: str, source, flips: list[str]):
    trial = deepcopy(source)
    for edge in flips:
        trial["lift_edges"] = flip_lift_pair(trial["lift_edges"], edge)
    cocycle = derive_edge_cocycle(trial)
    actual = actual_bridge_signature(cocycle)
    predicted = ansatz_signature(cocycle)
    A, sigma, tau = ansatz_invariants(cocycle)
    ok = actual == predicted
    print(label)
    print(f"  flips            = {flips}")
    print(f"  invariants       = A={A} sigma={sigma} tau={tau}")
    print(f"  actual_signature = return={actual[0]} square={actual[1]} twist={actual[2]}")
    print(f"  ansatz_signature = return={predicted[0]} square={predicted[1]} twist={predicted[2]}")
    print(f"  ansatz_match     = {'YES' if ok else 'NO'}")
    print()


def main() -> None:
    source = load_json("specs/signed_lift_source_v1.json")

    print("\n====================")
    print("CLUSTER INVARIANT ANSATZ CHECK")
    print("====================\n")

    run_trial("baseline", source, [])

    for edge in SINGLE_CORE:
        run_trial(f"single_core_{edge}", source, [edge])

    for edge in SINGLE_BOUNDARY:
        run_trial(f"single_boundary_{edge}", source, [edge])

    for edge in SINGLE_SPECTATOR:
        run_trial(f"single_spectator_{edge}", source, [edge])

    for e1, e2 in combinations(SINGLE_CORE, 2):
        run_trial(f"double_core_{e1}_{e2}", source, [e1, e2])

    for label, edges in TRIPLE_SETS:
        run_trial(label, source, edges)


if __name__ == "__main__":
    main()
