#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def get_position_signature(row: dict) -> str:
    edits = row["path"][0].get("edits", [])
    posns = sorted(e["position"] for e in edits)
    return "|".join(str(p) for p in posns)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-json")
    args = ap.parse_args()

    data = load_json(args.input)
    if data.get("target_family") != "action-cell":
        raise SystemExit("expected action-cell json")

    rows = data.get("failed_walks", []) + data.get("walks", [])
    seen = set()
    buckets = defaultdict(lambda: {
        "count": 0,
        "exact_count": 0,
        "stall_count": 0,
        "steps_sum": 0,
        "distances": [],
        "examples": [],
    })

    for row in rows:
        key = row["start_label"]
        if key in seen:
            continue
        seen.add(key)

        psig = get_position_signature(row)
        b = buckets[psig]
        b["count"] += 1
        if row.get("reached_exact_target"):
            b["exact_count"] += 1
        else:
            b["stall_count"] += 1
        b["steps_sum"] += row.get("steps_taken", 0)
        if row.get("start_distance") is not None:
            b["distances"].append(row["start_distance"])
        if len(b["examples"]) < 5:
            b["examples"].append({
                "start_label": row["start_label"],
                "start_distance": row.get("start_distance"),
                "reached_exact_target": row.get("reached_exact_target"),
                "steps_taken": row.get("steps_taken"),
            })

    out_rows = []
    for psig in sorted(buckets):
        b = buckets[psig]
        count = b["count"]
        out_rows.append({
            "position_signature": psig,
            "count": count,
            "exact_count": b["exact_count"],
            "exact_rate": b["exact_count"] / count if count else 0.0,
            "stall_count": b["stall_count"],
            "stall_rate": b["stall_count"] / count if count else 0.0,
            "avg_steps": b["steps_sum"] / count if count else 0.0,
            "min_distance": min(b["distances"]) if b["distances"] else None,
            "max_distance": max(b["distances"]) if b["distances"] else None,
            "examples": b["examples"],
        })

    payload = {
        "source": args.input,
        "target_family": "action-cell",
        "position_buckets": out_rows,
    }

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")

    print("posns  count  exact%  stall%  avg_steps  min_d  max_d")
    print("-----  -----  ------  ------  ---------  -----  -----")
    for row in out_rows:
        print(
            f"{row['position_signature']:<5}  "
            f"{row['count']:>5}  "
            f"{100.0*row['exact_rate']:>5.1f}%  "
            f"{100.0*row['stall_rate']:>5.1f}%  "
            f"{row['avg_steps']:>9.3f}  "
            f"{str(row['min_distance']):>5}  "
            f"{str(row['max_distance']):>5}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
