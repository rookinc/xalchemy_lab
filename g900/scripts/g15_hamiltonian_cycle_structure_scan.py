#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

from g15_cocycle_decode import VERTICES, EDGES, EDGE_INDEX

ADJ = {v: set() for v in VERTICES}
for a, b in EDGES:
    ADJ[a].add(b)
    ADJ[b].add(a)

START = "o0"
N = len(VERTICES)
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


def vertex_kind(v: str) -> str:
    return v[0]


def edge_kind(a: str, b: str) -> str:
    ka = vertex_kind(a)
    kb = vertex_kind(b)
    pair = "-".join(sorted((ka, kb)))
    return pair


def transition_histogram(cycle: list[str]) -> Dict[str, int]:
    hist: Dict[str, int] = {}
    for a, b in zip(cycle[:-1], cycle[1:]):
        k = edge_kind(a, b)
        hist[k] = hist.get(k, 0) + 1
    return dict(sorted(hist.items()))


def max_outer_run(cycle: list[str]) -> int:
    cyc = cycle[:-1]
    doubled = cyc + cyc
    best = 0
    cur = 0
    for v in doubled:
        if vertex_kind(v) == "o":
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return min(best, len(cyc))


def first_non_outer_index(cycle: list[str]) -> int:
    for i, v in enumerate(cycle[:-1]):
        if vertex_kind(v) != "o":
            return i
    return len(cycle) - 1


def signature(cycle: list[str]) -> Dict[str, object]:
    hist = transition_histogram(cycle)
    return {
        "transition_histogram": hist,
        "max_outer_run": max_outer_run(cycle),
        "first_non_outer_index": first_non_outer_index(cycle),
    }


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


def bump(bucket: Dict[str, int], key: str) -> None:
    bucket[key] = bucket.get(key, 0) + 1


def main() -> int:
    dfs([START], {START})

    rows = []
    good_sig_hist: Dict[str, int] = {}
    bad_sig_hist: Dict[str, int] = {}
    good_outer_run_hist: Dict[str, int] = {}
    bad_outer_run_hist: Dict[str, int] = {}

    good_count = 0
    bad_count = 0

    for cyc in solutions:
        labels = loop_edge_labels(cyc)
        p1 = loop_parity(labels)
        good = (p1 == 1)
        sig = signature(cyc)
        sig_key = json.dumps(sig["transition_histogram"], sort_keys=True)
        outer_key = str(sig["max_outer_run"])

        if good:
            good_count += 1
            bump(good_sig_hist, sig_key)
            bump(good_outer_run_hist, outer_key)
        else:
            bad_count += 1
            bump(bad_sig_hist, sig_key)
            bump(bad_outer_run_hist, outer_key)

        rows.append(
            {
                "cycle": cyc,
                "edge_labels": labels,
                "one_cycle_parity": p1,
                "matches_sign_rule": good,
                "transition_histogram": sig["transition_histogram"],
                "max_outer_run": sig["max_outer_run"],
                "first_non_outer_index": sig["first_non_outer_index"],
            }
        )

    payload = {
        "hamiltonian_cycle_count": len(solutions),
        "cocycle_support": sorted(COCYCLE_SUPPORT),
        "summary": {
            "good_count": good_count,
            "bad_count": bad_count,
            "good_outer_run_histogram": dict(sorted(good_outer_run_hist.items(), key=lambda kv: int(kv[0]))),
            "bad_outer_run_histogram": dict(sorted(bad_outer_run_hist.items(), key=lambda kv: int(kv[0]))),
            "good_transition_signature_histogram": dict(sorted(good_sig_hist.items())),
            "bad_transition_signature_histogram": dict(sorted(bad_sig_hist.items())),
        },
        "examples_good": [r for r in rows if r["matches_sign_rule"]][:10],
        "examples_bad": [r for r in rows if not r["matches_sign_rule"]][:10],
    }

    outpath = Path("artifacts/g15_hamiltonian_cycle_structure_scan.json")
    outpath.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {outpath}")
    print(json.dumps(payload["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
