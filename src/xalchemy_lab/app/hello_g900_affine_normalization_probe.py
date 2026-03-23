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

    same_macro = 900.0
    live_shift = 405.0

    midpoint = (same_macro + live_shift) / 2.0
    half_gap = (same_macro - live_shift) / 2.0

    target_mid = float(center)
    target_gap = float(bit1 - center)

    a = target_gap / half_gap
    b = target_mid - a * midpoint

    mapped_same = a * same_macro + b
    mapped_live = a * live_shift + b
    mapped_mid = a * midpoint + b

    print("\nG900 AFFINE NORMALIZATION PROBE")
    print("===============================")

    print("\nCARRIER DATA")
    print("============")
    print(f"same_macro          : {same_macro}")
    print(f"live_shift          : {live_shift}")
    print(f"midpoint            : {midpoint}")
    print(f"half_gap            : {half_gap}")

    print("\nEXPORTED TARGET")
    print("===============")
    print(f"bit0_face           : {bit0}")
    print(f"macro_rung          : {rung}")
    print(f"bit1_face           : {bit1}")
    print(f"target midpoint     : {target_mid}")
    print(f"target half_gap     : {target_gap}")

    print("\nAFFINE MAP")
    print("==========")
    print(f"w = a*r + b")
    print(f"a                   : {a}")
    print(f"b                   : {b}")

    print("\nMAPPED VALUES")
    print("=============")
    print(f"map(same_macro)     : {mapped_same}")
    print(f"map(live_shift)     : {mapped_live}")
    print(f"map(midpoint)       : {mapped_mid}")

    print("\nCHECK")
    print("=====")
    print(f"same -> bit1_face   : {abs(mapped_same - bit1) < 1e-9}")
    print(f"live -> bit0_face   : {abs(mapped_live - bit0) < 1e-9}")
    print(f"mid -> macro_rung   : {abs(mapped_mid - rung) < 1e-9}")

    print("\nINTERPRETATION")
    print("==============")
    print("This does not prove the export uses this affine map.")
    print("It tests whether a simple midpoint-preserving affine normalization can send")
    print("the asymmetric carrier role pair (same_macro, live_shift) to the signed prism law.")
    print("If it works exactly, then the next question is whether that affine map is principled or accidental.")

    print(f"\nread {PRISM_PATH}")


if __name__ == "__main__":
    main()
