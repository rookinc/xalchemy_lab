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

    layer_counts: DefaultDict[int, int] = defaultdict(int)

    edge_to_cells: DefaultDict[Edge, List[int]] = defaultdict(list)
    for idx, c in enumerate(cells):
        layer_counts[layer_index(c, n)] += 1
        v = c.verts
        for e in [edge_key(v[0], v[1]), edge_key(v[1], v[2]), edge_key(v[2], v[0])]:
            edge_to_cells[e].append(idx)

    layer_pair_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)
    for incident in edge_to_cells.values():
        if len(incident) != 2:
            continue
        a = cells[incident[0]]
        b = cells[incident[1]]
        if tuple(sorted((bit_index(a), bit_index(b)))) != (0, 1):
            continue
        la = layer_index(a, n)
        lb = layer_index(b, n)
        layer_pair_counts[tuple(sorted((la, lb)))] += 1

    same_macro = 900.0
    live_shift = 405.0
    half_gap = (same_macro - live_shift) / 2.0
    target_gap = 5.0
    scale_inverse = half_gap / target_gap  # 49.5

    L = len(layer_counts)
    midpoint_layer = L // 2
    predecessor_layer = midpoint_layer - 1

    candidates = [
        ("pre_midpoint_half_pop", layer_counts[predecessor_layer] / 2.0),
        ("midpoint_half_pop", layer_counts[midpoint_layer] / 2.0),
        ("midpoint_same_layer_contact_half", layer_pair_counts[(midpoint_layer, midpoint_layer)] / 2.0),
        ("pre_midpoint_same_layer_contact_half", layer_pair_counts[(predecessor_layer, predecessor_layer)] / 2.0),
    ]

    print("\nG900 COMPETING SCALE SOURCES")
    print("============================")
    print(f"target scale inverse       : {scale_inverse}")
    print(f"L                          : {L}")
    print(f"midpoint layer             : {midpoint_layer}")
    print(f"pre-midpoint layer         : {predecessor_layer}")

    print("\nCANDIDATES")
    print("==========")
    for name, value in candidates:
        diff = abs(value - scale_inverse)
        print(f"{name:32} = {value:6.1f}   diff={diff:6.1f}")

    print("\nINTERPRETATION")
    print("==============")
    print("The strongest scale-source candidate is the one with exact or best match")
    print("and the clearest structural role in the carrier.")
    print("If the pre-midpoint shell wins cleanly, the normalization hypothesis strengthens.")


if __name__ == "__main__":
    main()
