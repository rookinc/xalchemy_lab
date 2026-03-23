from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, List, Set, Tuple


Point = Tuple[int, int]
Edge = Tuple[Point, Point]


def canon_edge(a: Point, b: Point) -> Edge:
    return (a, b) if a <= b else (b, a)


@dataclass(frozen=True)
class TriCell:
    cell_id: int
    orient: str  # "up" or "down"
    verts: Tuple[Point, Point, Point]


def generate_order_n_triangular_cells(n: int) -> List[TriCell]:
    cells: List[TriCell] = []
    cell_id = 0

    # Integer barycentric-style lattice in 2 coordinates:
    # valid points are (i, j) with i >= 0, j >= 0, i + j <= n
    #
    # Up triangles:
    # (i,j), (i+1,j), (i,j+1)
    #
    # Down triangles:
    # (i+1,j), (i+1,j+1), (i,j+1)
    # valid when i + j <= n - 1 for up
    # valid when i + j <= n - 2 for down

    for i in range(n):
        for j in range(n - i):
            up = ((i, j), (i + 1, j), (i, j + 1))
            cells.append(TriCell(cell_id=cell_id, orient="up", verts=up))
            cell_id += 1

    for i in range(n - 1):
        for j in range(n - 1 - i):
            down = ((i + 1, j), (i + 1, j + 1), (i, j + 1))
            cells.append(TriCell(cell_id=cell_id, orient="down", verts=down))
            cell_id += 1

    return cells


def lattice_points(n: int) -> Set[Point]:
    pts: Set[Point] = set()
    for i in range(n + 1):
        for j in range(n + 1 - i):
            pts.add((i, j))
    return pts


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


def main() -> None:
    n = 30
    pts = lattice_points(n)
    cells = generate_order_n_triangular_cells(n)
    adj = build_adjacency(cells)

    up_count = sum(1 for c in cells if c.orient == "up")
    down_count = sum(1 for c in cells if c.orient == "down")
    total = len(cells)

    print("G900 FIRST SUBDIVISION PROBE")
    print("===========================")
    print(f"order n                = {n}")
    print(f"lattice points         = {len(pts)}")
    print(f"up triangles           = {up_count}")
    print(f"down triangles         = {down_count}")
    print(f"total smallest cells   = {total}")
    print(f"expected n^2           = {n*n}")
    print(f"match                  = {total == n*n}")

    degrees = defaultdict(int)
    for node, nbrs in adj.items():
        degrees[len(nbrs)] += 1

    print("\nadjacency degree histogram")
    for deg in sorted(degrees):
        print(f"  degree {deg}: {degrees[deg]}")

    print("\nfirst 10 cells")
    for c in cells[:10]:
        print(f"  id={c.cell_id:3d} orient={c.orient:4s} verts={c.verts}")


if __name__ == "__main__":
    main()
