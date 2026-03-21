from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ANCHOR = "e00"
ENDS = [("q0", "q1"), ("q1", "q0")]


def load_json(path: str):
    return json.loads(Path(path).read_text())


def main() -> None:
    source = load_json("specs/paper/bridge/signed_lift_source_v1.json")
    gauge = load_json("specs/paper/bridge/resolved_edge_cocycle_v1.json")
    edge_cocycle = gauge["edge_cocycle"]

    nbrs = defaultdict(list)
    edge_between = {}

    for label, u, v in source["base_edges"]:
        nbrs[u].append((v, label))
        nbrs[v].append((u, label))
        edge_between[frozenset((u, v))] = label

    print("\n====================")
    print("GEOMETRIC DERIVATION: ANCHOR TWO-SIDED FAN")
    print("====================\n")

    for start, end in ENDS:
        print(f"view through anchor {start}->{end}\n")

        # neighbors beyond the end vertex, excluding the anchor start
        branches = []
        for nxt, e1 in sorted(nbrs[end], key=lambda x: x[1]):
            if nxt == start:
                continue

            # close a 4-cycle start -> end -> nxt -> mid -> start
            found = False
            for mid, e2 in nbrs[nxt]:
                if mid in {start, end}:
                    continue
                if frozenset((mid, start)) not in edge_between:
                    continue
                e3 = edge_between[frozenset((mid, start))]
                cycle_edges = [ANCHOR, e1, e2, e3]
                if any(e not in edge_cocycle for e in cycle_edges):
                    continue
                parity = sum(edge_cocycle[e] for e in cycle_edges) % 2
                cycle = [start, end, nxt, mid, start]
                branches.append((parity, cycle, cycle_edges))
                found = True
                break

            if not found:
                branches.append((None, [start, end, nxt], [ANCHOR, e1]))

        branches.sort(key=lambda x: (2 if x[0] is None else x[0], x[2]))

        for parity, cycle, edges in branches:
            if parity is None:
                print(f"UNRESOLVED  cycle_prefix={cycle}  edges={edges}")
            else:
                tag = "EVEN" if parity == 0 else "ODD"
                print(f"{tag:4s}  cycle={cycle}  edges={edges}  packet={edges[1:]}")
        print()


if __name__ == "__main__":
    main()
