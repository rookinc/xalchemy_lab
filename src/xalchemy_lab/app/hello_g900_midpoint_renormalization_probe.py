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
        family_counts[family_name(ma, mb)] += 1

    center = prism["normalized_edge_law"]["center_weight"]
    offsets = prism["normalized_edge_law"]["offsets_from_center"]

    same_macro = family_counts["same_macro"]
    live_shift = family_counts["backward_shift"]
    dead_shift = family_counts["forward_shift"]

    midpoint = (same_macro + live_shift) / 2
    half_gap = abs(same_macro - live_shift) / 2

    print("\nG900 MIDPOINT RENORMALIZATION PROBE")
    print("===================================")

    print("\nCARRIER ROLE MASSES")
    print("===================")
    print(f"same_macro          : {same_macro}")
    print(f"live_shift          : {live_shift}")
    print(f"dead_shift          : {dead_shift}")

    print("\nMIDPOINT MODEL")
    print("==============")
    print(f"midpoint(same,live) : {midpoint}")
    print(f"half-gap            : {half_gap}")
    print(f"same = mid + gap    : {same_macro == midpoint + half_gap}")
    print(f"live = mid - gap    : {live_shift == midpoint - half_gap}")

    print("\nEXPORTED SIGNED LAW")
    print("===================")
    print(f"center weight       : {center}")
    print(f"bit0 offset         : {offsets['bit0_face']}")
    print(f"rung offset         : {offsets['macro_rung']}")
    print(f"bit1 offset         : {offsets['bit1_face']}")
    print(f"symmetric offsets   : {abs(offsets['bit0_face']) == abs(offsets['bit1_face'])}")

    print("\nINTERPRETATION")
    print("==============")
    print("This does not claim the raw carrier masses equal the exported weights.")
    print("It tests whether the export may be centering unequal relation roles around a midpoint,")
    print("then recording only signed offset from that center.")

    print(f"\nread {PRISM_PATH}")


if __name__ == "__main__":
    main()
