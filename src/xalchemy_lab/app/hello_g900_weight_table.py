from __future__ import annotations

import json
from pathlib import Path


WEIGHT_PATH = Path("specs/paper/g60/g900_prism_weight_table_v0_1.json")
EVEN_PATH = Path("specs/paper/g60/even_slice_prism_support_v0_1.json")
ODD_PATH = Path("specs/paper/g60/odd_slice_prism_support_v0_1.json")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def fmt(value) -> str:
    return "PENDING" if value is None else str(value)


def print_section(title: str, data: dict) -> None:
    print(f"\n{title}")
    print("=" * len(title))
    for key, value in data.items():
        print(f"{key:16} : {fmt(value)}")


def expect_equal(label: str, actual, expected) -> None:
    if actual != expected:
        raise ValueError(
            f"{label} mismatch: actual={actual!r} expected={expected!r}"
        )


def main() -> None:
    weights = load_json(WEIGHT_PATH)
    even_doc = load_json(EVEN_PATH)
    odd_doc = load_json(ODD_PATH)

    even_expected = even_doc["prism_model"]["weights"]
    odd_expected = odd_doc["prism_model"]["weights"]

    expect_equal("even weights", weights["even_slice"], even_expected)
    expect_equal("odd weights", weights["odd_slice"], odd_expected)

    print("\nG900 PRISM WEIGHT TABLE")
    print("=======================")
    print(f"name              : {weights['name']}")
    print(f"version           : {weights['version']}")
    print(f"status            : {weights['status']}")

    print_section("EVEN SLICE", weights["even_slice"])
    print_section("ODD SLICE", weights["odd_slice"])
    print_section("TRIANGLE PUSHFORWARD", weights["triangle_pushforward"])
    print_section("COMPARISON", weights["comparison"])

    print("\nWEIGHT CHECK")
    print("============")
    print("even slice source : PASS")
    print("odd slice source  : PASS")

    print(f"\nread {WEIGHT_PATH}")
    print(f"read {EVEN_PATH}")
    print(f"read {ODD_PATH}")


if __name__ == "__main__":
    main()
