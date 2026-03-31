from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from witness_machine.core import (
    action_cell,
    objective_cycle,
    subjective_cycle,
)

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def cycle_to_str(cycle: list[str]) -> str:
    return "-".join(cycle + [cycle[0]])


def hamming(a: str, b: str) -> int:
    if len(a) != len(b):
        raise ValueError("syndrome strings must have equal length")
    return sum(1 for x, y in zip(a, b) if x != y)


def normalize_cycle(cycle: list[str]) -> list[str]:
    n = len(cycle)
    rots = [cycle[i:] + cycle[:i] for i in range(n)]
    rev = list(reversed(cycle))
    rots += [rev[i:] + rev[:i] for i in range(n)]
    return min(rots)


def cycle_key(cycle: list[str]) -> tuple[str, ...]:
    return tuple(normalize_cycle(cycle))


# ---------------------------------------------------------------------
# Machine families
# ---------------------------------------------------------------------

def build_subjective_family(frame_count: int) -> list[dict[str, Any]]:
    r = frame_count // 5
    out = []
    for i in range(frame_count):
        cyc = subjective_cycle(i, r)
        out.append(
            {
                "frame": i,
                "phase": 0,
                "phase_label": "subjective",
                "cycle": cyc,
                "cycle_str": cycle_to_str(cyc),
                "cycle_key": list(cycle_key(cyc)),
                "alignment": "return",
                "spread": 4,
                "fiber": 26,
            }
        )
    return out


def build_objective_family(frame_count: int) -> list[dict[str, Any]]:
    r = frame_count // 5
    out = []
    for i in range(frame_count):
        cyc = objective_cycle(i, r)
        out.append(
            {
                "frame": i,
                "phase": 1,
                "phase_label": "objective",
                "cycle": cyc,
                "cycle_str": cycle_to_str(cyc),
                "cycle_key": list(cycle_key(cyc)),
                "alignment": "forward",
                "spread": 5,
                "fiber": 18,
            }
        )
    return out


def build_action_family(frame_count: int) -> list[dict[str, Any]]:
    r = frame_count // 5
    out = []
    for i in range(frame_count):
        cyc = action_cell(i, r)
        out.append(
            {
                "frame": i,
                "cycle": cyc,
                "cycle_str": cycle_to_str(cyc),
                "cycle_key": list(cycle_key(cyc)),
                "species": "O-S-T-S-T-S",
            }
        )
    return out


# ---------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------

def exact_cycle_match(candidates: list[dict[str, Any]], cycle: list[str]) -> list[dict[str, Any]]:
    key = cycle_key(cycle)
    return [c for c in candidates if tuple(c["cycle_key"]) == key]


def best_syndrome_match(candidates: list[dict[str, Any]], syndrome: str) -> list[dict[str, Any]]:
    scored = []
    for c in candidates:
        cand_syn = c.get("syndrome")
        if cand_syn is None:
            continue
        scored.append(
            {
                **c,
                "syndrome_distance": hamming(syndrome, cand_syn),
            }
        )
    if not scored:
        return []
    best = min(x["syndrome_distance"] for x in scored)
    return [x for x in scored if x["syndrome_distance"] == best]


def orbit_score_block(subjective_matches: list[dict[str, Any]], objective_matches: list[dict[str, Any]]) -> dict[str, Any]:
    s_exact = any(m.get("match_type") == "exact_cycle" for m in subjective_matches)
    o_exact = any(m.get("match_type") == "exact_cycle" for m in objective_matches)

    if o_exact and not s_exact:
        verdict = "objective-selected"
    elif s_exact and not o_exact:
        verdict = "subjective-selected"
    elif s_exact and o_exact:
        verdict = "mixed"
    else:
        s_best = min((m.get("syndrome_distance", 999999) for m in subjective_matches), default=None)
        o_best = min((m.get("syndrome_distance", 999999) for m in objective_matches), default=None)
        if s_best is None and o_best is None:
            verdict = "unresolved"
        elif s_best is None:
            verdict = "objective-nearest"
        elif o_best is None:
            verdict = "subjective-nearest"
        elif s_best < o_best:
            verdict = "subjective-nearest"
        elif o_best < s_best:
            verdict = "objective-nearest"
        else:
            verdict = "ambiguous-nearest"

    return {
        "subjective_exact": s_exact,
        "objective_exact": o_exact,
        "verdict": verdict,
    }


def classify_probe(
    subjective_matches: list[dict[str, Any]],
    objective_matches: list[dict[str, Any]],
    action_matches: list[dict[str, Any]],
) -> str:
    s_exact = any(m.get("match_type") == "exact_cycle" for m in subjective_matches)
    o_exact = any(m.get("match_type") == "exact_cycle" for m in objective_matches)
    a_exact = any(m.get("match_type") == "exact_cycle" for m in action_matches)

    if s_exact and not o_exact:
        return "subjective-state"
    if o_exact and not s_exact:
        return "objective-state"
    if a_exact and not s_exact and not o_exact:
        return "action-cell"
    if s_exact and o_exact:
        return "mixed"
    return "unresolved"


# ---------------------------------------------------------------------
# Main probe
# ---------------------------------------------------------------------

def probe_payload(payload: dict[str, Any]) -> dict[str, Any]:
    frame_count = int(payload.get("frame_count", 5))
    if frame_count % 5 != 0:
        raise ValueError("frame_count must be a multiple of 5")

    subjective_family = build_subjective_family(frame_count)
    objective_family = build_objective_family(frame_count)
    action_family = build_action_family(frame_count)

    cycle = payload.get("cycle")
    syndrome = payload.get("syndrome")

    subjective_matches: list[dict[str, Any]] = []
    objective_matches: list[dict[str, Any]] = []
    action_matches: list[dict[str, Any]] = []

    if cycle:
        s_exact = exact_cycle_match(subjective_family, cycle)
        o_exact = exact_cycle_match(objective_family, cycle)
        a_exact = exact_cycle_match(action_family, cycle)

        subjective_matches.extend([{**m, "match_type": "exact_cycle"} for m in s_exact])
        objective_matches.extend([{**m, "match_type": "exact_cycle"} for m in o_exact])
        action_matches.extend([{**m, "match_type": "exact_cycle"} for m in a_exact])

    if syndrome:
        subjective_matches.extend(
            [{**m, "match_type": "nearest_syndrome"} for m in best_syndrome_match(subjective_family, syndrome)]
        )
        objective_matches.extend(
            [{**m, "match_type": "nearest_syndrome"} for m in best_syndrome_match(objective_family, syndrome)]
        )
        action_matches.extend(
            [{**m, "match_type": "nearest_syndrome"} for m in best_syndrome_match(action_family, syndrome)]
        )

    orbit_block = orbit_score_block(subjective_matches, objective_matches)

    if any(m.get("match_type") == "exact_cycle" for m in action_matches):
        action_verdict = "action-cell-match"
    elif any("syndrome_distance" in m for m in action_matches):
        best = min(m["syndrome_distance"] for m in action_matches)
        action_verdict = f"nearest-action-cell distance={best}"
    else:
        action_verdict = "no-action-match"

    classification = classify_probe(
        subjective_matches=subjective_matches,
        objective_matches=objective_matches,
        action_matches=action_matches,
    )

    return {
        "input": payload,
        "machine_context": {
            "frame_count": frame_count,
            "subjective_family_size": len(subjective_family),
            "objective_family_size": len(objective_family),
            "action_family_size": len(action_family),
        },
        "subjective_matches": subjective_matches,
        "objective_matches": objective_matches,
        "action_matches": action_matches,
        "orbit_block": orbit_block,
        "action_block": {
            "verdict": action_verdict,
        },
        "classification": classification,
        "final_verdict": classification,
    }


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 scripts/g15_lift_selection_probe.py")
    p.add_argument("--input", required=True, help="JSON file with lift-side probe input")
    p.add_argument("--out", help="optional output JSON artifact path")
    return p


def main() -> int:
    args = build_parser().parse_args()

    input_path = Path(args.input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    result = probe_payload(payload)

    text = json.dumps(result, indent=2)

    if args.out:
        out_path = Path(args.out)
        out_path.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out_path}")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
