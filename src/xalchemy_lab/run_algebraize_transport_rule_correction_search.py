from __future__ import annotations

import json
from collections import defaultdict
from itertools import combinations
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

    "e16": "M",
    "e18": "M",
    "e19": "M",
    "e21": "M",
    "e26": "M",

    "e22": "D",
    "e27": "D",

    "e28": "X",
    "e29": "X",
}

VARS = ["A", "O", "E1", "E2", "M", "D"]
CORR_VARS = ["O", "E1", "M", "D"]


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


def monomial_value(bits: dict[str, int], monomial: tuple[str, ...]) -> int:
    out = 1
    for v in monomial:
        out &= bits[v]
    return out


def polynomial_value(bits: dict[str, int], monomials: list[tuple[str, ...]]) -> int:
    total = 0
    for mono in monomials:
        total ^= monomial_value(bits, mono)
    return total


def features_from_edges(edges: list[str]) -> dict[str, int]:
    trace = [SECTOR_BY_EDGE.get(e, "?") for e in edges]
    present = {v: 0 for v in VARS}
    for s in trace:
        if s in present:
            present[s] = 1
    return present


def format_monomial(m: tuple[str, ...]) -> str:
    return "1" if len(m) == 0 else "*".join(m)


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

    rows = []
    seen = set()

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

                    bits = features_from_edges(cycle_edges)
                    actual = sum(edge_cocycle[e] for e in cycle_edges) % 2
                    rows.append({
                        "edges": cycle_edges,
                        "bits": bits,
                        "actual": actual,
                    })

    print("\n====================")
    print("ALGEBRAIZE TRANSPORT RULE CORRECTION SEARCH")
    print("====================\n")
    print(f"supported_cycles = {len(rows)}\n")

    # Degree <=2 base monomials
    base_monomials: list[tuple[str, ...]] = [()]
    for v in VARS:
        base_monomials.append((v,))
    for a, b in combinations(VARS, 2):
        base_monomials.append((a, b))

    # Degree 3/4 correction monomials only on exception variables
    correction_monomials: list[tuple[str, ...]] = []
    for r in (3, 4):
        for mono in combinations(CORR_VARS, r):
            correction_monomials.append(mono)

    print("correction candidates:")
    print("  " + ", ".join(format_monomial(m) for m in correction_monomials))
    print()

    best = None
    exact = []

    # Search sparse quadratic bases of size up to 3, plus optional one correction term
    for base_size in range(1, 4):
        print(f"searching base_size = {base_size}")
        for idxs in combinations(range(len(base_monomials)), base_size):
            base = [base_monomials[i] for i in idxs]

            # also test no correction
            for correction in [None] + correction_monomials:
                chosen = list(base)
                if correction is not None:
                    chosen.append(correction)

                failures = 0
                for row in rows:
                    pred = polynomial_value(row["bits"], chosen)
                    if pred != row["actual"]:
                        failures += 1
                        if best is None or failures >= best["failures"]:
                            break

                if best is None or failures < best["failures"]:
                    best = {"failures": failures, "monomials": chosen}

                if failures == 0:
                    exact.append(chosen)
                    print("  exact fit found:", " + ".join(format_monomial(m) for m in chosen))
        if exact:
            break

    print()
    if exact:
        print("====================")
        print("EXACT FITS")
        print("====================\n")
        for i, chosen in enumerate(exact, start=1):
            print(f"{i:02d}. Pi = " + " + ".join(format_monomial(m) for m in chosen))
        print()
    else:
        print("====================")
        print("BEST APPROXIMATION")
        print("====================\n")
        print(f"best_failures = {best['failures']}")
        print("Pi = " + " + ".join(format_monomial(m) for m in best["monomials"]))
        print()

    print("====================")
    print("DATA ROWS")
    print("====================\n")
    for row in rows:
        bitstr = " ".join(f"{k}={row['bits'][k]}" for k in VARS)
        print(f"actual={row['actual']}  {bitstr}  edges={row['edges']}")


if __name__ == "__main__":
    main()
