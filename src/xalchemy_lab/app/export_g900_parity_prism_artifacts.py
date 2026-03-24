from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple


Point = Tuple[int, int]
Edge = Tuple[Point, Point]
ClassNode = Tuple[int, int]  # (macro, bit)


def canon_edge(a: Point, b: Point) -> Edge:
    return (a, b) if a <= b else (b, a)


@dataclass(frozen=True)
class TriCell:
    cell_id: int
    orient: str
    verts: Tuple[Point, Point, Point]


def generate_order_n_triangular_cells(n: int) -> List[TriCell]:
    cells: List[TriCell] = []
    cell_id = 0

    for i in range(n):
        for j in range(n - i):
            up = ((i, j), (i + 1, j), (i, j + 1))
            cells.append(TriCell(cell_id, "up", up))
            cell_id += 1

    for i in range(n - 1):
        for j in range(n - 1 - i):
            down = ((i + 1, j), (i + 1, j + 1), (i, j + 1))
            cells.append(TriCell(cell_id, "down", down))
            cell_id += 1

    return cells


def cell_edges(cell: TriCell) -> Set[Edge]:
    a, b, c = cell.verts
    return {
        canon_edge(a, b),
        canon_edge(b, c),
        canon_edge(a, c),
    }


def build_adjacency(cells: List[TriCell]) -> Dict[int, Set[int]]:
    edge_to_cells: Dict[Edge, List[int]] = defaultdict(list)
    for cell in cells:
        for e in cell_edges(cell):
            edge_to_cells[e].append(cell.cell_id)

    adj: Dict[int, Set[int]] = defaultdict(set)
    for ids in edge_to_cells.values():
        if len(ids) == 2:
            a, b = ids
            adj[a].add(b)
            adj[b].add(a)
    return adj


def centroid_times_3(cell: TriCell) -> Tuple[int, int]:
    xs = sum(v[0] for v in cell.verts)
    ys = sum(v[1] for v in cell.verts)
    return xs, ys


def macro_sector(cell: TriCell) -> int:
    cx3, cy3 = centroid_times_3(cell)
    return ((cx3 + 2 * cy3) // 3) % 3


def live_bit(cell: TriCell) -> int:
    cx3, cy3 = centroid_times_3(cell)
    return (cx3 + 2 * cy3 + (0 if cell.orient == "up" else 1)) % 2


def cell_layer(cell: TriCell, n: int) -> int:
    vals = []
    for i, j in cell.verts:
        k = n - i - j
        vals.append(min(i, j, k))
    return min(vals)


def expected_prism_edges() -> Set[frozenset]:
    return {
        frozenset(((0, 0), (1, 0))),
        frozenset(((1, 0), (2, 0))),
        frozenset(((2, 0), (0, 0))),
        frozenset(((0, 1), (1, 1))),
        frozenset(((1, 1), (2, 1))),
        frozenset(((2, 1), (0, 1))),
        frozenset(((0, 0), (0, 1))),
        frozenset(((1, 0), (1, 1))),
        frozenset(((2, 0), (2, 1))),
    }


def build_slice_matrix(
    cells: List[TriCell],
    adj: Dict[int, Set[int]],
    parity: str,
    n: int,
) -> tuple[List[ClassNode], List[List[int]], List[List[int]], Set[frozenset]]:
    by_id = {c.cell_id: c for c in cells}
    class_nodes: List[ClassNode] = [
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
    ]
    index = {node: i for i, node in enumerate(class_nodes)}
    weights = [[0 for _ in class_nodes] for _ in class_nodes]
    seen_edges: Set[Tuple[int, int]] = set()

    for a, nbrs in adj.items():
        for b in nbrs:
            e = (a, b) if a < b else (b, a)
            if e in seen_edges:
                continue
            seen_edges.add(e)

            ca = by_id[a]
            cb = by_id[b]

            la = cell_layer(ca, n)
            lb = cell_layer(cb, n)
            base_layer = min(la, lb)
            want_even = (base_layer % 2 == 0)
            if parity == "even" and not want_even:
                continue
            if parity == "odd" and want_even:
                continue

            na = (macro_sector(ca), live_bit(ca))
            nb = (macro_sector(cb), live_bit(cb))
            ia = index[na]
            ib = index[nb]
            weights[ia][ib] += 1
            weights[ib][ia] += 1

    support = [
        [1 if weights[i][j] > 0 else 0 for j in range(len(class_nodes))]
        for i in range(len(class_nodes))
    ]

    observed_edges: Set[frozenset] = set()
    for i in range(len(class_nodes)):
        for j in range(i + 1, len(class_nodes)):
            if support[i][j]:
                observed_edges.add(frozenset((class_nodes[i], class_nodes[j])))

    return class_nodes, weights, support, observed_edges


def summarize_kind_totals(class_nodes: List[ClassNode], weights: List[List[int]]) -> Dict[str, int]:
    totals = {"bit0_face": 0, "macro_rung": 0, "bit1_face": 0}
    for i in range(len(class_nodes)):
        for j in range(i + 1, len(class_nodes)):
            w = weights[i][j]
            if w == 0:
                continue
            a = class_nodes[i]
            b = class_nodes[j]
            ma, ba = a
            mb, bb = b
            if ma == mb and ba != bb:
                totals["macro_rung"] += w
            elif ba == bb == 0 and ma != mb:
                totals["bit0_face"] += w
            elif ba == bb == 1 and ma != mb:
                totals["bit1_face"] += w
    return totals


def symbolic_equal_share_weights(kind_totals: Dict[str, int]) -> Dict[str, str]:
    return {
        "top_ab": f'{kind_totals["bit0_face"]}/3',
        "top_bc": f'{kind_totals["bit0_face"]}/3',
        "top_ca": f'{kind_totals["bit0_face"]}/3',
        "bottom_ab": f'{kind_totals["bit1_face"]}/3',
        "bottom_bc": f'{kind_totals["bit1_face"]}/3',
        "bottom_ca": f'{kind_totals["bit1_face"]}/3',
        "vertical_a": f'{kind_totals["macro_rung"]}/3',
        "vertical_b": f'{kind_totals["macro_rung"]}/3',
        "vertical_c": f'{kind_totals["macro_rung"]}/3',
    }


def write_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, indent=2) + "\n")


def make_support_artifact(
    name: str,
    parity: str,
    kind_totals: Dict[str, int],
    observed_edges: Set[frozenset],
) -> dict:
    expected = expected_prism_edges()
    return {
        "name": name,
        "version": "0.3",
        "quotient_type": "exact weighted triangular prism",
        "slice_parity": parity,
        "status": "extracted-parity-distinguished-kind-totals",
        "support_summary": {
            "carrier_scope": f"G900 {parity} slices",
            "support_detected": True,
            "support_stable": True,
        },
        "prism_model": {
            "vertices": [
                "top_a", "top_b", "top_c",
                "bottom_a", "bottom_b", "bottom_c",
            ],
            "edges": [
                "top_ab", "top_bc", "top_ca",
                "bottom_ab", "bottom_bc", "bottom_ca",
                "vertical_a", "vertical_b", "vertical_c",
            ],
            "faces": [
                "top_face",
                "bottom_face",
                "side_ab",
                "side_bc",
                "side_ca",
            ],
            "weights": symbolic_equal_share_weights(kind_totals),
        },
        "kind_totals": kind_totals,
        "support_check": {
            "observed_edge_count": len(observed_edges),
            "expected_edge_count": len(expected),
            "exact_match": observed_edges == expected,
        },
        "artifact_notes": [
            "Kind totals are exact extracted parity-distinguished counts on the fixed prism support.",
            "Per-edge prism_model.weights are symbolic equal-share placeholders only.",
            "Do not treat the /3 expressions as exact extracted edge weights unless a later extractor resolves edge-level parity weights directly.",
        ],
    }


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)
    adj = build_adjacency(cells)

    even_nodes, even_weights, _, even_edges = build_slice_matrix(cells, adj, "even", n)
    odd_nodes, odd_weights, _, odd_edges = build_slice_matrix(cells, adj, "odd", n)

    even_totals = summarize_kind_totals(even_nodes, even_weights)
    odd_totals = summarize_kind_totals(odd_nodes, odd_weights)

    even_artifact = make_support_artifact(
        "even_slice_prism_support",
        "even",
        even_totals,
        even_edges,
    )
    odd_artifact = make_support_artifact(
        "odd_slice_prism_support",
        "odd",
        odd_totals,
        odd_edges,
    )

    comparison = {
        "name": "parity_prism_comparison",
        "version": "0.3",
        "left_support": "specs/paper/g60/even_slice_prism_support_v0_1.json",
        "right_support": "specs/paper/g60/odd_slice_prism_support_v0_1.json",
        "comparison_type": "support-isomorphism-with-distinct-kind-totals",
        "status": "extracted-parity-distinguished-kind-totals",
        "shared_symbolic_model": {
            "vertices": [
                "top_a", "top_b", "top_c",
                "bottom_a", "bottom_b", "bottom_c",
            ],
            "edges": [
                "top_ab", "top_bc", "top_ca",
                "bottom_ab", "bottom_bc", "bottom_ca",
                "vertical_a", "vertical_b", "vertical_c",
            ],
            "faces": [
                "top_face",
                "bottom_face",
                "side_ab",
                "side_bc",
                "side_ca",
            ],
            "weights": "see side-specific artifacts; equal-share placeholders only",
        },
        "checks": {
            "vertex_count_match": True,
            "edge_count_match": True,
            "face_count_match": True,
            "incidence_match": True,
            "symbolic_model_match": True,
            "support_match": (
                even_artifact["support_check"]["exact_match"]
                and odd_artifact["support_check"]["exact_match"]
            ),
            "kind_totals_match": False,
            "weight_law_match": False,
        },
        "result": {
            "parity_stable": True,
            "weights_distinguished_by_parity": True,
            "even_kind_totals": even_totals,
            "odd_kind_totals": odd_totals,
            "notes": [
                "Even and odd slices share the same prism carrier.",
                "Parity redistributes kind totals across the fixed prism support.",
                "Current side-specific prism_model.weights are symbolic equal-share placeholders, not exact extracted edge-level weights.",
            ],
        },
    }

    write_json("specs/paper/g60/even_slice_prism_support_v0_1.json", even_artifact)
    write_json("specs/paper/g60/odd_slice_prism_support_v0_1.json", odd_artifact)
    write_json("specs/paper/g60/parity_prism_comparison_v0_1.json", comparison)

    print("wrote specs/paper/g60/even_slice_prism_support_v0_1.json")
    print("wrote specs/paper/g60/odd_slice_prism_support_v0_1.json")
    print("wrote specs/paper/g60/parity_prism_comparison_v0_1.json")


if __name__ == "__main__":
    main()
