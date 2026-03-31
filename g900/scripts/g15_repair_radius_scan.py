#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from witness_machine.core import classify_cycle


def parse_cycle(text: str) -> list[str]:
    parts = [x.strip() for x in text.split(",") if x.strip()]
    if len(parts) < 3:
        raise ValueError("cycle must have at least 3 entries")
    return parts


def unique_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def default_vocab_for_cycle(cycle: list[str], r: int) -> list[str]:
    n = 5 * r
    vocab = []
    for i in range(n):
        vocab.extend([f"o{i}", f"s{i}", f"t{i}"])
    vocab.extend(cycle)
    return unique_preserve_order(vocab)


def one_edit_variants(seed: list[str], vocab: list[str]) -> list[dict[str, Any]]:
    out = []
    seen_cycles = set()
    for pos in range(len(seed)):
        original = seed[pos]
        for candidate in vocab:
            if candidate == original:
                continue
            mutated = seed.copy()
            mutated[pos] = candidate
            key = tuple(mutated)
            if key in seen_cycles:
                continue
            seen_cycles.add(key)
            out.append(
                {
                    "label": f"edit_pos{pos}_{original}_to_{candidate}",
                    "cycle": mutated,
                    "edits": [
                        {"position": pos, "from": original, "to": candidate},
                    ],
                }
            )
    return out


def depth2_variants(seed: list[str], vocab: list[str]) -> list[dict[str, Any]]:
    out = []
    seen_cycles = set()
    n = len(seed)
    for i in range(n):
        for j in range(i + 1, n):
            orig_i = seed[i]
            orig_j = seed[j]
            for repl_i in vocab:
                if repl_i == orig_i:
                    continue
                for repl_j in vocab:
                    if repl_j == orig_j:
                        continue
                    mutated = seed.copy()
                    mutated[i] = repl_i
                    mutated[j] = repl_j
                    key = tuple(mutated)
                    if key in seen_cycles:
                        continue
                    seen_cycles.add(key)
                    out.append(
                        {
                            "label": f"edit_pos{i}_{orig_i}_to_{repl_i}__pos{j}_{orig_j}_to_{repl_j}",
                            "cycle": mutated,
                            "edits": [
                                {"position": i, "from": orig_i, "to": repl_i},
                                {"position": j, "from": orig_j, "to": repl_j},
                            ],
                        }
                    )
    return out


def metric_key_for_family(family: str) -> str:
    mapping = {
        "subjective-state": "best_subjective_distance",
        "objective-state": "best_objective_distance",
        "action-cell": "best_action_distance",
    }
    if family not in mapping:
        raise ValueError(f"unsupported family: {family}")
    return mapping[family]


def classify_row(cycle: list[str], r: int, label: str, edits: list[dict[str, Any]]) -> dict[str, Any]:
    c = classify_cycle(cycle, r)
    return {
        "label": label,
        "cycle": cycle,
        "edits": edits,
        "classification": c["classification"],
        "confidence": c["confidence"],
        "distance_summary": c["distance_summary"],
    }


def choose_best_child(current: dict[str, Any], family: str, vocab: list[str], r: int) -> dict[str, Any] | None:
    metric = metric_key_for_family(family)
    current_distance = current["distance_summary"].get(metric)

    candidates = []
    for item in one_edit_variants(current["cycle"], vocab):
        row = classify_row(item["cycle"], r, item["label"], item["edits"])
        d = row["distance_summary"].get(metric, 10**9)
        candidates.append((d, row["label"], row))

    if not candidates:
        return None

    candidates.sort(key=lambda x: (x[0], x[1]))
    best = candidates[0][2]
    best_distance = best["distance_summary"].get(metric)

    if current_distance is None or best_distance is None:
        return None
    if best_distance > current_distance:
        return None

    return best


def greedy_walk(start: dict[str, Any], family: str, vocab: list[str], r: int, max_steps: int) -> dict[str, Any]:
    metric = metric_key_for_family(family)

    path = [start]
    seen = {tuple(start["cycle"])}
    current = start

    for _ in range(max_steps):
        nxt = choose_best_child(current, family, vocab, r)
        if nxt is None:
            break
        key = tuple(nxt["cycle"])
        if key in seen:
            break
        path.append(nxt)
        seen.add(key)
        current = nxt
        if current["classification"] == family and current["confidence"] == "exact":
            break

    start_distance = start["distance_summary"].get(metric)
    end_distance = current["distance_summary"].get(metric)
    reached_exact_target = current["classification"] == family and current["confidence"] == "exact"
    improved = (
        start_distance is not None and end_distance is not None and end_distance < start_distance
    )

    return {
        "start_label": start["label"],
        "start_cycle": start["cycle"],
        "start_classification": start["classification"],
        "start_confidence": start["confidence"],
        "start_distance": start_distance,
        "end_cycle": current["cycle"],
        "end_classification": current["classification"],
        "end_confidence": current["confidence"],
        "end_distance": end_distance,
        "steps_taken": max(0, len(path) - 1),
        "reached_exact_target": reached_exact_target,
        "improved": improved,
        "path": path,
    }


def generate_candidates(seed: list[str], vocab: list[str], depth: int) -> list[dict[str, Any]]:
    if depth == 1:
        return one_edit_variants(seed, vocab)
    if depth == 2:
        return depth2_variants(seed, vocab)
    raise ValueError("depth must be 1 or 2")


def filter_start_states(
    rows: list[dict[str, Any]],
    family: str,
    confidence: str | None,
    max_start_distance: int | None,
) -> list[dict[str, Any]]:
    metric = metric_key_for_family(family)
    out = []
    for row in rows:
        if row["classification"] != family:
            continue
        if confidence is not None and row["confidence"] != confidence:
            continue
        if max_start_distance is not None:
            d = row["distance_summary"].get(metric)
            if d is None or d > max_start_distance:
                continue
        out.append(row)
    return out


def average(xs: list[float]) -> float | None:
    if not xs:
        return None
    return sum(xs) / len(xs)


def summarize_walks(walks: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(walks)
    if total == 0:
        return {
            "count": 0,
            "reached_exact_count": 0,
            "reached_exact_rate": 0.0,
            "improved_count": 0,
            "improved_rate": 0.0,
            "stalled_count": 0,
            "stalled_rate": 0.0,
            "avg_start_distance": None,
            "avg_end_distance": None,
            "avg_steps_taken": None,
        }

    reached_exact_count = sum(1 for w in walks if w["reached_exact_target"])
    improved_count = sum(1 for w in walks if w["improved"])
    stalled_count = sum(1 for w in walks if not w["reached_exact_target"])

    start_distances = [w["start_distance"] for w in walks if w["start_distance"] is not None]
    end_distances = [w["end_distance"] for w in walks if w["end_distance"] is not None]
    steps = [w["steps_taken"] for w in walks]

    return {
        "count": total,
        "reached_exact_count": reached_exact_count,
        "reached_exact_rate": reached_exact_count / total,
        "improved_count": improved_count,
        "improved_rate": improved_count / total,
        "stalled_count": stalled_count,
        "stalled_rate": stalled_count / total,
        "avg_start_distance": average(start_distances),
        "avg_end_distance": average(end_distances),
        "avg_steps_taken": average(steps),
    }


def radius_scan(
    seed: list[str],
    family: str,
    vocab: list[str],
    r: int,
    start_depth: int,
    start_confidence: str | None,
    max_start_distance: int | None,
    max_steps: int,
    candidate_limit: int | None,
    walk_sample_limit: int = 50,
) -> dict[str, Any]:
    candidates = generate_candidates(seed, vocab, start_depth)
    rows = [
        classify_row(item["cycle"], r, item["label"], item["edits"])
        for item in candidates
    ]
    starts = filter_start_states(rows, family, start_confidence, max_start_distance)

    if candidate_limit is not None:
        starts = starts[:candidate_limit]

    walks = [
        greedy_walk(start, family, vocab, r, max_steps=max_steps)
        for start in starts
    ]

    failed_walks = [w for w in walks if not w["reached_exact_target"]]

    return {
        "seed_cycle": seed,
        "target_family": family,
        "start_depth": start_depth,
        "start_confidence_filter": start_confidence,
        "max_start_distance": max_start_distance,
        "vocab_size": len(vocab),
        "candidate_count": len(candidates),
        "start_count": len(starts),
        "max_steps": max_steps,
        "summary": summarize_walks(walks),
        "walk_sample_limit": walk_sample_limit,
        "walks": walks[:walk_sample_limit],
        "failed_walks": failed_walks,
        "failed_walk_count": len(failed_walks),
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 scripts/g15_repair_radius_scan.py")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--seed-cycle", help="comma-separated cycle entries")
    group.add_argument("--input", help="JSON input with seed_cycle")
    p.add_argument("--family", choices=["subjective-state", "objective-state", "action-cell"])
    p.add_argument("--r", type=int, default=1)
    p.add_argument("--vocab", help="comma-separated replacement vocabulary")
    p.add_argument("--start-depth", type=int, choices=[1, 2], default=2)
    p.add_argument("--start-confidence", choices=["exact", "nearest", "ambiguous"])
    p.add_argument("--max-start-distance", type=int)
    p.add_argument("--max-steps", type=int, default=6)
    p.add_argument("--candidate-limit", type=int)
    p.add_argument("--walk-sample-limit", type=int, default=50)
    p.add_argument("--out")
    return p


def main() -> int:
    args = build_parser().parse_args()

    if args.input:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        seed = payload.get("seed_cycle")
        if not seed:
            raise SystemExit("input JSON must contain 'seed_cycle'")
        vocab = payload.get("vocab")
        family = payload.get("family", args.family)
        start_depth = payload.get("start_depth", args.start_depth)
        start_confidence = payload.get("start_confidence", args.start_confidence)
        max_start_distance = payload.get("max_start_distance", args.max_start_distance)
        max_steps = payload.get("max_steps", args.max_steps)
        candidate_limit = payload.get("candidate_limit", args.candidate_limit)
        walk_sample_limit = payload.get("walk_sample_limit", args.walk_sample_limit)
    else:
        seed = parse_cycle(args.seed_cycle)
        vocab = parse_cycle(args.vocab) if args.vocab else None
        family = args.family
        start_depth = args.start_depth
        start_confidence = args.start_confidence
        max_start_distance = args.max_start_distance
        max_steps = args.max_steps
        candidate_limit = args.candidate_limit
        walk_sample_limit = args.walk_sample_limit

    if family is None:
        raise SystemExit("family is required either via --family or inside the input JSON")

    if vocab is None:
        vocab = default_vocab_for_cycle(seed, args.r)
    else:
        vocab = unique_preserve_order(vocab)

    result = radius_scan(
        seed=seed,
        family=family,
        vocab=vocab,
        r=args.r,
        start_depth=start_depth,
        start_confidence=start_confidence,
        max_start_distance=max_start_distance,
        max_steps=max_steps,
        candidate_limit=candidate_limit,
        walk_sample_limit=walk_sample_limit,
    )
    text = json.dumps(result, indent=2)

    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
