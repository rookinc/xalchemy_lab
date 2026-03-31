#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_possig(psig: str) -> set[int]:
    return {int(x) for x in psig.split("|")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-json")
    args = ap.parse_args()

    data = load_json(args.input)
    rows = data["position_buckets"]

    out = []
    for pos in range(6):
        matched = [row for row in rows if pos in parse_possig(row["position_signature"])]
        count = sum(row["count"] for row in matched)
        exact_count = sum(row["exact_count"] for row in matched)
        stall_count = sum(row["stall_count"] for row in matched)
        weighted_steps = sum(row["avg_steps"] * row["count"] for row in matched)

        out.append({
            "anchor_position": pos,
            "count": count,
            "exact_count": exact_count,
            "exact_rate": (exact_count / count) if count else 0.0,
            "stall_count": stall_count,
            "stall_rate": (stall_count / count) if count else 0.0,
            "avg_steps": (weighted_steps / count) if count else 0.0,
            "triples": [
                {
                    "position_signature": row["position_signature"],
                    "count": row["count"],
                    "exact_rate": row["exact_rate"],
                    "stall_rate": row["stall_rate"],
                    "avg_steps": row["avg_steps"],
                }
                for row in matched
            ],
        })

    payload = {
        "source": args.input,
        "anchor_summary": out,
    }

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")

    print("anchor  count  exact%  stall%  avg_steps")
    print("------  -----  ------  ------  ---------")
    for row in out:
        print(
            f"{row['anchor_position']:>6}  "
            f"{row['count']:>5}  "
            f"{100.0*row['exact_rate']:>5.1f}%  "
            f"{100.0*row['stall_rate']:>5.1f}%  "
            f"{row['avg_steps']:>9.3f}"
        )

    print()
    print("triples by anchor")
    for row in out:
        print(f"[anchor {row['anchor_position']}]")
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
