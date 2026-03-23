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

    cell_count = summary["cell_count"]
    layer_count = summary["layer_count"]
    macro_count = summary["macro_count"]
    bit_count = summary["bit_count"]
    d = law["offsets_from_center"]["bit1_face"]

    candidates = [
        ("layer_count / 2", layer_count / 2),
        ("macro_count + bit_count", macro_count + bit_count),
        ("layer_count / bit_count", layer_count / bit_count),
        ("cell_count / 180", cell_count / 180),
        ("macro_count * bit_count", macro_count * bit_count),
        ("(layer_count - bit_count) / 2", (layer_count - bit_count) / 2),
    ]

    print("\nG900 OFFSET CANDIDATE LAW COMPARISON")
    print("====================================")
    print(f"observed offset d   : {d}")
    print(f"cell_count          : {cell_count}")
    print(f"layer_count         : {layer_count}")
    print(f"macro_count         : {macro_count}")
    print(f"bit_count           : {bit_count}")

    print("\nCANDIDATES")
    print("==========")
    for name, value in candidates:
        print(f"{name:28} = {value}    match={value == d}")

    print("\nINTERPRETATION")
    print("==============")
    print("Exact matches are not automatically meaningful.")
    print("The current front-runner is the one that is exact and structurally interpretable.")
    print("Right now, layer_count / 2 is the strongest candidate because it fits the centered half-gap picture.")

    print(f"\nread {PRISM_PATH}")


if __name__ == "__main__":
    main()
