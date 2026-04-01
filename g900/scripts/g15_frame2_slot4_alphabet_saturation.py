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


def one_edit_variants(seed: list[str], vocab: list[str]) -> list[list[str]]:
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
            out.append(mutated)
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

    slot4_hist = Counter()
    slot4_frame2_hist = Counter()
    depth_hist = Counter()
    class_hist = Counter()

    exact_frame2_hits = []
    frame2_d1_hits = []
    t2_states = []

    while q:
        cyc, depth = q.popleft()
        c = classify_cached(cyc, cache, r)
        norm = normalize_cycle(cyc)
        s4 = norm[4]

        slot4_hist[s4] += 1
        depth_hist[depth] += 1
        class_hist[(c["classification"], c["confidence"], c["distance_summary"]["best_action_distance"])] += 1

        if is_frame2_d1(c):
            slot4_frame2_hist[s4] += 1
            if len(frame2_d1_hits) < 20:
                frame2_d1_hits.append(norm)

        if is_exact_frame2(c):
            if len(exact_frame2_hits) < 20:
                exact_frame2_hits.append(norm)

        if s4 == "t2":
            if len(t2_states) < 20:
                t2_states.append({
                    "normalized_cycle": norm,
                    "classification": c["classification"],
                    "confidence": c["confidence"],
                    "best_action_distance": c["distance_summary"]["best_action_distance"],
                    "nearest_action_frames": sorted({rec["frame"] for rec in c["nearest"]["action"]}),
                    "action_match_frames": sorted({m["frame"] for m in c["action_matches"]}),
                })

        if depth >= max_depth:
            continue

        for child in one_edit_variants(cyc, vocab):
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
        "slot4_histogram": dict(sorted(slot4_hist.items())),
        "slot4_frame2_histogram": dict(sorted(slot4_frame2_hist.items())),
        "depth_histogram": dict(sorted(depth_hist.items())),
        "class_histogram": [
            {
                "classification": cl,
                "confidence": conf,
                "best_action_distance": d,
                "count": n,
            }
            for (cl, conf, d), n in class_hist.items()
        ],
        "has_exact_frame2": len(exact_frame2_hits) > 0,
        "has_t2_anywhere": "t2" in slot4_hist,
        "has_t2_in_frame2_d1": "t2" in slot4_frame2_hist,
        "exact_frame2_hits": exact_frame2_hits,
        "frame2_d1_hits": frame2_d1_hits,
        "t2_states": t2_states,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--locked-input", default="artifacts/frame2_witness_reconciliation.json")
    ap.add_argument("--vocab-input", default="artifacts/repair_radius_action_d4.json")
    ap.add_argument("--out", default="artifacts/frame2_slot4_alphabet_saturation.json")
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--max-depth", type=int, default=8)
    ap.add_argument("--max-action-distance", type=int, default=3)
    ap.add_argument("--max-workers", type=int, default=max(1, min(8, (os.cpu_count() or 4) - 1)))
    args = ap.parse_args()

    t0 = time.perf_counter()
    cpu0 = time.process_time()

    locked_data = load_json(args.locked_input)
    payload = load_json(args.vocab_input)
    vocab = unique_preserve_order(payload["vocab"])

    starts = [row["start_cycle"] for row in locked_data["results"]]

    print(f"locked starts: {len(starts)}")
    print(f"max_depth: {args.max_depth}")
    print(f"max_action_distance: {args.max_action_distance}")
    print(f"max_workers: {args.max_workers}")

    results = []
    with ProcessPoolExecutor(max_workers=args.max_workers) as ex:
        futures = [
            ex.submit(
                probe_one_start,
                cyc,
                vocab,
                args.r,
                args.max_depth,
                args.max_action_distance,
            )
            for cyc in starts
        ]
        for i, fut in enumerate(as_completed(futures), start=1):
            results.append(fut.result())
            print(f"completed {i}/{len(futures)}")

    combined_slot4 = Counter()
    combined_slot4_frame2 = Counter()
    total_visited = 0
    has_exact_frame2_count = 0
    has_t2_anywhere_count = 0
    has_t2_in_frame2_d1_count = 0

    for row in results:
        total_visited += row["visited_state_count"]
        if row["has_exact_frame2"]:
            has_exact_frame2_count += 1
        if row["has_t2_anywhere"]:
            has_t2_anywhere_count += 1
        if row["has_t2_in_frame2_d1"]:
            has_t2_in_frame2_d1_count += 1

        for k, v in row["slot4_histogram"].items():
            combined_slot4[k] += v
        for k, v in row["slot4_frame2_histogram"].items():
            combined_slot4_frame2[k] += v

    observed_alphabet = sorted(combined_slot4.keys())
    observed_frame2_alphabet = sorted(combined_slot4_frame2.keys())

    # same symbol family / index neighborhood around frame 2
    candidate_symbols = ["o2", "s2", "t2", "o4", "s4", "t4", "o0", "s0", "t0", "o3", "s3", "t3"]
    missing_candidates_global = [x for x in candidate_symbols if x not in observed_alphabet]
    missing_candidates_frame2 = [x for x in candidate_symbols if x not in observed_frame2_alphabet]

    wall = time.perf_counter() - t0
    cpu = time.process_time() - cpu0

    out = {
        "locked_start_count": len(starts),
        "max_depth": args.max_depth,
        "max_action_distance": args.max_action_distance,
        "max_workers": args.max_workers,
        "summary": {
            "has_exact_frame2_count": has_exact_frame2_count,
            "has_t2_anywhere_count": has_t2_anywhere_count,
            "has_t2_in_frame2_d1_count": has_t2_in_frame2_d1_count,
            "total_visited_state_count": total_visited,
            "observed_slot4_alphabet_global": observed_alphabet,
            "observed_slot4_alphabet_frame2_d1": observed_frame2_alphabet,
            "missing_candidate_symbols_global": missing_candidates_global,
            "missing_candidate_symbols_frame2_d1": missing_candidates_frame2,
            "slot4_histogram_global": dict(sorted(combined_slot4.items())),
            "slot4_histogram_frame2_d1": dict(sorted(combined_slot4_frame2.items())),
        },
        "runtime_report": {
            "wall_seconds": wall,
            "cpu_seconds_parent_only": cpu,
        },
        "results": results,
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {args.out}")
    print("summary:")
    print(json.dumps(out["summary"], indent=2))
    print("runtime_report:")
    print(f"  wall_seconds={wall:.3f}")
    print(f"  cpu_seconds_parent_only={cpu:.3f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
