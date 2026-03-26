from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from .engine import generate_graph

router = APIRouter(prefix="/api/extruder", tags=["extruder"])


@router.get("/registry")
def api_extruder_registry() -> dict[str, Any]:
    return {
        "grammars": [
            {"key": "cycle", "label": "Cycle"},
            {"key": "path", "label": "Path"},
            {"key": "star", "label": "Star"},
            {"key": "complete", "label": "Complete Graph"},
            {"key": "petersen_preset", "label": "Petersen Preset"},
        ],
        "walkers": [
            {"key": "sequential", "label": "Sequential"},
            {"key": "radial", "label": "Radial"},
            {"key": "shell_grow", "label": "Shell Grow"},
        ],
        "layouts": [
            {"key": "circle", "label": "Circle"},
            {"key": "shell", "label": "Shell"},
            {"key": "grid", "label": "Grid"},
        ],
    }


@router.get("/generate")
def api_extruder_generate(
    vertex_count: int = Query(10, ge=1, le=60),
    grammar_key: str = Query("cycle"),
    walker_key: str = Query("sequential"),
    layout_key: str = Query("circle"),
) -> dict[str, Any]:
    try:
        return generate_graph(
            vertex_count=vertex_count,
            grammar_key=grammar_key,
            walker_key=walker_key,
            layout_key=layout_key,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
