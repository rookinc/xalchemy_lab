from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def write_json(path: str, data: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(data, indent=2) + "\n")


def strip_inverse(symbol: str) -> str:
    return symbol[:-3] if symbol.endswith("^-1") else symbol


def main() -> None:
    aliases = load_json("specs/bridge_edge_aliases_v1.json")["aliases"]
    symbolic = load_json("specs/tree_gauge_representative_v1.json")

    src = symbolic["edge_cocycle"]
    projected: dict[str, int] = {}

    for sym, resolved in aliases.items():
        sym_base = strip_inverse(sym)
        edge_base = strip_inverse(resolved)

        if sym_base not in src:
            raise KeyError(f"Missing symbolic cocycle value for {sym_base}")

        value = int(src[sym_base]) % 2

        if edge_base in projected and projected[edge_base] != value:
            raise ValueError(
                f"Conflicting projected values for {edge_base}: "
                f"{projected[edge_base]} vs {value}"
            )

        projected[edge_base] = value

    out = {
        "name": "resolved_edge_cocycle_v1",
        "version": "0.1",
        "status": "projected_from_symbolic_bridge_cocycle",
        "source_kind": "projected_from_symbolic_or_partial_seed",
        "source_tree_gauge": "specs/tree_gauge_representative_v1.json",
        "source_aliases": "specs/bridge_edge_aliases_v1.json",
        "edge_cocycle": projected
    }

    write_json("specs/resolved_edge_cocycle_v1.json", out)

    print("\n====================")
    print("PROJECT SYMBOLIC COCYCLE TO RESOLVED EDGES")
    print("====================\n")
    for k in sorted(projected):
        print(f"{k:4s} -> {projected[k]}")
    print("\nWrote specs/resolved_edge_cocycle_v1.json\n")


if __name__ == "__main__":
    main()
