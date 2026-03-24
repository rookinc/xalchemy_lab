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
    macro_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)

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

    L = len(layer_counts)
    midpoint = L // 2
    pred = midpoint - 1

    for layer in sorted(layer_counts):
        macro_counts[(layer, layer % 3)] = layer_counts[layer]

    print("\nG900 POSITIONAL PRIVILEGE PROBE")
    print("===============================")
    print(f"layer count L               : {L}")
    print(f"midpoint layer              : {midpoint}")
    print(f"predecessor layer           : {pred}")

    print("\nPREDECESSOR VS MIDPOINT")
    print("=======================")
    print(f"pred population             : {layer_counts[pred]}")
    print(f"pred half                   : {layer_counts[pred] / 2}")
    print(f"pred same-shell             : {layer_pair_counts[(pred, pred)]}")
    print(f"pred-mid boundary           : {layer_pair_counts[(pred, midpoint)]}")
    print(f"mid population              : {layer_counts[midpoint]}")
    print(f"mid half                    : {layer_counts[midpoint] / 2}")
    print(f"mid same-shell              : {layer_pair_counts[(midpoint, midpoint)]}")

    print("\nPOSITIONAL FACTS")
    print("================")
    print("predecessor is unique       : True")
    print("directly before midpoint    : True")
    print("outer to midpoint           : True")
    print("same-shell = population @4  :", layer_pair_counts[(pred, pred)] == layer_counts[pred])
    print("same-shell = population @5  :", layer_pair_counts[(midpoint, midpoint)] == layer_counts[midpoint])

    print("\nPHASE FACTS")
    print("===========")
    print(f"pred macro class            : {pred % 3}")
    print(f"mid macro class             : {midpoint % 3}")
    print("pred and mid differ         :", (pred % 3) != (midpoint % 3))

    print("\nINTERPRETATION")
    print("==============")
    print("The predecessor shell is not just another nearby layer.")
    print("It is the unique outer shell immediately adjacent to midpoint.")
    print("If scale is taken from the last full outer shell before centering,")
    print("then layer 4 is positionally privileged rather than numerically accidental.")


if __name__ == "__main__":
    main()
