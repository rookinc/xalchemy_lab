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
    if len(m) == 0:
        return "1"
    return "*".join(m)


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
                        "vertices": [q0, q1, q2, q3, q0],
                        "edges": cycle_edges,
                        "bits": bits,
                        "actual": actual,
                    })

    print("\n====================")
    print("ALGEBRAIZE TRANSPORT RULE SEARCH")
    print("====================\n")
    print(f"supported_cycles = {len(rows)}\n")

    # Build candidate monomials up to degree 2
    monomials: list[tuple[str, ...]] = [()]
    for v in VARS:
        monomials.append((v,))
    for a, b in combinations(VARS, 2):
        monomials.append((a, b))

    print("candidate monomials:")
    print("  " + ", ".join(format_monomial(m) for m in monomials))
    print()

    # Brute force over all XOR-subsets of monomials
    # There are 1 + 6 + 15 = 22 monomials, so 2^22 is too big.
    # Search by sparse support size up to 4 first.
    best = None
    exact_fits = []

    candidate_indices = list(range(len(monomials)))

    for support_size in range(1, 5):
        print(f"searching support_size = {support_size}")
        for idxs in combinations(candidate_indices, support_size):
            chosen = [monomials[i] for i in idxs]

            failures = 0
            for row in rows:
                pred = polynomial_value(row["bits"], chosen)
                if pred != row["actual"]:
                    failures += 1
                    if best is None or failures >= best["failures"]:
                        break

            if best is None or failures < best["failures"]:
                best = {
                    "failures": failures,
                    "monomials": chosen,
                }

            if failures == 0:
                exact_fits.append(chosen)
                print("  exact fit found:", " + ".join(format_monomial(m) for m in chosen))

        if exact_fits:
            break

    print()
    if exact_fits:
        print("====================")
        print("EXACT FITS")
        print("====================\n")
        for i, chosen in enumerate(exact_fits, start=1):
            expr = " + ".join(format_monomial(m) for m in chosen)
            print(f"{i:02d}. Pi = {expr}")
        print()
    else:
        print("====================")
        print("BEST APPROXIMATION")
        print("====================\n")
        expr = " + ".join(format_monomial(m) for m in best["monomials"])
        print(f"best_failures = {best['failures']}")
        print(f"Pi = {expr}")
        print()

    # Print truth rows for inspection
    print("====================")
    print("DATA ROWS")
    print("====================\n")
    for row in rows:
        bitstr = " ".join(f"{k}={row['bits'][k]}" for k in VARS)
        print(f"actual={row['actual']}  {bitstr}  edges={row['edges']}")


if __name__ == "__main__":
    main()
