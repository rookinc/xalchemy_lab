from __future__ import annotations

import json
from pathlib import Path


WEIGHT_PATH = Path("specs/paper/g60/g900_prism_weight_table_v0_1.json")


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


def main() -> None:
    data = load_json(WEIGHT_PATH)

    print("\nG900 PRISM WEIGHT TABLE")
    print("=======================")
    print(f"name              : {data['name']}")
    print(f"version           : {data['version']}")
    print(f"status            : {data['status']}")

    print_section("EVEN SLICE", data["even_slice"])
    print_section("ODD SLICE", data["odd_slice"])
    print_section("TRIANGLE PUSHFORWARD", data["triangle_pushforward"])
    print_section("COMPARISON", data["comparison"])

    print(f"\nread {WEIGHT_PATH}")


if __name__ == "__main__":
    main()
