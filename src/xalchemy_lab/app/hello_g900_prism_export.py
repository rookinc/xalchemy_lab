from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    artifact = {
        "name": "g900_weighted_prism_v0_1",
        "version": "0.1",
        "source": "order-30 triangular subdivision carrier classified by (macro, bit)",
        "carrier_summary": {
            "cell_count": 900,
            "layer_count": 10,
            "macro_count": 3,
            "bit_count": 2,
        },
        "class_node_order": [
            [0, 0],
            [1, 0],
            [2, 0],
            [0, 1],
            [1, 1],
            [2, 1],
        ],
        "weighted_adjacency_matrix": [
            [0, 140, 140, 145, 0,   0],
            [140, 0, 140, 0,   145, 0],
            [140, 140, 0, 0,   0,   145],
            [145, 0,   0, 0,   150, 150],
            [0,   145, 0, 150, 0,   150],
            [0,   0,   145, 150, 150, 0],
        ],
        "support_edges": [
            {"a": [0, 0], "b": [1, 0], "weight": 140, "kind": "bit0_face"},
            {"a": [0, 0], "b": [2, 0], "weight": 140, "kind": "bit0_face"},
            {"a": [1, 0], "b": [2, 0], "weight": 140, "kind": "bit0_face"},
            {"a": [0, 1], "b": [1, 1], "weight": 150, "kind": "bit1_face"},
            {"a": [0, 1], "b": [2, 1], "weight": 150, "kind": "bit1_face"},
            {"a": [1, 1], "b": [2, 1], "weight": 150, "kind": "bit1_face"},
            {"a": [0, 0], "b": [0, 1], "weight": 145, "kind": "macro_rung"},
            {"a": [1, 0], "b": [1, 1], "weight": 145, "kind": "macro_rung"},
            {"a": [2, 0], "b": [2, 1], "weight": 145, "kind": "macro_rung"},
        ],
        "support_graph_name": "triangular_prism",
        "support_graph_exact_match": True,
        "normalized_edge_law": {
            "center_weight": 145,
            "offsets_from_center": {
                "bit0_face": -5,
                "macro_rung": 0,
                "bit1_face": 5,
            },
        },
    }

    out_path = Path("specs/paper/g60/g900_weighted_prism_v0_1.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
