from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


PRISM_PATH = Path("specs/paper/g60/g900_weighted_prism_v0_1.json")
WEIGHT_PATH = Path("specs/paper/g60/g900_prism_weight_table_v0_1.json")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def expect(label: str, cond: bool) -> None:
    if not cond:
        raise ValueError(f"{label} failed")


def main() -> None:
    prism = load_json(PRISM_PATH)
    weights = load_json(WEIGHT_PATH)

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
    exported_layer_count = prism["carrier_summary"]["layer_count"]

    center = prism["normalized_edge_law"]["center_weight"]

    even = weights["even_slice"]
    top = even["top_ab"]
    rung = even["vertical_a"]
    bottom = even["bottom_ab"]

    half_layer = computed_layer_count / 2
    top_offset = center - top
    bottom_offset = bottom - center
    band_width = bottom - top

    expect("computed layer count matches export", computed_layer_count == exported_layer_count)
    expect("top and bottom symmetric about center", top + bottom == 2 * center)
    expect("rung equals center", rung == center)
    expect("top offset equals half-layer", top_offset == half_layer)
    expect("bottom offset equals half-layer", bottom_offset == half_layer)
    expect("band width equals computed layer count", band_width == computed_layer_count)

    print("\nG900 BARYCENTRIC BAND ALIGNMENT CHECK")
    print("=====================================")
    print(f"carrier order n           : {n}")
    print(f"computed layers           : {layers}")
    print(f"computed layer count L    : {computed_layer_count}")
    print(f"exported layer count      : {exported_layer_count}")

    print("\nPRISM VALUES")
    print("============")
    print(f"top                       : {top}")
    print(f"rung                      : {rung}")
    print(f"bottom                    : {bottom}")
    print(f"center I                  : {center}")

    print("\nALIGNMENT")
    print("=========")
    print(f"I - L/2                   : {center - half_layer}")
    print(f"I                         : {center}")
    print(f"I + L/2                   : {center + half_layer}")
    print(f"actual triple             : ({top}, {rung}, {bottom})")
    print(f"band width                : {band_width}")

    print("\nVERDICT")
    print("=======")
    print("The weighted prism triple is exactly aligned with the computed barycentric band width.")
    print("This supports reading top/rung/bottom as endpoint-midpoint-endpoint data for the carrier-derived 10-layer band.")
    print("It does not yet prove literal class identification by layer index alone.")

    print(f"\nread {PRISM_PATH}")
    print(f"read {WEIGHT_PATH}")


if __name__ == "__main__":
    main()
