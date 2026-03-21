from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


HINGES = ["e04", "e05"]


def load_json(path: str):
    return json.loads(Path(path).read_text())


def canonical_cycle(edges):
    n = len(edges)
    rots = []
    for i in range(n):
        rots.append(tuple(edges[i:] + edges[:i]))
    rev = list(reversed(edges))
    for i in range(n):
        rots.append(tuple(rev[i:] + rev[:i]))
    return min(rots)


def main() -> None:
    source = load_json("specs/signed_lift_source_v1.json")
    gauge = load_json("specs/resolved_edge_cocycle_v1.json")
    edge_cocycle = gauge["edge_cocycle"]

    nbrs = defaultdict(list)
    edge_between = {}

    for label, u, v in source["base_edges"]:
        nbrs[u].append((v, label))
        nbrs[v].append((u, label))
        edge_between[frozenset((u, v))] = label

    print("\n====================")
    print("GEOMETRIC DERIVATION: ARM DEPTH SCAN")
    print("====================\n")

    for hinge in HINGES:
        seen = set()
        cycles = []

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

                        if hinge not in cycle_edges:
                            continue
                        if any(e not in edge_cocycle for e in cycle_edges):
                            continue

                        parity = sum(edge_cocycle[e] for e in cycle_edges) % 2
                        verts = [q0, q1, q2, q3, q0]

                        if cycle_edges[0] != hinge:
                            for i in range(4):
                                rot_edges = cycle_edges[i:] + cycle_edges[:i]
                                rot_verts = verts[i:4] + verts[0:i+1]
                                if rot_edges[0] == hinge:
                                    cycle_edges = rot_edges
                                    verts = rot_verts
                                    break

                        cycles.append((parity, verts, cycle_edges))

        cycles.sort(key=lambda x: (x[0], x[2]))

        print(f"hinge = {hinge}\n")
        even = 0
        odd = 0
        for parity, verts, edges in cycles:
            tag = "EVEN" if parity == 0 else "ODD"
            if parity == 0:
                even += 1
            else:
                odd += 1
            print(f"{tag:4s}  cycle={verts}  edges={edges}  packet={edges[1:]}")
        print()
        print(f"hinge_cycles = {len(cycles)}")
        print(f"even_hinge_cycles = {even}")
        print(f"odd_hinge_cycles  = {odd}")
        print()

if __name__ == "__main__":
    main()
