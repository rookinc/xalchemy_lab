#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
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
            out.append({
                "label": f"edit_pos{pos}_{original}_to_{candidate}",
                "cycle": mutated,
                "position": pos,
                "from": original,
                "to": candidate,
            })
    return out


def is_frame2_d1(c: dict[str, Any]) -> bool:
    return (
        c["classification"] == "action-cell"
        and c["distance_summary"]["best_action_distance"] == 1
        and any(rec["frame"] == 2 for rec in c["nearest"]["action"])
    )


def slot4_value(cycle: list[str]) -> str:
    return normalize_cycle(cycle)[4]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--locked-input", default="artifacts/frame2_witness_reconciliation.json")
    ap.add_argument("--vocab-input", default="artifacts/repair_radius_action_d4.json")
    ap.add_argument("--out", default="artifacts/frame2_slot4_locked_automaton.json")
    args = ap.parse_args()

    t0 = time.perf_counter()
    cpu0 = time.process_time()

    locked_data = load_json(args.locked_input)
    payload = load_json(args.vocab_input)
    vocab = unique_preserve_order(payload["vocab"])

    locked_cycles = [row["start_cycle"] for row in locked_data["results"]]

    # canonical locked slot values from the 4 witness starts
    locked_slot_values = sorted({slot4_value(cyc) for cyc in locked_cycles})

    state_rows = []
    transition_counter = Counter()
    transition_examples = defaultdict(list)
    reachable_slot_values = Counter()
    target_frame_hist = Counter()

    for cyc in locked_cycles:
        c0 = classify_cycle(cyc, 1)
        from_norm = c0["normalized_cycle"]
        from_slot4 = from_norm[4]

        local_children = []
        for item in one_edit_variants(cyc, vocab):
            c = classify_cycle(item["cycle"], 1)
            if not is_frame2_d1(c):
                continue

            child_norm = c["normalized_cycle"]
            to_slot4 = child_norm[4]
            frames = sorted({rec["frame"] for rec in c["nearest"]["action"]})

            local_children.append({
                "label": item["label"],
                "position": item["position"],
                "from_raw": item["from"],
                "to_raw": item["to"],
                "normalized_cycle": child_norm,
                "to_slot4": to_slot4,
                "nearest_action_frames": frames,
            })

            transition_counter[(from_slot4, to_slot4)] += 1
            reachable_slot_values[to_slot4] += 1
            for f in frames:
                target_frame_hist[f] += 1

            if len(transition_examples[(from_slot4, to_slot4)]) < 5:
                transition_examples[(from_slot4, to_slot4)].append({
                    "label": item["label"],
                    "normalized_cycle": child_norm,
                    "nearest_action_frames": frames,
                })

        state_rows.append({
            "raw_cycle": cyc,
            "normalized_cycle": from_norm,
            "from_slot4": from_slot4,
            "frame2_d1_child_count": len(local_children),
            "frame2_d1_children": local_children,
        })

    closed_under_locked_values = all(
        to_slot4 in locked_slot_values
        for (_, to_slot4), _ in transition_counter.items()
    )

    out = {
        "locked_slot_values": locked_slot_values,
        "closed_under_locked_values": closed_under_locked_values,
        "summary": {
            "locked_state_count": len(state_rows),
            "reachable_slot_value_histogram": dict(sorted(reachable_slot_values.items())),
            "nearest_action_frame_histogram": dict(sorted(target_frame_hist.items())),
            "transition_histogram": [
                {"from_slot4": a, "to_slot4": b, "count": n}
                for (a, b), n in transition_counter.most_common()
            ],
        },
        "transition_examples": {
            f"{a}->{b}": rows
            for (a, b), rows in transition_examples.items()
        },
        "states": state_rows,
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    wall = time.perf_counter() - t0
    cpu = time.process_time() - cpu0

    print(f"wrote {args.out}")
    print(f"locked_slot_values={locked_slot_values}")
    print(f"closed_under_locked_values={closed_under_locked_values}")
    print("summary:")
    print(json.dumps(out["summary"], indent=2))
    print("runtime_report:")
    print(f"  wall_seconds={wall:.3f}")
    print(f"  cpu_seconds={cpu:.3f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
