from __future__ import annotations

import json
from collections import defaultdict
from copy import deepcopy
from itertools import combinations
from pathlib import Path


CORE = ["e00", "e01", "e02", "e04", "e05", "e07", "e10"]
BOUNDARY = ["e03", "e06", "e11", "e12", "e14", "e15"]
SPECTATORS = ["e13", "e16", "e22", "e25"]
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


def bridge_signature(edge_cocycle):
    r = (edge_cocycle["e00"] + edge_cocycle["e00"]) % 2
    q = (edge_cocycle["e00"] + edge_cocycle["e05"] + edge_cocycle["e10"] + edge_cocycle["e02"]) % 2
    w = (edge_cocycle["e00"] + edge_cocycle["e04"] + edge_cocycle["e07"] + edge_cocycle["e01"]) % 2
    return r, q, w


def invariants(edge_cocycle):
    A = edge_cocycle["e00"] % 2
    sigma = (edge_cocycle["e02"] + edge_cocycle["e05"] + edge_cocycle["e10"]) % 2
    tau = (edge_cocycle["e01"] + edge_cocycle["e04"] + edge_cocycle["e07"]) % 2
    return A, sigma, tau


def run_trial(source, flips):
    trial = deepcopy(source)
    for edge in flips:
        trial["lift_edges"] = flip_lift_pair(trial["lift_edges"], edge)
    cocycle = derive_edge_cocycle(trial)
    inv = invariants(cocycle)
    sig = bridge_signature(cocycle)
    return inv, sig


def main() -> None:
    source = load_json("specs/paper/bridge/signed_lift_source_v1.json")

    trials = []
    trials.append(("baseline", []))

    for e in CORE:
        trials.append((f"single_core_{e}", [e]))
    for e in BOUNDARY:
        trials.append((f"single_boundary_{e}", [e]))
    for e in SPECTATORS:
        trials.append((f"single_spectator_{e}", [e]))
    for e1, e2 in combinations(CORE, 2):
        trials.append((f"double_core_{e1}_{e2}", [e1, e2]))
    for label, edges in TRIPLE_SETS:
        trials.append((label, edges))

    by_invariant = defaultdict(list)
    by_signature = defaultdict(list)

    print("\n====================")
    print("CLUSTER INVARIANT ORBIT CLASSIFIER")
    print("====================\n")

    for label, flips in trials:
        inv, sig = run_trial(source, flips)
        by_invariant[inv].append((label, sig, flips))
        by_signature[sig].append((label, inv, flips))
        print(f"{label}")
        print(f"  flips      = {flips}")
        print(f"  invariants = A={inv[0]} sigma={inv[1]} tau={inv[2]}")
        print(f"  signature  = return={sig[0]} square={sig[1]} twist={sig[2]}")
        print()

    print("====================")
    print("BUCKETS BY INVARIANT TRIPLE")
    print("====================\n")
    for inv in sorted(by_invariant):
        items = by_invariant[inv]
        print(f"invariant {inv}  count={len(items)}")
        for label, sig, flips in items:
            print(f"  {label:28s} sig={sig} flips={flips}")
        print()

    print("====================")
    print("BUCKETS BY BRIDGE SIGNATURE")
    print("====================\n")
    for sig in sorted(by_signature):
        items = by_signature[sig]
        print(f"signature {sig}  count={len(items)}")
        for label, inv, flips in items:
            print(f"  {label:28s} inv={inv} flips={flips}")
        print()


if __name__ == "__main__":
    main()
