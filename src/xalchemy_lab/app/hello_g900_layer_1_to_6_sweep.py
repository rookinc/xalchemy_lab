from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple

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
    layer_macro_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)
    layer_bit_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)

    edge_to_cells: DefaultDict[Edge, List[int]] = defaultdict(list)
    for idx, c in enumerate(cells):
        layer = layer_index(c, n)
        macro = layer % 3
        bit = bit_index(c)

        layer_counts[layer] += 1
        layer_macro_counts[(layer, macro)] += 1
        layer_bit_counts[(layer, bit)] += 1

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

    print("\nG900 LAYER 1-6 SWEEP")
    print("====================")

    for layer in range(1, 7):
        counts = {m: layer_macro_counts[(layer, m)] for m in range(3)}
        dominant_macro = max(counts, key=counts.get)
        bit0 = layer_bit_counts[(layer, 0)]
        bit1 = layer_bit_counts[(layer, 1)]
        outward = layer_pair_counts.get((layer - 1, layer), 0)
        same = layer_pair_counts.get((layer, layer), 0)
        inward = layer_pair_counts.get((layer, layer + 1), 0)

        print(f"\nlayer {layer}")
        print(f"  population        : {layer_counts[layer]}")
        print(f"  half-population   : {layer_counts[layer] / 2}")
        print(f"  macro counts      : {counts}")
        print(f"  dominant macro    : {dominant_macro}")
        print(f"  expected mod 3    : {layer % 3}")
        print(f"  phase match       : {dominant_macro == (layer % 3)}")
        print(f"  bit split         : bit0={bit0}, bit1={bit1}")
        print(f"  bit imbalance     : {bit0 - bit1}")
        print(f"  outward contact   : {outward}")
        print(f"  same-layer contact: {same}")
        print(f"  inward contact    : {inward}")

    print("\nINTERPRETATION")
    print("==============")
    print("This sweep compares the outer-to-center approach layers.")
    print("The main question is whether layer 4 is uniquely special or part of a broader transition region.")


if __name__ == "__main__":
    main()
