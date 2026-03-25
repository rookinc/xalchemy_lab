from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector
from mysql.connector import Error as MySQLError
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_db_connection():
    return mysql.connector.connect(
        host=get_required_env("ALETHEOS_DB_HOST"),
        port=int(get_required_env("ALETHEOS_DB_PORT")),
        user=get_required_env("ALETHEOS_DB_USER"),
        password=os.getenv("ALETHEOS_DB_PASSWORD", ""),
        database=get_required_env("ALETHEOS_DB_NAME"),
    )


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(row)

    for key, value in list(normalized.items()):
        if isinstance(value, (bytes, bytearray)):
            normalized[key] = value.decode("utf-8")
        elif key in {
            "action_payload",
            "body_json",
            "params_json",
            "payload_json",
            "style_json",
            "constraints_json",
        } and isinstance(value, str):
            try:
                normalized[key] = json.loads(value)
            except json.JSONDecodeError:
                pass

    return normalized


def fetch_all(query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [normalize_row(row) for row in rows]
    except MySQLError as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc


@app.get("/")
def root() -> FileResponse:
    return FileResponse(BASE_DIR / "index.html")


@app.get("/api/bootstrap")
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
            ORDER BY workspace_module_id, sort_order, id
            """
        ),
    }


@app.get("/api/graphs/{graph_key}/views/{view_key}")
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


app.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static")
