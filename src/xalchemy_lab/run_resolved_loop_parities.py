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
    rtype = loop["representation_type"]

    if rtype == "symbolic_closed_walk":
        path = loop["resolved_base_walk"]
        return sum(edge_value(e, edge_cocycle) for e in path) % 2

    if rtype == "symbolic_two_path_loop":
        path_1 = loop["resolved_path_1"]
        path_2 = loop["resolved_path_2"]
        closed = list(path_1) + [f"{e}^-1" for e in reversed(path_2)]
        return sum(edge_value(e, edge_cocycle) for e in closed) % 2

    raise ValueError(f"Unsupported loop type: {rtype}")


def main() -> None:
    loops = load_json("specs/signed_lift_bridge_loops_resolved_v1.json")["loops"]
    edge_cocycle = load_json("specs/resolved_edge_cocycle_v1.json")["edge_cocycle"]

    print("\n====================")
    print("RESOLVED LOOP PARITIES")
    print("====================\n")

    for loop in loops:
        print(f"{loop['name']:14s} -> {loop_parity(loop, edge_cocycle)}")


if __name__ == "__main__":
    main()
