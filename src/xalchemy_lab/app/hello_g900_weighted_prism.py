from __future__ import annotations

import json
from pathlib import Path


PRISM_PATH = Path("specs/paper/g60/g900_weighted_prism_v0_1.json")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> None:
    data = load_json(PRISM_PATH)

    print("\nG900 WEIGHTED PRISM")
    print("===================")
    print(f"name              : {data['name']}")
    print(f"version           : {data['version']}")
    print(f"source            : {data['source']}")
    print(f"support graph     : {data['support_graph_name']}")
    print(f"exact match       : {data['support_graph_exact_match']}")

    summary = data["carrier_summary"]
    print("\nCARRIER SUMMARY")
    print("===============")
    print(f"cell count        : {summary['cell_count']}")
    print(f"layer count       : {summary['layer_count']}")
    print(f"macro count       : {summary['macro_count']}")
    print(f"bit count         : {summary['bit_count']}")

    print("\nCLASS NODE ORDER")
    print("================")
    for i, node in enumerate(data["class_node_order"]):
        print(f"{i:2d}                : {tuple(node)}")

    print("\nSUPPORT EDGES")
    print("=============")
    for edge in data["support_edges"]:
        print(
            f"{tuple(edge['a'])} <-> {tuple(edge['b'])} "
            f"weight={edge['weight']} kind={edge['kind']}"
        )

    law = data["normalized_edge_law"]
    print("\nNORMALIZED EDGE LAW")
    print("===================")
    print(f"center weight     : {law['center_weight']}")
    for key, value in law["offsets_from_center"].items():
        print(f"{key:16} : {value:+d}")

    print(f"\nread {PRISM_PATH}")


if __name__ == "__main__":
    main()
