from __future__ import annotations

import sys
from pathlib import Path

from fastapi import APIRouter, Query

HTTP_DIR = Path(__file__).resolve().parents[2]
ALCHEMY_LAB_DIR = HTTP_DIR.parent
G900_DIR = ALCHEMY_LAB_DIR / "g900"

if str(G900_DIR) not in sys.path:
    sys.path.insert(0, str(G900_DIR))

from witness_machine.core import action_dict, state_dict, validate_state  # noqa: E402

router = APIRouter(prefix="/api/witness", tags=["witness"])


@router.get("/state")
def api_witness_state(
    frame: int = Query(..., ge=0),
    phase: int = Query(..., ge=0, le=1),
    r: int = Query(1, ge=1),
):
    state = validate_state((frame, phase), r)
    return {
        "ok": True,
        "payload": state_dict(state, r),
    }


@router.get("/action")
def api_witness_action(
    frame: int = Query(..., ge=0),
    r: int = Query(1, ge=1),
):
    return {
        "ok": True,
        "payload": action_dict(frame, r),
    }
