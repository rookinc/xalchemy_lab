from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


# Refined toy sector model
SECTOR_BY_EDGE = {
    # anchor
    "e00": "A",

    # explicit odd branch
    "e01": "O",
    "e04": "O",
    "e07": "O",

    # even sheet 1
    "e02": "E1",
    "e05": "E1",
    "e08": "E1",
    "e10": "E1",
    "e11": "E1",
    "e12": "E1",
    "e15": "E1",

    # even sheet 2
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

    # merged continuation, apparently even-aligned
    "e16": "M+",
    "e18": "M+",
    "e19": "M+",
    "e21": "M+",
    "e26": "M+",

    # distal defect / outer odd candidates
    "e22": "D",
    "e27": "D",

    # unresolved outer edges
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


def refined_prediction(edges):
    """
    Refined falsifiable rule:

    odd if ANY of:
      1. anchor-exchange branch present: trace contains A and at least 2 O edges
      2. distal defect present with mixed sheet interaction:
         - contains D and at least one E1
         - or contains D and at least one E2
      3. pure distal E2 closure defect:
         - all four edges are E2

    else even.
    """
    trace = [SECTOR_BY_EDGE.get(e, "?") for e in edges]
    counts = defaultdict(int)
    for s in trace:
        counts[s] += 1

    if counts["A"] >= 1 and counts["O"] >= 2:
        return 1

    if counts["D"] >= 1 and (counts["E1"] >= 1 or counts["E2"] >= 1):
        return 1

    if counts["E2"] == 4:
        return 1

    return 0


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
                    predicted = refined_prediction(cycle_edges)
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
    print("SECTOR TRACE REFINED PROBE")
    print("====================\n")
    print("sector legend:")
    print("  A  = anchor")
    print("  O  = odd branch")
    print("  E1 = even sheet 1")
    print("  E2 = even sheet 2")
    print("  M+ = merged even-aligned continuation")
    print("  D  = distal defect carrier")
    print("  X  = unresolved outer continuation")
    print()

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
