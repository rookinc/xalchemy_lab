from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_loop_artifacts() -> dict[str, dict[str, Any]]:
    p = Path("specs/signed_lift_actual_loop_artifacts_v1.json")
    data = json.loads(p.read_text())
    return {loop["name"]: loop for loop in data["loops"]}


def load_tree_gauge_cocycle() -> dict[str, int]:
    """
    Expected minimal format:
    {
      "name": "tree_gauge_representative_v1",
      "edge_cocycle": {
        "x": 0,
        "s1": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "a": 0,
        "b": 0,
        "c": 1,
        "d": 0
      }
    }

    For now this file is the missing seam.
    """
    p = Path("specs/tree_gauge_representative_v1.json")
    if not p.exists():
        raise FileNotFoundError(
            "Missing specs/tree_gauge_representative_v1.json "
            "with actual edge cocycle data."
        )
    data = json.loads(p.read_text())
    return {str(k): int(v) % 2 for k, v in data["edge_cocycle"].items()}


def edge_value(symbol: str, cocycle: dict[str, int]) -> int:
    base = symbol[:-3] if symbol.endswith("^-1") else symbol
    if base not in cocycle:
        raise KeyError(f"Missing cocycle value for edge symbol: {base}")
    return cocycle[base]


def loop_parity(loop: dict[str, Any], cocycle: dict[str, int]) -> int:
    rtype = loop["base_walk_type"]

    if rtype == "symbolic_closed_walk":
        path = loop["base_walk"]
        return sum(edge_value(e, cocycle) for e in path) % 2

    if rtype == "symbolic_two_path_loop":
        path_1 = loop["path_1"]
        path_2 = loop["path_2"]
        # closed comparison cycle = path_1 + reverse(path_2)
        closed = list(path_1) + [f"{e}^-1" for e in reversed(path_2)]
        return sum(edge_value(e, cocycle) for e in closed) % 2

    raise ValueError(f"Unsupported loop type: {rtype}")


def main() -> None:
    loops = load_loop_artifacts()
    cocycle = load_tree_gauge_cocycle()

    print("\n====================")
    print("ACTUAL COCYCLE DERIVATION FROM ARTIFACT")
    print("====================\n")

    for name in ("global_return", "global_square", "global_twist"):
        parity = loop_parity(loops[name], cocycle)
        print(f"{name:14s} -> {parity}")


if __name__ == "__main__":
    main()
