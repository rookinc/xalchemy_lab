from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


Point = Tuple[int, int]
Edge = Tuple[Point, Point]


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


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)
    adj = build_adjacency(cells)
    by_id = {c.cell_id: c for c in cells}

    macro_counts = defaultdict(int)
    bit_counts = defaultdict(int)
    macro_bit_counts = defaultdict(int)

    seen_edges: Set[Tuple[int, int]] = set()
    macro_contact = defaultdict(int)

    for c in cells:
        m = macro_sector(c)
        b = live_bit(c)
        macro_counts[m] += 1
        bit_counts[b] += 1
        macro_bit_counts[(m, b)] += 1

    for a, nbrs in adj.items():
        for b in nbrs:
            e = (a, b) if a < b else (b, a)
            if e in seen_edges:
                continue
            seen_edges.add(e)

            ca = by_id[a]
            cb = by_id[b]
            ma = macro_sector(ca)
            mb = macro_sector(cb)
            if ma != mb:
                macro_contact[tuple(sorted((ma, mb)))] += 1

    print("G900 DIRECT CENTER PROBE")
    print("========================")

    print("\nmacro population counts")
    for k in sorted(macro_counts):
        print(f"  macro {k}: {macro_counts[k]}")

    print("\nbit population counts")
    for k in sorted(bit_counts):
        print(f"  bit {k}: {bit_counts[k]}")

    print("\nmacro/bit population counts")
    for k in sorted(macro_bit_counts):
        print(f"  {k}: {macro_bit_counts[k]}")

    print("\nmacro contact counts")
    vals = []
    for k in sorted(macro_contact):
        vals.append(macro_contact[k])
        print(f"  {k}: {macro_contact[k]}")

    if vals:
        print(f"\nmacro contact midpoint = {(min(vals) + max(vals)) / 2}")
        print(f"macro contact mean     = {sum(vals) / len(vals)}")


if __name__ == "__main__":
    main()
