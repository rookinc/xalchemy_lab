from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def summarize_run(data: dict[str, Any], label: str) -> dict[str, Any]:
    summary = data.get("summary", {})
    return {
        "label": label,
        "family": data.get("target_family"),
        "parent_count": data.get("parent_count"),
        "max_steps": data.get("max_steps"),
        "reached_exact_count": summary.get("reached_exact_count"),
        "reached_exact_rate": summary.get("reached_exact_rate"),
        "improved_count": summary.get("improved_count"),
        "improved_rate": summary.get("improved_rate"),
        "stalled_count": summary.get("stalled_count"),
        "stalled_rate": summary.get("stalled_rate"),
        "avg_start_distance": summary.get("avg_start_distance"),
        "avg_end_distance": summary.get("avg_end_distance"),
        "avg_steps_taken": summary.get("avg_steps_taken"),
    }


def render_table(rows: list[dict[str, Any]]) -> str:
    header = (
        f"{'scan':<12} {'family':<18} {'parents':>7} {'exact%':>8} "
        f"{'improve%':>9} {'stall%':>8} {'start_d':>9} {'end_d':>8} {'steps':>7}"
    )
    lines = [header, "-" * len(header)]
    for r in rows:
        lines.append(
            f"{r['label']:<12} "
            f"{str(r['family']):<18} "
            f"{int(r['parent_count'] or 0):>7} "
            f"{100.0 * float(r['reached_exact_rate'] or 0):>7.1f}% "
            f"{100.0 * float(r['improved_rate'] or 0):>8.1f}% "
            f"{100.0 * float(r['stalled_rate'] or 0):>7.1f}% "
            f"{float(r['avg_start_distance'] or 0):>9.3f} "
            f"{float(r['avg_end_distance'] or 0):>8.3f} "
            f"{float(r['avg_steps_taken'] or 0):>7.3f}"
        )
    return "\n".join(lines)


def render_takeaways(rows: list[dict[str, Any]]) -> str:
    out = ["takeaways:"]
    by_label = {r["label"]: r for r in rows}

    if {"subjective", "objective"} <= by_label.keys():
        s = by_label["subjective"]
        o = by_label["objective"]
        out.append(
            "- state repair mirror gap: "
            f"exact={abs((s['reached_exact_rate'] or 0) - (o['reached_exact_rate'] or 0)) * 100:.1f}%, "
            f"improve={abs((s['improved_rate'] or 0) - (o['improved_rate'] or 0)) * 100:.1f}%"
        )

    if "action" in by_label:
        a = by_label["action"]
        out.append(
            f"- action exact recovery: {(a['reached_exact_rate'] or 0) * 100:.1f}%"
        )
        out.append(
            f"- action mean distance contraction: "
            f"{(a['avg_start_distance'] or 0) - (a['avg_end_distance'] or 0):.3f}"
        )

    return "\n".join(out)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 scripts/g15_greedy_summary.py")
    p.add_argument("--subjective", required=True)
    p.add_argument("--objective", required=True)
    p.add_argument("--action", required=True)
    p.add_argument("--out-json")
    return p


def main() -> int:
    args = build_parser().parse_args()

    rows = [
        summarize_run(load_json(args.subjective), "subjective"),
        summarize_run(load_json(args.objective), "objective"),
        summarize_run(load_json(args.action), "action"),
    ]

    print(render_table(rows))
    print()
    print(render_takeaways(rows))

    if args.out_json:
        Path(args.out_json).write_text(
            json.dumps({"rows": rows}, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {args.out_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
