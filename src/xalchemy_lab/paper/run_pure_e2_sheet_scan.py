from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


E2_EDGES = {"e03", "e06", "e09", "e13", "e14", "e17", "e20", "e23", "e24", "e25"}

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
    source = load_json("specs/paper/bridge/signed_lift_source_v1.json")
    gauge = load_json("specs/paper/bridge/resolved_edge_cocycle_v1.json")
    edge_cocycle = gauge["edge_cocycle"]

    nbrs = defaultdict(list)
    edge_between = {}

    for label, u, v in source["base_edges"]:
        nbrs[u].append((v, label))
        nbrs[v].append((u, label))
        edge_between[frozenset((u, v))] = label

    seen = set()
    rows = []

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
                    if not any(e in E2_EDGES for e in cycle_edges):
                        continue

                    trace = [SECTOR_BY_EDGE.get(e, "?") for e in cycle_edges]
                    e2_count = sum(1 for s in trace if s == "E2")
                    if e2_count < 2:
                        continue

                    parity = sum(edge_cocycle[e] for e in cycle_edges) % 2
                    rows.append({
                        "vertices": [q0, q1, q2, q3, q0],
                        "edges": cycle_edges,
                        "trace": tuple(trace),
                        "canon_trace": canonical_trace(trace),
                        "e2_count": e2_count,
                        "parity": parity,
                    })

    rows.sort(key=lambda r: (-r["e2_count"], r["parity"], r["canon_trace"], r["edges"]))

    print("\n====================")
    print("PURE E2 SHEET SCAN")
    print("====================\n")

    by_trace = defaultdict(list)
    odd_rows = []
    even_rows = []

    for row in rows:
        by_trace[(row["canon_trace"], row["parity"])].append(row)
        if row["parity"] == 1:
            odd_rows.append(row)
        else:
            even_rows.append(row)

    print("E2-heavy supported 4-cycles\n")
    for row in rows:
        tag = "ODD " if row["parity"] == 1 else "EVEN"
        print(f"{tag}  e2_count={row['e2_count']}  trace={row['canon_trace']}")
        print(f"  vertices = {row['vertices']}")
        print(f"  edges    = {row['edges']}")
        print()

    print("====================")
    print("TRACE CLASS SUMMARY")
    print("====================\n")
    for (trace, parity), items in sorted(by_trace.items(), key=lambda kv: (-sum(1 for s in kv[0][0] if s == 'E2'), kv[0][1], kv[0][0])):
        tag = "ODD " if parity == 1 else "EVEN"
        print(f"{tag}  trace={trace}  count={len(items)}")

    print("\n====================")
    print("INTERPRETIVE SUMMARY")
    print("====================\n")
    print(f"total_e2_heavy_cycles = {len(rows)}")
    print(f"odd_e2_heavy_cycles   = {len(odd_rows)}")
    print(f"even_e2_heavy_cycles  = {len(even_rows)}")

    pure_e2_odd = [r for r in odd_rows if r["canon_trace"] == ("E2", "E2", "E2", "E2")]
    print(f"pure_E2_odd_count     = {len(pure_e2_odd)}")

    if len(pure_e2_odd) == 1:
        print("\nreading: pure E2 oddness appears isolated in the current local patch.")
    elif len(pure_e2_odd) > 1:
        print("\nreading: pure E2 oddness propagates in multiple local realizations.")
    else:
        print("\nreading: no pure E2 odd class found in this scan.")


if __name__ == "__main__":
    main()
