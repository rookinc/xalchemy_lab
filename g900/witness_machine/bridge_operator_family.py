from __future__ import annotations

from typing import Any

from .bridge import (
    EXACT_PAYLOAD,
    OBJECTIVE_PAYLOAD_BY_FRAME,
    SUBJECTIVE_PAYLOAD_BY_FRAME,
)

BASE_SUBJECTIVE = dict(SUBJECTIVE_PAYLOAD_BY_FRAME)
BASE_OBJECTIVE = dict(OBJECTIVE_PAYLOAD_BY_FRAME)


def _payload_for(frame: int, family: int, sheet: int, exact_frame: int = 2, exact_family: int = 0) -> str:
    if frame == exact_frame and family == exact_family and sheet == 1:
        return EXACT_PAYLOAD
    if family == 0:
        return BASE_SUBJECTIVE[frame]
    return BASE_OBJECTIVE[frame]


def _apply_op(frame: int, family: int, sheet: int, op: str) -> tuple[int, int, int]:
    if op == "tau":
        return ((frame + 1) % 5, family, sheet)
    if op == "tau_inv":
        return ((frame - 1) % 5, family, sheet)
    if op == "W":
        return (frame, family, 1 - sheet)
    if op == "mu":
        return (frame, 1 - family, sheet)
    raise ValueError(f"unknown op: {op}")


def _evaluate_operator_set(
    ops: list[str],
    exact_frame: int = 2,
    exact_family: int = 0,
) -> dict[str, Any]:
    rows = []
    exact_rows = []
    non_retained = []
    sheet_illegal = []

    for frame in range(5):
        for family in (0, 1):
            for sheet in (0, 1):
                payload = _payload_for(frame, family, sheet, exact_frame, exact_family)

                next_states = [_apply_op(frame, family, sheet, op) for op in ops]
                next_payloads = [
                    _payload_for(f, fam, sh, exact_frame, exact_family)
                    for (f, fam, sh) in next_states
                ]

                sheet_legal = payload != EXACT_PAYLOAD and EXACT_PAYLOAD not in next_payloads
                retained = sheet_legal

                row = {
                    "state": [frame, family, sheet],
                    "payload": payload,
                    "ops": ops,
                    "next_payloads": next_payloads,
                    "sheet_legal": sheet_legal,
                    "retained": retained,
                    "equivalent": sheet_legal == retained,
                }
                rows.append(row)

                if payload == EXACT_PAYLOAD:
                    exact_rows.append(row)
                if not retained:
                    non_retained.append(row)
                if not sheet_legal:
                    sheet_illegal.append(row)

    fringe_rows = [
        row for row in rows
        if row["payload"] != EXACT_PAYLOAD and EXACT_PAYLOAD in row["next_payloads"]
    ]

    non_retained_states = {tuple(row["state"]) for row in non_retained}
    sheet_illegal_states = {tuple(row["state"]) for row in sheet_illegal}
    core_fringe_states = {tuple(row["state"]) for row in exact_rows + fringe_rows}

    return {
        "ops": ops,
        "exact_core_count": len(exact_rows),
        "fringe_count": len(fringe_rows),
        "failure_sets_match": non_retained_states == sheet_illegal_states,
        "core_plus_fringe_match": (
            non_retained_states == core_fringe_states
            and sheet_illegal_states == core_fringe_states
        ),
        "all_equivalent": all(row["equivalent"] for row in rows),
    }



def verify_bridge_operator_invariants(r: int = 1) -> dict[str, Any]:
    bof = verify_bridge_operator_family(r)
    cases = bof.get("cases", [])

    exact_core_counts = [c["summary"]["exact_core_count"] for c in cases]
    fringe_counts = [c["summary"]["fringe_count"] for c in cases]
    failure_matches = [c["summary"]["failure_sets_match"] for c in cases]
    core_fringe_matches = [c["summary"]["core_plus_fringe_match"] for c in cases]
    equivalences = [c["summary"]["all_equivalent"] for c in cases]

    return {
        "scale": r,
        "status": "modeled",
        "operator_case_count": len(cases),
        "exact_core_count_invariant": len(set(exact_core_counts)) == 1 and set(exact_core_counts) == {1},
        "failure_equals_illegality_invariant": all(failure_matches),
        "core_plus_fringe_invariant": all(core_fringe_matches),
        "retained_sheet_legal_equivalence_invariant": all(equivalences),
        "fringe_size_operator_sensitive": len(set(fringe_counts)) > 1,
        "fringe_size_range": {
            "min": min(fringe_counts) if fringe_counts else None,
            "max": max(fringe_counts) if fringe_counts else None,
            "values": sorted(set(fringe_counts)),
        },
        "note": (
            "Checks which bridge properties remain invariant across operator families "
            "and which properties vary with the chosen continuation law."
        ),
    }

def verify_bridge_operator_family(r: int = 1) -> dict[str, Any]:
    if r != 1:
        return {
            "scale": r,
            "status": "modeled",
            "note": "bridge operator-family tester is currently pinned to r=1",
        }

    operator_sets = [
        ["tau", "W"],
        ["tau", "tau_inv", "W"],
        ["tau", "W", "mu"],
        ["tau", "tau_inv", "W", "mu"],
        ["tau_inv", "W"],
        ["W", "mu"],
    ]

    cases = []
    for ops in operator_sets:
        cases.append({
            "ops": ops,
            "summary": _evaluate_operator_set(ops),
        })

    stable_under_tested_operator_sets = all(
        c["summary"]["all_equivalent"]
        and c["summary"]["failure_sets_match"]
        and c["summary"]["core_plus_fringe_match"]
        and c["summary"]["exact_core_count"] == 1
        for c in cases
    )

    return {
        "scale": r,
        "status": "modeled",
        "tested_operator_set_count": len(cases),
        "stable_under_tested_operator_sets": stable_under_tested_operator_sets,
        "cases": cases,
        "note": "Tests whether the exact-core-plus-fringe law survives changes in the continuation operator set.",
    }
