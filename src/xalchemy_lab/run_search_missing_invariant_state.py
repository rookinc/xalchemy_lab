from __future__ import annotations

import json
from copy import deepcopy
from itertools import product
from pathlib import Path


SQUARE_CLUSTER = ["e02", "e05", "e10"]
TWIST_CLUSTER = ["e01", "e04", "e07"]
TARGET = (1, 1, 0)


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
        if len(pairs) != 2:
            continue
        crossed0 = sheet(pairs[0][0]) != sheet(pairs[0][1])
        crossed1 = sheet(pairs[1][0]) != sheet(pairs[1][1])
        if crossed0 != crossed1:
            raise ValueError(f"inconsistent lift type for {label}")
        result[label] = 1 if crossed0 else 0
    return result


def invariants(edge_cocycle):
    A = edge_cocycle["e00"] % 2
    sigma = (edge_cocycle["e02"] + edge_cocycle["e05"] + edge_cocycle["e10"]) % 2
    tau = (edge_cocycle["e01"] + edge_cocycle["e04"] + edge_cocycle["e07"]) % 2
    return A, sigma, tau


def signature(inv):
    A, sigma, tau = inv
    return 0, (A + sigma) % 2, (A + tau) % 2


def main() -> None:
    source = load_json("specs/signed_lift_source_v1.json")

    print("\n====================")
    print("SEARCH MISSING INVARIANT STATE")
    print("====================\n")
    print(f"target = {TARGET}")
    print(f"target_signature = {signature(TARGET)}\n")

    hits = []

    for s_edge, t_edge in product(SQUARE_CLUSTER, TWIST_CLUSTER):
        flips = ["e00", s_edge, t_edge]
        trial = deepcopy(source)
        for edge in flips:
            trial["lift_edges"] = flip_lift_pair(trial["lift_edges"], edge)
        cocycle = derive_edge_cocycle(trial)
        inv = invariants(cocycle)
        sig = signature(inv)
        is_hit = inv == TARGET
        if is_hit:
            hits.append((flips, sig))
        print(f"flips={flips} -> invariants={inv} signature={sig} hit={'YES' if is_hit else 'NO'}")

    print()
    print(f"hits = {len(hits)}")
    for flips, sig in hits:
        print(f"  realized by flips={flips} signature={sig}")


if __name__ == "__main__":
    main()
