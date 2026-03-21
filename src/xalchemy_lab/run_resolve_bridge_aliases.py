from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def write_json(path: str, data: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(data, indent=2) + "\n")


def resolve_symbol(symbol: str, aliases: dict[str, str]) -> str:
    is_inverse = symbol.endswith("^-1")
    base = symbol[:-3] if is_inverse else symbol

    if base not in aliases:
        raise KeyError(f"Missing alias for symbol: {symbol}")

    resolved = aliases[base]
    if is_inverse:
        return f"{resolved}^-1"
    return resolved


def main() -> None:
    loops = load_json("specs/signed_lift_bridge_loops_v1.json")
    aliases = load_json("specs/bridge_edge_aliases_v1.json")["aliases"]

    resolved_loops = []

    for loop in loops["loops"]:
        item = dict(loop)
        rtype = item["representation_type"]

        if rtype == "symbolic_closed_walk":
            item["resolved_base_walk"] = [resolve_symbol(s, aliases) for s in item["path"]]

        elif rtype == "symbolic_two_path_loop":
            item["resolved_path_1"] = [resolve_symbol(s, aliases) for s in item["path_1"]]
            item["resolved_path_2"] = [resolve_symbol(s, aliases) for s in item["path_2"]]

        else:
            raise ValueError(f"Unsupported loop type: {rtype}")

        resolved_loops.append(item)

    out = {
        "name": "signed_lift_bridge_loops_resolved_v1",
        "version": "0.1",
        "status": "resolved_against_full_G15_edge_aliases",
        "source_loop_spec": "specs/signed_lift_bridge_loops_v1.json",
        "source_aliases": "specs/bridge_edge_aliases_v1.json",
        "loops": resolved_loops
    }

    write_json("specs/signed_lift_bridge_loops_resolved_v1.json", out)
    print("wrote specs/signed_lift_bridge_loops_resolved_v1.json")


if __name__ == "__main__":
    main()
