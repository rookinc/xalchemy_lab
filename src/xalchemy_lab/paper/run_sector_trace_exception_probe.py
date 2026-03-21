from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


SECTOR_BY_EDGE = {
    "e00": "A",

    "e01": "O",
    "e04": "O",
    "e07": "O",

    "e02": "E1",
    "e05": "E1",
    "e08": "E1",
    "e10": "E1",
    "e11": "E1",
    "e12": "E1",
    "e15": "E1",

    "e03": "E2",
    "e06": "E2",
    "e09": "E2",
    "e13": "E2",
    "e14": "E2",
    "e17": "E2",
    "e20": "E2",
    "e23": "E2",
    "e24": "E2",
    "e25": "E2",

    "e16": "M+",
    "e18": "M+",
    "e19": "M+",
    "e21": "M+",
    "e26": "M+",

    "e22": "D",
    "e27": "D",

    "e28": "X",
    "e29": "X",
}


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


def canonical_trace(trace):
    n = len(trace)
    rots = []
    for i in range(n):
        rots.append(tuple(trace[i:] + trace[:i]))
    rev = list(reversed(trace))
    for i in range(n):
        rots.append(tuple(rev[i:] + rev[:i]))
    return min(rots)


EXCEPTION_TRACE = canonical_trace(["M+", "O", "E1", "D"])


def exception_prediction(edges):
    trace = [SECTOR_BY_EDGE.get(e, "?") for e in edges]
    ctr = defaultdict(int)
    for s in trace:
        ctr[s] += 1

    # 1. anchor oddness
    if ctr["A"] >= 1 and ctr["O"] >= 2:
        return 1

    # 2. special cancellation exception
    if canonical_trace(trace) == EXCEPTION_TRACE:
        return 0

    # 3. distal defect oddness
    if ctr["D"] >= 1 and (ctr["E1"] >= 1 or ctr["E2"] >= 1):
        return 1

    # 4. pure distal E2 oddness
    if ctr["E2"] == 4:
        return 1

    return 0


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

                    actual = sum(edge_cocycle[e] for e in cycle_edges) % 2
                    trace = [SECTOR_BY_EDGE.get(e, "?") for e in cycle_edges]
                    predicted = exception_prediction(cycle_edges)
                    rows.append({
                        "vertices": [q0, q1, q2, q3, q0],
                        "edges": cycle_edges,
                        "trace": trace,
                        "actual": actual,
                        "predicted": predicted,
                        "match": actual == predicted,
                    })

    rows.sort(key=lambda r: (r["actual"], r["trace"], r["edges"]))

    print("\n====================")
    print("SECTOR TRACE EXCEPTION PROBE")
    print("====================\n")
    print(f"exception_trace = {EXCEPTION_TRACE}\n")

    matches = 0
    failures = []
    for row in rows:
        tag = "EVEN" if row["actual"] == 0 else "ODD "
        pred = "EVEN" if row["predicted"] == 0 else "ODD "
        ok = "PASS" if row["match"] else "FAIL"
        if row["match"]:
            matches += 1
        else:
            failures.append(row)
        print(f"{tag}  pred={pred}  {ok}")
        print(f"  vertices = {row['vertices']}")
        print(f"  edges    = {row['edges']}")
        print(f"  sectors  = {row['trace']}")
        print()

    print(f"total_cycles = {len(rows)}")
    print(f"matches      = {matches}")
    print(f"failures     = {len(rows) - matches}")
    print()

    if failures:
        print("remaining failures")
        for row in failures:
            print(f"  actual={row['actual']} predicted={row['predicted']} edges={row['edges']} sectors={row['trace']}")
        print()


if __name__ == "__main__":
    main()
