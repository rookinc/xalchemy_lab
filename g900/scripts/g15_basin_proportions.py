from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def summarize_scan(data: dict[str, Any], label: str) -> dict[str, Any]:
    summary = data.get("summary", {})
    rows = data.get("results", [])
    total = int(summary.get("count", len(rows)))

    class_counts = summary.get("classification_counts", {})
    conf_counts = summary.get("confidence_counts", {})

    def pct(n: int) -> float:
        return 0.0 if total == 0 else 100.0 * n / total

    subj = int(class_counts.get("subjective-state", 0))
    obj = int(class_counts.get("objective-state", 0))
    act = int(class_counts.get("action-cell", 0))
    unres = int(class_counts.get("unresolved", 0))
    mixed = int(class_counts.get("mixed", 0))

    exact = int(conf_counts.get("exact", 0))
    nearest = int(conf_counts.get("nearest", 0))
    ambiguous = int(conf_counts.get("ambiguous", 0))

    return {
        "label": label,
        "seed_classification": data.get("seed_classification"),
        "total_edits": total,
        "counts": {
            "subjective-state": subj,
            "objective-state": obj,
            "action-cell": act,
            "unresolved": unres,
            "mixed": mixed,
            "exact": exact,
            "nearest": nearest,
            "ambiguous": ambiguous,
        },
        "proportions": {
            "subjective-state_pct": pct(subj),
            "objective-state_pct": pct(obj),
            "action-cell_pct": pct(act),
            "unresolved_pct": pct(unres),
            "mixed_pct": pct(mixed),
            "exact_pct": pct(exact),
            "nearest_pct": pct(nearest),
            "ambiguous_pct": pct(ambiguous),
        },
    }


def render_table(summaries: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    header = (
        f"{'scan':<12} {'seed':<18} {'total':>5} "
        f"{'subj%':>7} {'obj%':>7} {'act%':>7} {'unres%':>8} "
        f"{'exact%':>7} {'near%':>7} {'ambig%':>8}"
    )
    lines.append(header)
    lines.append("-" * len(header))

    for s in summaries:
        p = s["proportions"]
        lines.append(
            f"{s['label']:<12} "
            f"{str(s['seed_classification']):<18} "
            f"{s['total_edits']:>5} "
            f"{p['subjective-state_pct']:>6.1f}% "
            f"{p['objective-state_pct']:>6.1f}% "
            f"{p['action-cell_pct']:>6.1f}% "
            f"{p['unresolved_pct']:>7.1f}% "
            f"{p['exact_pct']:>6.1f}% "
            f"{p['nearest_pct']:>6.1f}% "
            f"{p['ambiguous_pct']:>7.1f}%"
        )
    return "\n".join(lines)


def render_takeaways(summaries: list[dict[str, Any]]) -> str:
    by_label = {s["label"]: s for s in summaries}
    out: list[str] = []
    out.append("takeaways:")

    subj = by_label.get("subjective")
    obj = by_label.get("objective")
    act = by_label.get("action")

    if subj and obj:
        ds = abs(
            subj["proportions"]["subjective-state_pct"]
            - obj["proportions"]["objective-state_pct"]
        )
        da = abs(
            subj["proportions"]["action-cell_pct"]
            - obj["proportions"]["action-cell_pct"]
        )
        du = abs(
            subj["proportions"]["unresolved_pct"]
            - obj["proportions"]["unresolved_pct"]
        )
        out.append(
            f"- subjective/objective mirror gap: core={ds:.1f}%, action_spill={da:.1f}%, unresolved={du:.1f}%"
        )

    if act:
        out.append(
            f"- action retention: {act['proportions']['action-cell_pct']:.1f}%"
        )
        out.append(
            f"- action -> objective drift: {act['proportions']['objective-state_pct']:.1f}%"
        )
        out.append(
            f"- action -> subjective drift: {act['proportions']['subjective-state_pct']:.1f}%"
        )

    return "\n".join(out)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 scripts/g15_basin_proportions.py")
    p.add_argument("--subjective", required=True)
    p.add_argument("--objective", required=True)
    p.add_argument("--action", required=True)
    p.add_argument("--out-json")
    return p


def main() -> int:
    args = build_parser().parse_args()

    summaries = [
        summarize_scan(load_json(args.subjective), "subjective"),
        summarize_scan(load_json(args.objective), "objective"),
        summarize_scan(load_json(args.action), "action"),
    ]

    print(render_table(summaries))
    print()
    print(render_takeaways(summaries))

    if args.out_json:
        payload = {"summaries": summaries}
        Path(args.out_json).write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {args.out_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
