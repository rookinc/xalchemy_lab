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

    print("\nG900 SHELL POPULATION VS SAME-LAYER PROBE")
    print("=========================================")

    exact_match_layers = []

    print("\nLAYER COMPARISON")
    print("================")
    for layer in sorted(layer_counts):
        pop = layer_counts[layer]
        same = layer_pair_counts.get((layer, layer), 0)
        diff = pop - same
        match = pop == same
        if match:
            exact_match_layers.append(layer)
        print(
            f"layer {layer:2d}   population={pop:3d}   "
            f"same_layer_contact={same:3d}   diff={diff:3d}   match={match}"
        )

    print("\nCHECK")
    print("=====")
    print(f"exact match layers        : {exact_match_layers}")

    print("\nINTERPRETATION")
    print("==============")
    print("If population equals same-layer contact across the shell family,")
    print("then those are not competing scale sources in this regime.")
    print("They are the same invariant viewed in two ways.")


if __name__ == "__main__":
    main()
