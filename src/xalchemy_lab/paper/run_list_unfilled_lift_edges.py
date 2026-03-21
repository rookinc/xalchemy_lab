from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def main() -> None:
    data = load_json("specs/paper/bridge/signed_lift_source_v1.json")

    base_edges = {label: (u, v) for label, u, v in data["base_edges"]}
    lift_edges = data["lift_edges"]

    print("\n====================")
    print("UNFILLED LIFT EDGES")
    print("====================\n")

    count = 0
    for i, row in enumerate(lift_edges):
        label, u, v = row
        if "TBD" in u or "TBD" in v:
            bu, bv = base_edges[label]
            print(f"{i:02d}: {label} downstairs=({bu},{bv}) upstairs=({u},{v})")
            count += 1

    print()
    print(f"unfilled_rows = {count}")
    print()


if __name__ == "__main__":
    main()
