#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from witness_machine.core import normalize_cycle


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        default="artifacts/unresolved20_depth4_frame2_d1_hits.json",
        help="Extracted frame-2 d1 examples.",
    )
    ap.add_argument(
        "--out",
        default="artifacts/frame2_d1_mismatch_patterns.json",
        help="Output JSON report.",
    )
    args = ap.parse_args()

    t0 = time.perf_counter()
    cpu0 = time.process_time()

    data = load_json(args.input)

    # Exact frame-2 action representative from the classifier family
    target = ["o4", "s4", "t2", "s2", "t0", "s0"]
    target_norm = normalize_cycle(target)

    per_cycle_counter = Counter()
    mismatch_signature_counter = Counter()
    position_mismatch_counter = Counter()
    value_sub_counter = Counter()
    hamming_counter = Counter()

    examples_by_signature: dict[tuple[tuple[int, str, str], ...], list[list[str]]] = defaultdict(list)

    all_hits = []
    for row in data["results"]:
        start = row["start_cycle"]
        for hit in row["frame2_d1_hits"]:
            cyc = hit["cycle"]
            cyc_norm = normalize_cycle(cyc)

            diffs = []
            for i, (a, b) in enumerate(zip(cyc_norm, target_norm)):
                if a != b:
                    diffs.append((i, a, b))
                    position_mismatch_counter[i] += 1
                    value_sub_counter[(i, a, b)] += 1

            sig = tuple(diffs)
            mismatch_signature_counter[sig] += 1
            per_cycle_counter[tuple(cyc_norm)] += 1
            hamming_counter[len(diffs)] += 1

            if len(examples_by_signature[sig]) < 5:
                examples_by_signature[sig].append(cyc_norm)

            all_hits.append({
                "start_cycle": start,
                "raw_cycle": cyc,
                "normalized_cycle": cyc_norm,
                "mismatch_signature": [{"position": i, "from": a, "to": b} for i, a, b in diffs],
                "hamming_to_frame2_target": len(diffs),
                "labels": hit["labels"],
            })

    out = {
        "source": args.input,
        "exact_frame2_target": target,
        "normalized_frame2_target": target_norm,
        "summary": {
            "start_count_with_examples": data["start_count_with_frame2_d1_example"],
            "total_recorded_frame2_d1_hits": len(all_hits),
            "hamming_histogram": [
                {"hamming": k, "count": v} for k, v in sorted(hamming_counter.items())
            ],
            "most_common_normalized_cycles": [
                {"cycle": list(cyc), "count": n}
                for cyc, n in per_cycle_counter.most_common()
            ],
            "most_common_mismatch_signatures": [
                {
                    "signature": [
                        {"position": i, "from": a, "to": b} for i, a, b in sig
                    ],
                    "count": n,
                    "example_cycles": [list(ex) for ex in examples_by_signature[sig]],
                }
                for sig, n in mismatch_signature_counter.most_common()
            ],
            "position_mismatch_counts": [
                {"position": pos, "count": n}
                for pos, n in sorted(position_mismatch_counter.items())
            ],
            "value_substitution_counts": [
                {
                    "position": pos,
                    "from": a,
                    "to": b,
                    "count": n,
                }
                for (pos, a, b), n in value_sub_counter.most_common()
            ],
        },
        "hits": all_hits,
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
    print("runtime_report:")
    print(f"  wall_seconds={wall:.3f}")
    print(f"  cpu_seconds={cpu:.3f}")
    if rss_mb is not None:
        print(f"  max_rss_mb={rss_mb:.2f}")

    print("\nhamming_histogram:")
    for k, v in sorted(hamming_counter.items()):
        print(f"  {k}: {v}")

    print("\nmost_common_mismatch_signatures:")
    for sig, n in mismatch_signature_counter.most_common(10):
        rendered = ", ".join([f"pos{i}:{a}->{b}" for i, a, b in sig]) if sig else "exact"
        print(f"  {n} :: {rendered}")

    print("\nmost_common_value_substitutions:")
    for (pos, a, b), n in value_sub_counter.most_common(15):
        print(f"  {n} :: pos{pos}: {a} -> {b}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
