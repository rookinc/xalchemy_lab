#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def species_of(label: str) -> str:
    return label[0]


def index_of(label: str) -> int:
    return int(label[1:])


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def positional_signature(start_row: dict) -> dict:
    edits = start_row["path"][0].get("edits", [])

    by_position = []
    position_set = []
    species_flip_count = 0
    index_preserved_count = 0
    index_shift_count = 0

    for e in sorted(edits, key=lambda x: x["position"]):
        pos = e["position"]
        frm = e["from"]
        to = e["to"]

        sf = species_of(frm)
        st = species_of(to)
        if sf != st:
            species_flip_count += 1

        if index_of(frm) == index_of(to):
            index_preserved_count += 1
        else:
            index_shift_count += 1

        position_set.append(str(pos))
        by_position.append(f"{pos}:{frm}->{to}")

    return {
        "edit_count": len(edits),
        "position_signature": "|".join(position_set),
        "transition_signature": "|".join(by_position),
        "species_flip_count": species_flip_count,
        "index_preserved_count": index_preserved_count,
        "index_shift_count": index_shift_count,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-json")
    args = ap.parse_args()

    data = load_json(args.input)
    if data.get("target_family") != "action-cell":
        raise SystemExit("expected an action-cell result json")

    rows = data.get("failed_walks", []) + data.get("walks", [])

    seen = set()
    buckets = defaultdict(lambda: {
        "count": 0,
        "exact_count": 0,
        "stall_count": 0,
        "steps_sum": 0,
        "examples": [],
    })

    for row in rows:
        key = row["start_label"]
        if key in seen:
            continue
        seen.add(key)

        d = row.get("start_distance")
        if d is None:
            continue

        sig = positional_signature(row)

        bucket_key = (
            d,
            sig["position_signature"],
            sig["transition_signature"],
            sig["species_flip_count"],
            sig["index_preserved_count"],
            sig["index_shift_count"],
        )

        b = buckets[bucket_key]
        b["count"] += 1
        if row.get("reached_exact_target"):
            b["exact_count"] += 1
        else:
            b["stall_count"] += 1
        b["steps_sum"] += row.get("steps_taken", 0)

        if len(b["examples"]) < 3:
            b["examples"].append({
                "start_label": row["start_label"],
                "start_cycle": row["start_cycle"],
                "reached_exact_target": row["reached_exact_target"],
                "steps_taken": row["steps_taken"],
                "end_classification": row["end_classification"],
                "end_confidence": row["end_confidence"],
            })

    out_rows = []
    for key in sorted(buckets):
        (
            distance,
            position_signature,
            transition_signature,
            species_flip_count,
            index_preserved_count,
            index_shift_count,
        ) = key

        b = buckets[key]
        count = b["count"]
        out_rows.append({
            "distance": distance,
            "position_signature": position_signature,
            "transition_signature": transition_signature,
            "species_flip_count": species_flip_count,
            "index_preserved_count": index_preserved_count,
            "index_shift_count": index_shift_count,
            "count": count,
            "exact_count": b["exact_count"],
            "exact_rate": (b["exact_count"] / count) if count else 0.0,
            "stall_count": b["stall_count"],
            "stall_rate": (b["stall_count"] / count) if count else 0.0,
            "avg_steps": (b["steps_sum"] / count) if count else 0.0,
            "examples": b["examples"],
        })

    payload = {
        "source": args.input,
        "target_family": "action-cell",
        "signature_buckets": out_rows,
    }

    text = json.dumps(payload, indent=2)
    if args.out_json:
        Path(args.out_json).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")
    else:
        print(text)

    print()
    print("dist  posns  transition_signature                         flips  keep_i  shift_i  count  exact%  stall%  avg_steps")
    print("----  -----  ------------------------------------------  -----  ------  -------  -----  ------  ------  ---------")
    for row in out_rows:
        print(
            f"{row['distance']:>4}  "
            f"{row['position_signature']:<5}  "
            f"{row['transition_signature']:<42}  "
            f"{row['species_flip_count']:>5}  "
            f"{row['index_preserved_count']:>6}  "
            f"{row['index_shift_count']:>7}  "
            f"{row['count']:>5}  "
            f"{100.0*row['exact_rate']:>5.1f}%  "
            f"{100.0*row['stall_rate']:>5.1f}%  "
            f"{row['avg_steps']:>9.3f}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
