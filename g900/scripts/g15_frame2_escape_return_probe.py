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
            out.append({
                "label": f"edit_pos{pos}_{original}_to_{candidate}",
                "cycle": mutated,
            })
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
    max_examples: int = 5,
) -> dict[str, Any]:
    cache: dict[tuple[str, ...], dict[str, Any]] = {}
    q = deque()
    visited = set()

    start_key = tuple(normalize_cycle(start_cycle))
    q.append((start_cycle, 0, []))
    visited.add(start_key)

    found_exact = {}
    found_frame2_d1 = {}
    depth_hist = Counter()
    class_hist = Counter()
    slot4_hist = Counter()

    while q:
        cyc, depth, labels = q.popleft()
        c = classify_cached(cyc, cache, r)
        norm = normalize_cycle(cyc)

        depth_hist[depth] += 1
        class_hist[(c["classification"], c["confidence"], c["distance_summary"]["best_action_distance"])] += 1
        slot4_hist[slot4_value(cyc)] += 1

        if is_exact_frame2(c):
            found_exact[tuple(norm)] = {
                "depth": depth,
                "labels": labels,
                "cycle": cyc,
                "normalized_cycle": norm,
            }
            continue

        if is_frame2_d1(c):
            found_frame2_d1[tuple(norm)] = {
                "depth": depth,
                "labels": labels,
                "cycle": cyc,
                "normalized_cycle": norm,
            }

        if depth >= max_depth:
            continue

        for item in one_edit_variants(cyc, vocab):
            child = item["cycle"]
            child_key = tuple(normalize_cycle(child))
            if child_key in visited:
                continue

            cc = classify_cached(child, cache, r)
            d = cc["distance_summary"]["best_action_distance"]

            # Escape-and-return corridor:
            # allow states up to a capped action distance, not just frame2 corridor.
            keep = False
            if is_exact_frame2(cc):
                keep = True
            elif d is not None and d <= max_action_distance:
                keep = True

            if not keep:
                continue

            visited.add(child_key)
            q.append((child, depth + 1, labels + [item["label"]]))

    return {
        "start_cycle": start_cycle,
        "normalized_start_cycle": normalize_cycle(start_cycle),
        "has_exact_frame2": len(found_exact) > 0,
        "has_frame2_d1": len(found_frame2_d1) > 0,
        "exact_frame2_hits": list(found_exact.values())[:max_examples],
        "frame2_d1_hits": list(found_frame2_d1.values())[:max_examples],
        "visited_state_count": len(visited),
        "depth_histogram": dict(sorted(depth_hist.items())),
        "slot4_value_histogram": dict(slot4_hist),
        "class_histogram": [
            {
                "classification": cl,
                "confidence": conf,
                "best_action_distance": d,
                "count": n,
            }
            for (cl, conf, d), n in class_hist.items()
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--witnesses", default="artifacts/unresolved20_depth4_frame2_d1_hits.json")
    ap.add_argument("--vocab-input", default="artifacts/repair_radius_action_d4.json")
    ap.add_argument("--out", default="artifacts/frame2_escape_return_probe.json")
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--max-depth", type=int, default=6)
    ap.add_argument("--max-action-distance", type=int, default=3)
    ap.add_argument("--max-workers", type=int, default=max(1, min(8, (os.cpu_count() or 4) - 1)))
    args = ap.parse_args()

    t0 = time.perf_counter()
    cpu0 = time.process_time()

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

    print(f"unique frame2 witness starts: {len(starts)}")
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

    has_exact = sum(1 for r in results if r["has_exact_frame2"])
    has_frame2_d1 = sum(1 for r in results if r["has_frame2_d1"])

    wall = time.perf_counter() - t0
    cpu = time.process_time() - cpu0
    rss_mb = None
    try:
        import resource
        rr = resource.getrusage(resource.RUSAGE_SELF)
        rss_mb = rr.ru_maxrss / (1024 * 1024)
    except Exception:
        pass

    out = {
        "unique_start_count": len(starts),
        "max_depth": args.max_depth,
        "max_action_distance": args.max_action_distance,
        "max_workers": args.max_workers,
        "summary": {
            "has_exact_frame2_count": has_exact,
            "has_frame2_d1_count": has_frame2_d1,
        },
        "runtime_report": {
            "wall_seconds": wall,
            "cpu_seconds": cpu,
            "max_rss_mb": rss_mb,
        },
        "results": results,
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    print("summary:", out["summary"])
    print("runtime_report:")
    print(f"  wall_seconds={wall:.3f}")
    print(f"  cpu_seconds={cpu:.3f}")
    if rss_mb is not None:
        print(f"  max_rss_mb={rss_mb:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
