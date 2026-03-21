from __future__ import annotations

import json
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any


BASE_EDGES_TO_TEST = ["e01", "e02", "e05", "e16", "e22", "e25"]


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def sheet(v: str) -> str:
    if v.endswith("+"):
        return "+"
    if v.endswith("-"):
        return "-"
    raise ValueError(f"bad lift vertex: {v}")


def flip_lift_pair(rows: list[list[str]], edge_label: str) -> list[list[str]]:
    out = []
    seen = 0
    for row in rows:
        label, u, v = row
        if label != edge_label:
            out.append(row)
            continue

        if "TBD" in u or "TBD" in v:
            raise ValueError(f"cannot flip unfilled edge {edge_label}")

        # Parallel <-> crossed by flipping target sheet.
        if seen == 0:
            new_v = v[:-1] + ("-" if v.endswith("+") else "+")
            out.append([label, u, new_v])
        elif seen == 1:
            new_v = v[:-1] + ("-" if v.endswith("+") else "+")
            out.append([label, u, new_v])
        else:
            raise ValueError(f"edge {edge_label} appears more than twice")
        seen += 1

    if seen != 2:
        raise ValueError(f"edge {edge_label} appears {seen} times, expected 2")
    return out


def derive_edge_cocycle(data: dict[str, Any]) -> dict[str, int]:
    lift_edges: dict[str, list[tuple[str, str]]] = {}
    for label, u, v in data["lift_edges"]:
        if "TBD" in u or "TBD" in v:
            continue
        lift_edges.setdefault(label, []).append((u, v))

    result: dict[str, int] = {}
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


def canonical_cycle(edges: list[str]) -> tuple[str, ...]:
    n = len(edges)
    rots = []
    for i in range(n):
        rots.append(tuple(edges[i:] + edges[:i]))
    rev = list(reversed(edges))
    for i in range(n):
        rots.append(tuple(rev[i:] + rev[:i]))
    return min(rots)


def scan_4cycles(source: dict[str, Any], edge_cocycle: dict[str, int]) -> tuple[int, int, int]:
    base_edges = source["base_edges"]
    nbrs: dict[str, list[tuple[str, str]]] = defaultdict(list)
    edge_between: dict[frozenset[str], str] = {}

    for label, u, v in base_edges:
        nbrs[u].append((v, label))
        nbrs[v].append((u, label))
        edge_between[frozenset((u, v))] = label

    seen: set[tuple[str, ...]] = set()
    even_count = 0
    odd_count = 0
    supported = 0

    for q0 in sorted(nbrs):
        for q1, e01 in nbrs[q0]:
            if q1 == q0:
                continue
            for q2, e12 in nbrs[q1]:
                if q2 in {q0, q1}:
                    continue
                for q3, e23 in nbrs[q2]:
                    if q3 in {q0, q1, q2}:
                        continue
                    if frozenset((q3, q0)) not in edge_between:
                        continue
                    e30 = edge_between[frozenset((q3, q0))]
                    cycle_edges = [e01, e12, e23, e30]
                    key = canonical_cycle(cycle_edges)
                    if key in seen:
                        continue
                    seen.add(key)
                    if any(e not in edge_cocycle for e in cycle_edges):
                        continue
                    parity = sum(edge_cocycle[e] for e in cycle_edges) % 2
                    supported += 1
                    if parity == 0:
                        even_count += 1
                    else:
                        odd_count += 1

    return supported, even_count, odd_count


def bridge_signature(edge_cocycle: dict[str, int]) -> tuple[int, int, int]:
    # Current class representatives
    global_return = edge_cocycle["e00"] + edge_cocycle["e00"]
    global_square = edge_cocycle["e00"] + edge_cocycle["e05"] + edge_cocycle["e10"] + edge_cocycle["e02"]
    global_twist = edge_cocycle["e00"] + edge_cocycle["e04"] + edge_cocycle["e07"] + edge_cocycle["e01"]
    return global_return % 2, global_square % 2, global_twist % 2


def main() -> None:
    source = load_json("specs/signed_lift_source_v1.json")
    baseline_cocycle = derive_edge_cocycle(source)
    base_supported, base_even, base_odd = scan_4cycles(source, baseline_cocycle)
    base_sig = bridge_signature(baseline_cocycle)

    print("\n====================")
    print("BRIDGE ROBUSTNESS SINGLE-FLIP SWEEP")
    print("====================\n")

    print("baseline")
    print(f"  supported_4cycles = {base_supported}")
    print(f"  even_4cycles      = {base_even}")
    print(f"  odd_4cycles       = {base_odd}")
    print(f"  bridge_signature  = return={base_sig[0]} square={base_sig[1]} twist={base_sig[2]}")
    print()

    for edge_label in BASE_EDGES_TO_TEST:
        trial = deepcopy(source)
        trial["lift_edges"] = flip_lift_pair(trial["lift_edges"], edge_label)
        cocycle = derive_edge_cocycle(trial)
        supported, even_count, odd_count = scan_4cycles(trial, cocycle)
        sig = bridge_signature(cocycle)

        survives = sig == (0, 0, 1)

        print(f"flip {edge_label}")
        print(f"  supported_4cycles = {supported}")
        print(f"  even_4cycles      = {even_count}")
        print(f"  odd_4cycles       = {odd_count}")
        print(f"  bridge_signature  = return={sig[0]} square={sig[1]} twist={sig[2]}")
        print(f"  theorem_survives  = {'YES' if survives else 'NO'}")
        print()

if __name__ == "__main__":
    main()
