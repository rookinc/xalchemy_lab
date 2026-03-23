from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


Node = Tuple[int, int]


def layer_index(cell, n: int) -> int:
    vals = []
    for i, j in cell.verts:
        k = n - i - j
        vals.append(min(i, j, k))
    return min(vals)


def bit_index(cell) -> int:
    return 0 if cell.orient == "up" else 1


def quotient_node(cell, n: int) -> Node:
    layer = layer_index(cell, n)
    macro = layer % 3
    bit = bit_index(cell)
    return (macro, bit)


def edge_key(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    return tuple(sorted((a, b)))


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)

    # Map lattice edge -> incident cell indices
    edge_to_cells: DefaultDict[Tuple[Tuple[int, int], Tuple[int, int]], List[int]] = defaultdict(list)
    for idx, c in enumerate(cells):
        verts = c.verts
        edges = [
            edge_key(verts[0], verts[1]),
            edge_key(verts[1], verts[2]),
            edge_key(verts[2], verts[0]),
        ]
        for e in edges:
            edge_to_cells[e].append(idx)

    nodes: List[Node] = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)]
    node_to_index: Dict[Node, int] = {node: i for i, node in enumerate(nodes)}

    adjacency = [[0 for _ in nodes] for _ in nodes]
    support_counts: DefaultDict[Tuple[Node, Node], int] = defaultdict(int)

    for incident in edge_to_cells.values():
        if len(incident) != 2:
            continue  # boundary edge
        a_idx, b_idx = incident
        a_node = quotient_node(cells[a_idx], n)
        b_node = quotient_node(cells[b_idx], n)

        if a_node == b_node:
            continue

        i = node_to_index[a_node]
        j = node_to_index[b_node]
        adjacency[i][j] += 1
        adjacency[j][i] += 1
        support_counts[tuple(sorted((a_node, b_node)))] += 1

    print("\nG900 CANDIDATE QUOTIENT ADJACENCY")
    print("=================================")
    print("rule: prism macro = layer mod 3, prism bit = orientation bit")
    print(f"total cells                : {len(cells)}")
    print(f"internal carrier edges     : {sum(len(v) == 2 for v in edge_to_cells.values())}")

    print("\nNODE ORDER")
    print("==========")
    for i, node in enumerate(nodes):
        print(f"{i}: {node}")

    print("\nQUOTIENT ADJACENCY MATRIX")
    print("=========================")
    for row in adjacency:
        print(" ".join(f"{x:4d}" for x in row))

    print("\nNONZERO SUPPORT EDGES")
    print("=====================")
    for (a, b), w in sorted(support_counts.items()):
        print(f"{a} <-> {b}  weight={w}")

    print("\nINTERPRETATION")
    print("==============")
    print("This computes the induced 6x6 quotient adjacency under the direct carrier rule.")
    print("The next question is whether its support graph is exactly the triangular prism and")
    print("whether its weights can be normalized to the exported prism law 140/145/150.")


if __name__ == "__main__":
    main()
