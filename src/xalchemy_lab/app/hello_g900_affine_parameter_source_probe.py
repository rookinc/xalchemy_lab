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
    scale = half_gap / target_gap   # 49.5

    print("\nG900 AFFINE PARAMETER SOURCE PROBE")
    print("==================================")
    print(f"carrier half-gap / target gap   : {scale}")

    print("\nLAYER COUNTS")
    print("============")
    for layer in sorted(layer_counts):
        print(f"layer {layer:2d}                : {layer_counts[layer]}")

    print("\nCANDIDATE SOURCES")
    print("=================")
    for layer in sorted(layer_counts):
        count = layer_counts[layer]
        print(f"layer {layer:2d} / 2            : {count / 2}")

    print("\nCHECK")
    print("=====")
    matches = []
    for layer in sorted(layer_counts):
        if abs(layer_counts[layer] / 2 - scale) < 1e-9:
            matches.append(layer)

    print(f"matching layers for count/2     : {matches}")

    print("\nINTERPRETATION")
    print("==============")
    if matches:
        print("The affine scale factor matches half of an actual carrier layer count.")
        print("This suggests the normalization may be tied to a specific barycentric layer population.")
    else:
        print("The affine scale factor does not match half of any barycentric layer count.")
        print("A different carrier source is needed.")
