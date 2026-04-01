#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from witness_machine.core import classify_cycle, normalize_cycle, normalized_diff


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
            out.append({
                "label": f"edit_pos{pos}_{original}_to_{candidate}",
                "cycle": mutated,
                "position": pos,
                "from": original,
                "to": candidate,
            })
    return out


def is_exact_frame2(c: dict[str, Any]) -> bool:
    return (
        c["classification"] == "action-cell"
        and c["confidence"] == "exact"
        and any(m["frame"] == 2 for m in c["action_matches"])
    )


def is_frame2_d1(c: dict[str, Any]) -> bool:
    return (
        c["classification"] == "action-cell"
        and c["distance_summary"]["best_action_distance"] == 1
        and any(rec["frame"] == 2 for rec in c["nearest"]["action"])
    )


def slot4_value(cycle: list[str]) -> str:
    return normalize_cycle(cycle)[4]


def audit_cycle(cycle: list[str], vocab: list[str]) -> dict[str, Any]:
    c0 = classify_cycle(cycle, 1)
    frame2_target = ["o4", "s4", "t2", "s2", "t0", "s0"]

    classification_hist = Counter()
    confidence_hist = Counter()
    best_action_hist = Counter()
    nearest_frame_hist = Counter()
    slot4_trans = Counter()

    exact_children = []
    exact_frame2_children = []
    frame2_d1_children = []

    parent_norm = normalize_cycle(cycle)
    parent_slot4 = parent_norm[4]

    for item in one_edit_variants(cycle, vocab):
        c = classify_cycle(item["cycle"], 1)

        classification_hist[c["classification"]] += 1
        confidence_hist[c["confidence"]] += 1
        best_action_hist[c["distance_summary"]["best_action_distance"]] += 1

        frames = sorted({rec["frame"] for rec in c["nearest"]["action"]})
        for f in frames:
            nearest_frame_hist[f] += 1

        child_norm = c["normalized_cycle"]
        child_slot4 = child_norm[4]
        slot4_trans[(parent_slot4, child_slot4)] += 1

        row = {
            "label": item["label"],
            "position": item["position"],
            "from": item["from"],
            "to": item["to"],
            "normalized_cycle": child_norm,
            "classification": c["classification"],
            "confidence": c["confidence"],
            "best_action_distance": c["distance_summary"]["best_action_distance"],
            "nearest_action_frames": frames,
            "diff_to_frame2_target": normalized_diff(item["cycle"], frame2_target),
        }

        if c["classification"] == "action-cell" and c["confidence"] == "exact":
            exact_children.append(row)
            if is_exact_frame2(c):
                exact_frame2_children.append(row)

        if is_frame2_d1(c):
            frame2_d1_children.append(row)

    return {
        "raw_cycle": cycle,
        "normalized_cycle": c0["normalized_cycle"],
        "classification": c0["classification"],
        "confidence": c0["confidence"],
        "best_action_distance": c0["distance_summary"]["best_action_distance"],
        "nearest_action_frames": sorted({rec["frame"] for rec in c0["nearest"]["action"]}),
        "diff_to_frame2_target": normalized_diff(cycle, frame2_target),
        "slot4_value": slot4_value(cycle),
        "classification_histogram": dict(sorted(classification_hist.items())),
        "confidence_histogram": dict(sorted(confidence_hist.items())),
        "best_action_distance_histogram": dict(sorted(best_action_hist.items())),
        "nearest_action_frame_histogram": dict(sorted(nearest_frame_hist.items())),
        "slot4_transition_histogram": [
            {"from": a, "to": b, "count": n}
            for (a, b), n in slot4_trans.most_common()
        ],
        "exact_child_count": len(exact_children),
        "exact_frame2_child_count": len(exact_frame2_children),
        "frame2_d1_child_count": len(frame2_d1_children),
        "exact_children": exact_children[:20],
        "exact_frame2_children": exact_frame2_children[:20],
        "frame2_d1_children": frame2_d1_children[:20],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vocab-input", default="artifacts/repair_radius_action_d4.json")
    ap.add_argument("--locked-input", default="artifacts/frame2_witness_reconciliation.json")
    ap.add_argument("--out", default="artifacts/easy_vs_locked_frame2_comparison.json")
    args = ap.parse_args()

    t0 = time.perf_counter()
    cpu0 = time.process_time()

    payload = load_json(args.vocab_input)
    vocab = unique_preserve_order(payload["vocab"])

    locked_data = load_json(args.locked_input)
    locked_cycles = [row["start_cycle"] for row in locked_data["results"]]

    # The easy witness discovered through CLI audit
    easy_cycle = ["o4", "s4", "t4", "s2", "t0", "s0"]

    out = {
        "easy_witness": audit_cycle(easy_cycle, vocab),
        "locked_witnesses": [audit_cycle(cyc, vocab) for cyc in locked_cycles],
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    wall = time.perf_counter() - t0
    cpu = time.process_time() - cpu0
    print(f"wrote {args.out}")
    print("runtime_report:")
    print(f"  wall_seconds={wall:.3f}")
    print(f"  cpu_seconds={cpu:.3f}")

    print("\neasy witness:")
    print(" normalized:", " | ".join(out["easy_witness"]["normalized_cycle"]))
    print(" diff_to_frame2_target:", out["easy_witness"]["diff_to_frame2_target"])
    print(" exact_frame2_child_count:", out["easy_witness"]["exact_frame2_child_count"])

    print("\nlocked witnesses:")
    for i, row in enumerate(out["locked_witnesses"], start=1):
        print()
        print(f" locked #{i}")
        print("  normalized:", " | ".join(row["normalized_cycle"]))
        print("  diff_to_frame2_target:", row["diff_to_frame2_target"])
        print("  exact_frame2_child_count:", row["exact_frame2_child_count"])
        print("  frame2_d1_child_count:", row["frame2_d1_child_count"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
