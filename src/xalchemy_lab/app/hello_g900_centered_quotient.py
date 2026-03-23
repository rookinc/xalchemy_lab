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


def main() -> None:
    prism = load_json(PRISM_PATH)
    weights = load_json(WEIGHT_PATH)

    center = prism["normalized_edge_law"]["center_weight"]
    even = weights["even_slice"]

    top = even["top_ab"]
    rung = even["vertical_a"]
    bottom = even["bottom_ab"]
    q_of_i = top + bottom

    print("\nG900 CENTERED QUOTIENT CHECK")
    print("===========================")
    print(f"I (center)         : {center}")
    print(f"top preimage       : {top} = I - {center - top}")
    print(f"rung               : {rung} = I")
    print(f"bottom preimage    : {bottom} = I + {bottom - center}")

    print("\nQUOTIENT IMAGE")
    print("==============")
    print(f"Q(I) candidate     : {top} + {bottom} = {q_of_i}")
    print(f"2I                 : 2 * {center} = {2 * center}")
    print(f"Q(I) = 2I          : {q_of_i == 2 * center}")

    print("\nCOMPACT FORM")
    print("============")
    print(f"(I-d, I, I+d)      : ({top}, {rung}, {bottom})")
    print(f"with I={center}, d={bottom - center}")
    print(f"quotient image     : 2I = {2 * center}")

    print(f"\nread {PRISM_PATH}")
    print(f"read {WEIGHT_PATH}")


if __name__ == "__main__":
    main()
