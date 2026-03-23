from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


def layer_index(cell, n: int) -> int:
    vals = []
    for i, j in cell.verts:
        k = n - i - j
        vals.append(min(i, j, k))
    return min(vals)


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)

    layer_counts: DefaultDict[int, int] = defaultdict(int)
    for c in cells:
        layer_counts[layer_index(c, n)] += 1

    same_macro = 900.0
    live_shift = 405.0
    half_gap = (same_macro - live_shift) / 2.0
    target_gap = 5.0
    affine_scale = half_gap / target_gap

    L = len(layer_counts)
    midpoint_layer = L // 2
    predecessor_layer = midpoint_layer - 1

    pred_half_pop = layer_counts[predecessor_layer] / 2.0

    print("\nG900 PRE-MIDPOINT SHELL PROBE")
    print("=============================")
    print(f"computed layer count L        : {L}")
    print(f"midpoint layer                : {midpoint_layer}")
    print(f"pre-midpoint layer            : {predecessor_layer}")
    print(f"population of layer {predecessor_layer}      : {layer_counts[predecessor_layer]}")
    print(f"half-population               : {pred_half_pop}")
    print(f"affine scale inverse          : {affine_scale}")

    print("\nCHECK")
    print("=====")
    print(f"half-pop(pre-midpoint) == scale inverse : {abs(pred_half_pop - affine_scale) < 1e-9}")

    print("\nINTERPRETATION")
    print("==============")
    print("This tests whether the affine normalization scale is set by")
    print("the last full outer shell immediately before the midpoint layer.")


if __name__ == "__main__":
    main()
