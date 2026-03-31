from __future__ import annotations

import argparse
import itertools
import json
import time
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

from g15_cocycle_decode import (
    build_A,
    build_B,
    EDGE_LABELS,
    VERTICES,
    classify_support,
    xor_dot,
)

# ============================================================
# Fast weight-6 syndrome scan
# ============================================================

def bits16(n: int) -> str:
    return format(n, "016b")


def syndrome_from_x(A: List[List[int]], x: List[int]) -> str:
    bits = [str(xor_dot(row, x)) for row in A]
    return "".join(bits)


def edge_vector_from_support(support: Tuple[int, ...], n_edges: int = 30) -> List[int]:
    x = [0] * n_edges
    for i in support:
        x[i] = 1
    return x


def summarize_type_bucket(records: List[dict]) -> str:
    types = sorted({r["support_type"] for r in records})
    if len(types) == 1:
        return types[0]
    return "+".join(types)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Enumerate all weight-6 supports on G15 and bucket their induced syndromes."
    )
    parser.add_argument(
        "--json-out",
        default="artifacts/g15_weight6_syndrome_scan.json",
        help="Output JSON path.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=20000,
        help="Progress print interval.",
    )
    args = parser.parse_args()

    A = build_A()
    B = build_B()

    start = time.time()
    total_supports = 0

    syndrome_to_records: Dict[str, List[dict]] = defaultdict(list)
    support_type_hist = Counter()
    syndrome_type_hist = Counter()

    examples_by_type: Dict[str, List[dict]] = defaultdict(list)

    for support in itertools.combinations(range(30), 6):
        total_supports += 1

        x = edge_vector_from_support(support)
        syndrome = syndrome_from_x(A, x)

        closed, connected, support_type, boundary_vertices = classify_support(x, B)

        record = {
            "edge_labels": [EDGE_LABELS[i] for i in support],
            "closed": closed,
            "connected": connected,
            "support_type": support_type,
            "boundary_vertices": boundary_vertices,
        }
        syndrome_to_records[syndrome].append(record)
        support_type_hist[support_type] += 1

        if total_supports % args.progress_every == 0:
            elapsed = time.time() - start
            print(
                f"[progress] supports={total_supports} "
                f"unique_syndromes={len(syndrome_to_records)} "
                f"elapsed={elapsed:.1f}s"
            )

    for syndrome, records in syndrome_to_records.items():
        bucket = summarize_type_bucket(records)
        syndrome_type_hist[bucket] += 1
        if len(examples_by_type[bucket]) < 12:
            examples_by_type[bucket].append(
                {
                    "syndrome": syndrome,
                    "example_count": len(records),
                    "first_examples": records[:3],
                }
            )

    payload = {
        "mode": "weight6_support_scan",
        "total_supports_scanned": total_supports,
        "unique_syndromes_hit": len(syndrome_to_records),
        "support_type_histogram_over_supports": dict(support_type_hist),
        "syndrome_type_histogram": dict(syndrome_type_hist),
        "examples_by_type": dict(examples_by_type),
    }

    with open(args.json_out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)

    elapsed = time.time() - start
    print(json.dumps(payload, indent=2))
    print(f"\nWrote {args.json_out}")
    print(f"Elapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
