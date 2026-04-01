#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Set

from g15_cocycle_decode import EDGE_LABELS

EDGE_SET = set(EDGE_LABELS)


def parse_edge_list(text: str) -> List[str]:
    parts = [x.strip() for x in text.split(",") if x.strip()]
    bad = [x for x in parts if x not in EDGE_SET]
    if bad:
        raise ValueError(f"unknown edge labels: {', '.join(bad)}")
    return parts


def parity_of_loop(loop_edges: List[str], cocycle_support: Set[str]) -> int:
    return sum(1 for e in loop_edges if e in cocycle_support) % 2


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Probe loop parity against a chosen cocycle representative on G15."
    )
    parser.add_argument(
        "--cocycle-support",
        required=True,
        help="Comma-separated edge labels representing a cocycle support, e.g. e1,e7,e12",
    )
    parser.add_argument(
        "--loop",
        required=True,
        help="Comma-separated edge labels for the loop to test",
    )
    parser.add_argument(
        "--json-out",
        default="",
        help="Optional JSON output path",
    )
    args = parser.parse_args()

    cocycle_edges = set(parse_edge_list(args.cocycle_support))
    loop_edges = parse_edge_list(args.loop)

    one_parity = parity_of_loop(loop_edges, cocycle_edges)
    two_parity = (2 * one_parity) % 2

    payload = {
        "cocycle_support": sorted(cocycle_edges),
        "loop_edges": loop_edges,
        "one_cycle_parity": one_parity,
        "two_cycle_parity": two_parity,
        "one_cycle_sheet_effect": "flip" if one_parity == 1 else "preserve",
        "two_cycle_sheet_effect": "restore" if two_parity == 0 else "flip",
        "sign_rule_check": {
            "one_cycle_matches_n15_eq_minus_n0": one_parity == 1,
            "two_cycle_matches_n30_eq_n0": two_parity == 0,
        },
    }

    print(json.dumps(payload, indent=2))

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"\nWrote {args.json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
