from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


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
    gauge = load_json("specs/resolved_edge_cocycle_v1.json")
    edge_cocycle = gauge["edge_cocycle"]

    nbrs = defaultdict(list)
    edge_between = {}

    for label, u, v in source["base_edges"]:
        nbrs[u].append((v, label))
        nbrs[v].append((u, label))
        edge_between[frozenset((u, v))] = label

    seen = set()
    by_trace = defaultdict(list)

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

                    trace = [SECTOR_BY_EDGE.get(e, "?") for e in cycle_edges]
                    tkey = canonical_trace(trace)
                    parity = sum(edge_cocycle[e] for e in cycle_edges) % 2
                    by_trace[(tkey, parity)].append({
                        "vertices": [q0, q1, q2, q3, q0],
                        "edges": cycle_edges,
                    })

    print("\n====================")
    print("TRACE CLASS CATALOG")
    print("====================\n")

    for (trace, parity), rows in sorted(by_trace.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        tag = "EVEN" if parity == 0 else "ODD "
        print(f"{tag} trace={trace} count={len(rows)}")
        for row in rows:
            print(f"  vertices={row['vertices']} edges={row['edges']}")
        print()

    out = {
        "name": "trace_class_catalog_v1",
        "trace_classes": []
    }
    for (trace, parity), rows in sorted(by_trace.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        out["trace_classes"].append({
            "trace": list(trace),
            "parity": parity,
            "count": len(rows),
            "cycles": rows,
        })

    Path("specs/trace_class_catalog_v1.json").write_text(json.dumps(out, indent=2) + "\n")
    print("Wrote specs/trace_class_catalog_v1.json")


if __name__ == "__main__":
    main()
