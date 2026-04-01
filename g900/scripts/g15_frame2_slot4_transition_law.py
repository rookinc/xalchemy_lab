#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, defaultdict, deque
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


def is_frame2_d1(c: dict[str, Any]) -> bool:
    if not (c["classification"] == "action-cell" and c["distance_summary"]["best_action_distance"] == 1):
        return False
    return any(rec["frame"] == 2 for rec in c["nearest"]["action"])


def is_exact_frame2(c: dict[str, Any]) -> bool:
    if not (c["classification"] == "action-cell" and c["confidence"] == "exact"):
        return False
    return any(m["frame"] == 2 for m in c["action_matches"])


def slot4_value(cycle: list[str]) -> str:
    return normalize_cycle(cycle)[4]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--witnesses", default="artifacts/unresolved20_depth4_frame2_d1_hits.json")
    ap.add_argument("--vocab-input", default="artifacts/repair_radius_action_d4.json")
    ap.add_argument("--out", default="artifacts/frame2_slot4_transition_law.json")
    ap.add_argument("--max-depth", type=int, default=4)
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
            if key not in seen:
                seen.add(key)
                starts.append(hit["cycle"])

    transition_counter = Counter()
    slot4_visit_counter = Counter()
    exact_attempts = []
    off_corridor_t2_examples = []
    corridor_t2_examples = []

    visited = set()
    q = deque()

    for cyc in starts:
        key = tuple(normalize_cycle(cyc))
        q.append((cyc, 0, []))
        visited.add(key)

    while q:
        cyc, depth, path = q.popleft()
        c = classify_cycle(cyc, 1)
        norm = normalize_cycle(cyc)
        s4 = norm[4]
        slot4_visit_counter[s4] += 1

        if depth >= args.max_depth:
            continue

        for item in one_edit_variants(cyc, vocab):
            child = item["cycle"]
            child_norm = normalize_cycle(child)
            child_s4 = child_norm[4]
            cc = classify_cycle(child, 1)

            transition_counter[(s4, child_s4, cc["classification"], cc["confidence"], cc["distance_summary"]["best_action_distance"])] += 1

            if is_exact_frame2(cc):
                exact_attempts.append({
                    "from_cycle": norm,
                    "to_cycle": child_norm,
                    "from_slot4": s4,
                    "to_slot4": child_s4,
                    "label": item["label"],
                    "depth": depth + 1,
                    "path": path + [item["label"]],
                })

            if child_s4 == "t2":
                ex = {
                    "from_cycle": norm,
                    "to_cycle": child_norm,
                    "label": item["label"],
                    "depth": depth + 1,
                    "classification": cc["classification"],
                    "confidence": cc["confidence"],
                    "best_action_distance": cc["distance_summary"]["best_action_distance"],
                    "path": path + [item["label"]],
                }
                if is_frame2_d1(cc):
                    corridor_t2_examples.append(ex)
                else:
                    if len(off_corridor_t2_examples) < 20:
                        off_corridor_t2_examples.append(ex)

            # continue exploring only frame2 d1 corridor
            if is_frame2_d1(cc):
                key = tuple(child_norm)
                if key not in visited:
                    visited.add(key)
                    q.append((child, depth + 1, path + [item["label"]]))

    out = {
        "unique_frame2_witness_starts": [normalize_cycle(c) for c in starts],
        "summary": {
            "start_count": len(starts),
            "visited_corridor_state_count": len(visited),
            "slot4_visit_histogram": dict(slot4_visit_counter),
            "exact_frame2_one_edit_hits_found": len(exact_attempts),
            "corridor_t2_examples_found": len(corridor_t2_examples),
            "off_corridor_t2_examples_found": len(off_corridor_t2_examples),
            "top_transition_counts": [
                {
                    "from_slot4": a,
                    "to_slot4": b,
                    "classification": cl,
                    "confidence": conf,
                    "best_action_distance": d,
                    "count": n,
                }
                for (a, b, cl, conf, d), n in transition_counter.most_common(50)
            ],
        },
        "exact_attempts": exact_attempts[:20],
        "corridor_t2_examples": corridor_t2_examples[:20],
        "off_corridor_t2_examples": off_corridor_t2_examples[:20],
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    wall = time.perf_counter() - t0
    cpu = time.process_time() - cpu0
    rss_mb = None
    try:
        import resource
        rr = resource.getrusage(resource.RUSAGE_SELF)
        rss_mb = rr.ru_maxrss / (1024 * 1024)
    except Exception:
        pass

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
