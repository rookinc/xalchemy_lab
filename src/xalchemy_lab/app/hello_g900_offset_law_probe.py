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
    law = prism["normalized_edge_law"]

    center = law["center_weight"]
    offsets = law["offsets_from_center"]

    top = center + offsets["bit0_face"]
    rung = center + offsets["macro_rung"]
    bottom = center + offsets["bit1_face"]

    print("\nG900 OFFSET LAW PROBE")
    print("=====================")
    print(f"center weight      : {center}")
    print(f"bit0 offset        : {offsets['bit0_face']:+d}")
    print(f"rung offset        : {offsets['macro_rung']:+d}")
    print(f"bit1 offset        : {offsets['bit1_face']:+d}")

    print("\nRECOVERED WEIGHTS")
    print("=================")
    print(f"top face           : {center} + ({offsets['bit0_face']:+d}) = {top}")
    print(f"rung               : {center} + ({offsets['macro_rung']:+d}) = {rung}")
    print(f"bottom face        : {center} + ({offsets['bit1_face']:+d}) = {bottom}")

    print("\nINTERPRETATION")
    print("==============")
    print("The export already encodes the prism weights as center-plus-offset data.")
    print("So d = 5 is not only observed in the weights; it is built into the normalized edge law.")
    print("What remains open is whether that normalized law itself is forced by deeper carrier structure.")

    print(f"\nread {PRISM_PATH}")


if __name__ == "__main__":
    main()
