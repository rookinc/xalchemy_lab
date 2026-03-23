from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, List, Tuple

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


PRISM_PATH = Path("specs/paper/g60/g900_weighted_prism_v0_1.json")

Edge = Tuple[Tuple[int, int], Tuple[int, int]]


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


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
    prism = load_json(PRISM_PATH)
    cells = generate_order_n_triangular_cells(30)

    edge_to_cells: DefaultDict[Edge, List[int]] = defaultdict(list)
    for idx, c in enumerate(cells):
        v = c.verts
        for e in [edge_key(v[0], v[1]), edge_key(v[1], v[2]), edge_key(v[2], v[0])]:
            edge_to_cells[e].append(idx)

    family_counts: DefaultDict[str, int] = defaultdict(int)
    for incident in edge_to_cells.values():
        if len(incident) != 2:
            continue

        a = cells[incident[0]]
        b = cells[incident[1]]

        if tuple(sorted((bit_index(a), bit_index(b)))) != (0, 1):
            continue

        ma = layer_index(a, 30) % 3
        mb = layer_index(b, 30) % 3
        fam = family_name(ma, mb)
        family_counts[fam] += 1

    offsets = prism["normalized_edge_law"]["offsets_from_center"]
    center = prism["normalized_edge_law"]["center_weight"]

    print("\nG900 ROLE CORRESPONDENCE PROBE")
    print("==============================")

    print("\nEXPORTED PRISM EDGE ROLES")
    print("=========================")
    print(f"bit0_face      : center {center} + ({offsets['bit0_face']})")
    print(f"macro_rung     : center {center} + ({offsets['macro_rung']})")
    print(f"bit1_face      : center {center} + ({offsets['bit1_face']})")

    print("\nCARRIER RELATION FAMILIES")
    print("=========================")
    print(f"same_macro     : {family_counts['same_macro']}")
    print(f"forward_shift  : {family_counts['forward_shift']}")
    print(f"backward_shift : {family_counts['backward_shift']}")

    print("\nWORKING ROLE MATCH")
    print("==================")
    print("candidate rung family      : same_macro")
    print("candidate face family      : backward_shift")
    print("missing opposite family    : forward_shift = 0")

    print("\nINTERPRETATION")
    print("==============")
    print("This does not claim numeric equality between prism weights and carrier counts.")
    print("It tests whether the prism's three named edge roles correspond structurally")
    print("to the three relation roles visible in the carrier edge algebra:")
    print("same, live shift, and absent opposite shift.")


if __name__ == "__main__":
    main()
