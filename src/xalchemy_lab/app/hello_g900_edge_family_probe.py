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


def family_name(ma: int, mb: int) -> str:
    if ma == mb:
        return "same_macro"
    if (mb - ma) % 3 == 1:
        return "forward_shift"
    if (mb - ma) % 3 == 2:
        return "backward_shift"
    raise ValueError("unreachable")


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)

    edge_to_cells: DefaultDict[Edge, List[int]] = defaultdict(list)
    for idx, c in enumerate(cells):
        v = c.verts
        for e in [edge_key(v[0], v[1]), edge_key(v[1], v[2]), edge_key(v[2], v[0])]:
            edge_to_cells[e].append(idx)

    family_counts: DefaultDict[str, int] = defaultdict(int)
    macro_pair_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)
    layer_pair_counts: DefaultDict[Tuple[Tuple[int, int], str], int] = defaultdict(int)

    for incident in edge_to_cells.values():
        if len(incident) != 2:
            continue

        a = cells[incident[0]]
        b = cells[incident[1]]

        la = layer_index(a, n)
        lb = layer_index(b, n)
        ba = bit_index(a)
        bb = bit_index(b)

        if tuple(sorted((ba, bb))) != (0, 1):
            continue

        ma = la % 3
        mb = lb % 3

        fam = family_name(ma, mb)

        family_counts[fam] += 1
        macro_pair_counts[(ma, mb)] += 1
        layer_pair_counts[(tuple(sorted((la, lb))), fam)] += 1

    print("\nG900 EDGE FAMILY PROBE")
    print("======================")
    print("Families are defined on oriented macro phase pairs across cross-bit carrier edges.")
    print("same_macro      : ma = mb")
    print("forward_shift   : mb = ma + 1 mod 3")
    print("backward_shift  : mb = ma - 1 mod 3")

    print("\nFAMILY TOTALS")
    print("=============")
    for fam in ["same_macro", "forward_shift", "backward_shift"]:
        print(f"{fam:16} : {family_counts[fam]}")

    print("\nORIENTED MACRO-PAIR TOTALS")
    print("==========================")
    for key, count in sorted(macro_pair_counts.items()):
        print(f"{key} : {count}")

    print("\nTOP LAYER-PAIR CONTRIBUTIONS")
    print("============================")
    shown = 0
    for key, count in sorted(layer_pair_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        (layer_pair, fam) = key
        print(f"layers={layer_pair}  family={fam:14}  count={count}")
        shown += 1
        if shown >= 30:
            break

    print("\nINTERPRETATION")
    print("==============")
    print("If one family behaves like rungs and the shifted families behave like face transport,")
    print("then the weighted prism may live at the level of cross-bit edge-relation families,")
    print("not direct cell-adjacency quotienting.")


if __name__ == "__main__":
    main()
