from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    in_path = Path("specs/tree_gauge_representative_import_v1.json")
    out_path = Path("specs/tree_gauge_representative_v1.json")

    if not in_path.exists():
        raise FileNotFoundError(
            "Missing specs/tree_gauge_representative_import_v1.json"
        )

    data = json.loads(in_path.read_text())

    required = ["x", "s1", "s2", "s3", "s4", "a", "b", "c", "d"]
    edge_cocycle = data.get("edge_cocycle", {})

    for key in required:
        if key not in edge_cocycle:
            raise ValueError(f"Missing required edge key: {key}")
        if edge_cocycle[key] not in (0, 1):
            raise ValueError(f"Edge {key} must be 0 or 1")

    promoted = {
        "name": "tree_gauge_representative_v1",
        "version": "1.0",
        "status": "independent_signed_lift_data_imported",
        "source_kind": "independent",
        "purpose": "Z2 cocycle representative on base-edge symbols for computing loop holonomy parity.",
        "convention": {
            "domain": "G15 base-edge symbols",
            "codomain": "Z2",
            "orientation_rule": "symbol^-1 uses the same cocycle value as symbol"
        },
        "edge_cocycle": {k: int(edge_cocycle[k]) for k in required},
        "import_metadata": {
            "import_source": data.get("import_source", "unspecified"),
            "import_notes": data.get("import_notes", [])
        }
    }

    out_path.write_text(json.dumps(promoted, indent=2) + "\n")
    print(f"imported independent tree-gauge data to {out_path}")


if __name__ == "__main__":
    main()
