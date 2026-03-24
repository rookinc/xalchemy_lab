from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def load_loop_artifacts() -> dict[str, dict[str, Any]]:
    data = load_json("specs/paper/bridge/signed_lift_actual_loop_artifacts_v1.json")
    return {loop["name"]: loop for loop in data["loops"]}


def load_tree_gauge_cocycle() -> dict[str, int]:
    data = load_json("specs/paper/bridge/tree_gauge_representative_v1.json")
    return {str(k): int(v) % 2 for k, v in data["edge_cocycle"].items()}


def load_aliases() -> dict[str, str]:
    data = load_json("specs/paper/bridge/bridge_edge_aliases_v1.json")
    return {str(k): str(v) for k, v in data["aliases"].items()}


def resolve_symbol(symbol: str, aliases: dict[str, str]) -> str:
    inverse = symbol.endswith("^-1")
    base = symbol[:-3] if inverse else symbol
    resolved = aliases.get(base, base)
    return f"{resolved}^-1" if inverse else resolved


def edge_value(symbol: str, cocycle: dict[str, int], aliases: dict[str, str]) -> int:
    resolved = resolve_symbol(symbol, aliases)
    base = resolved[:-3] if resolved.endswith("^-1") else resolved
    if base not in cocycle:
        raise KeyError(f"Missing cocycle value for edge symbol: {base}")
    return cocycle[base]


def loop_parity(loop: dict[str, Any], cocycle: dict[str, int], aliases: dict[str, str]) -> int:
    rtype = loop["base_walk_type"]

    if rtype == "symbolic_closed_walk":
        path = loop["base_walk"]
        return sum(edge_value(e, cocycle, aliases) for e in path) % 2

    if rtype == "symbolic_two_path_loop":
        path_1 = loop["path_1"]
        path_2 = loop["path_2"]
        closed = list(path_1) + [f"{e}^-1" for e in reversed(path_2)]
        return sum(edge_value(e, cocycle, aliases) for e in closed) % 2

    raise ValueError(f"Unsupported loop type: {rtype}")


def main() -> None:
    loops = load_loop_artifacts()
    cocycle = load_tree_gauge_cocycle()
    aliases = load_aliases()

    print("\n====================")
    print("ACTUAL COCYCLE DERIVATION FROM ARTIFACT")
    print("====================\n")

    for name in ("global_return", "global_square", "global_twist"):
        parity = loop_parity(loops[name], cocycle, aliases)
        print(f"{name:14s} -> {parity}")


if __name__ == "__main__":
    main()
