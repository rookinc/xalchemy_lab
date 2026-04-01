#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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
        default="artifacts/unresolved20_depth4_parallel_probe.json",
        help="Depth-4 unresolved20 probe output JSON.",
    )
    ap.add_argument(
        "--out",
        default="artifacts/unresolved20_depth4_frame2_d1_hits.json",
        help="Output JSON for frame-2-nearest d1 hits.",
    )
    args = ap.parse_args()

    t0 = time.perf_counter()
    cpu0 = time.process_time()

    data = load_json(args.input)
    results = data["results"]

    extracted = []
    hit_counter = Counter()

    for row in results:
        start = row["start_cycle"]
        kept = []

        for hit in row.get("d1_examples", []):
            nearest = hit.get("nearest_action", [])
            frames = sorted({rec["frame"] for rec in nearest})
            if 2 in frames:
                kept.append({
                    "start_cycle": start,
                    "labels": hit["labels"],
                    "cycle": hit["cycle"],
                    "nearest_frames": frames,
                    "distance_summary": hit["distance_summary"],
                })
                hit_counter[tuple(hit["cycle"])] += 1

        if kept:
            extracted.append({
                "start_cycle": start,
                "frame2_d1_hits": kept,
            })

    out = {
        "source_probe": args.input,
        "start_count_with_frame2_d1_example": len(extracted),
        "common_frame2_d1_hit_cycles": [
            {"cycle": list(cyc), "count": n}
            for cyc, n in hit_counter.most_common()
        ],
        "results": extracted,
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    wall = time.perf_counter() - t0
    cpu = time.process_time() - cpu0
    rss_mb = None
    try:
        import resource
        rr = resource.getrusage(resource.RUSAGE_SELF)
        rss_mb = rr.ru_maxrss / (1024 * 1024)
    except Exception:
        pass

    print(f"wrote {args.out}")
    print(f"start_count_with_frame2_d1_example={len(extracted)}")
    print("runtime_report:")
    print(f"  wall_seconds={wall:.3f}")
    print(f"  cpu_seconds={cpu:.3f}")
    if rss_mb is not None:
        print(f"  max_rss_mb={rss_mb:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
