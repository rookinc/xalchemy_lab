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
    if not (c["classification"] == "action-cell" and c["confidence"] == "exact"):
        return False
    return any(m["frame"] == 2 for m in c["action_matches"])


def is_frame2_d1(c: dict[str, Any]) -> bool:
    if not (c["classification"] == "action-cell" and c["distance_summary"]["best_action_distance"] == 1):
        return False
    return any(rec["frame"] == 2 for rec in c["nearest"]["action"])


def target_slot_value(cycle: list[str]) -> tuple[list[str], list[str]]:
    target = ["o4", "s4", "t2", "s2", "t0", "s0"]
    return normalize_cycle(cycle), normalize_cycle(target)


def slot4_value(cycle: list[str]) -> str:
    norm = normalize_cycle(cycle)
    return norm[4]


def mismatch_signature_to_frame2(cycle: list[str]) -> list[dict[str, Any]]:
    norm, target = target_slot_value(cycle)
    out = []
    for i, (a, b) in enumerate(zip(norm, target)):
        if a != b:
            out.append({"position": i, "from": a, "to": b})
    return out


def probe_one_start(
    start_cycle: list[str],
    vocab: list[str],
    r: int,
    max_depth: int,
    max_action_distance: int,
    max_examples: int = 5,
) -> dict[str, Any]:
    cache: dict[tuple[str, ...], dict[str, Any]] = {}
    start_c = classify_cached(start_cycle, cache, r)

    # BFS over normalized states, restricted to action distance <= max_action_distance
    q = deque()
    visited = set()
    start_key = tuple(normalize_cycle(start_cycle))
    q.append((start_cycle, 0, []))
    visited.add(start_key)

    found_exact = {}
    found_frame2_d1 = {}
    depth_hist = Counter()
    slot4_hist = Counter()

    expanded = 0
    accepted = 0

    while q:
        cycle, depth, labels = q.popleft()
        c = classify_cached(cycle, cache, r)

        depth_hist[depth] += 1
        slot4_hist[slot4_value(cycle)] += 1

        if is_exact_frame2(c):
            found_exact[tuple(normalize_cycle(cycle))] = {
                "depth": depth,
                "labels": labels,
                "cycle": cycle,
                "normalized_cycle": normalize_cycle(cycle),
                "mismatch_signature": mismatch_signature_to_frame2(cycle),
            }
            continue

        if is_frame2_d1(c):
            found_frame2_d1[tuple(normalize_cycle(cycle))] = {
                "depth": depth,
                "labels": labels,
                "cycle": cycle,
                "normalized_cycle": normalize_cycle(cycle),
                "mismatch_signature": mismatch_signature_to_frame2(cycle),
            }

        if depth >= max_depth:
            continue

        for item in one_edit_variants(cycle, vocab):
            expanded += 1
            child = item["cycle"]
            key = tuple(normalize_cycle(child))
            if key in visited:
                continue

            cc = classify_cached(child, cache, r)
            d = cc["distance_summary"]["best_action_distance"]

            # Deep but still targeted: keep only cycles in the frame-2 near corridor
            # or exact frame-2 closure.
            keep = False
            if is_exact_frame2(cc):
                keep = True
            elif d is not None and d <= max_action_distance:
                if cc["classification"] == "action-cell":
                    # Prefer cycles that are tied to frame 2 when near-action.
                    if cc["confidence"] == "nearest":
                        keep = any(rec["frame"] == 2 for rec in cc["nearest"]["action"])
                    elif cc["confidence"] == "ambiguous":
                        # leave ambiguous out of the tight corridor
                        keep = False
                    else:
                        keep = False
                else:
                    keep = False

            if not keep:
                continue

            visited.add(key)
            accepted += 1
            q.append((child, depth + 1, labels + [item["label"]]))

    return {
        "start_cycle": start_cycle,
        "normalized_start_cycle": normalize_cycle(start_cycle),
        "start_mismatch_signature": mismatch_signature_to_frame2(start_cycle),
        "start_slot4_value": slot4_value(start_cycle),
        "max_depth": max_depth,
        "max_action_distance": max_action_distance,
        "visited_state_count": len(visited),
        "expanded_edge_count": expanded,
        "accepted_state_count": accepted,
        "has_exact_frame2": len(found_exact) > 0,
        "has_frame2_d1": len(found_frame2_d1) > 0,
        "exact_frame2_hits": list(found_exact.values())[:max_examples],
        "frame2_d1_hits": list(found_frame2_d1.values())[:max_examples],
        "depth_histogram": dict(sorted(depth_hist.items())),
        "slot4_value_histogram": dict(slot4_hist),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        default="artifacts/unresolved20_depth4_frame2_d1_hits.json",
        help="Extracted frame-2 d1 examples.",
    )
    ap.add_argument(
        "--vocab-input",
        default="artifacts/repair_radius_action_d4.json",
        help="Input payload for vocab.",
    )
    ap.add_argument(
        "--out",
        default="artifacts/frame2_slot4_deep_probe.json",
        help="Output JSON report.",
    )
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--max-depth", type=int, default=6)
    ap.add_argument("--max-action-distance", type=int, default=2)
    ap.add_argument("--max-workers", type=int, default=max(1, min(8, (os.cpu_count() or 4) - 1)))
    args = ap.parse_args()

    t0 = time.perf_counter()
    cpu0 = time.process_time()

    data = load_json(args.input)
    payload = load_json(args.vocab_input)
    vocab = unique_preserve_order(payload["vocab"])

    # Deduplicate normalized witness cycles
    starts = []
    seen = set()
    for row in data["results"]:
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

    results: list[dict[str, Any]] = []
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
    has_d1 = sum(1 for r in results if r["has_frame2_d1"])
    slot4_start_hist = Counter(r["start_slot4_value"] for r in results)
    slot4_end_hist = Counter()
    for r in results:
        for hit in r["frame2_d1_hits"]:
            norm = hit["normalized_cycle"]
            slot4_end_hist[norm[4]] += 1
        for hit in r["exact_frame2_hits"]:
            norm = hit["normalized_cycle"]
            slot4_end_hist[norm[4]] += 1

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
        "max_workers": args.max_workers,
        "max_depth": args.max_depth,
        "max_action_distance": args.max_action_distance,
        "summary": {
            "has_exact_frame2_count": has_exact,
            "has_frame2_d1_count": has_d1,
            "start_slot4_value_histogram": dict(slot4_start_hist),
            "observed_hit_slot4_value_histogram": dict(slot4_end_hist),
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
