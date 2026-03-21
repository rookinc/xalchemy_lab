from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def canonical_cycle(edges: list[str]) -> tuple[str, ...]:
    n = len(edges)
    rots = []
    for i in range(n):
        rots.append(tuple(edges[i:] + edges[:i]))
    rev = list(reversed(edges))
    for i in range(n):
        rots.append(tuple(rev[i:] + rev[:i]))
    return min(rots)


def main() -> None:
    source = load_json("specs/paper/bridge/signed_lift_source_v1.json")
    gauge = load_json("specs/paper/bridge/resolved_edge_cocycle_v1.json")
    edge_cocycle = gauge["edge_cocycle"]

    base_edges = source["base_edges"]

    nbrs: dict[str, list[tuple[str, str]]] = defaultdict(list)
    edge_between: dict[frozenset[str], str] = {}

    for label, u, v in base_edges:
        nbrs[u].append((v, label))
        nbrs[v].append((u, label))
        edge_between[frozenset((u, v))] = label

    seen: set[tuple[str, ...]] = set()
    found: list[tuple[list[str], list[str], int]] = []
    skipped = 0

    vertices = sorted(nbrs.keys())

    for q0 in vertices:
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
                        skipped += 1
                        continue

                    parity = sum(int(edge_cocycle[e]) for e in cycle_edges) % 2
                    cycle_vertices = [q0, q1, q2, q3, q0]
                    found.append((cycle_vertices, cycle_edges, parity))

    print("\n====================")
    print("SEARCH EVEN SQUARE CANDIDATES")
    print("====================\n")

    if not found:
        print("No fully-supported 4-cycles found under current partial cocycle.")
        print(f"skipped_4cycles = {skipped}")
        return

    found.sort(key=lambda item: (item[2], item[1]))

    even_count = 0
    odd_count = 0

    for verts, edges, parity in found:
        tag = "EVEN" if parity == 0 else "ODD"
        if parity == 0:
            even_count += 1
        else:
            odd_count += 1
        print(f"{tag:4s}  vertices={verts}  edges={edges}  parity={parity}")

    print()
    print(f"supported_4cycles = {len(found)}")
    print(f"skipped_4cycles   = {skipped}")
    print(f"even_4cycles      = {even_count}")
    print(f"odd_4cycles       = {odd_count}")
    print()


if __name__ == "__main__":
    main()
