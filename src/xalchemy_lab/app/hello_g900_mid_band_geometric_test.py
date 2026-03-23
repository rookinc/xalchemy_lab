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
    top_offset = law["offsets_from_center"]["bit0_face"]
    rung_offset = law["offsets_from_center"]["macro_rung"]
    bottom_offset = law["offsets_from_center"]["bit1_face"]

    top = center + top_offset
    rung = center + rung_offset
    bottom = center + bottom_offset

    half_layer = layer_count / 2
    band_width = bottom - top
    centered = (top + bottom == 2 * rung)

    print("\nG900 MID-BAND GEOMETRIC TEST")
    print("============================")
    print(f"layer count        : {layer_count}")
    print(f"half-layer         : {half_layer}")
    print(f"top                : {top}")
    print(f"rung               : {rung}")
    print(f"bottom             : {bottom}")
    print(f"band width         : {band_width}")

    print("\nCHECKS")
    print("======")
    print(f"centered band       : {centered}")
    print(f"top offset          : {top_offset}")
    print(f"bottom offset       : {bottom_offset}")
    print(f"|top offset|=L/2    : {abs(top_offset) == half_layer}")
    print(f"bottom offset=L/2   : {bottom_offset == half_layer}")
    print(f"band width = L      : {band_width == layer_count}")

    print("\nINTERPRETATION")
    print("==============")
    if centered and abs(top_offset) == half_layer and bottom_offset == half_layer and band_width == layer_count:
        print("The exported law is exactly consistent with a centered 10-layer face-to-face band.")
        print("This supports the mid-band geometric reading of d = 5.")
    else:
        print("The exported law does not match the simple centered-band reading.")
        print("The half-layer interpretation would need revision.")

    print(f"\nread {PRISM_PATH}")


if __name__ == "__main__":
    main()
