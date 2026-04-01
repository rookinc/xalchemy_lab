#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter, deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from witness_machine.core import classify_cycle, normalize_cycle


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def unique_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def one_edit_variants(seed: list[str], vocab: list[str]) -> list[dict[str, Any]]:
    out = []
    seen = set()
    for pos in range(len(seed)):
        original = seed[pos]
        for candidate in vocab:
            if candidate == original:
                continue
            mutated = seed.copy()
            mutated[pos] = candidate
            key = tuple(mutated)
            if key in seen:
                continue
            seen.add(key)
            out.append({"label": f"edit_pos{pos}_{original}_to_{candidate}", "cycle": mutated})
    return out


def classify_cached(cycle: list[str], cache: dict[tuple[str, ...], dict[str, Any]], r: int) -> dict[str, Any]:
    key = tuple(normalize_cycle(cycle))
    if key not in cache:
        cache[key] = classify_cycle(cycle, r)
    return cache[key]


def is_exact_frame2(c: dict[str, Any]) -> bool:
    return (
        c["classification"] == "action-cell"
        and c["confidence"] == "exact"
        and any(m["frame"] == 2 for m in c["action_matches"])
    )


def is_frame2_d1(c: dict[str, Any]) -> bool:
    return (
        c["classification"] == "action-cell"
        and c["distance_summary"]["best_action_distance"] == 1
        and any(rec["frame"] == 2 for rec in c["nearest"]["action"])
    )


def slot4_value(cycle: list[str]) -> str:
    return normalize_cycle(cycle)[4]


def probe_one_start(
    start_cycle: list[str],
    vocab: list[str],
    r: int,
    max_depth: int,
    max_action_distance: int,
) -> dict[str, Any]:
    cache: dict[tuple[str, ...], dict[str, Any]] = {}
    q = deque()
    visited = set()

    start_key = tuple(normalize_cycle(start_cycle))
    q.append((start_cycle, 0))
    visited.add(start_key)

    has_exact = False
    has_frame2_d1 = False
    has_t2_anywhere = False
    has_t2_in_frame2_d1 = False

    slot4_hist = Counter()
    depth_hist = Counter()

    while q:
        cyc, depth = q.popleft()
        c = classify_cached(cyc, cache, r)
        norm = normalize_cycle(cyc)

        depth_hist[depth] += 1
        s4 = norm[4]
        slot4_hist[s4] += 1

        if s4 == "t2":
            has_t2_anywhere = True
            if is_frame2_d1(c):
                has_t2_in_frame2_d1 = True

        if is_exact_frame2(c):
            has_exact = True

        if is_frame2_d1(c):
            has_frame2_d1 = True

        if depth >= max_depth:
            continue

        for item in one_edit_variants(cyc, vocab):
            child = item["cycle"]
            key = tuple(normalize_cycle(child))
            if key in visited:
                continue

            cc = classify_cached(child, cache, r)
            d = cc["distance_summary"]["best_action_distance"]

            keep = False
            if is_exact_frame2(cc):
                keep = True
            elif d is not None and d <= max_action_distance:
                keep = True

            if not keep:
                continue

            visited.add(key)
            q.append((child, depth + 1))

    return {
        "start_cycle": start_cycle,
        "normalized_start_cycle": normalize_cycle(start_cycle),
        "visited_state_count": len(visited),
        "has_exact_frame2": has_exact,
        "has_frame2_d1": has_frame2_d1,
        "has_t2_anywhere": has_t2_anywhere,
        "has_t2_in_frame2_d1": has_t2_in_frame2_d1,
        "slot4_histogram": dict(slot4_hist),
        "depth_histogram": dict(depth_hist),
    }


def run_depth(starts: list[list[str]], vocab: list[str], r: int, max_depth: int, max_action_distance: int, max_workers: int) -> dict[str, Any]:
    t0 = time.perf_counter()
    cpu0 = time.process_time()

    results: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(probe_one_start, cyc, vocab, r, max_depth, max_action_distance) for cyc in starts]
        for i, fut in enumerate(as_completed(futures), start=1):
            results.append(fut.result())
            print(f"depth {max_depth}: completed {i}/{len(futures)}")

    has_exact = sum(1 for r in results if r["has_exact_frame2"])
    has_frame2_d1 = sum(1 for r in results if r["has_frame2_d1"])
    has_t2_anywhere = sum(1 for r in results if r["has_t2_anywhere"])
    has_t2_in_frame2_d1 = sum(1 for r in results if r["has_t2_in_frame2_d1"])

    combined_slot4 = Counter()
    total_visited = 0
    for r in results:
        total_visited += r["visited_state_count"]
        for k, v in r["slot4_histogram"].items():
            combined_slot4[k] += v

    wall = time.perf_counter() - t0
    cpu = time.process_time() - cpu0

    return {
        "max_depth": max_depth,
        "max_action_distance": max_action_distance,
        "summary": {
            "start_count": len(starts),
            "has_exact_frame2_count": has_exact,
            "has_frame2_d1_count": has_frame2_d1,
            "has_t2_anywhere_count": has_t2_anywhere,
            "has_t2_in_frame2_d1_count": has_t2_in_frame2_d1,
            "total_visited_state_count": total_visited,
            "slot4_histogram": dict(combined_slot4),
        },
        "runtime_report": {
            "wall_seconds": wall,
            "cpu_seconds_parent_only": cpu,
        },
        "results": results,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--witnesses", default="artifacts/unresolved20_depth4_frame2_d1_hits.json")
    ap.add_argument("--vocab-input", default="artifacts/repair_radius_action_d4.json")
    ap.add_argument("--out", default="artifacts/frame2_escape_return_depth_sweep.json")
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--depths", default="4,5,6,7,8")
    ap.add_argument("--max-action-distance", type=int, default=3)
    ap.add_argument("--max-workers", type=int, default=max(1, min(8, (os.cpu_count() or 4) - 1)))
    args = ap.parse_args()

    witness_data = load_json(args.witnesses)
    payload = load_json(args.vocab_input)
    vocab = unique_preserve_order(payload["vocab"])

    starts = []
    seen = set()
    for row in witness_data["results"]:
        for hit in row["frame2_d1_hits"]:
            key = tuple(normalize_cycle(hit["cycle"]))
            if key in seen:
                continue
            seen.add(key)
            starts.append(hit["cycle"])

    depths = [int(x.strip()) for x in args.depths.split(",") if x.strip()]
    print(f"unique frame2 witness starts: {len(starts)}")
    print(f"depths: {depths}")
    print(f"max_action_distance: {args.max_action_distance}")
    print(f"max_workers: {args.max_workers}")

    runs = []
    for d in depths:
        runs.append(run_depth(starts, vocab, args.r, d, args.max_action_distance, args.max_workers))

    out = {
        "unique_start_count": len(starts),
        "max_action_distance": args.max_action_distance,
        "max_workers": args.max_workers,
        "runs": runs,
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    for run in runs:
        print(f"\ndepth {run['max_depth']} summary: {run['summary']}")
        print(f"depth {run['max_depth']} runtime_report: {run['runtime_report']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
