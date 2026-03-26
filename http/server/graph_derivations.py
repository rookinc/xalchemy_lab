from __future__ import annotations

import math
from typing import Any


def derive_identity_graph(
    graph: dict[str, Any],
    base_nodes: list[dict[str, Any]],
    base_edges: list[dict[str, Any]],
    view: dict[str, Any],
    view_nodes: list[dict[str, Any]],
    view_edges: list[dict[str, Any]],
) -> dict[str, Any]:
    derived_graph = {
        "id": graph["id"],
        "graph_key": graph["graph_key"],
        "label": graph["label"],
        "description": graph.get("description"),
        "graph_kind": graph.get("graph_kind"),
        "status": "derived",
    }

    return {
        "graph": derived_graph,
        "source_graph": graph,
        "view": view,
        "nodes": base_nodes,
        "edges": base_edges,
        "view_nodes": view_nodes,
        "view_edges": view_edges,
    }


def derive_line_graph(
    graph: dict[str, Any],
    base_nodes: list[dict[str, Any]],
    base_edges: list[dict[str, Any]],
) -> dict[str, Any]:
    node_id_to_key = {row["id"]: row["node_key"] for row in base_nodes}

    derived_nodes: list[dict[str, Any]] = []
    edge_to_vertex: dict[int, dict[str, Any]] = {}

    for idx, edge in enumerate(base_edges):
        source_key = node_id_to_key.get(edge["source_node_id"], str(edge["source_node_id"]))
        target_key = node_id_to_key.get(edge["target_node_id"], str(edge["target_node_id"]))
        derived_key = edge["edge_key"] or f"e_{source_key}_{target_key}"

        derived_node = {
            "id": idx + 1,
            "graph_id": graph["id"],
            "node_key": derived_key,
            "label": derived_key,
            "payload_json": {
                "source_edge_id": edge["id"],
                "source_edge_key": edge["edge_key"],
                "source_edge_class": edge["edge_class"],
                "source_node_ids": [edge["source_node_id"], edge["target_node_id"]],
                "source_node_keys": [source_key, target_key],
            },
            "sort_order": idx,
        }
        derived_nodes.append(derived_node)
        edge_to_vertex[edge["id"]] = derived_node

    derived_edges: list[dict[str, Any]] = []
    seen_pairs: set[tuple[int, int]] = set()

    for i in range(len(base_edges)):
        for j in range(i + 1, len(base_edges)):
            a = base_edges[i]
            b = base_edges[j]

            shared = {
                a["source_node_id"],
                a["target_node_id"],
            } & {
                b["source_node_id"],
                b["target_node_id"],
            }

            if not shared:
                continue

            va = edge_to_vertex[a["id"]]
            vb = edge_to_vertex[b["id"]]
            pair = tuple(sorted((va["id"], vb["id"])))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            shared_node_ids = sorted(shared)
            shared_node_keys = [node_id_to_key[x] for x in shared_node_ids]

            derived_edges.append(
                {
                    "id": len(derived_edges) + 1,
                    "graph_id": graph["id"],
                    "source_node_id": va["id"],
                    "target_node_id": vb["id"],
                    "edge_key": f"lg_{va['node_key']}__{vb['node_key']}",
                    "edge_class": "line_graph_adjacency",
                    "payload_json": {
                        "shared_node_ids": shared_node_ids,
                        "shared_node_keys": shared_node_keys,
                        "source_edge_ids": [a["id"], b["id"]],
                        "source_edge_keys": [a["edge_key"], b["edge_key"]],
                    },
                    "sort_order": len(derived_edges),
                }
            )

    n = len(derived_nodes)
    radius = 220.0

    derived_view_nodes: list[dict[str, Any]] = []
    for i, node in enumerate(derived_nodes):
        angle = (2.0 * math.pi * i) / max(n, 1)
        derived_view_nodes.append(
            {
                "id": i + 1,
                "graph_view_id": None,
                "graph_node_id": node["id"],
                "x": math.cos(angle) * radius,
                "y": math.sin(angle) * radius,
                "z": 0.0,
                "pinned": 0,
                "style_json": None,
            }
        )

    derived_view_edges: list[dict[str, Any]] = []
    for i, edge in enumerate(derived_edges):
        derived_view_edges.append(
            {
                "id": i + 1,
                "graph_view_id": None,
                "graph_edge_id": edge["id"],
                "style_json": {
                    "stroke": "#9d7bff",
                    "lineWidth": 2.0,
                },
                "is_visible": 1,
            }
        )

    view = {
        "id": None,
        "graph_id": graph["id"],
        "view_key": "derived_line_graph",
        "label": f"{graph['label']} through Line Graph Lens",
        "view_kind": "spring_2d",
        "renderer_key": "canvas_2d",
        "params_json": {
            "repulsion": 9000,
            "springK": 0.01,
            "springLength": 120,
            "centering": 0.002,
            "damping": 0.85,
            "maxSpeed": 12,
            "nodeRadius": 10,
        },
        "is_default": 0,
        "status": "derived",
    }

    derived_graph = {
        "id": graph["id"],
        "graph_key": f"{graph['graph_key']}__line_graph",
        "label": f"{graph['label']} :: Line Graph Lens",
        "description": f"Derived graph produced by applying the line_graph lens to '{graph['graph_key']}'.",
        "graph_kind": "derived_line_graph",
        "status": "derived",
    }

    return {
        "graph": derived_graph,
        "source_graph": graph,
        "view": view,
        "nodes": derived_nodes,
        "edges": derived_edges,
        "view_nodes": derived_view_nodes,
        "view_edges": derived_view_edges,
    }


def derive_incidence_graph(
    graph: dict[str, Any],
    base_nodes: list[dict[str, Any]],
    base_edges: list[dict[str, Any]],
) -> dict[str, Any]:
    source_vertex_nodes: list[dict[str, Any]] = []
    source_edge_nodes: list[dict[str, Any]] = []

    source_node_id_to_derived_id: dict[int, int] = {}
    source_edge_id_to_derived_id: dict[int, int] = {}

    next_id = 1

    for idx, node in enumerate(base_nodes):
        derived_node = {
            "id": next_id,
            "graph_id": graph["id"],
            "node_key": f"v::{node['node_key']}",
            "label": node["label"] or node["node_key"],
            "payload_json": {
                "source_kind": "vertex",
                "source_node_id": node["id"],
                "source_node_key": node["node_key"],
            },
            "sort_order": idx,
        }
        source_vertex_nodes.append(derived_node)
        source_node_id_to_derived_id[node["id"]] = next_id
        next_id += 1

    for idx, edge in enumerate(base_edges):
        derived_node = {
            "id": next_id,
            "graph_id": graph["id"],
            "node_key": f"e::{edge['edge_key'] or edge['id']}",
            "label": edge["edge_key"] or f"e{edge['id']}",
            "payload_json": {
                "source_kind": "edge",
                "source_edge_id": edge["id"],
                "source_edge_key": edge["edge_key"],
                "source_edge_class": edge["edge_class"],
            },
            "sort_order": len(base_nodes) + idx,
        }
        source_edge_nodes.append(derived_node)
        source_edge_id_to_derived_id[edge["id"]] = next_id
        next_id += 1

    derived_nodes = source_vertex_nodes + source_edge_nodes

    derived_edges: list[dict[str, Any]] = []
    for edge in base_edges:
        edge_vertex_id = source_edge_id_to_derived_id[edge["id"]]
        for source_node_id in (edge["source_node_id"], edge["target_node_id"]):
            derived_edges.append(
                {
                    "id": len(derived_edges) + 1,
                    "graph_id": graph["id"],
                    "source_node_id": source_node_id_to_derived_id[source_node_id],
                    "target_node_id": edge_vertex_id,
                    "edge_key": f"inc_{source_node_id}_{edge['id']}",
                    "edge_class": "incidence",
                    "payload_json": {
                        "source_node_id": source_node_id,
                        "source_edge_id": edge["id"],
                    },
                    "sort_order": len(derived_edges),
                }
            )

    vertex_radius = 220.0
    edge_radius = 120.0

    derived_view_nodes: list[dict[str, Any]] = []

    for i, node in enumerate(source_vertex_nodes):
        angle = (2.0 * math.pi * i) / max(len(source_vertex_nodes), 1)
        derived_view_nodes.append(
            {
                "id": len(derived_view_nodes) + 1,
                "graph_view_id": None,
                "graph_node_id": node["id"],
                "x": math.cos(angle) * vertex_radius,
                "y": math.sin(angle) * vertex_radius,
                "z": 0.0,
                "pinned": 0,
                "style_json": {"fill": "#7cc4ff"},
            }
        )

    for i, node in enumerate(source_edge_nodes):
        angle = (2.0 * math.pi * i) / max(len(source_edge_nodes), 1)
        derived_view_nodes.append(
            {
                "id": len(derived_view_nodes) + 1,
                "graph_view_id": None,
                "graph_node_id": node["id"],
                "x": math.cos(angle) * edge_radius,
                "y": math.sin(angle) * edge_radius,
                "z": 0.0,
                "pinned": 0,
                "style_json": {"fill": "#ffd166"},
            }
        )

    derived_view_edges: list[dict[str, Any]] = []
    for i, edge in enumerate(derived_edges):
        derived_view_edges.append(
            {
                "id": i + 1,
                "graph_view_id": None,
                "graph_edge_id": edge["id"],
                "style_json": {
                    "stroke": "#7cc4ff",
                    "lineWidth": 1.8,
                },
                "is_visible": 1,
            }
        )

    view = {
        "id": None,
        "graph_id": graph["id"],
        "view_key": "derived_incidence",
        "label": f"{graph['label']} through Incidence Lens",
        "view_kind": "spring_2d",
        "renderer_key": "canvas_2d",
        "params_json": {
            "repulsion": 9000,
            "springK": 0.01,
            "springLength": 100,
            "centering": 0.002,
            "damping": 0.85,
            "maxSpeed": 12,
            "nodeRadius": 10,
        },
        "is_default": 0,
        "status": "derived",
    }

    derived_graph = {
        "id": graph["id"],
        "graph_key": f"{graph['graph_key']}__incidence",
        "label": f"{graph['label']} :: Incidence Lens",
        "description": f"Derived incidence graph produced from '{graph['graph_key']}'.",
        "graph_kind": "derived_incidence",
        "status": "derived",
    }

    return {
        "graph": derived_graph,
        "source_graph": graph,
        "view": view,
        "nodes": derived_nodes,
        "edges": derived_edges,
        "view_nodes": derived_view_nodes,
        "view_edges": derived_view_edges,
    }
