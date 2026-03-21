from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def sheet(v: str) -> str:
    if "TBD" in v:
        raise ValueError(f"Unfilled lift vertex: {v}")
    if v.endswith("+"):
        return "+"
    if v.endswith("-"):
        return "-"
    raise ValueError(f"Lift vertex missing sheet sign: {v}")


def derive_edge_cocycle(data: dict[str, Any]) -> dict[str, int]:
    lift_edges = {}
    for label, u, v in data["lift_edges"]:
        if "TBD" in u or "TBD" in v:
            continue
        lift_edges.setdefault(label, []).append((u, v))

    result: dict[str, int] = {}

    for label, _u0, _v0 in data["base_edges"]:
        pairs = lift_edges.get(label, [])
        if len(pairs) == 0:
            continue
        if len(pairs) != 2:
            raise ValueError(f"Base edge {label} has partial lift data: found {len(pairs)} rows")

        kinds = []
        for u, v in pairs:
            kinds.append(sheet(u) != sheet(v))

        if kinds[0] != kinds[1]:
            raise ValueError(f"Inconsistent lift type for edge {label}: {pairs}")

        result[label] = 1 if kinds[0] else 0

    return result


def main() -> None:
    data = load_json("specs/signed_lift_source_v1.json")
    edge_cocycle = derive_edge_cocycle(data)

    out = {
        "name": "tree_gauge_representative_v1",
        "version": "0.2",
        "status": "derived_from_partial_signed_lift_source",
        "source_kind": "derived_from_signed_lift_source",
        "purpose": "Z2 cocycle representative derived from the currently filled portion of the lift data.",
        "convention": {
            "domain": "G15 base-edge symbols",
            "codomain": "Z2",
            "orientation_rule": "symbol^-1 uses the same cocycle value as symbol"
        },
        "edge_cocycle": edge_cocycle,
        "notes": [
            "Only fully filled lift edges are included.",
            "Unfilled TBD rows are ignored."
        ]
    }

    Path("specs/tree_gauge_representative_v1.json").write_text(json.dumps(out, indent=2) + "\n")

    print("\n====================")
    print("DERIVE COCYCLE FROM SIGNED LIFT")
    print("====================\n")
    for k in sorted(edge_cocycle):
        print(f"{k:3s} -> {edge_cocycle[k]}")
    print("\nUpdated specs/tree_gauge_representative_v1.json\n")


if __name__ == "__main__":
    main()
