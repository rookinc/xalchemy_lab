#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        default="artifacts/hard_d2_depth3_parallel_probe.json",
        help="Depth-3 parallel probe output JSON.",
    )
    ap.add_argument(
        "--out",
        default="artifacts/hard_d2_depth3_unresolved_20.json",
        help="Output JSON for unresolved depth-3 hard states.",
    )
    args = ap.parse_args()

    t0 = time.perf_counter()
    proc0 = time.process_time()

    data = load_json(args.input)
    results = data["results"]

    unresolved = [
        r for r in results
        if (not r.get("has_exact")) and (not r.get("has_d1"))
    ]

    hist = Counter()
    for r in unresolved:
        hist[(r["found_d1_count"], r["found_exact_count"])] += 1

    out = {
        "source_probe": args.input,
        "hard_d2_count": data.get("hard_d2_count"),
        "unresolved_count": len(unresolved),
        "histogram_found_d1_found_exact": [
            {"found_d1_count": k[0], "found_exact_count": k[1], "count": v}
            for k, v in sorted(hist.items())
        ],
        "unresolved_results": unresolved,
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    wall = time.perf_counter() - t0
    cpu = time.process_time() - proc0
    rss_mb = None
    try:
        import resource
        r = resource.getrusage(resource.RUSAGE_SELF)
        # macOS ru_maxrss is bytes
        rss_mb = r.ru_maxrss / (1024 * 1024)
    except Exception:
        pass

    print(f"wrote {args.out}")
    print(f"unresolved_count={len(unresolved)}")
    print("runtime_report:")
    print(f"  wall_seconds={wall:.3f}")
    print(f"  cpu_seconds={cpu:.3f}")
    if rss_mb is not None:
        print(f"  max_rss_mb={rss_mb:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
