#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
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
                    "cycle": mutated,
                    "position": pos,
                    "from_raw": original,
                    "to_raw": candidate,
                }
            )
    return out


def is_frame2_d1(c: dict[str, Any]) -> bool:
    return (
        c["classification"] == "action-cell"
        and c["distance_summary"]["best_action_distance"] == 1
        and any(rec["frame"] == 2 for rec in c["nearest"]["action"])
    )


def is_exact_frame2(c: dict[str, Any]) -> bool:
    return (
        c["classification"] == "action-cell"
        and c["confidence"] == "exact"
        and any(m["frame"] == 2 for m in c["action_matches"])
    )


def nearest_action_frames(c: dict[str, Any]) -> list[int]:
    return sorted({rec["frame"] for rec in c["nearest"]["action"]})


def action_match_frames(c: dict[str, Any]) -> list[int]:
    return sorted({m["frame"] for m in c["action_matches"]})


def family(sym: str) -> str:
    return sym[0]


def index_of(sym: str) -> int:
    return int(sym[1:])


def keep_child(c: dict[str, Any], max_action_distance: int) -> bool:
    d = c["distance_summary"]["best_action_distance"]
    return is_exact_frame2(c) or (d is not None and d <= max_action_distance)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--locked-input", default="artifacts/frame2_witness_reconciliation.json")
    ap.add_argument("--vocab-input", default="artifacts/repair_radius_action_d4.json")
    ap.add_argument("--out-json", default="artifacts/frame2_slot4_retained_substitutions.json")
    ap.add_argument("--out-csv", default="artifacts/frame2_slot4_retained_substitutions.csv")
    ap.add_argument("--max-action-distance", type=int, default=3)
    args = ap.parse_args()

    locked_data = load_json(args.locked_input)
    vocab_payload = load_json(args.vocab_input)
    vocab = unique_preserve_order(vocab_payload["vocab"])

    starts = [row["start_cycle"] for row in locked_data["results"]]

    rows: list[dict[str, Any]] = []
    template_counter = Counter()
    seam_transition_counter = Counter()
    retained_slot4_counter = Counter()
    retained_seam_slot4_counter = Counter()

    for start_idx, start_cycle in enumerate(starts):
        start_norm = normalize_cycle(start_cycle)
        start_class = classify_cycle(start_cycle, 1)
        start_slot4 = start_norm[4]

        for item in one_edit_variants(start_cycle, vocab):
            child_cycle = item["cycle"]
            child_class = classify_cycle(child_cycle, 1)
            child_norm = child_class["normalized_cycle"]
            child_slot4 = child_norm[4]

            retained = keep_child(child_class, args.max_action_distance)
            frame2_d1 = is_frame2_d1(child_class)
            exact_frame2 = is_exact_frame2(child_class)

            row = {
                "start_index": start_idx,
                "start_cycle_raw": start_cycle,
                "start_cycle_normalized": start_norm,
                "start_slot4": start_slot4,
                "edit_label": item["label"],
                "position": item["position"],
                "from_raw": item["from_raw"],
                "to_raw": item["to_raw"],
                "from_family": family(item["from_raw"]),
                "to_family": family(item["to_raw"]),
                "from_index": index_of(item["from_raw"]),
                "to_index": index_of(item["to_raw"]),
                "child_cycle_normalized": child_norm,
                "child_slot4": child_slot4,
                "child_classification": child_class["classification"],
                "child_confidence": child_class["confidence"],
                "child_best_action_distance": child_class["distance_summary"]["best_action_distance"],
                "child_nearest_action_frames": nearest_action_frames(child_class),
                "child_action_match_frames": action_match_frames(child_class),
                "retained_bounded": retained,
                "frame2_d1": frame2_d1,
                "exact_frame2": exact_frame2,
            }
            rows.append(row)

            if retained:
                retained_slot4_counter[child_slot4] += 1
                template_counter[
                    (
                        item["position"],
                        family(item["from_raw"]),
                        family(item["to_raw"]),
                        child_slot4,
                        child_class["classification"],
                        child_class["confidence"],
                        child_class["distance_summary"]["best_action_distance"],
                    )
                ] += 1

            if frame2_d1:
                retained_seam_slot4_counter[child_slot4] += 1
                seam_transition_counter[(start_slot4, child_slot4)] += 1

    summary = {
        "locked_start_count": len(starts),
        "raw_substitution_count": len(rows),
        "max_action_distance": args.max_action_distance,
        "retained_bounded_slot4_histogram": dict(sorted(retained_slot4_counter.items())),
        "retained_frame2_d1_slot4_histogram": dict(sorted(retained_seam_slot4_counter.items())),
        "retained_bounded_slot4_alphabet": sorted(retained_slot4_counter.keys()),
        "retained_frame2_d1_slot4_alphabet": sorted(retained_seam_slot4_counter.keys()),
        "seam_transitions": [
            {"from_slot4": a, "to_slot4": b, "count": n}
            for (a, b), n in seam_transition_counter.most_common()
        ],
        "template_counts": [
            {
                "position": pos,
                "from_family": ff,
                "to_family": tf,
                "child_slot4": s4,
                "child_classification": cl,
                "child_confidence": conf,
                "child_best_action_distance": d,
                "count": n,
            }
            for (pos, ff, tf, s4, cl, conf, d), n in template_counter.most_common()
        ],
    }

    out = {
        "summary": summary,
        "rows": rows,
    }

    Path(args.out_json).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    fieldnames = [
        "start_index",
        "start_cycle_raw",
        "start_cycle_normalized",
        "start_slot4",
        "edit_label",
        "position",
        "from_raw",
        "to_raw",
        "from_family",
        "to_family",
        "from_index",
        "to_index",
        "child_cycle_normalized",
        "child_slot4",
        "child_classification",
        "child_confidence",
        "child_best_action_distance",
        "child_nearest_action_frames",
        "child_action_match_frames",
        "retained_bounded",
        "frame2_d1",
        "exact_frame2",
    ]

    with Path(args.out_csv).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            cooked = row.copy()
            cooked["start_cycle_raw"] = " ".join(cooked["start_cycle_raw"])
            cooked["start_cycle_normalized"] = " ".join(cooked["start_cycle_normalized"])
            cooked["child_cycle_normalized"] = " ".join(cooked["child_cycle_normalized"])
            cooked["child_nearest_action_frames"] = ",".join(map(str, cooked["child_nearest_action_frames"]))
            cooked["child_action_match_frames"] = ",".join(map(str, cooked["child_action_match_frames"]))
            writer.writerow(cooked)

    print(f"wrote {args.out_json}")
    print(f"wrote {args.out_csv}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
