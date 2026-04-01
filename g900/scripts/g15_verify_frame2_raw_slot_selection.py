#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from witness_machine.core import classify_cycle, normalize_cycle

RAW_A2 = ["o4", "s4", "t2", "s2", "t0", "s0"]


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def unique_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def one_edit_variants(seed: list[str], vocab: list[str]) -> list[dict[str, Any]]:
    out = []
    seen = set()
    for pos in range(len(seed)):
        original = seed[pos]
        for candidate in vocab:
            if candidate == original:
                continue
            mutated = seed.copy()
            mutated[pos] = candidate
            key = tuple(mutated)
            if key in seen:
                continue
            seen.add(key)
            out.append(
                {
                    "label": f"edit_pos{pos}_{original}_to_{candidate}",
                    "position": pos,
                    "from_raw": original,
                    "to_raw": candidate,
                    "cycle": mutated,
                }
            )
    return out


def is_frame2_d1(c: dict[str, Any]) -> bool:
    return (
        c["classification"] == "action-cell"
        and c["distance_summary"]["best_action_distance"] == 1
        and any(rec["frame"] == 2 for rec in c["nearest"]["action"])
    )


def nearest_action_frames(c: dict[str, Any]) -> list[int]:
    return sorted({rec["frame"] for rec in c["nearest"]["action"]})


def slot4_value(cycle: list[str]) -> str:
    return normalize_cycle(cycle)[4]


def main() -> int:
    vocab_payload = load_json("artifacts/repair_radius_action_d4.json")
    vocab = unique_preserve_order(vocab_payload["vocab"])

    rows = []
    seam_survivors_by_slot = Counter()
    seam_survivor_values_by_slot: dict[int, set[str]] = defaultdict(set)
    seam_survivor_slot4_by_slot: dict[int, set[str]] = defaultdict(set)
    seam_survivor_cycles_by_slot: dict[int, set[tuple[str, ...]]] = defaultdict(set)

    failure_modes_by_slot: dict[int, Counter] = defaultdict(Counter)

    for item in one_edit_variants(RAW_A2, vocab):
        cyc = item["cycle"]
        cc = classify_cycle(cyc, 1)
        norm = cc["normalized_cycle"]
        seam = is_frame2_d1(cc)

        frames = nearest_action_frames(cc)
        dA = cc["distance_summary"]["best_action_distance"]

        row = {
            "label": item["label"],
            "position": item["position"],
            "from_raw": item["from_raw"],
            "to_raw": item["to_raw"],
            "raw_cycle": cyc,
            "normalized_cycle": norm,
            "classification": cc["classification"],
            "confidence": cc["confidence"],
            "best_action_distance": dA,
            "nearest_action_frames": frames,
            "frame2_d1": seam,
            "slot4": norm[4],
        }
        rows.append(row)

        if seam:
            seam_survivors_by_slot[item["position"]] += 1
            seam_survivor_values_by_slot[item["position"]].add(item["to_raw"])
            seam_survivor_slot4_by_slot[item["position"]].add(norm[4])
            seam_survivor_cycles_by_slot[item["position"]].add(tuple(norm))
        else:
            if cc["classification"] != "action-cell":
                failure_modes_by_slot[item["position"]]["not_action_cell"] += 1
            elif dA != 1:
                failure_modes_by_slot[item["position"]][f"action_cell_distance_{dA}"] += 1
            elif 2 not in frames:
                failure_modes_by_slot[item["position"]]["action_cell_d1_wrong_frame"] += 1
            else:
                failure_modes_by_slot[item["position"]]["other"] += 1

    summary = {
        "raw_A2": RAW_A2,
        "row_count": len(rows),
        "seam_survivors_by_slot": dict(sorted(seam_survivors_by_slot.items())),
        "seam_survivor_values_by_slot": {
            str(k): sorted(v) for k, v in sorted(seam_survivor_values_by_slot.items())
        },
        "seam_survivor_slot4_by_slot": {
            str(k): sorted(v) for k, v in sorted(seam_survivor_slot4_by_slot.items())
        },
        "seam_survivor_distinct_cycles_by_slot": {
            str(k): [list(c) for c in sorted(v)] for k, v in sorted(seam_survivor_cycles_by_slot.items())
        },
        "failure_modes_by_slot": {
            str(k): dict(sorted(v.items())) for k, v in sorted(failure_modes_by_slot.items())
        },
    }

    out = {
        "summary": summary,
        "rows": rows,
    }

    outpath = Path("artifacts/frame2_raw_slot_selection_verification.json")
    outpath.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {outpath}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
