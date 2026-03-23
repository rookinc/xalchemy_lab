from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, List, Tuple

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


Edge = Tuple[Tuple[int, int], Tuple[int, int]]


def edge_key(a: Tuple[int, int], b: Tuple[int, int]) -> Edge:
    return tuple(sorted((a, b)))


def layer_index(cell, n: int) -> int:
    vals = []
    for i, j in cell.verts:
        k = n - i - j
        vals.append(min(i, j, k))
    return min(vals)


def bit_index(cell) -> int:
    return 0 if cell.orient == "up" else 1


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)

    edge_to_cells: DefaultDict[Edge, List[int]] = defaultdict(list)
    for idx, c in enumerate(cells):
        v = c.verts
        for e in [edge_key(v[0], v[1]), edge_key(v[1], v[2]), edge_key(v[2], v[0])]:
            edge_to_cells[e].append(idx)

    layer_pair_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)
    zero_incident_counts: DefaultDict[int, int] = defaultdict(int)

    for incident in edge_to_cells.values():
        if len(incident) != 2:
            continue
        a = cells[incident[0]]
        b = cells[incident[1]]
        if tuple(sorted((bit_index(a), bit_index(b)))) != (0, 1):
            continue

        la = layer_index(a, n)
        lb = layer_index(b, n)
        pair = tuple(sorted((la, lb)))
        layer_pair_counts[pair] += 1

        if 0 in pair:
            other = pair[1] if pair[0] == 0 else pair[0]
            zero_incident_counts[other] += 1

    print("\nG900 0:1 LAUNCH PROBE")
    print("====================")
    print("Testing whether 0:1 is the distinguished first outward launch relation.")

    print("\nZERO-LAYER CONTACTS")
    print("===================")
    for other, count in sorted(zero_incident_counts.items()):
        print(f"(0,{other})                : {count}")

    print("\nCHECK")
    print("=====")
    print(f"(0,1) present             : {(0, 1) in layer_pair_counts}")
    print(f"(0,1) count               : {layer_pair_counts.get((0, 1), 0)}")
    print(f"other zero-layer contacts : {[k for k in sorted(zero_incident_counts) if k != 1]}")

    print("\nINTERPRETATION")
    print("==============")
    print("If layer 0 only contacts layer 1, then 0:1 is the unique first outward launch boundary.")
    print("That makes it the cleanest current candidate for the launch primitive in the G900 grammar.")


if __name__ == "__main__":
    main()
