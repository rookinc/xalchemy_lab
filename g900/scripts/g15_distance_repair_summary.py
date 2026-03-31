#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def metric_key_for_family(family: str) -> str:
    return {
        "subjective-state": "best_subjective_distance",
        "objective-state": "best_objective_distance",
        "action-cell": "best_action_distance",
    }[family]


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def summarize_by_distance(data: dict) -> dict:
    family = data["target_family"]
    metric = metric_key_for_family(family)
    walks = data.get("failed_walks", []) + data.get("walks", [])

    # dedupe by start_label because many files store a sample of walks plus failed_walks separately
    seen = set()
    rows = []
    for w in walks:
        key = w.get("start_label")
        if key in seen:
            continue
        seen.add(key)
        rows.append(w)

    buckets: dict[int, dict] = defaultdict(lambda: {
        "count": 0,
        "exact_count": 0,
        "stall_count": 0,
        "steps_sum": 0,
        "improved_count": 0,
    })

    for w in rows:
        d = w.get("start_distance")
        if d is None:
            continue
        b = buckets[int(d)]
        b["count"] += 1
        if w.get("reached_exact_target"):
            b["exact_count"] += 1
        else:
            b["stall_count"] += 1
        if w.get("improved"):
            b["improved_count"] += 1
        b["steps_sum"] += w.get("steps_taken", 0)

    ordered = []
    for d in sorted(buckets):
        b = buckets[d]
        count = b["count"]
        ordered.append({
            "distance": d,
            "count": count,
            "exact_count": b["exact_count"],
            "exact_rate": (b["exact_count"] / count) if count else 0.0,
            "stall_count": b["stall_count"],
            "stall_rate": (b["stall_count"] / count) if count else 0.0,
            "improved_count": b["improved_count"],
            "improved_rate": (b["improved_count"] / count) if count else 0.0,
            "avg_steps": (b["steps_sum"] / count) if count else 0.0,
        })

    return {
        "family": family,
        "metric": metric,
        "distance_buckets": ordered,
    }


def render_table(summaries: list[dict]) -> str:
    lines = []
    for summary in summaries:
        lines.append(f"family: {summary['family']}")
        lines.append(f"metric: {summary['metric']}")
        lines.append("distance  count  exact  exact%  stalls  stall%  improved%  avg_steps")
        lines.append("--------  -----  -----  ------  ------  ------  ---------  ---------")
        for row in summary["distance_buckets"]:
            lines.append(
                f"{row['distance']:>8}  "
                f"{row['count']:>5}  "
                f"{row['exact_count']:>5}  "
                f"{100.0*row['exact_rate']:>5.1f}%  "
                f"{row['stall_count']:>6}  "
                f"{100.0*row['stall_rate']:>5.1f}%  "
                f"{100.0*row['improved_rate']:>8.1f}%  "
                f"{row['avg_steps']:>9.3f}"
            )
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subjective")
    ap.add_argument("--objective")
    ap.add_argument("--action")
    ap.add_argument("--out-json")
    args = ap.parse_args()

    summaries = []
    if args.subjective:
        summaries.append(summarize_by_distance(load_json(args.subjective)))
    if args.objective:
        summaries.append(summarize_by_distance(load_json(args.objective)))
    if args.action:
        summaries.append(summarize_by_distance(load_json(args.action)))

    print(render_table(summaries))

    if args.out_json:
        payload = {"summaries": summaries}
        Path(args.out_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"\nwrote {args.out_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
