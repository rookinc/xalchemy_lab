from __future__ import annotations

from typing import Any

from .core import frame2_socket_cycle, witness_assembly
from .lifted import (
    LiftedState,
    lifted_W,
    lifted_tau,
    validate_lifted_state,
    visible_projection,
)

ALLOWED_SLOT4_PAYLOADS = ["o4", "s0", "s2", "s3", "s4", "t0", "t3", "t4"]
EXACT_PAYLOAD = "t2"

# First nondegenerate bridge table:
# for each frame, subjective/objective project to different bounded payloads.
SUBJECTIVE_PAYLOAD_BY_FRAME = {
    0: "t0",
    1: "s0",
    2: "o4",
    3: "s2",
    4: "s4",
}

OBJECTIVE_PAYLOAD_BY_FRAME = {
    0: "t3",
    1: "s3",
    2: "t4",
    3: "s4",
    4: "o4",
}


def base_payload(frame: int, family: int, r: int = 1) -> str:
    frame = frame % (5 * r)
    if r != 1:
        # For now keep the richer bridge pinned to r=1.
        frame = frame % 5
    if family == 0:
        return SUBJECTIVE_PAYLOAD_BY_FRAME[frame % 5]
    return OBJECTIVE_PAYLOAD_BY_FRAME[frame % 5]


def projected_payload(state: LiftedState, r: int = 1) -> str:
    frame, family, sheet = validate_lifted_state(state, r)

    payload = base_payload(frame, family, r)

    # Bridge doctrine:
    # one distinguished exact-forbidden install appears only on the hidden sheet.
    # This creates a real puncture candidate instead of a trivial always-bounded family.
    if frame % 5 == 2 and family == 0 and sheet == 1:
        return EXACT_PAYLOAD

    return payload


def projected_cycle(state: LiftedState, r: int = 1) -> list[str]:
    payload = projected_payload(state, r)
    return frame2_socket_cycle(payload, r)


def in_slot4_family(state: LiftedState, r: int = 1) -> bool:
    payload = projected_payload(state, r)
    return payload in ALLOWED_SLOT4_PAYLOADS


def sheet_legal(state: LiftedState, r: int = 1) -> bool:
    state = validate_lifted_state(state, r)
    if projected_payload(state, r) == EXACT_PAYLOAD:
        return False
    for nxt in next_lifted_states(state, r):
        if projected_payload(nxt, r) == EXACT_PAYLOAD:
            return False
    return True


def next_lifted_states(state: LiftedState, r: int = 1) -> list[LiftedState]:
    state = validate_lifted_state(state, r)
    # Native continuation uses frame advance and full sheet-flip operator.
    return [
        lifted_tau(state, r),
        lifted_W(state, r),
    ]


def escapes(state: LiftedState, r: int = 1) -> bool:
    state = validate_lifted_state(state, r)
    if not in_slot4_family(state, r):
        return True
    for nxt in next_lifted_states(state, r):
        if not in_slot4_family(nxt, r):
            return True
    return False


def retained(state: LiftedState, r: int = 1) -> bool:
    state = validate_lifted_state(state, r)
    return not escapes(state, r)


def bridge_state_dict(state: LiftedState, r: int = 1) -> dict[str, Any]:
    state = validate_lifted_state(state, r)
    cyc = projected_cycle(state, r)
    asm = witness_assembly(cyc, r)
    payload = asm["payload"]
    nxt = next_lifted_states(state, r)
    return {
        "lifted_state": list(state),
        "visible_projection": list(visible_projection(state, r)),
        "projected_cycle": cyc,
        "payload": payload,
        "in_slot4_family": in_slot4_family(state, r),
        "next_lifted_states": [list(x) for x in nxt],
        "next_payloads": [projected_payload(x, r) for x in nxt],
        "escapes": escapes(state, r),
        "sheet_legal": sheet_legal(state, r),
        "retained": retained(state, r),
        "exact_payload": EXACT_PAYLOAD,
        "is_exact_payload": payload == EXACT_PAYLOAD,
    }



def verify_causal_bridge(r: int = 1) -> dict[str, Any]:
    eq = verify_retained_sheet_equivalence(r)
    rows = eq["checks"]

    exact_rows = [row for row in rows if row["payload"] == EXACT_PAYLOAD]
    non_retained = [row for row in rows if not row["retained"]]
    sheet_illegal = [row for row in rows if not row["sheet_legal"]]

    non_retained_states = {tuple(row["state"]) for row in non_retained}
    sheet_illegal_states = {tuple(row["state"]) for row in sheet_illegal}

    exact_is_non_retained = all(not row["retained"] for row in exact_rows)
    exact_is_sheet_illegal = all(not row["sheet_legal"] for row in exact_rows)
    failure_sets_match = non_retained_states == sheet_illegal_states

    return {
        "scale": r,
        "status": "modeled",
        "exact_state_count": len(exact_rows),
        "non_retained_count": len(non_retained),
        "sheet_illegal_count": len(sheet_illegal),
        "exact_is_non_retained": exact_is_non_retained,
        "exact_is_sheet_illegal": exact_is_sheet_illegal,
        "failure_sets_match": failure_sets_match,
        "exact_states": exact_rows,
        "non_retained_states": non_retained,
        "sheet_illegal_states": sheet_illegal,
        "note": (
            "Causal bridge layer checks whether the exact-forbidden puncture pattern "
            "matches the current modeled failure/illegality sets."
        ),
    }


def verify_forbidden_fringe(r: int = 1) -> dict[str, Any]:
    eq = verify_retained_sheet_equivalence(r)
    rows = eq["checks"]

    def reaches_exact_in_one_step(row: dict[str, Any]) -> bool:
        return EXACT_PAYLOAD in row.get("next_payloads", [])

    exact_rows = [row for row in rows if row["payload"] == EXACT_PAYLOAD]
    fringe_rows = [row for row in rows if row["payload"] != EXACT_PAYLOAD and reaches_exact_in_one_step(row)]

    non_retained = [row for row in rows if not row["retained"]]
    sheet_illegal = [row for row in rows if not row["sheet_legal"]]

    forbidden_core_and_fringe = [row for row in rows if row["payload"] == EXACT_PAYLOAD or reaches_exact_in_one_step(row)]

    non_retained_states = {tuple(row["state"]) for row in non_retained}
    sheet_illegal_states = {tuple(row["state"]) for row in sheet_illegal}
    core_fringe_states = {tuple(row["state"]) for row in forbidden_core_and_fringe}

    return {
        "scale": r,
        "status": "modeled",
        "exact_core_count": len(exact_rows),
        "fringe_count": len(fringe_rows),
        "non_retained_count": len(non_retained),
        "sheet_illegal_count": len(sheet_illegal),
        "every_non_retained_is_core_or_fringe": non_retained_states.issubset(core_fringe_states),
        "every_sheet_illegal_is_core_or_fringe": sheet_illegal_states.issubset(core_fringe_states),
        "non_retained_equals_core_plus_fringe": non_retained_states == core_fringe_states,
        "sheet_illegal_equals_core_plus_fringe": sheet_illegal_states == core_fringe_states,
        "exact_rows": exact_rows,
        "fringe_rows": fringe_rows,
        "note": (
            "Forbidden fringe layer checks whether the current failure/illegality set "
            "is exactly the unique exact-forbidden t2 core plus its one-step causal fringe."
        ),
    }


def verify_fringe_dynamics(r: int = 1) -> dict[str, Any]:
    ff = verify_forbidden_fringe(r)

    fringe_rows = []
    for row in ff["fringe_rows"]:
        next_payloads = row.get("next_payloads", [])
        fringe_rows.append(
            {
                **row,
                "feeds_exact_core_in_one_step": EXACT_PAYLOAD in next_payloads,
                "is_not_exact_core": row.get("payload") != EXACT_PAYLOAD,
                "is_non_retained": not row.get("retained", True),
                "is_sheet_illegal": not row.get("sheet_legal", True),
            }
        )

    all_feed_exact_in_one_step = all(row["feeds_exact_core_in_one_step"] for row in fringe_rows)
    all_are_genuine_fringe = all(
        row["is_not_exact_core"] and row["is_non_retained"] and row["is_sheet_illegal"]
        for row in fringe_rows
    )

    return {
        "scale": r,
        "status": "modeled",
        "fringe_count": len(fringe_rows),
        "all_feed_exact_in_one_step": all_feed_exact_in_one_step,
        "all_are_genuine_fringe": all_are_genuine_fringe,
        "fringe_rows": fringe_rows,
        "note": (
            "Fringe dynamics checks whether every fringe state is genuinely outside the exact core "
            "and has a one-step continuation into the exact forbidden t2 core."
        ),
    }

def verify_retained_sheet_equivalence(r: int = 1) -> dict[str, Any]:
    checks = []
    n = 5 * r
    for frame in range(n):
        for family in (0, 1):
            for sheet in (0, 1):
                st: LiftedState = (frame, family, sheet)
                legal = sheet_legal(st, r)
                kept = retained(st, r)
                info = bridge_state_dict(st, r)
                checks.append(
                    {
                        "state": [frame, family, sheet],
                        "payload": info["payload"],
                        "next_payloads": info["next_payloads"],
                        "escapes": info["escapes"],
                        "sheet_legal": legal,
                        "retained": kept,
                        "equivalent": legal == kept,
                    }
                )

    exact_states = [row for row in checks if row["payload"] == EXACT_PAYLOAD]

    return {
        "scale": r,
        "state_count": len(checks),
        "all_equivalent": all(x["equivalent"] for x in checks),
        "all_retained_are_non_escape": all((not x["retained"]) or (not x["escapes"]) for x in checks),
        "exact_state_count": len(exact_states),
        "exact_states": exact_states,
        "checks": checks,
        "status": "modeled",
        "note": (
            "Bridge is now nondegenerate: projected payload depends on frame/family/sheet, "
            "exact payload t2 appears on a hidden-sheet branch, and retained is tested through native continuation."
        ),
    }
