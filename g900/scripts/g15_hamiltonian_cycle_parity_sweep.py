#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

from g15_cocycle_decode import VERTICES, EDGES, EDGE_INDEX

ADJ = {v: set() for v in VERTICES}
for a, b in EDGES:
    ADJ[a].add(b)
    ADJ[b].add(a)

START = "o0"
N = len(VERTICES)

# Sample cocycle representative currently used in the successful probe.
COCYCLE_SUPPORT = {"e1", "e7", "e12", "e18", "e24", "e29"}


def canon_cycle(cycle: list[str]) -> tuple[str, ...]:
    cyc = cycle[:-1] if cycle[0] == cycle[-1] else cycle[:]
    rots = [tuple(cyc[i:] + cyc[:i]) for i in range(len(cyc))]
    rev = list(reversed(cyc))
    rots += [tuple(rev[i:] + rev[:i]) for i in range(len(rev))]
    return min(rots)


def edge_label_for_pair(a: str, b: str) -> str:
    key = tuple(sorted((a, b)))
    idx = EDGE_INDEX.get(key)
    if idx is None:
        raise ValueError(f"no G15 edge between {a} and {b}")
    return f"e{idx+1}"


def loop_edge_labels(cycle: list[str]) -> list[str]:
    return [edge_label_for_pair(a, b) for a, b in zip(cycle[:-1], cycle[1:])]


def loop_parity(edge_labels: list[str]) -> int:
    return sum(1 for e in edge_labels if e in COCYCLE_SUPPORT) % 2


seen = set()
solutions: List[list[str]] = []


def dfs(path: list[str], used: set[str]) -> None:
    cur = path[-1]
    if len(path) == N:
        if START in ADJ[cur]:
            cyc = path + [START]
            key = canon_cycle(cyc)
            if key not in seen:
                seen.add(key)
                solutions.append(cyc)
        return

    for nxt in sorted(ADJ[cur]):
        if nxt in used:
            continue
        used.add(nxt)
        path.append(nxt)
        dfs(path, used)
        path.pop()
        used.remove(nxt)


def main() -> int:
    dfs([START], {START})

    rows = []
    odd_count = 0
    even_count = 0

    for cyc in solutions:
        labels = loop_edge_labels(cyc)
        p1 = loop_parity(labels)
        p2 = (2 * p1) % 2
        if p1 == 1:
            odd_count += 1
        else:
            even_count += 1
        rows.append(
            {
                "cycle": cyc,
                "edge_labels": labels,
                "one_cycle_parity": p1,
                "two_cycle_parity": p2,
                "one_cycle_sheet_effect": "flip" if p1 == 1 else "preserve",
                "two_cycle_sheet_effect": "restore" if p2 == 0 else "flip",
                "matches_sign_rule": (p1 == 1 and p2 == 0),
            }
        )

    payload = {
        "hamiltonian_cycle_count": len(solutions),
        "cocycle_support": sorted(COCYCLE_SUPPORT),
        "summary": {
            "odd_one_cycle_count": odd_count,
            "even_one_cycle_count": even_count,
            "sign_rule_match_count": sum(1 for r in rows if r["matches_sign_rule"]),
        },
        "examples": rows[:20],
    }

    outpath = Path("artifacts/g15_hamiltonian_cycle_parity_sweep.json")
    outpath.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {outpath}")
    print(json.dumps(payload["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
