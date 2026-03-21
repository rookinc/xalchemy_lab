from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def edge_value(symbol: str, edge_cocycle: dict[str, Any]) -> int:
    base = symbol[:-3] if symbol.endswith("^-1") else symbol
    value = edge_cocycle.get(base, None)
    if value is None:
        raise ValueError(f"Missing cocycle value for edge symbol: {base}")
    return int(value) % 2


def loop_parity(loop: dict[str, Any], edge_cocycle: dict[str, Any]) -> int:
    loop_type = loop["base_walk_type"]

    if loop_type == "symbolic_closed_walk":
        path = loop["base_walk"]
        return sum(edge_value(e, edge_cocycle) for e in path) % 2

    if loop_type == "symbolic_two_path_loop":
        path_1 = loop["path_1"]
        path_2 = loop["path_2"]
        closed = list(path_1) + [f"{e}^-1" for e in reversed(path_2)]
        return sum(edge_value(e, edge_cocycle) for e in closed) % 2

    raise ValueError(f"Unsupported loop type: {loop_type}")


def main() -> None:
    artifacts = load_json("specs/signed_lift_actual_loop_artifacts_v1.json")
    gauge = load_json("specs/tree_gauge_representative_v1.json")
    edge_cocycle = gauge["edge_cocycle"]

    loops = {loop["name"]: loop for loop in artifacts["loops"]}

    print("\n====================")
    print("TREE-GAUGE LOOP PARITIES")
    print("====================\n")

    for name in ("global_return", "global_square", "global_twist"):
        parity = loop_parity(loops[name], edge_cocycle)
        print(f"{name:14s} -> {parity}")


if __name__ == "__main__":
    main()
