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

    even = weights["even_slice"]

    top = even["top_ab"]
    vertical = even["vertical_a"]
    bottom = even["bottom_ab"]

    ab_base = even["top_ab"] + even["bottom_ab"]
    bc_base = even["top_bc"] + even["bottom_bc"]
    ca_base = even["top_ca"] + even["bottom_ca"]

    center = prism["normalized_edge_law"]["center_weight"]

    expect("midpoint law", 2 * vertical == top + bottom)
    expect("center agreement", vertical == center)
    expect("top offset", top == center - 5)
    expect("bottom offset", bottom == center + 5)
    expect("uniform triangle base AB", ab_base == 290)
    expect("uniform triangle base BC", bc_base == 290)
    expect("uniform triangle base CA", ca_base == 290)
    expect("doubled center law", 2 * center == 290)

    print("\nG900 CENTERED PRISM LEMMA CHECK")
    print("===============================")
    print(f"top               : {top}")
    print(f"vertical          : {vertical}")
    print(f"bottom            : {bottom}")
    print(f"center            : {center}")

    print("\nIDENTITIES")
    print("==========")
    print(f"145 = (140 + 150)/2      : {vertical == (top + bottom) / 2}")
    print(f"140 = 145 - 5            : {top == center - 5}")
    print(f"150 = 145 + 5            : {bottom == center + 5}")
    print(f"290 = 140 + 150          : {ab_base == 290}")
    print(f"290 = 2 * 145            : {2 * center == 290}")

    print("\nTRIANGLE BASE CANDIDATES")
    print("========================")
    print(f"AB                : {ab_base}")
    print(f"BC                : {bc_base}")
    print(f"CA                : {ca_base}")

    print("\nVERDICT")
    print("=======")
    print("centered prism descent lemma: PASS")

    print(f"\nread {PRISM_PATH}")
    print(f"read {WEIGHT_PATH}")


if __name__ == "__main__":
    main()
