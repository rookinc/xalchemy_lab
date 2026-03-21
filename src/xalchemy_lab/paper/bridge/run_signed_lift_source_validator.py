from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def main() -> None:
    p = Path("specs/paper/bridge/signed_lift_source_v1.json")
    data = json.loads(p.read_text())

    base_vertices = set(data.get("base_vertices", []))
    lift_vertices = set(data.get("lift_vertices", []))
    projection = data.get("projection", {})
    base_edges = data.get("base_edges", [])
    lift_edges = data.get("lift_edges", [])

    print("\n====================")
    print("SIGNED-LIFT SOURCE VALIDATOR")
    print("====================\n")

    problems: list[str] = []

    if len(base_vertices) != 15:
        problems.append(f"expected 15 base vertices, found {len(base_vertices)}")

    if len(lift_vertices) != 30:
        problems.append(f"expected 30 lift vertices, found {len(lift_vertices)}")

    if set(projection.keys()) != lift_vertices:
        problems.append("projection keys do not match lift vertex set")

    base_edge_labels = []
    for row in base_edges:
        if len(row) != 3:
            problems.append(f"bad base edge row: {row}")
            continue
        label, u, v = row
        base_edge_labels.append(label)
        if u not in base_vertices or v not in base_vertices:
            problems.append(f"base edge {label} uses unknown base vertex")

    lift_edge_labels = []
    for row in lift_edges:
        if len(row) != 3:
            problems.append(f"bad lift edge row: {row}")
            continue
        label, u, v = row
        lift_edge_labels.append(label)
        if u not in lift_vertices or v not in lift_vertices:
            problems.append(f"lift edge {label} uses unknown lift vertex")

    base_counts = Counter(base_edge_labels)
    lift_counts = Counter(lift_edge_labels)

    for label, n in base_counts.items():
        if n != 1:
            problems.append(f"base edge label {label} appears {n} times; expected 1")
        if lift_counts.get(label, 0) != 2:
            problems.append(f"lift edge label {label} appears {lift_counts.get(label, 0)} times; expected 2")

    extra_lift_labels = set(lift_counts) - set(base_counts)
    if extra_lift_labels:
        problems.append(f"lift labels with no downstairs edge: {sorted(extra_lift_labels)}")

    print(f"base_vertices = {len(base_vertices)}")
    print(f"lift_vertices = {len(lift_vertices)}")
    print(f"base_edges    = {len(base_edges)}")
    print(f"lift_edges    = {len(lift_edges)}")

    if len(base_edges) == 30 and len(lift_edges) == 60:
        print("coverage      = FULL_G15_SIGNED_LIFT")
    else:
        print("coverage      = PARTIAL_SEED_ONLY")

    print()

    if problems:
        print("problems:")
        for msg in problems:
            print(f"  - {msg}")
        raise SystemExit(1)

    print("status: PASS")
    print()


if __name__ == "__main__":
    main()
