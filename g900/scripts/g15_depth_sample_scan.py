#!/data/data/com.termux/files/usr/bin/python3
from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from witness_machine.core import classify_cycle


def unique_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def metric_key_for_family(family: str) -> str:
    return {
        "subjective-state": "best_subjective_distance",
        "objective-state": "best_objective_distance",
        "action-cell": "best_action_distance",
    }[family]


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
                "edits": [{"position": pos, "from": original, "to": candidate}],
            })
    return out


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
    improved = start_distance is not None and end_distance is not None and end_distance < start_distance

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


def sample_cycles_at_depth(seed: list[str], vocab: list[str], depth: int, sample_size: int, random_seed: int) -> list[dict[str, Any]]:
    rng = random.Random(random_seed)
    n = len(seed)
    combos = []

    for positions in itertools.combinations(range(n), depth):
        replacement_lists = []
        for pos in positions:
            replacement_lists.append([x for x in vocab if x != seed[pos]])
        for repls in itertools.product(*replacement_lists):
            mutated = seed.copy()
            edits = []
            for pos, repl in zip(positions, repls):
                edits.append({"position": pos, "from": seed[pos], "to": repl})
                mutated[pos] = repl
            combos.append({
                "label": "__".join([f"edit_pos{e['position']}_{e['from']}_to_{e['to']}" for e in edits]),
                "cycle": mutated,
                "edits": edits,
            })

    rng.shuffle(combos)
    seen = set()
    out = []
    for item in combos:
        key = tuple(item["cycle"])
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
        if len(out) >= sample_size:
            break
    return out


def average(xs: list[float]) -> float | None:
    if not xs:
        return None
    return sum(xs) / len(xs)


def summarize(walks: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(walks)
    reached = sum(1 for w in walks if w["reached_exact_target"])
    improved = sum(1 for w in walks if w["improved"])
    failed = sum(1 for w in walks if not w["reached_exact_target"])
    return {
        "count": total,
        "reached_exact_count": reached,
        "reached_exact_rate": (reached / total) if total else 0.0,
        "improved_count": improved,
        "improved_rate": (improved / total) if total else 0.0,
        "stalled_count": failed,
        "stalled_rate": (failed / total) if total else 0.0,
        "avg_start_distance": average([w["start_distance"] for w in walks if w["start_distance"] is not None]),
        "avg_end_distance": average([w["end_distance"] for w in walks if w["end_distance"] is not None]),
        "avg_steps_taken": average([w["steps_taken"] for w in walks]),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--out")
    args = ap.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    seed = payload["seed_cycle"]
    vocab = unique_preserve_order(payload["vocab"])
    family = payload["family"]
    depth = payload.get("sample_depth", 3)
    sample_size = payload.get("sample_size", 400)
    random_seed = payload.get("random_seed", 17)
    max_steps = payload.get("max_steps", 8)

    samples = sample_cycles_at_depth(seed, vocab, depth, sample_size, random_seed)
    starts = [classify_row(s["cycle"], args.r, s["label"], s["edits"]) for s in samples]
    family_starts = [s for s in starts if s["classification"] == family]

    walks = [greedy_walk(s, family, vocab, args.r, max_steps=max_steps) for s in family_starts]
    failed_walks = [w for w in walks if not w["reached_exact_target"]]

    out = {
        "seed_cycle": seed,
        "target_family": family,
        "sample_depth": depth,
        "sample_size_requested": sample_size,
        "sample_size_realized": len(samples),
        "family_start_count": len(family_starts),
        "vocab_size": len(vocab),
        "max_steps": max_steps,
        "summary": summarize(walks),
        "walks": walks[:50],
        "failed_walks": failed_walks,
        "failed_walk_count": len(failed_walks),
    }

    text = json.dumps(out, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
