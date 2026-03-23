from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

Point = Tuple[int, int]

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

    table: Dict[int, Dict[Tuple[int, int], int]] = defaultdict(lambda: defaultdict(int))

    for c in cells:
        layer = cell_layer(c, n)
        m = macro_sector(c)
        b = live_bit(c)
        table[layer][(m, b)] += 1

    print("G900 MACRO SECTOR PROBE")
    print("=======================")

    for layer in sorted(table):
        total = sum(table[layer].values())
        print(f"\nlayer {layer:2d} total={total}")
        for m in range(3):
            for b in range(2):
                print(f"  macro {m} bit {b}: {table[layer][(m,b)]}")

if __name__ == "__main__":
    main()
