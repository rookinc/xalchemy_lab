#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
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
            out.append(
                {
                    "label": f"edit_pos{pos}_{original}_to_{candidate}",
                    "cycle": mutated,
                    "edits": [{"position": pos, "from": original, "to": candidate}],
                }
            )
    return out


def classify_cached(
    cycle: list[str],
    cache: dict[tuple[str, ...], dict[str, Any]],
    r: int,
) -> dict[str, Any]:
    key = tuple(normalize_cycle(cycle))
    if key not in cache:
        cache[key] = classify_cycle(cycle, r)
    return cache[key]


def find_hard_d2_states(
    exact_pref_path: str,
    input_path: str,
    r: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    data = load_json(exact_pref_path)
    payload = load_json(input_path)
    vocab = unique_preserve_order(payload["vocab"])

    fails = [w for w in data["walks"] if not w["reached_exact_target"]]
    d2 = [w for w in fails if w["end_distance"] == 2]

    hard: list[dict[str, Any]] = []
    cache: dict[tuple[str, ...], dict[str, Any]] = {}

    for w in d2:
        start = w["end_cycle"]
        found = False
        for item1 in one_edit_variants(start, vocab):
            c1 = classify_cached(item1["cycle"], cache, r)
            if c1["classification"] == "action-cell" and (
                c1["confidence"] == "exact"
                or c1["distance_summary"]["best_action_distance"] == 1
            ):
                found = True
                break

            for item2 in one_edit_variants(item1["cycle"], vocab):
                c2 = classify_cached(item2["cycle"], cache, r)
                if c2["classification"] == "action-cell" and (
                    c2["confidence"] == "exact"
                    or c2["distance_summary"]["best_action_distance"] == 1
                ):
                    found = True
                    break
            if found:
                break

        if not found:
            hard.append(w)

    return hard, vocab


def probe_one_start(
    start_cycle: list[str],
    vocab: list[str],
    r: int,
    max_examples: int = 5,
) -> dict[str, Any]:
    cache: dict[tuple[str, ...], dict[str, Any]] = {}

    found_exact: dict[tuple[str, ...], dict[str, Any]] = {}
    found_d1: dict[tuple[str, ...], dict[str, Any]] = {}

    # Coarse-grained DFS with local cache.
    for item1 in one_edit_variants(start_cycle, vocab):
        cyc1 = item1["cycle"]

        for item2 in one_edit_variants(cyc1, vocab):
            cyc2 = item2["cycle"]

            for item3 in one_edit_variants(cyc2, vocab):
                cyc3 = item3["cycle"]
                c3 = classify_cached(cyc3, cache, r)

                if c3["classification"] == "action-cell" and c3["confidence"] == "exact":
                    found_exact[tuple(cyc3)] = {
                        "labels": (item1["label"], item2["label"], item3["label"]),
                        "cycle": cyc3,
                        "classification": c3["classification"],
                        "confidence": c3["confidence"],
                        "distance_summary": c3["distance_summary"],
                        "action_matches": c3["action_matches"],
                        "nearest_action": c3["nearest"]["action"],
                    }
                elif (
                    c3["classification"] == "action-cell"
                    and c3["distance_summary"]["best_action_distance"] == 1
                ):
                    found_d1[tuple(cyc3)] = {
                        "labels": (item1["label"], item2["label"], item3["label"]),
                        "cycle": cyc3,
                        "classification": c3["classification"],
                        "confidence": c3["confidence"],
                        "distance_summary": c3["distance_summary"],
                        "action_matches": c3["action_matches"],
                        "nearest_action": c3["nearest"]["action"],
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
    ap.add_argument(
        "--input",
        default="artifacts/repair_radius_action_d4.json",
        help="Input payload used for vocab.",
    )
    ap.add_argument(
        "--exact-pref",
        default="artifacts/repair_radius_action_d4_result_two_step_lookahead_exact_pref.json",
        help="Patched exact-preference result JSON.",
    )
    ap.add_argument(
        "--out",
        default="artifacts/hard_d2_depth3_parallel_probe.json",
        help="Output JSON path.",
    )
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument(
        "--max-workers",
        type=int,
        default=max(1, min(8, (os.cpu_count() or 4) - 1)),
    )
    args = ap.parse_args()

    hard, vocab = find_hard_d2_states(args.exact_pref, args.input, args.r)
    print(f"hard d2 states: {len(hard)}")
    print(f"max_workers: {args.max_workers}")

    results: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=args.max_workers) as ex:
        futures = [
            ex.submit(probe_one_start, w["end_cycle"], vocab, args.r)
            for w in hard
        ]
        for i, fut in enumerate(as_completed(futures), start=1):
            res = fut.result()
            results.append(res)
            if i % 5 == 0 or i == len(futures):
                print(f"completed {i}/{len(futures)}")

    has_3step_exact = sum(1 for r in results if r["has_exact"])
    has_3step_d1 = sum(1 for r in results if r["has_d1"])
    to_frame2_d1 = sum(1 for r in results if r["has_frame2_d1"])

    hist = Counter((r["found_d1_count"], r["found_exact_count"]) for r in results)
    exact_target_hist = Counter()
    d1_target_hist = Counter()

    for r in results:
        for rec in r["exact_targets"]:
            exact_target_hist[(rec["frame"], tuple(rec["cycle"]))] += rec["count"]
        for rec in r["d1_targets"]:
            d1_target_hist[(rec["frame"], tuple(rec["cycle"]))] += rec["count"]

    out = {
        "hard_d2_count": len(hard),
        "max_workers": args.max_workers,
        "summary": {
            "has_3step_exact": has_3step_exact,
            "has_3step_d1": has_3step_d1,
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
        "results": results,
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"has_3step_exact={has_3step_exact}")
    print(f"has_3step_d1={has_3step_d1}")
    print(f"to_frame2_d1={to_frame2_d1}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
