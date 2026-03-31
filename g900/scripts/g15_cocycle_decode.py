from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

# ============================================================
# G15 = L(Petersen) cocycle decoding helper
# ============================================================

# Vertex order on G15
VERTICES = [
    "o0", "o1", "o2", "o3", "o4",
    "s0", "s1", "s2", "s3", "s4",
    "t0", "t1", "t2", "t3", "t4",
]

# Edge order on G15
EDGES = [
    ("o0", "o1"),  # e1
    ("o1", "o2"),  # e2
    ("o2", "o3"),  # e3
    ("o3", "o4"),  # e4
    ("o4", "o0"),  # e5

    ("o0", "s0"),  # e6
    ("o1", "s1"),  # e7
    ("o2", "s2"),  # e8
    ("o3", "s3"),  # e9
    ("o4", "s4"),  # e10

    ("o0", "s1"),  # e11
    ("o1", "s2"),  # e12
    ("o2", "s3"),  # e13
    ("o3", "s4"),  # e14
    ("o4", "s0"),  # e15

    ("s0", "t0"),  # e16
    ("s1", "t1"),  # e17
    ("s2", "t2"),  # e18
    ("s3", "t3"),  # e19
    ("s4", "t4"),  # e20

    ("s0", "t3"),  # e21
    ("s1", "t4"),  # e22
    ("s2", "t0"),  # e23
    ("s3", "t1"),  # e24
    ("s4", "t2"),  # e25

    ("t0", "t2"),  # e26
    ("t1", "t3"),  # e27
    ("t2", "t4"),  # e28
    ("t3", "t0"),  # e29
    ("t4", "t1"),  # e30
]

EDGE_LABELS = [f"e{i}" for i in range(1, 31)]
EDGE_INDEX: Dict[Tuple[str, str], int] = {}
for i, (u, v) in enumerate(EDGES):
    EDGE_INDEX[tuple(sorted((u, v)))] = i

VERTEX_INDEX = {v: i for i, v in enumerate(VERTICES)}

# Fundamental cycle basis from the note, in edge-label form.
CYCLE_EDGE_LABELS: List[List[str]] = [
    ["e1", "e2", "e3", "e4", "e5"],                       # C0
    ["e1", "e7", "e11"],                                  # C1
    ["e2", "e8", "e12"],                                  # C2
    ["e3", "e9", "e13"],                                  # C3
    ["e4", "e10", "e14"],                                 # C4
    ["e5", "e6", "e15"],                                  # C5
    ["e8", "e2", "e1", "e6", "e16", "e23"],              # C6
    ["e9", "e3", "e2", "e7", "e17", "e24"],              # C7
    ["e10", "e4", "e3", "e8", "e18", "e25"],             # C8
    ["e6", "e1", "e2", "e3", "e9", "e19", "e21"],        # C9
    ["e7", "e2", "e3", "e4", "e10", "e20", "e22"],       # C10
    ["e16", "e6", "e1", "e2", "e8", "e18", "e26"],       # C11
    ["e17", "e7", "e2", "e3", "e9", "e19", "e27"],       # C12
    ["e18", "e8", "e3", "e4", "e10", "e20", "e28"],      # C13
    ["e19", "e9", "e3", "e2", "e1", "e6", "e16", "e29"], # C14
    ["e20", "e10", "e4", "e3", "e2", "e7", "e17", "e30"] # C15
]


@dataclass
class Solution:
    weight: int
    edge_labels: List[str]
    closed: bool
    connected: bool
    support_type: str
    boundary_vertices: List[str]


def xor_dot(row: List[int], x: List[int]) -> int:
    s = 0
    for a, b in zip(row, x):
        s ^= (a & b)
    return s


def build_A() -> List[List[int]]:
    rows: List[List[int]] = []
    for cycle in CYCLE_EDGE_LABELS:
        row = [0] * len(EDGES)
        for label in cycle:
            idx = int(label[1:]) - 1
            row[idx] = 1
        rows.append(row)
    return rows


def build_B() -> List[List[int]]:
    rows = [[0] * len(EDGES) for _ in VERTICES]
    for j, (u, v) in enumerate(EDGES):
        rows[VERTEX_INDEX[u]][j] = 1
        rows[VERTEX_INDEX[v]][j] = 1
    return rows


def parse_syndrome(bits: str) -> List[int]:
    bits = bits.strip().replace(" ", "")
    if len(bits) != 16 or any(ch not in "01" for ch in bits):
        raise ValueError("Syndrome must be a 16-bit string of 0/1.")
    return [int(ch) for ch in bits]


def edge_vector_to_labels(x: List[int]) -> List[str]:
    return [EDGE_LABELS[i] for i, bit in enumerate(x) if bit == 1]


def build_support_graph(x: List[int]) -> Dict[str, Set[str]]:
    g: Dict[str, Set[str]] = defaultdict(set)
    for bit, (u, v) in zip(x, EDGES):
        if bit:
            g[u].add(v)
            g[v].add(u)
    return g


def connected_components(g: Dict[str, Set[str]]) -> List[Set[str]]:
    seen: Set[str] = set()
    comps: List[Set[str]] = []
    for v in g:
        if v in seen:
            continue
        comp: Set[str] = set()
        stack = [v]
        seen.add(v)
        while stack:
            u = stack.pop()
            comp.add(u)
            for w in g[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        comps.append(comp)
    return comps


def classify_support(x: List[int], B: List[List[int]]) -> Tuple[bool, bool, str, List[str]]:
    boundary = [xor_dot(row, x) for row in B]
    boundary_vertices = [VERTICES[i] for i, b in enumerate(boundary) if b == 1]
    closed = len(boundary_vertices) == 0

    g = build_support_graph(x)
    if not g:
        return closed, False, "empty", boundary_vertices

    comps = connected_components(g)
    connected = len(comps) == 1

    degrees = sorted(len(g[v]) for v in g)
    edge_count = sum(x)
    vertex_count = len(g)

    if connected and all(d == 2 for d in degrees):
        if edge_count == 6 and vertex_count == 6:
            return closed, connected, "C6", boundary_vertices
        return closed, connected, "cycle", boundary_vertices

    if connected:
        deg1 = sum(1 for d in degrees if d == 1)
        deg2 = sum(1 for d in degrees if d == 2)
        if deg1 == 2 and deg1 + deg2 == vertex_count:
            if edge_count == 6 and vertex_count == 7:
                return closed, connected, "P7", boundary_vertices
            return closed, connected, "path", boundary_vertices

    if closed and not connected and edge_count == 6:
        comp_sizes = sorted(sum(len(g[v]) for v in comp) // 2 for comp in comps)
        if comp_sizes == [3, 3]:
            return closed, connected, "C3+C3", boundary_vertices

    return closed, connected, "other", boundary_vertices


def solve_min_weight(syndrome: List[int], max_weight: int = 6) -> List[Solution]:
    A = build_A()
    B = build_B()
    n = len(EDGES)

    for w in range(max_weight + 1):
        sols: List[Solution] = []
        for support in itertools.combinations(range(n), w):
            x = [0] * n
            for idx in support:
                x[idx] = 1
            if all(xor_dot(row, x) == s for row, s in zip(A, syndrome)):
                closed, connected, support_type, boundary_vertices = classify_support(x, B)
                sols.append(Solution(
                    weight=w,
                    edge_labels=edge_vector_to_labels(x),
                    closed=closed,
                    connected=connected,
                    support_type=support_type,
                    boundary_vertices=boundary_vertices,
                ))
        if sols:
            return sols
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description="Decode minimum-weight cocycle representatives on G15.")
    parser.add_argument(
        "--syndrome",
        required=True,
        help="16-bit syndrome string, e.g. 0101010101010101",
    )
    parser.add_argument(
        "--max-weight",
        type=int,
        default=6,
        help="Maximum weight to search.",
    )
    parser.add_argument(
        "--json-out",
        default="",
        help="Optional JSON output path.",
    )
    args = parser.parse_args()

    syndrome = parse_syndrome(args.syndrome)
    sols = solve_min_weight(syndrome, max_weight=args.max_weight)

    payload = {
        "syndrome": "".join(str(b) for b in syndrome),
        "solution_count": len(sols),
        "solutions": [
            {
                "weight": s.weight,
                "edge_labels": s.edge_labels,
                "closed": s.closed,
                "connected": s.connected,
                "support_type": s.support_type,
                "boundary_vertices": s.boundary_vertices,
            }
            for s in sols
        ],
    }

    print(json.dumps(payload, indent=2))

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        print(f"\nWrote {args.json_out}")


if __name__ == "__main__":
    main()
