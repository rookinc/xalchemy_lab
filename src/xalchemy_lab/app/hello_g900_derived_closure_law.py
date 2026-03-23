from __future__ import annotations

import json
from pathlib import Path


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

    center = prism["normalized_edge_law"]["center_weight"]
    layer_count = prism["carrier_summary"]["layer_count"]

    even = weights["even_slice"]
    top = even["top_ab"]
    rung = even["vertical_a"]
    bottom = even["bottom_ab"]

    d = bottom - center
    half_layer = layer_count / 2
    q_of_i = top + bottom

    expect("midpoint law", 2 * center == top + bottom)
    expect("rung equals center", rung == center)
    expect("export band law", d == half_layer)
    expect("derived closure law", q_of_i == 2 * center)

    print("\nG900 DERIVED CLOSURE LAW CHECK")
    print("==============================")
    print(f"I (center)         : {center}")
    print(f"L (layer count)    : {layer_count}")
    print(f"L/2                : {half_layer}")
    print(f"top                : {top}")
    print(f"rung               : {rung}")
    print(f"bottom             : {bottom}")
    print(f"d                  : {d}")

    print("\nDERIVATION")
    print("==========")
    print(f"(I - d, I, I + d)  : ({top}, {rung}, {bottom})")
    print(f"(I - L/2, I, I+L/2): ({center-half_layer}, {center}, {center+half_layer})")
    print(f"Q(I) candidate     : {top} + {bottom} = {q_of_i}")
    print(f"2I                 : 2 * {center} = {2 * center}")

    print("\nVERDICT")
    print("=======")
    print("(I - L/2, I, I + L/2) -> Q(I) = 2I : PASS")

    print(f"\nread {PRISM_PATH}")
    print(f"read {WEIGHT_PATH}")


if __name__ == "__main__":
    main()
