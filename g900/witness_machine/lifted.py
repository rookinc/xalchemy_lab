from __future__ import annotations

from typing import Any, Tuple

from .core import frame_count, mod_n, objective_cycle, subjective_cycle

LiftedState = Tuple[int, int, int]  # (frame, family, sheet)


def make_lifted_state(frame: int, family: int, sheet: int) -> LiftedState:
    return (frame, family, sheet)


def validate_lifted_state(state: LiftedState, r: int = 1) -> LiftedState:
    frame, family, sheet = state
    n = frame_count(r)
    if not isinstance(frame, int) or not isinstance(family, int) or not isinstance(sheet, int):
        raise TypeError("lifted state entries must be ints")
    if not (0 <= frame < n):
        raise ValueError(f"frame must satisfy 0 <= frame < {n}")
    if family not in (0, 1):
        raise ValueError("family must be 0 or 1")
    if sheet not in (0, 1):
        raise ValueError("sheet must be 0 or 1")
    return state


def family_label(state: LiftedState, r: int = 1) -> str:
    _, family, _ = validate_lifted_state(state, r)
    return "subjective" if family == 0 else "objective"


def sheet_label(state: LiftedState, r: int = 1) -> str:
    _, _, sheet = validate_lifted_state(state, r)
    return "+" if sheet == 0 else "-"


def lifted_tau(state: LiftedState, r: int = 1) -> LiftedState:
    frame, family, sheet = validate_lifted_state(state, r)
    n = frame_count(r)
    return (mod_n(frame + 1, n), family, sheet)


def lifted_tau_inv(state: LiftedState, r: int = 1) -> LiftedState:
    frame, family, sheet = validate_lifted_state(state, r)
    n = frame_count(r)
    return (mod_n(frame - 1, n), family, sheet)


def lifted_mu(state: LiftedState, r: int = 1) -> LiftedState:
    frame, family, sheet = validate_lifted_state(state, r)
    return (frame, 1 - family, sheet)


def lifted_W(state: LiftedState, r: int = 1) -> LiftedState:
    frame, family, sheet = validate_lifted_state(state, r)
    return (frame, family, 1 - sheet)


def visible_projection(state: LiftedState, r: int = 1) -> tuple[int, int]:
    frame, family, _ = validate_lifted_state(state, r)
    return (frame, family)


def lifted_witness_cycle(state: LiftedState, r: int = 1) -> list[str]:
    frame, family, _ = validate_lifted_state(state, r)
    return subjective_cycle(frame, r) if family == 0 else objective_cycle(frame, r)


def lifted_state_dict(state: LiftedState, r: int = 1) -> dict[str, Any]:
    state = validate_lifted_state(state, r)
    frame, family, sheet = state
    vis = visible_projection(state, r)
    after_g15 = lifted_W(state, r)
    after_g30 = lifted_W(after_g15, r)

    return {
        "lifted_state": [frame, family, sheet],
        "frame": frame,
        "family": family,
        "family_label": family_label(state, r),
        "sheet": sheet,
        "sheet_label": sheet_label(state, r),
        "visible_projection": list(vis),
        "witness_cycle": lifted_witness_cycle(state, r),
        "tau": list(lifted_tau(state, r)),
        "tau_inv": list(lifted_tau_inv(state, r)),
        "mu": list(lifted_mu(state, r)),
        "W": list(after_g15),
        "W2": list(after_g30),
        "sign_closing_rule": "n_15 = -n_0",
        "identity_restoring_rule": "n_30 = n_0",
    }


def lifted_orbit_summary(frame: int = 0, family: int = 0, r: int = 1) -> dict[str, Any]:
    n = frame_count(r)
    frame = mod_n(frame, n)
    family = family % 2

    start = (frame, family, 0)
    after_g15 = lifted_W(start, r)
    after_g30 = lifted_W(after_g15, r)

    return {
        "frame": frame,
        "family": family,
        "family_label": "subjective" if family == 0 else "objective",
        "g15_length": n,
        "g30_length": 2 * n,
        "start": lifted_state_dict(start, r),
        "after_g15": lifted_state_dict(after_g15, r),
        "after_g30": lifted_state_dict(after_g30, r),
        "projection_invariant_under_W": visible_projection(start, r) == visible_projection(after_g15, r),
        "sheet_flip_under_W": start[2] != after_g15[2],
        "sheet_restore_under_W2": start[2] == after_g30[2],
    }


def verify_lifted_core_laws(r: int = 1) -> dict[str, Any]:
    n = frame_count(r)
    checks = []
    for frame in range(n):
        for family in (0, 1):
            for sheet in (0, 1):
                st = (frame, family, sheet)
                checks.append({
                    "state": [frame, family, sheet],
                    "projection_invariant_under_W": visible_projection(st, r) == visible_projection(lifted_W(st, r), r),
                    "sheet_flip_under_W": lifted_W(st, r)[2] != st[2],
                    "sheet_restore_under_W2": lifted_W(lifted_W(st, r), r) == st,
                    "family_preserved_under_W": lifted_W(st, r)[1] == st[1],
                    "frame_preserved_under_W": lifted_W(st, r)[0] == st[0],
                })

    return {
        "scale": r,
        "state_count": len(checks),
        "all_projection_invariant_under_W": all(x["projection_invariant_under_W"] for x in checks),
        "all_sheet_flip_under_W": all(x["sheet_flip_under_W"] for x in checks),
        "all_sheet_restore_under_W2": all(x["sheet_restore_under_W2"] for x in checks),
        "all_family_preserved_under_W": all(x["family_preserved_under_W"] for x in checks),
        "all_frame_preserved_under_W": all(x["frame_preserved_under_W"] for x in checks),
        "checks": checks,
    }
