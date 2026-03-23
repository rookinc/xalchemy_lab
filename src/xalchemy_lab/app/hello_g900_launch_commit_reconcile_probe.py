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
    predecessor = midpoint - 1

    launch_pair = (0, 1)
    commit_layers = [1, 2, 3, 4]
    reconcile_pairs = [(predecessor, predecessor), (predecessor, midpoint), (midpoint, midpoint)]

    print("\nG900 LAUNCH / COMMIT / RECONCILE PROBE")
    print("======================================")
    print(f"layer count L              : {L}")
    print(f"midpoint layer             : {midpoint}")
    print(f"pre-midpoint layer         : {predecessor}")

    print("\nLAUNCH CANDIDATE")
    print("================")
    print(f"pair {launch_pair}               : {layer_pair_counts[launch_pair]}")

    print("\nCOMMIT CANDIDATES")
    print("=================")
    for layer in commit_layers:
        print(
            f"layer {layer:2d} same-shell      : {layer_pair_counts[(layer, layer)]}   "
            f"half-pop={layer_counts[layer] / 2}"
        )

    print("\nRECONCILE CANDIDATES")
    print("====================")
    for pair in reconcile_pairs:
        print(f"pair {pair}               : {layer_pair_counts[pair]}")

    print("\nWORKING INTERPRETATION")
    print("======================")
    print("launch     : first outward cross-shell contact from the center boundary")
    print("commit     : stable same-shell transport in the regular outer family")
    print("reconcile  : pre-midpoint / midpoint closure boundary")

    print("\nQUESTION")
    print("========")
    print("Do these three zones look structurally distinct enough to support")
    print("the grammar: launch -> commit -> reconcile ?")


if __name__ == "__main__":
    main()
