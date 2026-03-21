from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


# First toy sector model
SECTOR_BY_EDGE = {
    # anchor
    "e00": "A",

    # odd branch core
    "e01": "O",
    "e04": "O",
    "e07": "O",

    # chosen even sheet arm from anchor
    "e02": "E1",
    "e05": "E1",
    "e10": "E1",

    # sibling even sheet arm from anchor
    "e03": "E2",
    "e06": "E2",
    "e13": "E2",
}

# Optional extensions seen farther out
SECTOR_BY_EDGE.update({
    "e08": "E1",
    "e11": "E1",
    "e12": "E1",
    "e15": "E1",
    "e16": "M",
    "e18": "M",
    "e19": "M",
    "e21": "M",
    "e09": "E2",
    "e14": "E2",
    "e17": "E2",
    "e20": "E2",
    "e22": "M",
    "e23": "E2",
    "e24": "E2",
    "e25": "E2",
    "e26": "M",
    "e27": "M",
    "e28": "M",
    "e29": "M",
})


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


def sector_trace(edges):
    return [SECTOR_BY_EDGE.get(e, "?") for e in edges]


def simple_prediction(edges):
    """
    First toy predictive rule:
    - odd iff the cycle contains at least 2 O-sector edges
    - else even

    This is intentionally simple and falsifiable.
    """
    trace = sector_trace(edges)
    o_count = sum(1 for s in trace if s == "O")
    return 1 if o_count >= 2 else 0


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
                    predicted = simple_prediction(cycle_edges)
                    rows.append({
                        "vertices": [q0, q1, q2, q3, q0],
                        "edges": cycle_edges,
                        "trace": sector_trace(cycle_edges),
                        "actual": actual,
                        "predicted": predicted,
                        "match": actual == predicted,
                    })

    rows.sort(key=lambda r: (r["actual"], r["trace"], r["edges"]))

    print("\n====================")
    print("SECTOR TRACE PARITY PROBE")
    print("====================\n")
    print("sector legend:")
    print("  A  = anchor")
    print("  O  = odd branch")
    print("  E1 = chosen even sheet")
    print("  E2 = sibling even sheet")
    print("  M  = merged/outer continuation")
    print()

    matches = 0
    for row in rows:
        tag = "EVEN" if row["actual"] == 0 else "ODD "
        pred = "EVEN" if row["predicted"] == 0 else "ODD "
        ok = "PASS" if row["match"] else "FAIL"
        if row["match"]:
            matches += 1
        print(f"{tag}  pred={pred}  {ok}")
        print(f"  vertices = {row['vertices']}")
        print(f"  edges    = {row['edges']}")
        print(f"  sectors  = {row['trace']}")
        print()

    print(f"total_cycles = {len(rows)}")
    print(f"matches      = {matches}")
    print(f"failures     = {len(rows) - matches}")
    print()


if __name__ == "__main__":
    main()
