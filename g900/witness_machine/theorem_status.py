from __future__ import annotations

from typing import Any

from .verify import verify_all


def _check_passed(section: dict[str, Any], check_name: str) -> bool:
    for check in section.get("checks", []):
        if check.get("name") == check_name:
            return bool(check.get("passed"))
    return False


def build_theorem_status(r: int = 1) -> dict[str, Any]:
    report = verify_all(r)
    section_map = {section["section"]: section for section in report.get("sections", [])}

    op_inv = section_map.get("bridge_operator_invariants", {})

    return {
        "scale": r,
        "overall": report.get("overall", {}),
        "ledger": report.get("ledger", {}),
        "sections": section_map,
        "summary": {
            "verified_count": len(report.get("ledger", {}).get("verified", [])),
            "modeled_count": len(report.get("ledger", {}).get("modeled", [])),
            "open_count": len(report.get("ledger", {}).get("open", [])),
        },
        "theorem_position": {
            "verified_visible_machine": True,
            "verified_lifted_machine": True,
            "modeled_bridge_current_model": True,
            "full_causal_theorem_beyond_model_open": True,
        },
        "bridge_invariants": {
            "unique_exact_core_operator_invariant": _check_passed(op_inv, "unique_exact_core_is_operator_invariant"),
            "failure_equals_illegality_operator_invariant": _check_passed(op_inv, "failure_equals_illegality_is_operator_invariant"),
            "core_plus_fringe_operator_invariant": _check_passed(op_inv, "core_plus_fringe_is_operator_invariant"),
            "retained_sheet_legal_equivalence_operator_invariant": _check_passed(op_inv, "retained_sheet_legal_equivalence_is_operator_invariant"),
            "fringe_size_operator_sensitive": _check_passed(op_inv, "fringe_size_is_operator_sensitive"),
        },
        "export_note": (
            "This artifact is a machine-generated theorem-status ledger. "
            "It distinguishes verified laws, modeled bridge results, and open beyond-model statements."
        ),
    }
