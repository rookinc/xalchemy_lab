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


def cell_layer(cell: TriCell, n: int) -> int:
    vals = []
    for i, j in cell.verts:
        k = n - i - j
        vals.append(min(i, j, k))
    return min(vals)


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

    bit_table: Dict[Tuple[int, int], int] = defaultdict(int)
    macro_table: Dict[Tuple[int, int], int] = defaultdict(int)
    macrobit_table: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int] = defaultdict(int)
    layer_bit_table: Dict[Tuple[int, Tuple[int, int]], int] = defaultdict(int)

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
            ma = macro_sector(ca)
            mb = macro_sector(cb)
            ba = live_bit(ca)
            bb = live_bit(cb)

            bit_key = tuple(sorted((ba, bb)))
            macro_key = tuple(sorted((ma, mb)))
            mba = (ma, ba)
            mbb = (mb, bb)
            macrobit_key = tuple(sorted((mba, mbb)))
            layer_key = min(la, lb)

            bit_table[bit_key] += 1
            macro_table[macro_key] += 1
            macrobit_table[macrobit_key] += 1
            layer_bit_table[(layer_key, bit_key)] += 1

    print("G900 CONTACT SURFACE PROBE")
    print("=========================")
    print(f"cells          = {len(cells)}")
    print(f"adjacency edges= {len(seen_edges)}")

    print("\nbit-to-bit contact table")
    for key in sorted(bit_table):
        print(f"  {key}: {bit_table[key]}")

    print("\nmacro-to-macro contact table")
    for key in sorted(macro_table):
        print(f"  {key}: {macro_table[key]}")

    print("\n(macro,bit)-to-(macro,bit) contact table")
    for key in sorted(macrobit_table):
        print(f"  {key}: {macrobit_table[key]}")

    print("\nlayer-conditioned bit contacts")
    layer_keys = sorted({k[0] for k in layer_bit_table})
    for layer in layer_keys:
        print(f"  layer {layer}:")
        for bit_key in sorted({k[1] for k in layer_bit_table if k[0] == layer}):
            print(f"    {bit_key}: {layer_bit_table[(layer, bit_key)]}")


if __name__ == "__main__":
    main()
