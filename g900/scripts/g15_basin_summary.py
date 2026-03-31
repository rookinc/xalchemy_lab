from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_scan(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def summarize_scan(data: dict[str, Any], label: str) -> dict[str, Any]:
    seed_class = data.get("seed_classification")
    summary = data.get("summary", {})
    class_counts = summary.get("classification_counts", {})
    conf_counts = summary.get("confidence_counts", {})
    rows = data.get("results", [])

    ambiguous_rows = [r for r in rows if r.get("confidence") == "ambiguous"]
    nearest_action_rows = [
        r for r in rows
        if r.get("classification") == "action-cell" and r.get("confidence") == "nearest"
    ]
    nearest_subjective_rows = [
        r for r in rows
        if r.get("classification") == "subjective-state" and r.get("confidence") == "nearest"
    ]
    nearest_objective_rows = [
        r for r in rows
        if r.get("classification") == "objective-state" and r.get("confidence") == "nearest"
    ]

    return {
        "label": label,
        "seed_classification": seed_class,
        "total_edits": summary.get("count", len(rows)),
        "class_counts": class_counts,
        "confidence_counts": conf_counts,
        "ambiguous_count": len(ambiguous_rows),
        "nearest_action_count": len(nearest_action_rows),
        "nearest_subjective_count": len(nearest_subjective_rows),
        "nearest_objective_count": len(nearest_objective_rows),
    }


def render_table(summaries: list[dict[str, Any]]) -> str:
    lines = []
    header = (
        f"{'scan':<12} {'seed':<18} {'total':<6} "
        f"{'subj':<6} {'obj':<6} {'act':<6} {'unres':<6} "
        f"{'ambig':<6} {'nearS':<6} {'nearO':<6} {'nearA':<6}"
    )
    lines.append(header)
    lines.append("-" * len(header))

    for s in summaries:
        cc = s["class_counts"]
        lines.append(
            f"{s['label']:<12} "
            f"{str(s['seed_classification']):<18} "
            f"{s['total_edits']:<6} "
            f"{cc.get('subjective-state', 0):<6} "
            f"{cc.get('objective-state', 0):<6} "
            f"{cc.get('action-cell', 0):<6} "
            f"{cc.get('unresolved', 0):<6} "
            f"{s['ambiguous_count']:<6} "
            f"{s['nearest_subjective_count']:<6} "
            f"{s['nearest_objective_count']:<6} "
            f"{s['nearest_action_count']:<6}"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 scripts/g15_basin_summary.py")
    p.add_argument("--subjective", required=True)
    p.add_argument("--objective", required=True)
    p.add_argument("--action", required=True)
    p.add_argument("--out-json")
    return p


def main() -> int:
    args = build_parser().parse_args()

    summaries = [
        summarize_scan(load_scan(args.subjective), "subjective"),
        summarize_scan(load_scan(args.objective), "objective"),
        summarize_scan(load_scan(args.action), "action"),
    ]

    print(render_table(summaries))

    if args.out_json:
        Path(args.out_json).write_text(
            json.dumps({"summaries": summaries}, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {args.out_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
