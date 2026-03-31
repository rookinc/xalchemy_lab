#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: ./scripts/g15_extract_full_failures.py <result.json> [more.json ...]", file=sys.stderr)
        return 1

    for arg in sys.argv[1:]:
        p = Path(arg)
        data = json.loads(p.read_text(encoding="utf-8"))

        family = data.get("target_family", "unknown")
        summary = data.get("summary", {})
        walks = data.get("walks", [])

        failures = [w for w in walks if not w.get("reached_exact_target", False)]

        out = {
            "source_file": str(p),
            "target_family": family,
            "summary": {
                "count": summary.get("count"),
                "reached_exact_count": summary.get("reached_exact_count"),
                "reached_exact_rate": summary.get("reached_exact_rate"),
                "improved_count": summary.get("improved_count"),
                "improved_rate": summary.get("improved_rate"),
                "stalled_count": summary.get("stalled_count"),
                "stalled_rate": summary.get("stalled_rate"),
                "avg_start_distance": summary.get("avg_start_distance"),
                "avg_end_distance": summary.get("avg_end_distance"),
                "avg_steps_taken": summary.get("avg_steps_taken"),
            },
            "saved_walk_count": len(walks),
            "saved_failure_count": len(failures),
            "saved_failures": failures,
            "diagnostic": (
                "WARNING: result JSON only stores a truncated walks sample. "
                "If summary.stalled_count > saved_failure_count, then some failed starts "
                "are not present in this file and cannot be beam-tested from this artifact alone."
            ),
        }

        out_path = p.with_name(p.stem + "_failure_diagnostic.json")
        out_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

        print(f"wrote {out_path}")
        print(f"family={family}")
        print(f"summary.stalled_count={summary.get('stalled_count')}")
        print(f"saved_failure_count={len(failures)}")
        if summary.get("stalled_count", 0) > len(failures):
            print("status=TRUNCATED_SAMPLE")
        else:
            print("status=COMPLETE_OR_SUFFICIENT")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
