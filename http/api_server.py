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
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_db_connection():
    return mysql.connector.connect(
        host=get_required_env("ALETHEOS_DB_HOST"),
        port=int(get_required_env("ALETHEOS_DB_PORT")),
        user=get_required_env("ALETHEOS_DB_USER"),
        password=get_required_env("ALETHEOS_DB_PASSWORD"),
        database=get_required_env("ALETHEOS_DB_NAME"),
    )


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(row)

    for key, value in list(normalized.items()):
        if isinstance(value, (bytes, bytearray)):
            normalized[key] = value.decode("utf-8")
        elif key in {"action_payload", "body_json"} and isinstance(value, str):
            try:
                normalized[key] = json.loads(value)
            except json.JSONDecodeError:
                pass

    return normalized


def fetch_all(query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [normalize_row(row) for row in rows]
    except MySQLError as exc:
        raise HTTPException(status_code=500, detail=f"MySQL error: {exc}") from exc
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


@app.get("/api/health")
def api_health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/bootstrap")
def api_bootstrap() -> dict[str, Any]:
    app_settings = fetch_all(
        """
        SELECT setting_key, setting_value, setting_type, notes
        FROM app_settings
        ORDER BY setting_key
        """
    )

    workspace_modules = fetch_all(
        """
        SELECT id, module_key, label, module_type, route_slug, description, is_active, sort_order
        FROM workspace_modules
        ORDER BY sort_order, id
        """
    )

    global_nav_items = fetch_all(
        """
        SELECT id, workspace_module_id, label, nav_key, icon_name, is_active, sort_order
        FROM global_nav_items
        ORDER BY sort_order, id
        """
    )

    tool_groups = fetch_all(
        """
        SELECT id, workspace_module_id, group_key, label, description, is_active, sort_order
        FROM tool_groups
        ORDER BY workspace_module_id, sort_order, id
        """
    )

    tool_items = fetch_all(
        """
        SELECT id, tool_group_id, item_key, label, action_type, action_payload, is_active, sort_order
        FROM tool_items
        ORDER BY tool_group_id, sort_order, id
        """
    )

    content_entries = fetch_all(
        """
        SELECT id, workspace_module_id, parent_entry_id, entry_key, title, entry_type, slug,
               body_html, body_json, status, is_default, sort_order
        FROM content_entries
        ORDER BY workspace_module_id, sort_order, id
        """
    )

    return {
        "app_settings": app_settings,
        "workspace_modules": workspace_modules,
        "global_nav_items": global_nav_items,
        "tool_groups": tool_groups,
        "tool_items": tool_items,
        "content_entries": content_entries,
    }


@app.get("/")
def site_root() -> FileResponse:
    return FileResponse(BASE_DIR / "index.html")


app.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static")
