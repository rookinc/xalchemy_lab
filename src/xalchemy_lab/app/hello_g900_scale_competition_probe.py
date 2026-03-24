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

    L = len(layer_counts)
    midpoint = L // 2
    pred = midpoint - 1

    target = 49.5

    candidates = {
        "pred_half_population": layer_counts[pred] / 2,
        "mid_half_population": layer_counts[midpoint] / 2,
        "pred_same_shell_half": layer_pair_counts[(pred, pred)] / 2,
        "mid_same_shell_half": layer_pair_counts[(midpoint, midpoint)] / 2,
        "pred_mid_boundary_half": layer_pair_counts[(pred, midpoint)] / 2,
    }

    print("\nG900 SCALE COMPETITION PROBE")
    print("============================")
    print(f"layer count L              : {L}")
    print(f"midpoint layer             : {midpoint}")
    print(f"predecessor layer          : {pred}")
    print(f"target scale               : {target}")

    print("\nCANDIDATES")
    print("==========")
    for name, value in candidates.items():
        diff = abs(value - target)
        print(f"{name:24s} = {value:6.1f}   diff = {diff:4.1f}")

    print("\nINTERPRETATION")
    print("==============")
    print("Best candidates are those that:")
    print("- match the target scale exactly or most closely")
    print("- preserve the centered law")
    print("- have the cleanest structural status in the carrier")


if __name__ == "__main__":
    main()
