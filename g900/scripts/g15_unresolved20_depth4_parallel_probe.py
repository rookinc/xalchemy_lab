#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
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


def probe_one_start(start_cycle: list[str], vocab: list[str], r: int, max_examples: int = 5) -> dict[str, Any]:
    cache: dict[tuple[str, ...], dict[str, Any]] = {}
    found_exact: dict[tuple[str, ...], dict[str, Any]] = {}
    found_d1: dict[tuple[str, ...], dict[str, Any]] = {}

    lvl1 = one_edit_variants(start_cycle, vocab)
    for item1 in lvl1:
        lvl2 = one_edit_variants(item1["cycle"], vocab)
        for item2 in lvl2:
            lvl3 = one_edit_variants(item2["cycle"], vocab)
            for item3 in lvl3:
                lvl4 = one_edit_variants(item3["cycle"], vocab)
                for item4 in lvl4:
                    cyc4 = item4["cycle"]
                    c4 = classify_cached(cyc4, cache, r)

                    if c4["classification"] == "action-cell" and c4["confidence"] == "exact":
                        found_exact[tuple(cyc4)] = {
                            "labels": (item1["label"], item2["label"], item3["label"], item4["label"]),
                            "cycle": cyc4,
                            "classification": c4["classification"],
                            "confidence": c4["confidence"],
                            "distance_summary": c4["distance_summary"],
                            "action_matches": c4["action_matches"],
                            "nearest_action": c4["nearest"]["action"],
                        }
                    elif (
                        c4["classification"] == "action-cell"
                        and c4["distance_summary"]["best_action_distance"] == 1
                    ):
                        found_d1[tuple(cyc4)] = {
                            "labels": (item1["label"], item2["label"], item3["label"], item4["label"]),
                            "cycle": cyc4,
                            "classification": c4["classification"],
                            "confidence": c4["confidence"],
                            "distance_summary": c4["distance_summary"],
                            "action_matches": c4["action_matches"],
                            "nearest_action": c4["nearest"]["action"],
                        }

    exact_targets = Counter()
    d1_targets = Counter()
    d1_has_frame2 = False

    for hit in found_exact.values():
        for rec in hit["action_matches"]:
            exact_targets[(rec["frame"], tuple(rec["cycle"]))] += 1

    for hit in found_d1.values():
        for rec in hit["nearest_action"]:
            d1_targets[(rec["frame"], tuple(rec["cycle"]))] += 1
            if rec["frame"] == 2:
                d1_has_frame2 = True

    return {
        "start_cycle": start_cycle,
        "found_exact_count": len(found_exact),
        "found_d1_count": len(found_d1),
        "has_exact": len(found_exact) > 0,
        "has_d1": len(found_d1) > 0,
        "has_frame2_d1": d1_has_frame2,
        "exact_targets": [
            {"frame": frame, "cycle": list(cyc), "count": n}
            for (frame, cyc), n in exact_targets.items()
        ],
        "d1_targets": [
            {"frame": frame, "cycle": list(cyc), "count": n}
            for (frame, cyc), n in d1_targets.items()
        ],
        "exact_examples": list(found_exact.values())[:max_examples],
        "d1_examples": list(found_d1.values())[:max_examples],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="artifacts/repair_radius_action_d4.json")
    ap.add_argument("--unresolved", default="artifacts/hard_d2_depth3_unresolved_20.json")
    ap.add_argument("--out", default="artifacts/unresolved20_depth4_parallel_probe.json")
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--max-workers", type=int, default=max(1, min(8, (os.cpu_count() or 4) - 1)))
    args = ap.parse_args()

    t0 = time.perf_counter()
    cpu0 = time.process_time()

    payload = load_json(args.input)
    vocab = unique_preserve_order(payload["vocab"])

    unresolved = load_json(args.unresolved)["unresolved_results"]
    starts = [row["start_cycle"] for row in unresolved]

    print(f"unresolved starts: {len(starts)}")
    print(f"max_workers: {args.max_workers}")

    results: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=args.max_workers) as ex:
        futures = [ex.submit(probe_one_start, cyc, vocab, args.r) for cyc in starts]
        for i, fut in enumerate(as_completed(futures), start=1):
            results.append(fut.result())
            print(f"completed {i}/{len(futures)}")

    has_4step_exact = sum(1 for r in results if r["has_exact"])
    has_4step_d1 = sum(1 for r in results if r["has_d1"])
    to_frame2_d1 = sum(1 for r in results if r["has_frame2_d1"])

    hist = Counter((r["found_d1_count"], r["found_exact_count"]) for r in results)
    exact_target_hist = Counter()
    d1_target_hist = Counter()

    for r in results:
        for rec in r["exact_targets"]:
            exact_target_hist[(rec["frame"], tuple(rec["cycle"]))] += rec["count"]
        for rec in r["d1_targets"]:
            d1_target_hist[(rec["frame"], tuple(rec["cycle"]))] += rec["count"]

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
        "unresolved_start_count": len(starts),
        "max_workers": args.max_workers,
        "summary": {
            "has_4step_exact": has_4step_exact,
            "has_4step_d1": has_4step_d1,
            "to_frame2_d1": to_frame2_d1,
            "histogram_found_d1_found_exact": [
                {"found_d1_count": k[0], "found_exact_count": k[1], "count": v}
                for k, v in sorted(hist.items())
            ],
            "exact_targets": [
                {"frame": frame, "cycle": list(cyc), "count": n}
                for (frame, cyc), n in exact_target_hist.most_common()
            ],
            "d1_targets": [
                {"frame": frame, "cycle": list(cyc), "count": n}
                for (frame, cyc), n in d1_target_hist.most_common()
            ],
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
    print(f"has_4step_exact={has_4step_exact}")
    print(f"has_4step_d1={has_4step_d1}")
    print(f"to_frame2_d1={to_frame2_d1}")
    print("runtime_report:")
    print(f"  wall_seconds={wall:.3f}")
    print(f"  cpu_seconds={cpu:.3f}")
    if rss_mb is not None:
        print(f"  max_rss_mb={rss_mb:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
