from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from typing import Dict, List

from g15_cocycle_decode import parse_syndrome, solve_min_weight


def bits16(n: int) -> str:
    return format(n, "016b")


def summarize_solution_types(solutions) -> str:
    types = sorted({sol.support_type for sol in solutions})
    if len(types) == 1:
        return types[0]
    return "+".join(types)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Brute-force all 16-bit syndromes for G15 cocycle decoding."
    )
    parser.add_argument(
        "--max-weight",
        type=int,
        default=6,
        help="Maximum support weight to search for each syndrome.",
    )
    parser.add_argument(
        "--only-weight",
        type=int,
        default=None,
        help="If set, only keep syndromes whose minimum weight equals this value.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional cap on number of syndromes to inspect (for testing).",
    )
    parser.add_argument(
        "--json-out",
        default="",
        help="Optional JSON output path.",
    )
    args = parser.parse_args()

    total = 0
    kept = 0

    min_weight_hist = Counter()
    support_type_hist = Counter()
    mixed_type_hist = Counter()

    examples_by_type: Dict[str, List[dict]] = defaultdict(list)

    upper = 1 << 16
    if args.limit is not None:
        upper = min(upper, args.limit)

    for n in range(upper):
        syndrome_str = bits16(n)
        syndrome = parse_syndrome(syndrome_str)
        sols = solve_min_weight(syndrome, max_weight=args.max_weight)

        total += 1

        if not sols:
            min_weight_hist["no_solution_up_to_bound"] += 1
            continue

        min_w = sols[0].weight
        min_weight_hist[min_w] += 1

        if args.only_weight is not None and min_w != args.only_weight:
            continue

        kept += 1

        type_key = summarize_solution_types(sols)
        mixed_type_hist[type_key] += 1

        for sol in sols:
            support_type_hist[sol.support_type] += 1

        if len(examples_by_type[type_key]) < 8:
            examples_by_type[type_key].append(
                {
                    "syndrome": syndrome_str,
                    "solution_count": len(sols),
                    "min_weight": min_w,
                    "types": sorted({sol.support_type for sol in sols}),
                    "first_solutions": [
                        {
                            "edge_labels": sol.edge_labels,
                            "closed": sol.closed,
                            "connected": sol.connected,
                            "support_type": sol.support_type,
                            "boundary_vertices": sol.boundary_vertices,
                        }
                        for sol in sols[:3]
                    ],
                }
            )

    payload = {
        "total_syndromes_checked": total,
        "kept_syndromes": kept,
        "max_weight": args.max_weight,
        "only_weight": args.only_weight,
        "min_weight_histogram": dict(min_weight_hist),
        "support_type_histogram_over_kept_solutions": dict(support_type_hist),
        "syndrome_type_histogram": dict(mixed_type_hist),
        "examples_by_type": dict(examples_by_type),
    }

    print(json.dumps(payload, indent=2))

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        print(f"\nWrote {args.json_out}")


if __name__ == "__main__":
    main()
