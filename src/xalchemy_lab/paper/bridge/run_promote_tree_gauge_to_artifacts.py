from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def write_json(path: str, data: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(data, indent=2) + "\n")


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
    artifacts_path = "specs/paper/bridge/signed_lift_actual_loop_artifacts_v1.json"
    gauge_path = "specs/paper/bridge/tree_gauge_representative_v1.json"

    artifacts = load_json(artifacts_path)
    gauge = load_json(gauge_path)
    edge_cocycle = gauge["edge_cocycle"]

    print("\n====================")
    print("PROMOTE TREE-GAUGE VALUES TO ARTIFACTS")
    print("====================\n")

    for loop in artifacts["loops"]:
        computed = loop_parity(loop, edge_cocycle)
        old = loop.get("actual_cocycle", None)
        loop["actual_cocycle"] = computed
        loop["status"] = "computed_from_tree_gauge_representative_v1"
        print(f"{loop['name']:14s} old={old} new={computed}")

    write_json(artifacts_path, artifacts)

    print("\nUpdated:")
    print(f"  {artifacts_path}")
    print()


if __name__ == "__main__":
    main()
