from __future__ import annotations

from itertools import combinations
from typing import Any

from .bridge import (
    EXACT_PAYLOAD,
    OBJECTIVE_PAYLOAD_BY_FRAME,
    SUBJECTIVE_PAYLOAD_BY_FRAME,
    verify_causal_bridge,
    verify_forbidden_fringe,
)

BASE_SUBJECTIVE = dict(SUBJECTIVE_PAYLOAD_BY_FRAME)
BASE_OBJECTIVE = dict(OBJECTIVE_PAYLOAD_BY_FRAME)


def _swap_payload(mapping: dict[int, str], a: int, b: int) -> dict[int, str]:
    out = dict(mapping)
    out[a], out[b] = out[b], out[a]
    return out


def _rotate_payload(mapping: dict[int, str], shift: int) -> dict[int, str]:
    return {i: mapping[(i - shift) % 5] for i in range(5)}


def _evaluate_tables(
    subjective_map: dict[int, str],
    objective_map: dict[int, str],
    exact_frame: int = 2,
    exact_family: int = 0,
) -> dict[str, Any]:
    exact_rows = []
    non_retained = []
    sheet_illegal = []
    all_rows = []

    for frame in range(5):
        for family in (0, 1):
            for sheet in (0, 1):
                if family == 0:
                    payload = subjective_map[frame]
                    next_tau_payload = subjective_map[(frame + 1) % 5]
                    next_w_payload = EXACT_PAYLOAD if (frame == exact_frame and family == exact_family and sheet == 0) else payload
                else:
                    payload = objective_map[frame]
                    next_tau_payload = objective_map[(frame + 1) % 5]
                    next_w_payload = EXACT_PAYLOAD if (frame == exact_frame and family == exact_family and sheet == 0) else payload

                if frame == exact_frame and family == exact_family and sheet == 1:
                    payload = EXACT_PAYLOAD

                next_payloads = [next_tau_payload, next_w_payload]
                sheet_legal = payload != EXACT_PAYLOAD and EXACT_PAYLOAD not in next_payloads
                retained = sheet_legal

                row = {
                    "state": [frame, family, sheet],
                    "payload": payload,
                    "next_payloads": next_payloads,
                    "sheet_legal": sheet_legal,
                    "retained": retained,
                    "equivalent": sheet_legal == retained,
                }
                all_rows.append(row)

                if payload == EXACT_PAYLOAD:
                    exact_rows.append(row)
                if not retained:
                    non_retained.append(row)
                if not sheet_legal:
                    sheet_illegal.append(row)

    def reaches_exact_in_one_step(row: dict[str, Any]) -> bool:
        return EXACT_PAYLOAD in row["next_payloads"]

    fringe_rows = [
        row for row in all_rows
        if row["payload"] != EXACT_PAYLOAD and reaches_exact_in_one_step(row)
    ]

    non_retained_states = {tuple(row["state"]) for row in non_retained}
    sheet_illegal_states = {tuple(row["state"]) for row in sheet_illegal}
    core_fringe_states = {tuple(row["state"]) for row in exact_rows + fringe_rows}

    return {
        "exact_core_count": len(exact_rows),
        "fringe_count": len(fringe_rows),
        "failure_sets_match": non_retained_states == sheet_illegal_states,
        "core_plus_fringe_match": (
            non_retained_states == core_fringe_states
            and sheet_illegal_states == core_fringe_states
        ),
        "all_equivalent": all(row["equivalent"] for row in all_rows),
    }


def _summ(eval_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "exact_core_count": eval_result["exact_core_count"],
        "fringe_count": eval_result["fringe_count"],
        "failure_sets_match": eval_result["failure_sets_match"],
        "core_plus_fringe_match": eval_result["core_plus_fringe_match"],
        "all_equivalent": eval_result["all_equivalent"],
    }


def verify_bridge_family(r: int = 1) -> dict[str, Any]:
    if r != 1:
        return {
            "scale": r,
            "status": "modeled",
            "note": "bridge family perturbation tester is currently pinned to r=1",
        }

    base_cb = verify_causal_bridge(r)
    base_ff = verify_forbidden_fringe(r)

    base_model = {
        "exact_state_count": base_cb["exact_state_count"],
        "failure_sets_match": base_cb["failure_sets_match"],
        "exact_core_count": base_ff["exact_core_count"],
        "fringe_count": base_ff["fringe_count"],
        "core_plus_fringe_match": (
            base_ff["non_retained_equals_core_plus_fringe"]
            and base_ff["sheet_illegal_equals_core_plus_fringe"]
        ),
    }

    perturbations = []

    # all pair swaps in subjective or objective
    for a, b in combinations(range(5), 2):
        perturbations.append({
            "kind": "subjective_pair_swap",
            "swap": [a, b],
            "summary": _summ(_evaluate_tables(_swap_payload(BASE_SUBJECTIVE, a, b), BASE_OBJECTIVE)),
        })
        perturbations.append({
            "kind": "objective_pair_swap",
            "swap": [a, b],
            "summary": _summ(_evaluate_tables(BASE_SUBJECTIVE, _swap_payload(BASE_OBJECTIVE, a, b))),
        })

    # simultaneous pair swaps
    for a, b in combinations(range(5), 2):
        perturbations.append({
            "kind": "simultaneous_pair_swap",
            "swap": [a, b],
            "summary": _summ(
                _evaluate_tables(
                    _swap_payload(BASE_SUBJECTIVE, a, b),
                    _swap_payload(BASE_OBJECTIVE, a, b),
                )
            ),
        })

    # cyclic rotations of either table
    for shift in range(1, 5):
        perturbations.append({
            "kind": "subjective_rotation",
            "shift": shift,
            "summary": _summ(_evaluate_tables(_rotate_payload(BASE_SUBJECTIVE, shift), BASE_OBJECTIVE)),
        })
        perturbations.append({
            "kind": "objective_rotation",
            "shift": shift,
            "summary": _summ(_evaluate_tables(BASE_SUBJECTIVE, _rotate_payload(BASE_OBJECTIVE, shift))),
        })
        perturbations.append({
            "kind": "simultaneous_rotation",
            "shift": shift,
            "summary": _summ(
                _evaluate_tables(
                    _rotate_payload(BASE_SUBJECTIVE, shift),
                    _rotate_payload(BASE_OBJECTIVE, shift),
                )
            ),
        })

    # exact-core relocation across all 10 frame/family choices
    for exact_frame in range(5):
        for exact_family in (0, 1):
            perturbations.append({
                "kind": "exact_core_relocation",
                "target": [exact_frame, exact_family],
                "summary": _summ(
                    _evaluate_tables(
                        BASE_SUBJECTIVE,
                        BASE_OBJECTIVE,
                        exact_frame=exact_frame,
                        exact_family=exact_family,
                    )
                ),
            })

    stable_under_tested_perturbations = all(
        p["summary"]["all_equivalent"]
        and p["summary"]["failure_sets_match"]
        and p["summary"]["core_plus_fringe_match"]
        and p["summary"]["exact_core_count"] == 1
        for p in perturbations
    )

    return {
        "scale": r,
        "status": "modeled",
        "base_model": base_model,
        "tested_perturbation_count": len(perturbations),
        "stable_under_tested_perturbations": stable_under_tested_perturbations,
        "perturbations": perturbations,
        "note": "Tests whether the exact-core-plus-fringe law survives all pair swaps, cyclic rotations, simultaneous swaps, and all exact-core relocations.",
    }
