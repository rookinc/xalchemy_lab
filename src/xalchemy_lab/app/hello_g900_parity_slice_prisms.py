from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
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


def build_slice_matrix(cells: List[TriCell], adj: Dict[int, Set[int]], parity: str, n: int):
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

    support = [[1 if weights[i][j] > 0 else 0 for j in range(len(class_nodes))] for i in range(len(class_nodes))]
    observed_edges = set()
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


def print_matrix(name: str, class_nodes: List[ClassNode], weights: List[List[int]], support: List[List[int]], observed_edges: Set[frozenset]) -> None:
    print(f"\n{name}")
    print("-" * len(name))
    print("class node order:")
    for i, node in enumerate(class_nodes):
        print(f"  {i}: {node}")

    print("\nweighted adjacency matrix")
    for row in weights:
        print("  " + " ".join(f"{v:3d}" for v in row))

    print("\nsupport matrix")
    for row in support:
        print("  " + " ".join(str(v) for v in row))

    totals = summarize_kind_totals(class_nodes, weights)
    print("\nkind totals")
    for k, v in totals.items():
        print(f"  {k}: {v}")

    expected = expected_prism_edges()
    print("\nprism support match")
    print(f"  observed edge count = {len(observed_edges)}")
    print(f"  expected edge count = {len(expected)}")
    print(f"  exact match         = {observed_edges == expected}")


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)
    adj = build_adjacency(cells)

    even_nodes, even_weights, even_support, even_edges = build_slice_matrix(cells, adj, "even", n)
    odd_nodes, odd_weights, odd_support, odd_edges = build_slice_matrix(cells, adj, "odd", n)

    print("G900 PARITY SLICE PRISM PROBE")
    print("=============================")

    print_matrix("EVEN SLICE", even_nodes, even_weights, even_support, even_edges)
    print_matrix("ODD SLICE", odd_nodes, odd_weights, odd_support, odd_edges)


if __name__ == "__main__":
    main()
