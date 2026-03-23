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

    center = prism["normalized_edge_law"]["center_weight"]
    offsets = prism["normalized_edge_law"]["offsets_from_center"]

    bit0 = center + offsets["bit0_face"]
    rung = center + offsets["macro_rung"]
    bit1 = center + offsets["bit1_face"]

    print("\nG900 SIGNED OFFSET PROBE")
    print("========================")
    print(f"center weight        : {center}")
    print(f"bit0_face offset     : {offsets['bit0_face']}")
    print(f"macro_rung offset    : {offsets['macro_rung']}")
    print(f"bit1_face offset     : {offsets['bit1_face']}")

    print("\nRECOVERED WEIGHTS")
    print("=================")
    print(f"bit0_face            : {center} + ({offsets['bit0_face']}) = {bit0}")
    print(f"macro_rung           : {center} + ({offsets['macro_rung']}) = {rung}")
    print(f"bit1_face            : {center} + ({offsets['bit1_face']}) = {bit1}")

    print("\nSIGNED STRUCTURE")
    print("================")
    print(f"negative face role   : {bit0} = {center} - {center - bit0}")
    print(f"neutral rung role    : {rung} = {center}")
    print(f"positive face role   : {bit1} = {center} + {bit1 - center}")
    print(f"symmetric offsets    : {(center - bit0) == (bit1 - center)}")

    print("\nWORKING QUESTION")
    print("================")
    print("The carrier relation algebra is chiral, but the exported prism law is centered and signed.")
    print("So the next theorem target is not whether chirality exists, but how chiral relation roles")
    print("are renormalized into symmetric signed offsets around the center weight.")

    print(f"\nread {PRISM_PATH}")


if __name__ == "__main__":
    main()
