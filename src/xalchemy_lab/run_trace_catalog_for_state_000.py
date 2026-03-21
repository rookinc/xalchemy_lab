from __future__ import annotations

import json
from collections import defaultdict
from copy import deepcopy
from pathlib import Path


# Use a minimal realization of (0,0,0)
FLIPS = ["e01"]

SECTOR_BY_EDGE = {
    "e00": "A",
    "e01": "O", "e04": "O", "e07": "O",
    "e02": "E1", "e05": "E1", "e08": "E1", "e10": "E1", "e11": "E1", "e12": "E1", "e15": "E1",
    "e03": "E2", "e06": "E2", "e09": "E2", "e13": "E2", "e14": "E2", "e17": "E2", "e20": "E2", "e23": "E2", "e24": "E2", "e25": "E2",
    "e16": "M+", "e18": "M+", "e19": "M+", "e21": "M+", "e26": "M+",
    "e22": "D", "e27": "D",
    "e28": "X", "e29": "X",
}


def load_json(path: str):
    return json.loads(Path(path).read_text())


def sheet(v: str) -> str:
    if v.endswith("+"):
        return "+"
    if v.endswith("-"):
        return "-"
    raise ValueError(v)


def flip_lift_pair(rows, edge_label: str):
    out = []
    seen = 0
    for label, u, v in rows:
        if label != edge_label:
            out.append([label, u, v])
            continue
        new_v = v[:-1] + ("-" if v.endswith("+") else "+")
        out.append([label, u, new_v])
        seen += 1
    if seen != 2:
        raise ValueError(f"{edge_label} appears {seen} times")
    return out


def derive_edge_cocycle(data):
    lift_edges = defaultdict(list)
    for label, u, v in data["lift_edges"]:
        lift_edges[label].append((u, v))

    result = {}
    for label, _u, _v in data["base_edges"]:
        pairs = lift_edges[label]
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


def bridge_signature(inv):
    A, sigma, tau = inv
    return 0, (A + sigma) % 2, (A + tau) % 2


def canonical_cycle(edges):
    n = len(edges)
    rots = [tuple(edges[i:] + edges[:i]) for i in range(n)]
    rev = list(reversed(edges))
    rots += [tuple(rev[i:] + rev[:i]) for i in range(n)]
    return min(rots)


def canonical_trace(trace):
    n = len(trace)
    rots = [tuple(trace[i:] + trace[:i]) for i in range(n)]
    rev = list(reversed(trace))
    rots += [tuple(rev[i:] + rev[:i]) for i in range(n)]
    return min(rots)


def main() -> None:
    source = load_json("specs/signed_lift_source_v1.json")
    trial = deepcopy(source)
    for edge in FLIPS:
        trial["lift_edges"] = flip_lift_pair(trial["lift_edges"], edge)

    edge_cocycle = derive_edge_cocycle(trial)
    inv = invariants(edge_cocycle)
    sig = bridge_signature(inv)

    nbrs = defaultdict(list)
    edge_between = {}
    for label, u, v in trial["base_edges"]:
        nbrs[u].append((v, label))
        nbrs[v].append((u, label))
        edge_between[frozenset((u, v))] = label

    seen = set()
    rows = []
    by_trace = defaultdict(int)

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
                    parity = sum(edge_cocycle[e] for e in cycle_edges) % 2
                    trace = canonical_trace([SECTOR_BY_EDGE.get(e, "?") for e in cycle_edges])
                    rows.append((parity, trace, [q0, q1, q2, q3, q0], cycle_edges))
                    by_trace[(parity, trace)] += 1

    rows.sort(key=lambda r: (r[0], r[1], r[3]))

    print("\n====================")
    print("TRACE CATALOG FOR STATE (0,0,0)")
    print("====================\n")
    print(f"flips              = {FLIPS}")
    print(f"invariants         = {inv}")
    print(f"bridge_signature   = {sig}\n")

    for parity, trace, verts, edges in rows:
        tag = "ODD " if parity == 1 else "EVEN"
        print(f"{tag} trace={trace}")
        print(f"  vertices = {verts}")
        print(f"  edges    = {edges}")
        print()

    print("====================")
    print("TRACE SUMMARY")
    print("====================\n")
    for (parity, trace), count in sorted(by_trace.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        tag = "ODD " if parity == 1 else "EVEN"
        print(f"{tag} trace={trace} count={count}")


if __name__ == "__main__":
    main()
