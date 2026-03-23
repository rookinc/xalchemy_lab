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


def edge_kind(a: ClassNode, b: ClassNode) -> str:
    ma, ba = a
    mb, bb = b

    if ma == mb and ba != bb:
        return "macro_rung"
    if ba == bb == 0 and ma != mb:
        return "bit0_face"
    if ba == bb == 1 and ma != mb:
        return "bit1_face"
    return "other"


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)
    adj = build_adjacency(cells)
    by_id = {c.cell_id: c for c in cells}

    parity_kind_counts: Dict[Tuple[str, str], int] = defaultdict(int)
    layer_kind_counts: Dict[Tuple[int, str], int] = defaultdict(int)

    seen_edges: Set[Tuple[int, int]] = set()

    for a, nbrs in adj.items():
        for b in nbrs:
            e = (a, b) if a < b else (b, a)
            if e in seen_edges:
                continue
            seen_edges.add(e)

            ca = by_id[a]
            cb = by_id[b]

            na = (macro_sector(ca), live_bit(ca))
            nb = (macro_sector(cb), live_bit(cb))
            kind = edge_kind(na, nb)
            if kind == "other":
                continue

            la = cell_layer(ca, n)
            lb = cell_layer(cb, n)
            base_layer = min(la, lb)
            parity = "even" if base_layer % 2 == 0 else "odd"

            parity_kind_counts[(parity, kind)] += 1
            layer_kind_counts[(base_layer, kind)] += 1

    print("G900 LAYER PARITY VS PRISM WEIGHT PROBE")
    print("=======================================")

    print("\nparity-by-kind totals")
    for parity in ["even", "odd"]:
        print(f"  {parity}:")
        for kind in ["bit0_face", "macro_rung", "bit1_face"]:
            print(f"    {kind}: {parity_kind_counts[(parity, kind)]}")

    print("\nlayer-by-kind totals")
    layers = sorted({layer for layer, _ in layer_kind_counts})
    for layer in layers:
        print(f"  layer {layer}:")
        for kind in ["bit0_face", "macro_rung", "bit1_face"]:
            print(f"    {kind}: {layer_kind_counts[(layer, kind)]}")

    print("\ncoarse totals reconstructed")
    for kind in ["bit0_face", "macro_rung", "bit1_face"]:
        total = parity_kind_counts[("even", kind)] + parity_kind_counts[("odd", kind)]
        print(f"  {kind}: {total}")


if __name__ == "__main__":
    main()
