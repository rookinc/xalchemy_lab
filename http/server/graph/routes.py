from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from server.db import fetch_all
from .derivations import (
    derive_identity_graph,
    derive_incidence_graph,
    derive_line_graph,
)

router = APIRouter()


@router.get("/bootstrap")
def api_bootstrap() -> dict[str, Any]:
    return {
        "app_settings": fetch_all(
            """
            SELECT id, setting_key, setting_value, value_type, sort_order
            FROM app_settings
            ORDER BY sort_order, id
            """
        ),
        "workspace_modules": fetch_all(
            """
            SELECT id, module_key, label, module_kind, renderer_key, description,
                   is_active, sort_order, created_at, updated_at
            FROM workspace_modules
            ORDER BY sort_order, id
            """
        ),
        "global_nav_items": fetch_all(
            """
            SELECT id, nav_key, label, workspace_module_id, is_active, sort_order
            FROM global_nav_items
            ORDER BY sort_order, id
            """
        ),
        "tool_groups": fetch_all(
            """
            SELECT id, workspace_module_id, group_key, label, is_active, sort_order
            FROM tool_groups
            ORDER BY sort_order, id
            """
        ),
        "tool_items": fetch_all(
            """
            SELECT id, tool_group_id, item_key, label, action_payload, is_active, sort_order
            FROM tool_items
            ORDER BY sort_order, id
            """
        ),
        "content_entries": fetch_all(
            """
            SELECT id, workspace_module_id, entry_key, title, body_html, body_json,
                   is_default, status, sort_order, created_at, updated_at
            FROM content_entries
            ORDER BY workspace_modules_id, sort_order, id
            """
        ),
    }


@router.get("/graphs")
def api_graphs() -> dict[str, Any]:
    graphs = fetch_all(
        """
        SELECT
          g.id,
          g.graph_key,
          g.label,
          g.description,
          g.graph_kind,
          g.status,
          COUNT(DISTINCT n.id) AS node_count,
          COUNT(DISTINCT e.id) AS edge_count
        FROM graphs g
        LEFT JOIN graph_nodes n
          ON n.graph_id = g.id
        LEFT JOIN graph_edges e
          ON e.graph_id = g.id
        GROUP BY
          g.id, g.graph_key, g.label, g.description, g.graph_kind, g.status
        ORDER BY g.graph_key
        """
    )
    return {"ok": True, "items": graphs, "count": len(graphs)}


@router.get("/graphs/{graph_key}")
def api_graph(graph_key: str) -> dict[str, Any]:
    graph_rows = fetch_all(
        """
        SELECT id, graph_key, label, description, graph_kind, status, created_at, updated_at
        FROM graphs
        WHERE graph_key = %s
        LIMIT 1
        """,
        (graph_key,),
    )
    if not graph_rows:
        raise HTTPException(status_code=404, detail=f"Graph not found: {graph_key}")

    graph = graph_rows[0]

    nodes = fetch_all(
        """
        SELECT id, graph_id, node_key, label, payload_json, sort_order
        FROM graph_nodes
        WHERE graph_id = %s
        ORDER BY sort_order, id
        """,
        (graph["id"],),
    )

    edges = fetch_all(
        """
        SELECT id, graph_id, source_node_id, target_node_id, edge_key, edge_class,
               payload_json, sort_order
        FROM graph_edges
        WHERE graph_id = %s
        ORDER BY sort_order, id
        """,
        (graph["id"],),
    )

    return {"ok": True, "graph": graph, "nodes": nodes, "edges": edges}


@router.get("/graphs/{graph_key}/views")
def api_graph_views_for_graph(graph_key: str) -> dict[str, Any]:
    graph_rows = fetch_all(
        """
        SELECT id, graph_key, label, description, graph_kind, status
        FROM graphs
        WHERE graph_key = %s
        LIMIT 1
        """,
        (graph_key,),
    )
    if not graph_rows:
        raise HTTPException(status_code=404, detail=f"Graph not found: {graph_key}")

    graph = graph_rows[0]

    views = fetch_all(
        """
        SELECT
          id,
          graph_id,
          view_key,
          label,
          view_kind,
          renderer_key,
          params_json,
          is_default,
          status
        FROM graph_views
        WHERE graph_id = %s
        ORDER BY is_default DESC, view_key
        """,
        (graph["id"],),
    )

    return {"ok": True, "graph": graph, "items": views, "count": len(views)}


@router.get("/graphs/{graph_key}/views/{view_key}")
def api_graph_view(graph_key: str, view_key: str) -> dict[str, Any]:
    graph_rows = fetch_all(
        """
        SELECT id, graph_key, label, description, graph_kind, status, created_at, updated_at
        FROM graphs
        WHERE graph_key = %s
        LIMIT 1
        """,
        (graph_key,),
    )
    if not graph_rows:
        raise HTTPException(status_code=404, detail=f"Graph not found: {graph_key}")

    graph = graph_rows[0]

    view_rows = fetch_all(
        """
        SELECT id, graph_id, view_key, label, view_kind, renderer_key, params_json,
               is_default, status
        FROM graph_views
        WHERE graph_id = %s AND view_key = %s
        LIMIT 1
        """,
        (graph["id"], view_key),
    )
    if not view_rows:
        raise HTTPException(
            status_code=404,
            detail=f"View not found for graph '{graph_key}': {view_key}",
        )

    view = view_rows[0]

    nodes = fetch_all(
        """
        SELECT id, graph_id, node_key, label, payload_json, sort_order
        FROM graph_nodes
        WHERE graph_id = %s
        ORDER BY sort_order, id
        """,
        (graph["id"],),
    )

    edges = fetch_all(
        """
        SELECT id, graph_id, source_node_id, target_node_id, edge_key, edge_class,
               payload_json, sort_order
        FROM graph_edges
        WHERE graph_id = %s
        ORDER BY sort_order, id
        """,
        (graph["id"],),
    )

    view_nodes = fetch_all(
        """
        SELECT id, graph_view_id, graph_node_id, x, y, z, pinned, style_json
        FROM graph_view_nodes
        WHERE graph_view_id = %s
        ORDER BY id
        """,
        (view["id"],),
    )

    view_edges = fetch_all(
        """
        SELECT id, graph_view_id, graph_edge_id, style_json, is_visible
        FROM graph_view_edges
        WHERE graph_view_id = %s
        ORDER BY id
        """,
        (view["id"],),
    )

    actions = fetch_all(
        """
        SELECT
          ga.id,
          ga.action_key,
          ga.label,
          ga.action_kind,
          ga.handler_key,
          ga.description,
          ga.params_json,
          ga.status,
          gva.is_enabled,
          gva.sort_order,
          gva.constraints_json
        FROM graph_view_actions gva
        JOIN graph_actions ga
          ON ga.id = gva.graph_action_id
        WHERE gva.graph_view_id = %s
        ORDER BY gva.sort_order, ga.id
        """,
        (view["id"],),
    )

    return {
        "graph": graph,
        "view": view,
        "nodes": nodes,
        "edges": edges,
        "view_nodes": view_nodes,
        "view_edges": view_edges,
        "actions": actions,
    }


@router.get("/graph-views")
def api_graph_views() -> list[dict[str, Any]]:
    return fetch_all(
        """
        SELECT
          g.graph_key,
          g.label AS graph_label,
          gv.view_key,
          gv.label AS view_label,
          gv.view_kind,
          gv.renderer_key,
          gv.is_default
        FROM graph_views gv
        JOIN graphs g
          ON g.id = gv.graph_id
        WHERE g.status = 'active'
          AND gv.status = 'active'
        ORDER BY g.graph_key, gv.view_key
        """
    )


@router.get("/graphs/{graph_key}/lenses")
def api_graph_lenses(graph_key: str) -> list[dict[str, Any]]:
    graph_rows = fetch_all(
        """
        SELECT id, graph_key, label, description, graph_kind, status
        FROM graphs
        WHERE graph_key = %s
        LIMIT 1
        """,
        (graph_key,),
    )
    if not graph_rows:
        raise HTTPException(status_code=404, detail=f"Graph not found: {graph_key}")

    graph = graph_rows[0]

    return fetch_all(
        """
        SELECT
          gl.id,
          gl.lens_key,
          gl.label,
          gl.lens_kind,
          gl.description,
          gl.params_json,
          gl.status,
          glb.is_enabled,
          glb.sort_order,
          glb.params_json AS binding_params_json
        FROM graph_lens_bindings glb
        JOIN graph_lenses gl
          ON gl.id = glb.graph_lens_id
        WHERE glb.graph_id = %s
          AND gl.status = 'active'
          AND glb.is_enabled = 1
        ORDER BY glb.sort_order, gl.lens_key
        """,
        (graph["id"],),
    )


@router.get("/graphs/{graph_key}/lenses/{lens_key}")
def api_graph_lens(graph_key: str, lens_key: str) -> dict[str, Any]:
    graph_rows = fetch_all(
        """
        SELECT id, graph_key, label, description, graph_kind, status
        FROM graphs
        WHERE graph_key = %s
        LIMIT 1
        """,
        (graph_key,),
    )
    if not graph_rows:
        raise HTTPException(status_code=404, detail=f"Graph not found: {graph_key}")

    graph = graph_rows[0]

    lens_rows = fetch_all(
        """
        SELECT
          gl.id,
          gl.lens_key,
          gl.label,
          gl.lens_kind,
          gl.description,
          gl.params_json,
          gl.status,
          glb.is_enabled,
          glb.sort_order,
          glb.params_json AS binding_params_json
        FROM graph_lens_bindings glb
        JOIN graph_lenses gl
          ON gl.id = glb.graph_lens_id
        WHERE glb.graph_id = %s
          AND gl.lens_key = %s
        LIMIT 1
        """,
        (graph["id"], lens_key),
    )
    if not lens_rows:
        raise HTTPException(
            status_code=404,
            detail=f"Lens not found for graph '{graph_key}': {lens_key}",
        )

    return {"graph": graph, "lens": lens_rows[0]}


@router.get("/graphs/{graph_key}/lenses/{lens_key}/derive")
def api_graph_lens_derive(graph_key: str, lens_key: str) -> dict[str, Any]:
    graph_rows = fetch_all(
        """
        SELECT id, graph_key, label, description, graph_kind, status
        FROM graphs
        WHERE graph_key = %s
        LIMIT 1
        """,
        (graph_key,),
    )
    if not graph_rows:
        raise HTTPException(status_code=404, detail=f"Graph not found: {graph_key}")

    base_graph = graph_rows[0]

    nodes = fetch_all(
        """
        SELECT id, graph_id, node_key, label, payload_json, sort_order
        FROM graph_nodes
        WHERE graph_id = %s
        ORDER BY sort_order, id
        """,
        (base_graph["id"],),
    )

    edges = fetch_all(
        """
        SELECT id, graph_id, source_node_id, target_node_id, edge_key, edge_class,
               payload_json, sort_order
        FROM graph_edges
        WHERE graph_id = %s
        ORDER BY sort_order, id
        """,
        (base_graph["id"],),
    )

    view_rows = fetch_all(
        """
        SELECT id, graph_id, view_key, label, view_kind, renderer_key, params_json,
               is_default, status
        FROM graph_views
        WHERE graph_id = %s
        ORDER BY is_default DESC, id
        LIMIT 1
        """,
        (base_graph["id"],),
    )
    if not view_rows:
        raise HTTPException(
            status_code=404,
            detail=f"No graph view found for graph '{graph_key}'",
        )

    view = view_rows[0]

    view_nodes = fetch_all(
        """
        SELECT id, graph_view_id, graph_node_id, x, y, z, pinned, style_json
        FROM graph_view_nodes
        WHERE graph_view_id = %s
        ORDER BY id
        """,
        (view["id"],),
    )

    view_edges = fetch_all(
        """
        SELECT id, graph_view_id, graph_edge_id, style_json, is_visible
        FROM graph_view_edges
        WHERE graph_view_id = %s
        ORDER BY id
        """,
        (view["id"],),
    )

    if lens_key == "identity":
        derived = derive_identity_graph(base_graph, nodes, edges, view, view_nodes, view_edges)
    elif lens_key == "line_graph":
        derived = derive_line_graph(base_graph, nodes, edges, view, view_nodes, view_edges)
    elif lens_key == "incidence":
        derived = derive_incidence_graph(base_graph, nodes, edges, view, view_nodes, view_edges)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Unsupported derivation lens for graph '{graph_key}': {lens_key}",
        )

    return derived

