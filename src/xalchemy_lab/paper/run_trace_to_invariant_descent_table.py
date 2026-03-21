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


def invariants_from_cocycle(edge_cocycle):
    A = edge_cocycle["e00"] % 2
    sigma = (edge_cocycle["e02"] + edge_cocycle["e05"] + edge_cocycle["e10"]) % 2
    tau = (edge_cocycle["e01"] + edge_cocycle["e04"] + edge_cocycle["e07"]) % 2
    return A, sigma, tau


def bridge_signature(inv):
    A, sigma, tau = inv
    return 0, (A + sigma) % 2, (A + tau) % 2


def bridge_reading(trace):
    t = set(trace)
    if "A" in t and "O" in t:
        return "anchor-exchange / twist-side generator"
    if "D" in t:
        return "distal-defect regime"
    if trace == ("E2", "E2", "E2", "E2"):
        return "pure E2 closure residue"
    if "A" in t and ("E1" in t or "E2" in t):
        return "anchored even continuation"
    if "O" in t and ("E1" in t or "E2" in t):
        return "odd-branch continuation / mixed even closure"
    return "even-sheet / merged continuation"


def main() -> None:
    source = load_json("specs/paper/bridge/signed_lift_source_v1.json")
    gauge = load_json("specs/paper/bridge/resolved_edge_cocycle_v1.json")
    edge_cocycle = gauge["edge_cocycle"]

    inv = invariants_from_cocycle(edge_cocycle)
    sig = bridge_signature(inv)

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

                    trace = [SECTOR_BY_EDGE.get(e, "?") for e in cycle_edges]
                    tkey = canonical_trace(trace)
                    parity = sum(edge_cocycle[e] for e in cycle_edges) % 2
                    rows.append({
                        "vertices": [q0, q1, q2, q3, q0],
                        "edges": cycle_edges,
                        "trace": tkey,
                        "parity": parity,
                        "invariants": inv,
                        "bridge_signature": sig,
                        "reading": bridge_reading(tkey),
                    })

    rows.sort(key=lambda r: (r["parity"], r["trace"], r["edges"]))

    print("\n====================")
    print("TRACE TO INVARIANT DESCENT TABLE")
    print("====================\n")
    print(f"global local invariant state  = {inv}")
    print(f"global local bridge signature = {sig}\n")

    for row in rows:
        tag = "ODD " if row["parity"] == 1 else "EVEN"
        print(f"{tag}  trace={row['trace']}")
        print(f"  vertices         = {row['vertices']}")
        print(f"  edges            = {row['edges']}")
        print(f"  invariants       = {row['invariants']}")
        print(f"  bridge_signature = {row['bridge_signature']}")
        print(f"  reading          = {row['reading']}")
        print()

    out = {
        "name": "trace_to_invariant_descent_table_v1",
        "local_invariants": {
            "A": inv[0],
            "sigma": inv[1],
            "tau": inv[2],
        },
        "bridge_signature": {
            "return": sig[0],
            "square": sig[1],
            "twist": sig[2],
        },
        "rows": rows,
    }
    Path("specs/paper/g60/trace_to_invariant_descent_table_v1.json").write_text(json.dumps(out, indent=2) + "\n")
    print("Wrote specs/paper/g60/trace_to_invariant_descent_table_v1.json")


if __name__ == "__main__":
    main()
