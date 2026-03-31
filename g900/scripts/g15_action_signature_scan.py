#!/data/data/com.termux/files/usr/bin/python3
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


def classify_edit_signature(path0: dict, seed_cycle: list[str]) -> dict:
    edits = path0.get("edits", [])
    species_pairs = []
    species_flip_count = 0
    index_preserved_count = 0
    index_shift_count = 0

    for e in edits:
        frm = e["from"]
        to = e["to"]
        sf = species_of(frm)
        st = species_of(to)
        species_pairs.append(f"{sf}->{st}")
        if sf != st:
            species_flip_count += 1
        if index_of(frm) == index_of(to):
            index_preserved_count += 1
        else:
            index_shift_count += 1

    species_pairs.sort()

    return {
        "edit_count": len(edits),
        "species_signature": "|".join(species_pairs),
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
    family = data["target_family"]
    if family != "action-cell":
        raise SystemExit("this script expects an action-cell repair result json")

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

        start_distance = row.get("start_distance")
        if start_distance is None:
            continue

        first = row["path"][0]
        sig = classify_edit_signature(first, data["seed_cycle"])

        bucket_key = (
            start_distance,
            sig["edit_count"],
            sig["species_signature"],
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

        if len(b["examples"]) < 5:
            b["examples"].append({
                "start_label": row["start_label"],
                "start_cycle": row["start_cycle"],
                "end_confidence": row["end_confidence"],
                "end_classification": row["end_classification"],
                "reached_exact_target": row["reached_exact_target"],
                "steps_taken": row["steps_taken"],
            })

    out_rows = []
    for key in sorted(buckets):
        d, edit_count, species_signature, species_flip_count, index_preserved_count, index_shift_count = key
        b = buckets[key]
        count = b["count"]
        out_rows.append({
            "distance": d,
            "edit_count": edit_count,
            "species_signature": species_signature,
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
        "target_family": family,
        "signature_buckets": out_rows,
    }

    text = json.dumps(payload, indent=2)
    if args.out_json:
        Path(args.out_json).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")
    else:
        print(text)

    print()
    print("distance  edits  species_sig              flips  keep_i  shift_i  count  exact%  stall%  avg_steps")
    print("--------  -----  -----------------------  -----  ------  -------  -----  ------  ------  ---------")
    for row in out_rows:
        print(
            f"{row['distance']:>8}  "
            f"{row['edit_count']:>5}  "
            f"{row['species_signature']:<23}  "
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
