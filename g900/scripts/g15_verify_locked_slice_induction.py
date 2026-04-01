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


E2 = ["o4", "s0", "t0", "s2", "t2", "s4"]


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


def slot4_value(cycle: list[str]) -> str:
    return normalize_cycle(cycle)[4]


def mismatch_positions(cycle: list[str], ref: list[str]) -> list[int]:
    norm = normalize_cycle(cycle)
    return [i for i, (a, b) in enumerate(zip(norm, ref)) if a != b]


def main() -> int:
    seam_data = load_json("artifacts/frame2_o_anchor_residue_frame2_d1.json")
    vocab_payload = load_json("artifacts/repair_radius_action_d4.json")
    vocab = unique_preserve_order(vocab_payload["vocab"])

    starts = []
    seen = set()
    for row in seam_data["rows"]:
        cyc = row["normalized_cycle"]
        key = tuple(cyc)
        if key not in seen:
            seen.add(key)
            starts.append(cyc)

    seam_child_counter = Counter()
    child_mismatch_counter = Counter()
    child_slot4_counter = Counter()
    parent_to_children = defaultdict(list)
    bad_t2_children = []
    off_slice_children = []

    for parent in starts:
        parent_norm = normalize_cycle(parent)
        parent_key = tuple(parent_norm)

        for item in one_edit_variants(parent_norm, vocab):
            cc = classify_cycle(item["cycle"], 1)
            if not is_frame2_d1(cc):
                continue

            child_norm = cc["normalized_cycle"]
            child_key = tuple(child_norm)

            seam_child_counter[parent_key] += 1
            child_slot4_counter[child_norm[4]] += 1

            mism = mismatch_positions(child_norm, E2)
            child_mismatch_counter[tuple(mism)] += 1

            row = {
                "label": item["label"],
                "position": item["position"],
                "from_raw": item["from_raw"],
                "to_raw": item["to_raw"],
                "parent_cycle": parent_norm,
                "child_cycle": child_norm,
                "child_slot4": child_norm[4],
                "child_mismatch_positions_vs_E2": mism,
            }
            parent_to_children[str(list(parent_norm))].append(row)

            if child_norm[4] == "t2":
                bad_t2_children.append(row)

            if mism != [4]:
                off_slice_children.append(row)

    summary = {
        "slot4_slice_state_count": len(starts),
        "E2": E2,
        "total_seam_to_seam_children": sum(seam_child_counter.values()),
        "distinct_parent_count_with_children": len(seam_child_counter),
        "child_slot4_histogram": dict(sorted(child_slot4_counter.items())),
        "child_mismatch_patterns_vs_E2": {
            str(list(k)): v for k, v in sorted(child_mismatch_counter.items())
        },
        "t2_child_count": len(bad_t2_children),
        "off_slice_child_count": len(off_slice_children),
    }

    out = {
        "summary": summary,
        "bad_t2_child_examples": bad_t2_children[:50],
        "off_slice_child_examples": off_slice_children[:50],
        "parent_to_children": dict(parent_to_children),
    }

    outpath = Path("artifacts/frame2_locked_slice_induction_verification.json")
    outpath.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {outpath}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
