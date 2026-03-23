from __future__ import annotations

import json
from pathlib import Path


PRISM_PATH = Path("specs/paper/g60/g900_weighted_prism_v0_1.json")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> None:
    prism = load_json(PRISM_PATH)

    summary = prism["carrier_summary"]
    law = prism["normalized_edge_law"]

    layer_count = summary["layer_count"]
    center = law["center_weight"]
    offsets = law["offsets_from_center"]

    d = offsets["bit1_face"]
    half_layer = layer_count / 2

    print("\nG900 HALF-LAYER OFFSET PROBE")
    print("============================")
    print(f"layer count        : {layer_count}")
    print(f"center I           : {center}")
    print(f"offset d           : {d}")
    print(f"layer_count / 2    : {half_layer}")

    print("\nCHECK")
    print("=====")
    print(f"d == layer_count/2 : {d == half_layer}")

    print("\nRECONSTRUCTION")
    print("==============")
    print(f"I - d              : {center - d}")
    print(f"I                  : {center}")
    print(f"I + d              : {center + d}")

    print("\nINTERPRETATION")
    print("==============")
    if d == half_layer:
        print("The extracted offset equals half the layer count.")
        print("This supports the half-layer offset hypothesis.")
    else:
        print("The extracted offset does not equal half the layer count.")
        print("The half-layer offset hypothesis fails on the current export.")

    print(f"\nread {PRISM_PATH}")


if __name__ == "__main__":
    main()
