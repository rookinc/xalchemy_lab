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

    even = weights["even_slice"]

    ab_base = even["top_ab"] + even["bottom_ab"]
    bc_base = even["top_bc"] + even["bottom_bc"]
    ca_base = even["top_ca"] + even["bottom_ca"]

    center = prism["normalized_edge_law"]["center_weight"]

    print("\nG900 TRIANGLE PUSHFORWARD PROBE")
    print("===============================")
    print(f"top face weight    : {even['top_ab']}")
    print(f"vertical weight    : {even['vertical_a']}")
    print(f"bottom face weight : {even['bottom_ab']}")
    print(f"center weight      : {center}")

    print("\nBASE TRIANGLE EDGE SUMS")
    print("=======================")
    print(f"AB base            : {even['top_ab']} + {even['bottom_ab']} = {ab_base}")
    print(f"BC base            : {even['top_bc']} + {even['bottom_bc']} = {bc_base}")
    print(f"CA base            : {even['top_ca']} + {even['bottom_ca']} = {ca_base}")

    print("\nCOMPARISON")
    print("==========")
    print(f"macro contact      : 290")
    print(f"AB base == 290     : {ab_base == 290}")
    print(f"BC base == 290     : {bc_base == 290}")
    print(f"CA base == 290     : {ca_base == 290}")

    print("\nCURRENT INTERPRETATION")
    print("======================")
    print("triangle pushforward is not yet fully extracted")
    print("base sums already land at 290 on each edge class")
    print("side contribution remains unresolved")

    print(f"\nread {PRISM_PATH}")
    print(f"read {WEIGHT_PATH}")


if __name__ == "__main__":
    main()
