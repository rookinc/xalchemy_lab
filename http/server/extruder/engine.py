from __future__ import annotations

import math
from typing import Any


def _circle_layout(node_ids: list[str], *, cx: float = 420, cy: float = 300, r: float = 210) -> dict[str, tuple[float, float]]:
    n = max(1, len(node_ids))
    out: dict[str, tuple[float, float]] = {}
    for i, node_id in enumerate(node_ids):
        theta = (2.0 * math.pi * i) / n - math.pi / 2.0
        out[node_id] = (cx + r * math.cos(theta), cy + r * math.sin(theta))
    return out


def _grid_layout(node_ids: list[str], *, x0: float = 120, y0: float = 100, dx: float = 90, dy: float = 90) -> dict[str, tuple[float, float]]:
    out: dict[str, tuple[float, float]] = {}
    cols = max(1, math.ceil(math.sqrt(max(1, len(node_ids)))))
    for i, node_id in enumerate(node_ids):
        row = i // cols
        col = i % cols
        out[node_id] = (x0 + col * dx, y0 + row * dy)
    return out


def _shell_layout(node_ids: list[str]) -> dict[str, tuple[float, float]]:
    return _circle_layout(node_ids)


def _apply_layout(node_ids: list[str], layout_key: str) -> dict[str, tuple[float, float]]:
    if layout_key == "grid":
        return _grid_layout(node_ids)
    if layout_key == "shell":
        return _shell_layout(node_ids)
    return _circle_layout(node_ids)


def _materialize(
    *,
    graph_key: str,
    label: str,
    grammar_key: str,
    walker_key: str,
    layout_key: str,
    vertex_count: int,
    node_ids: list[str],
    edge_pairs: list[tuple[str, str]],
    derivation_log: list[dict[str, Any]],
    is_closed: bool,
) -> dict[str, Any]:
    coords = _apply_layout(node_ids, layout_key)

    nodes = [
        {
            "id": node_id,
            "label": node_id,
            "x": round(coords[node_id][0], 3),
            "y": round(coords[node_id][1], 3),
        }
        for node_id in node_ids
    ]

    edges = [
        {
            "id": f"e{i}",
            "source": a,
            "target": b,
        }
        for i, (a, b) in enumerate(edge_pairs)
    ]

    return {
        "graph": {
            "graph_key": graph_key,
            "label": label,
            "graph_kind": "derived",
        },
        "params": {
            "vertex_count": vertex_count,
            "grammar_key": grammar_key,
            "walker_key": walker_key,
            "layout_key": layout_key,
        },
        "nodes": nodes,
        "edges": edges,
        "derivation_log": derivation_log,
        "meta": {
            "is_closed": is_closed,
            "step_count": len(derivation_log),
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
    }


def build_cycle(vertex_count: int, walker_key: str, layout_key: str) -> dict[str, Any]:
    node_ids = [f"v{i}" for i in range(vertex_count)]
    edge_pairs: list[tuple[str, str]] = []
    derivation_log: list[dict[str, Any]] = []

    if vertex_count == 1:
        return _materialize(
            graph_key="extruded__cycle__1",
            label="Extruded Cycle (1)",
            grammar_key="cycle",
            walker_key=walker_key,
            layout_key=layout_key,
            vertex_count=vertex_count,
            node_ids=node_ids,
            edge_pairs=[],
            derivation_log=[],
            is_closed=True,
        )

    for i in range(1, vertex_count):
        a = node_ids[i - 1]
        b = node_ids[i]
        edge_pairs.append((a, b))
        derivation_log.append(
            {
                "step_index": len(derivation_log),
                "rule_key": "attach_next",
                "active_vertex": a,
                "added_edges": [f"{a}->{b}"],
                "note": f"Attached {b} to {a}.",
            }
        )

    if vertex_count > 2:
        a = node_ids[-1]
        b = node_ids[0]
        edge_pairs.append((a, b))
        derivation_log.append(
            {
                "step_index": len(derivation_log),
                "rule_key": "close_cycle",
                "active_vertex": a,
                "added_edges": [f"{a}->{b}"],
                "note": "Closed the cycle back to the seed.",
            }
        )

    return _materialize(
        graph_key=f"extruded__cycle__{vertex_count}",
        label=f"Extruded Cycle ({vertex_count})",
        grammar_key="cycle",
        walker_key=walker_key,
        layout_key=layout_key,
        vertex_count=vertex_count,
        node_ids=node_ids,
        edge_pairs=edge_pairs,
        derivation_log=derivation_log,
        is_closed=vertex_count > 2,
    )


def build_path(vertex_count: int, walker_key: str, layout_key: str) -> dict[str, Any]:
    node_ids = [f"v{i}" for i in range(vertex_count)]
    edge_pairs: list[tuple[str, str]] = []
    derivation_log: list[dict[str, Any]] = []

    for i in range(1, vertex_count):
        a = node_ids[i - 1]
        b = node_ids[i]
        edge_pairs.append((a, b))
        derivation_log.append(
            {
                "step_index": len(derivation_log),
                "rule_key": "attach_next",
                "active_vertex": a,
                "added_edges": [f"{a}->{b}"],
                "note": f"Extended the path from {a} to {b}.",
            }
        )

    return _materialize(
        graph_key=f"extruded__path__{vertex_count}",
        label=f"Extruded Path ({vertex_count})",
        grammar_key="path",
        walker_key=walker_key,
        layout_key=layout_key,
        vertex_count=vertex_count,
        node_ids=node_ids,
        edge_pairs=edge_pairs,
        derivation_log=derivation_log,
        is_closed=False,
    )


def build_star(vertex_count: int, walker_key: str, layout_key: str) -> dict[str, Any]:
    node_ids = [f"v{i}" for i in range(vertex_count)]
    edge_pairs: list[tuple[str, str]] = []
    derivation_log: list[dict[str, Any]] = []

    if not node_ids:
        return _materialize(
            graph_key="extruded__star__0",
            label="Extruded Star (0)",
            grammar_key="star",
            walker_key=walker_key,
            layout_key=layout_key,
            vertex_count=vertex_count,
            node_ids=[],
            edge_pairs=[],
            derivation_log=[],
            is_closed=False,
        )

    center = node_ids[0]
    for i in range(1, vertex_count):
        b = node_ids[i]
        edge_pairs.append((center, b))
        derivation_log.append(
            {
                "step_index": len(derivation_log),
                "rule_key": "attach_to_center",
                "active_vertex": center,
                "added_edges": [f"{center}->{b}"],
                "note": f"Attached {b} to center {center}.",
            }
        )

    return _materialize(
        graph_key=f"extruded__star__{vertex_count}",
        label=f"Extruded Star ({vertex_count})",
        grammar_key="star",
        walker_key=walker_key,
        layout_key=layout_key,
        vertex_count=vertex_count,
        node_ids=node_ids,
        edge_pairs=edge_pairs,
        derivation_log=derivation_log,
        is_closed=False,
    )


def build_complete(vertex_count: int, walker_key: str, layout_key: str) -> dict[str, Any]:
    node_ids = [f"v{i}" for i in range(vertex_count)]
    edge_pairs: list[tuple[str, str]] = []
    derivation_log: list[dict[str, Any]] = []

    for i in range(vertex_count):
        for j in range(i + 1, vertex_count):
            a = node_ids[i]
            b = node_ids[j]
            edge_pairs.append((a, b))
            derivation_log.append(
                {
                    "step_index": len(derivation_log),
                    "rule_key": "complete_pair",
                    "active_vertex": a,
                    "added_edges": [f"{a}->{b}"],
                    "note": f"Joined pair ({a}, {b}).",
                }
            )

    return _materialize(
        graph_key=f"extruded__complete__{vertex_count}",
        label=f"Extruded Complete Graph ({vertex_count})",
        grammar_key="complete",
        walker_key=walker_key,
        layout_key=layout_key,
        vertex_count=vertex_count,
        node_ids=node_ids,
        edge_pairs=edge_pairs,
        derivation_log=derivation_log,
        is_closed=True,
    )


def build_petersen_preset(walker_key: str, layout_key: str) -> dict[str, Any]:
    node_ids = [f"v{i}" for i in range(10)]
    edge_pairs = [
        ("v0", "v1"), ("v1", "v2"), ("v2", "v3"), ("v3", "v4"), ("v4", "v0"),
        ("v5", "v7"), ("v7", "v9"), ("v9", "v6"), ("v6", "v8"), ("v8", "v5"),
        ("v0", "v5"), ("v1", "v6"), ("v2", "v7"), ("v3", "v8"), ("v4", "v9"),
    ]
    derivation_log = [
        {
            "step_index": i,
            "rule_key": "preset_edge",
            "active_vertex": a,
            "added_edges": [f"{a}->{b}"],
            "note": "Materialized canonical Petersen edge.",
        }
        for i, (a, b) in enumerate(edge_pairs)
    ]
    return _materialize(
        graph_key="extruded__petersen_preset",
        label="Petersen Preset",
        grammar_key="petersen_preset",
        walker_key=walker_key,
        layout_key=layout_key,
        vertex_count=10,
        node_ids=node_ids,
        edge_pairs=edge_pairs,
        derivation_log=derivation_log,
        is_closed=True,
    )


def generate_graph(
    *,
    vertex_count: int,
    grammar_key: str,
    walker_key: str,
    layout_key: str,
) -> dict[str, Any]:
    vertex_count = max(1, min(vertex_count, 60))

    if grammar_key == "cycle":
        return build_cycle(vertex_count, walker_key, layout_key)
    if grammar_key == "path":
        return build_path(vertex_count, walker_key, layout_key)
    if grammar_key == "star":
        return build_star(vertex_count, walker_key, layout_key)
    if grammar_key == "complete":
        return build_complete(vertex_count, walker_key, layout_key)
    if grammar_key == "petersen_preset":
        return build_petersen_preset(walker_key, layout_key)

    raise ValueError(f"Unknown grammar_key: {grammar_key}")
