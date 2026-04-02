from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from witness_machine.core import (
    action_cell,
    apply_word,
    frame_count,
    state_count,
    state_dict,
    validate_state,
    witness_assembly,
    witness_cycle,
)

router = APIRouter(prefix="/api/witness", tags=["witness"])


class ApplyRequest(BaseModel):
    state: list[int]
    op: Literal["tau", "tau_inv", "mu"]


def structure_payload(state: tuple[int, int], r: int = 1) -> dict:
    payload = state_dict(state, r)
    cycle = payload["witness_cycle"]
    assembly = witness_assembly(cycle, r)

    nodes = []
    for idx, label in enumerate(assembly["normalized_cycle"]):
        role = ["W", "X", "Y", "Z", "T", "I"][idx]
        nodes.append(
            {
                "id": label,
                "label": label,
                "role": role,
                "kind": label[0],
                "is_payload": role == "T",
            }
        )

    scaffold = assembly["assembly"]
    edge_specs = [
        ("WX", "diad"),
        ("XY", "coupler"),
        ("YZ", "diad"),
        ("ZT", "coupler"),
        ("TI", "diad"),
        ("IW", "coupler"),
    ]

    edges = []
    for edge_id, edge_type in edge_specs:
        a_role = edge_id[0]
        b_role = edge_id[1]
        edges.append(
            {
                "id": edge_id,
                "source": scaffold[a_role],
                "target": scaffold[b_role],
                "type": edge_type,
                "is_payload_edge": "T" in edge_id,
            }
        )

    return {
        "state": payload["state"],
        "code": payload["code"],
        "phase": payload["phase"],
        "phase_label": payload["phase_label"],
        "witness_cycle": payload["witness_cycle"],
        "action_cell": payload["action_cell"],
        "nodes": nodes,
        "edges": edges,
        "meta": {
            "assembly": assembly["assembly"],
            "payload": assembly["payload"],
            "socket": assembly["socket"],
            "diads": assembly["diads"],
            "couplers": assembly["couplers"],
            "rigid_edges": assembly["rigid_edges"],
            "variable_edges": assembly["variable_edges"],
            "exact_frame2_payload": assembly["exact_frame2_payload"],
            "is_exact_payload": assembly["is_exact_payload"],
        },
    }


@router.get("/info")
def api_witness_info(r: int = Query(1, ge=1)):
    return {
        "ok": True,
        "payload": {
            "scale": r,
            "frame_count": frame_count(r),
            "state_count": state_count(r),
            "initial_state": [0, 0],
            "phase_labels": {
                "0": "subjective",
                "1": "objective",
            },
            "ops": ["tau", "tau_inv", "mu"],
        },
    }


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
        "payload": {
            "frame": frame,
            "action_cell": action_cell(frame, r),
        },
    }


@router.get("/structure")
def api_witness_structure(
    frame: int = Query(..., ge=0),
    phase: int = Query(..., ge=0, le=1),
    r: int = Query(1, ge=1),
):
    state = validate_state((frame, phase), r)
    return {
        "ok": True,
        "payload": structure_payload(state, r),
    }


@router.post("/apply")
def api_witness_apply(body: ApplyRequest, r: int = Query(1, ge=1)):
    if len(body.state) != 2:
        raise HTTPException(status_code=400, detail="state must be [frame, phase]")

    state = validate_state((int(body.state[0]), int(body.state[1])), r)
    next_state = apply_word(state, [body.op], r)

    return {
        "ok": True,
        "payload": state_dict(next_state, r),
    }
