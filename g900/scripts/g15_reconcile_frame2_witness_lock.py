#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from witness_machine.core import classify_cycle, normalize_cycle


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--witnesses", default="artifacts/unresolved20_depth4_frame2_d1_hits.json")
    ap.add_argument("--vocab-input", default="artifacts/repair_radius_action_d4.json")
    ap.add_argument("--out", default="artifacts/frame2_witness_reconciliation.json")
    args = ap.parse_args()

    t0 = time.perf_counter()
    cpu0 = time.process_time()

    witness_data = load_json(args.witnesses)
    payload = load_json(args.vocab_input)
    vocab = unique_preserve_order(payload["vocab"])

    starts = []
    seen = set()
    for row in witness_data["results"]:
        for hit in row["frame2_d1_hits"]:
            key = tuple(normalize_cycle(hit["cycle"]))
            if key in seen:
                continue
            seen.add(key)
            starts.append(hit["cycle"])

    results = []
    for cyc in starts:
        start_c = classify_cycle(cyc, 1)

        exact_children = []
        exact_frame2_children = []
        frame2_d1_children = []
        all_exact_children = []

        for item in one_edit_variants(cyc, vocab):
            c = classify_cycle(item["cycle"], 1)
            row = {
                "label": item["label"],
                "position": item["position"],
                "from": item["from"],
                "to": item["to"],
                "raw_cycle": item["cycle"],
                "normalized_cycle": c["normalized_cycle"],
                "classification": c["classification"],
                "confidence": c["confidence"],
                "best_action_distance": c["distance_summary"]["best_action_distance"],
                "action_match_frames": [m["frame"] for m in c["action_matches"]],
                "nearest_action_frames": sorted({rec["frame"] for rec in c["nearest"]["action"]}),
            }

            if c["classification"] == "action-cell" and c["confidence"] == "exact":
                all_exact_children.append(row)
                if is_exact_frame2(c):
                    exact_frame2_children.append(row)
                else:
                    exact_children.append(row)

            if is_frame2_d1(c):
                frame2_d1_children.append(row)

        results.append({
            "start_cycle": cyc,
            "normalized_start_cycle": start_c["normalized_cycle"],
            "start_classification": start_c["classification"],
            "start_confidence": start_c["confidence"],
            "start_best_action_distance": start_c["distance_summary"]["best_action_distance"],
            "start_nearest_action_frames": sorted({rec["frame"] for rec in start_c["nearest"]["action"]}),
            "all_exact_child_count": len(all_exact_children),
            "exact_frame2_child_count": len(exact_frame2_children),
            "frame2_d1_child_count": len(frame2_d1_children),
            "all_exact_children": all_exact_children[:20],
            "exact_frame2_children": exact_frame2_children[:20],
            "frame2_d1_children": frame2_d1_children[:20],
        })

    out = {
        "unique_start_count": len(starts),
        "results": results,
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    wall = time.perf_counter() - t0
    cpu = time.process_time() - cpu0
    print(f"wrote {args.out}")
    print(f"unique_start_count={len(starts)}")
    print("runtime_report:")
    print(f"  wall_seconds={wall:.3f}")
    print(f"  cpu_seconds={cpu:.3f}")

    for i, row in enumerate(results, start=1):
        print()
        print(f"start #{i}")
        print(" raw:", " | ".join(row["start_cycle"]))
        print(" norm:", " | ".join(row["normalized_start_cycle"]))
        print(" start_nearest_action_frames:", row["start_nearest_action_frames"])
        print(" all_exact_child_count:", row["all_exact_child_count"])
        print(" exact_frame2_child_count:", row["exact_frame2_child_count"])
        print(" frame2_d1_child_count:", row["frame2_d1_child_count"])
        if row["exact_frame2_children"]:
            print(" exact_frame2_children:")
            for ex in row["exact_frame2_children"][:5]:
                print("  ", ex["label"], "::", " | ".join(ex["normalized_cycle"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
