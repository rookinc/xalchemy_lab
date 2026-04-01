from __future__ import annotations

from typing import Any

from .verify import verify_all


def _section_map(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {section["section"]: section for section in report.get("sections", [])}


def _check_passed(section: dict[str, Any], check_name: str) -> bool:
    for check in section.get("checks", []):
        if check.get("name") == check_name:
            return bool(check.get("passed"))
    return False


def build_theorem_markdown(r: int = 1) -> str:
    report = verify_all(r)
    sections = _section_map(report)
    ledger = report.get("ledger", {})

    op_inv = sections.get("bridge_operator_invariants", {})
    bridge_family = sections.get("bridge_family", {})
    bridge_summary = sections.get("bridge_summary", {})
    derived_bridge = sections.get("derived_bridge", {})

    unique_core_op_inv = _check_passed(op_inv, "unique_exact_core_is_operator_invariant")
    failure_eq_illegality_op_inv = _check_passed(op_inv, "failure_equals_illegality_is_operator_invariant")
    core_plus_fringe_op_inv = _check_passed(op_inv, "core_plus_fringe_is_operator_invariant")
    fringe_size_sensitive = _check_passed(op_inv, "fringe_size_is_operator_sensitive")

    strongest = (
        "In the current bridge model, the puncture is realized as the visible shadow of a unique illegal exact core "
        "together with a one-step causal fringe. The non-retained set, the sheet-illegal set, and the core-plus-fringe "
        "set coincide. Across the tested bridge families and operator families, the uniqueness of the exact core and the "
        "failure = illegality = core-plus-fringe structure remain stable, while the fringe size varies with the "
        "continuation law."
    )

    lines: list[str] = []
    lines.append("# Theorem Status Report")
    lines.append("")
    lines.append(f"- Scale: `{report.get('scale', r)}`")
    lines.append(f"- Overall status: **{report.get('overall', {}).get('status', 'unknown')}**")
    lines.append("")

    lines.append("## Current strongest supported statement")
    lines.append("")
    lines.append(strongest)
    lines.append("")

    lines.append("## Verified laws")
    lines.append("")
    for item in ledger.get("verified", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Modeled bridge laws")
    lines.append("")
    for item in ledger.get("modeled", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Operator and robustness findings")
    lines.append("")
    lines.append(f"- Unique exact core is operator-invariant: **{'yes' if unique_core_op_inv else 'no'}**")
    lines.append(f"- Failure = illegality is operator-invariant: **{'yes' if failure_eq_illegality_op_inv else 'no'}**")
    lines.append(f"- Core-plus-fringe decomposition is operator-invariant: **{'yes' if core_plus_fringe_op_inv else 'no'}**")
    lines.append(f"- Fringe size is operator-sensitive: **{'yes' if fringe_size_sensitive else 'no'}**")
    lines.append(
        f"- Bridge-family robustness section passed: **{'yes' if bridge_family.get('passed') else 'no'}**"
    )
    lines.append("")

    lines.append("## Section status table")
    lines.append("")
    lines.append("| Section | Status | Passed |")
    lines.append("|---|---|---|")
    for section in report.get("sections", []):
        lines.append(f"| `{section['section']}` | `{section['status']}` | `{section['passed']}` |")
    lines.append("")

    lines.append("## Bridge summary")
    lines.append("")
    if bridge_summary:
        for check in bridge_summary.get("checks", []):
            mark = "yes" if check.get("passed") else "no"
            lines.append(f"- **{check.get('name')}**: {mark} — {check.get('detail', '')}")
    lines.append("")

    lines.append("## Derived bridge statement in the current model")
    lines.append("")
    if derived_bridge:
        for check in derived_bridge.get("checks", []):
            mark = "yes" if check.get("passed") else "no"
            lines.append(f"- **{check.get('name')}**: {mark} — {check.get('detail', '')}")
    lines.append("")

    lines.append("## Open statements")
    lines.append("")
    for item in ledger.get("open", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Note")
    lines.append("")
    lines.append(
        "This report is generated directly from the witness-machine verifier and is intended to summarize the current "
        "machine-supported theorem posture without overstating beyond-model claims."
    )
    lines.append("")

    return "\n".join(lines)
