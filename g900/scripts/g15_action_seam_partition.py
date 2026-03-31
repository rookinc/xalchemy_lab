#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_possig(psig: str) -> tuple[int, ...]:
    return tuple(int(x) for x in psig.split("|"))


def classify(psig: str) -> str:
    s = set(parse_possig(psig))

    if s == {0, 4, 5}:
        return "exact_045"

    if 0 in s and 5 in s:
        return "contains_0_and_5"

    if 4 in s and 5 in s and 0 not in s:
        return "contains_4_and_5_not_0"

    if 0 in s:
        return "contains_0_only"

    if 5 in s:
        return "contains_5_only"

    return "other"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-json")
    args = ap.parse_args()

    data = load_json(args.input)
    rows = data["position_buckets"]

    buckets = defaultdict(lambda: {
        "count": 0,
        "exact_count": 0,
        "stall_count": 0,
        "steps_weighted_sum": 0.0,
        "triples": [],
    })

    for row in rows:
        cls = classify(row["position_signature"])
        count = row["count"]
        b = buckets[cls]
        b["count"] += count
        b["exact_count"] += row["exact_count"]
        b["stall_count"] += row["stall_count"]
        b["steps_weighted_sum"] += row["avg_steps"] * count
        b["triples"].append({
            "position_signature": row["position_signature"],
            "count": row["count"],
            "exact_rate": row["exact_rate"],
            "stall_rate": row["stall_rate"],
            "avg_steps": row["avg_steps"],
        })

    order = [
        "exact_045",
        "contains_0_and_5",
        "contains_4_and_5_not_0",
        "contains_0_only",
        "contains_5_only",
        "other",
    ]

    out = []
    for cls in order:
        if cls not in buckets:
            continue
        b = buckets[cls]
        count = b["count"]
        out.append({
            "class": cls,
            "count": count,
            "exact_count": b["exact_count"],
            "exact_rate": b["exact_count"] / count if count else 0.0,
            "stall_count": b["stall_count"],
            "stall_rate": b["stall_count"] / count if count else 0.0,
            "avg_steps": b["steps_weighted_sum"] / count if count else 0.0,
            "triples": b["triples"],
        })

    payload = {
        "source": args.input,
        "partition_summary": out,
    }

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")

    print("class                      count  exact%  stall%  avg_steps")
    print("-------------------------  -----  ------  ------  ---------")
    for row in out:
        print(
            f"{row['class']:<25}  "
            f"{row['count']:>5}  "
            f"{100.0*row['exact_rate']:>5.1f}%  "
            f"{100.0*row['stall_rate']:>5.1f}%  "
            f"{row['avg_steps']:>9.3f}"
        )

    print()
    print("triples by class")
    for row in out:
        print(f"[{row['class']}]")
        for t in row["triples"]:
            print(
                f"  {t['position_signature']}: "
                f"count={t['count']} "
                f"exact%={100.0*t['exact_rate']:.1f} "
                f"stall%={100.0*t['stall_rate']:.1f} "
                f"avg_steps={t['avg_steps']:.3f}"
            )
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
