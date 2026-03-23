from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict, Dict, List, Tuple

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


Node = Tuple[int, int]
Rule = Callable[[object, int], int]


def edge_key(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    return tuple(sorted((a, b)))


def layer_index(cell, n: int) -> int:
    vals = []
    for i, j in cell.verts:
        k = n - i - j
        vals.append(min(i, j, k))
    return min(vals)


def bit_index(cell) -> int:
    return 0 if cell.orient == "up" else 1


def min_x_mod3(cell, n: int) -> int:
    xs = [v[0] for v in cell.verts]
    return min(xs) % 3


def min_y_mod3(cell, n: int) -> int:
    ys = [v[1] for v in cell.verts]
    return min(ys) % 3


def min_k_mod3(cell, n: int) -> int:
    ks = [n - i - j for i, j in cell.verts]
    return min(ks) % 3


def layer_mod3(cell, n: int) -> int:
    return layer_index(cell, n) % 3


def argmin_sector(cell, n: int) -> int:
    mins = []
    for i, j in cell.verts:
        k = n - i - j
        mins.append((i, j, k))
    a = min(x[0] for x in mins)
    b = min(x[1] for x in mins)
    c = min(x[2] for x in mins)
    triple = [a, b, c]
    return triple.index(min(triple))


EXPECTED_SUPPORT = {
    ((0, 0), (1, 0)),
    ((0, 0), (2, 0)),
    ((1, 0), (2, 0)),
    ((0, 1), (1, 1)),
    ((0, 1), (2, 1)),
    ((1, 1), (2, 1)),
    ((0, 0), (0, 1)),
    ((1, 0), (1, 1)),
    ((2, 0), (2, 1)),
}


def support_for_rule(cells, n: int, macro_rule: Rule) -> Dict[Tuple[Node, Node], int]:
    edge_to_cells: DefaultDict[Tuple[Tuple[int, int], Tuple[int, int]], List[int]] = defaultdict(list)
    for idx, c in enumerate(cells):
        v = c.verts
        edges = [edge_key(v[0], v[1]), edge_key(v[1], v[2]), edge_key(v[2], v[0])]
        for e in edges:
            edge_to_cells[e].append(idx)

    support_counts: DefaultDict[Tuple[Node, Node], int] = defaultdict(int)

    for incident in edge_to_cells.values():
        if len(incident) != 2:
            continue
        a_idx, b_idx = incident
        a = cells[a_idx]
        b = cells[b_idx]
        a_node = (macro_rule(a, n), bit_index(a))
        b_node = (macro_rule(b, n), bit_index(b))
        if a_node == b_node:
            continue
        support_counts[tuple(sorted((a_node, b_node)))] += 1

    return dict(support_counts)


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)

    rules: List[Tuple[str, Rule]] = [
        ("min_x_mod3", min_x_mod3),
        ("min_y_mod3", min_y_mod3),
        ("min_k_mod3", min_k_mod3),
        ("layer_mod3", layer_mod3),
        ("argmin_sector", argmin_sector),
    ]

    print("\nG900 MACRO RULE COMPARISON")
    print("==========================")

    for name, rule in rules:
        support = support_for_rule(cells, n, rule)
        support_set = set(support.keys())
        overlap = len(support_set & EXPECTED_SUPPORT)
        extra = len(support_set - EXPECTED_SUPPORT)
        missing = len(EXPECTED_SUPPORT - support_set)

        print(f"\nRULE: {name}")
        print("-" * (6 + len(name)))
        print(f"support edge count   : {len(support_set)}")
        print(f"prism overlap        : {overlap}")
        print(f"extra edges          : {extra}")
        print(f"missing prism edges  : {missing}")

        for edge, w in sorted(support.items()):
            print(f"{edge[0]} <-> {edge[1]}  weight={w}")

    print("\nINTERPRETATION")
    print("==============")
    print("The best macro rule is the one with the highest prism-overlap and the fewest extra/missing edges.")
