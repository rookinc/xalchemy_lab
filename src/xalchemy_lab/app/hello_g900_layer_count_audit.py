from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


PRISM_PATH = Path("specs/paper/g60/g900_weighted_prism_v0_1.json")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> None:
    prism = load_json(PRISM_PATH)
    exported_layer_count = prism["carrier_summary"]["layer_count"]

    n = 30
    cells = generate_order_n_triangular_cells(n)

    layer_counts: Dict[int, int] = defaultdict(int)

    for c in cells:
        vals = []
        for i, j in c.verts:
            k = n - i - j
            vals.append(min(i, j, k))
        layer = min(vals)
        layer_counts[layer] += 1

    layers = sorted(layer_counts)
    computed_layer_count = len(layers)
    max_layer = max(layers)

    print("\nG900 LAYER COUNT AUDIT")
    print("======================")
    print(f"carrier order n         : {n}")
    print(f"total cells             : {len(cells)}")
    print(f"computed layers         : {layers}")
    print(f"computed layer count    : {computed_layer_count}")
    print(f"computed max layer      : {max_layer}")
    print(f"exported layer count    : {exported_layer_count}")

    print("\nLAYER HISTOGRAM")
    print("===============")
    for layer in layers:
        print(f"layer {layer:2d}            : {layer_counts[layer]}")

    print("\nCHECK")
    print("=====")
    print(f"computed == exported    : {computed_layer_count == exported_layer_count}")

    print("\nINTERPRETATION")
    print("==============")
    if computed_layer_count == exported_layer_count:
        print("The exported prism layer_count matches the computed barycentric layer count.")
        print("This supports treating L = 10 as carrier-derived rather than merely decorative metadata.")
    else:
        print("The exported prism layer_count does not match the computed barycentric layer count.")
        print("The current L = 10 story needs revision.")

    print(f"\nread {PRISM_PATH}")


if __name__ == "__main__":
    main()
