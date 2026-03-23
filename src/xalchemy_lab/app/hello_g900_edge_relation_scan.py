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

    edge_to_cells: DefaultDict[Edge, List[int]] = defaultdict(list)
    for idx, c in enumerate(cells):
        v = c.verts
        edges = [
            edge_key(v[0], v[1]),
            edge_key(v[1], v[2]),
            edge_key(v[2], v[0]),
        ]
        for e in edges:
            edge_to_cells[e].append(idx)

    relation_counts: DefaultDict[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]], int] = defaultdict(int)
    simple_counts: DefaultDict[Tuple[Tuple[int, int], Tuple[int, int]], int] = defaultdict(int)

    for incident in edge_to_cells.values():
        if len(incident) != 2:
            continue

        a = cells[incident[0]]
        b = cells[incident[1]]

        la = layer_index(a, n)
        lb = layer_index(b, n)
        ba = bit_index(a)
        bb = bit_index(b)
        ma = la % 3
        mb = lb % 3

        layer_pair = tuple(sorted((la, lb)))
        bit_pair = tuple(sorted((ba, bb)))
        macro_pair = tuple(sorted((ma, mb)))

        relation_counts[(layer_pair, bit_pair, macro_pair)] += 1
        simple_counts[(bit_pair, macro_pair)] += 1

    print("\nG900 EDGE RELATION SCAN")
    print("=======================")

    print("\nBIT-PAIR x MACRO-PAIR")
    print("=====================")
    for key, count in sorted(simple_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{key}  count={count}")

    print("\nFULL RELATION TYPES")
    print("===================")
    for key, count in sorted(relation_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:40]:
        layer_pair, bit_pair, macro_pair = key
        print(
            f"layers={layer_pair}  bits={bit_pair}  macros={macro_pair}  count={count}"
        )

    print("\nINTERPRETATION")
    print("==============")
    print("This scan looks for natural edge-relation types in the carrier.")
    print("The next step is to see whether a small number of dominant relation types correspond to top-face, bottom-face, and rung classes.")


if __name__ == "__main__":
    main()
