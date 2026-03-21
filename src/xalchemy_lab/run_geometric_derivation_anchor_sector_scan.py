from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ANCHOR = "e00"


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

    seen = set()
    anchor_cycles = []
    other_edge_counts = Counter()

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

                    if ANCHOR not in cycle_edges:
                        continue

                    parity = sum(edge_cocycle[e] for e in cycle_edges) % 2
                    cycle_vertices = [q0, q1, q2, q3, q0]
                    anchor_cycles.append((cycle_vertices, cycle_edges, parity))

                    for e in cycle_edges:
                        if e != ANCHOR:
                            other_edge_counts[e] += 1

    print("\n====================")
    print("GEOMETRIC DERIVATION: ANCHOR SECTOR SCAN")
    print("====================\n")

    if not anchor_cycles:
        print("No supported 4-cycles contain the anchor edge.")
        return

    even = 0
    odd = 0
    for verts, edges, parity in anchor_cycles:
        tag = "EVEN" if parity == 0 else "ODD"
        if parity == 0:
            even += 1
        else:
            odd += 1
        print(f"{tag:4s}  vertices={verts}  edges={edges}  parity={parity}")

    print()
    print(f"anchor_cycles = {len(anchor_cycles)}")
    print(f"even_anchor_cycles = {even}")
    print(f"odd_anchor_cycles  = {odd}")
    print()

    print("co-occurring edges with e00")
    for edge, count in sorted(other_edge_counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {edge:3s}  count={count}")

    print()


if __name__ == "__main__":
    main()
