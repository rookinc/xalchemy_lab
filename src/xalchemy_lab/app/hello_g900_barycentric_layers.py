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

def centroid_key(cell: TriCell) -> Tuple[float, float]:
    xs = [v[0] for v in cell.verts]
    ys = [v[1] for v in cell.verts]
    return (sum(xs) / 3.0, sum(ys) / 3.0)

def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)

    layer_counts: Dict[int, int] = defaultdict(int)
    orient_counts: Dict[Tuple[int, str], int] = defaultdict(int)

    # crude layer index by minimum distance from outer boundary in lattice coordinates
    for c in cells:
        pts = c.verts
        vals = []
        for i, j in pts:
            k = n - i - j
            vals.append(min(i, j, k))
        layer = min(vals)
        layer_counts[layer] += 1
        orient_counts[(layer, c.orient)] += 1

    print("G900 BARYCENTRIC LAYER PROBE")
    print("===========================")
    print(f"total cells = {len(cells)}")

    print("\nlayer counts")
    for layer in sorted(layer_counts):
        print(
            f"  layer {layer:2d}: total={layer_counts[layer]:3d} "
            f"up={orient_counts[(layer, 'up')]:3d} "
            f"down={orient_counts[(layer, 'down')]:3d}"
        )

if __name__ == "__main__":
    main()
