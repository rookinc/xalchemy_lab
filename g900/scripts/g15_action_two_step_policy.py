#!/usr/bin/env python3
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


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def unique_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


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


def sample_family_starts(seed: list[str], vocab: list[str], family: str, depth: int, sample_size: int, random_seed: int, r: int) -> list[dict[str, Any]]:
    rng = random.Random(random_seed)
    combos = []

    for positions in itertools.combinations(range(len(seed)), depth):
        repl_lists = []
        for pos in positions:
            repl_lists.append([x for x in vocab if x != seed[pos]])
        for repls in itertools.product(*repl_lists):
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

    out = []
    seen = set()
    for item in combos:
        key = tuple(item["cycle"])
        if key in seen:
            continue
        seen.add(key)
        row = classify_row(item["cycle"], r, item["label"], item["edits"])
        if row["classification"] == family:
            out.append(row)
        if len(out) >= sample_size:
            break
    return out


def best_action_distance(row: dict[str, Any]) -> int | None:
    return row["distance_summary"].get("best_action_distance")


def choose_best_child_two_step(current: dict[str, Any], vocab: list[str], r: int, top_first: int = 8, top_second: int = 8) -> dict[str, Any] | None:
    current_d = best_action_distance(current)
    first_candidates = []

    for item1 in one_edit_variants(current["cycle"], vocab):
        first = classify_row(item1["cycle"], r, item1["label"], item1["edits"])
        d1 = best_action_distance(first)
        if d1 is None:
            continue
        first_candidates.append((d1, first["label"], first))

    if not first_candidates:
        return None

    first_candidates.sort(key=lambda x: (x[0], x[1]))
    first_candidates = first_candidates[:top_first]

    scored = []
    for d1, _, first in first_candidates:
        if first["classification"] == "action-cell" and first["confidence"] == "exact":
            return first

        second_candidates = []
        for item2 in one_edit_variants(first["cycle"], vocab):
            second = classify_row(item2["cycle"], r, item2["label"], item2["edits"])
            d2 = best_action_distance(second)
            if d2 is None:
                continue
            second_candidates.append((d2, second["label"], second))
        second_candidates.sort(key=lambda x: (x[0], x[1]))
        second_candidates = second_candidates[:top_second]

        if second_candidates:
            best_second_d = second_candidates[0][0]
        else:
            best_second_d = 10**9

        scored.append((best_second_d, d1, first["label"], first))

    scored.sort(key=lambda x: (x[0], x[1], x[2]))
    chosen = scored[0][3]
    chosen_d = best_action_distance(chosen)

    if current_d is None or chosen_d is None:
        return None
    if chosen_d > current_d:
        return None
    return chosen


def walk_two_step(start: dict[str, Any], vocab: list[str], r: int, max_steps: int, top_first: int = 8, top_second: int = 8) -> dict[str, Any]:
    path = [start]
    seen = {tuple(start["cycle"])}
    current = start

    for _ in range(max_steps):
        nxt = choose_best_child_two_step(current, vocab, r, top_first=top_first, top_second=top_second)
        if nxt is None:
            break
        key = tuple(nxt["cycle"])
        if key in seen:
            break
        path.append(nxt)
        seen.add(key)
        current = nxt
        if current["classification"] == "action-cell" and current["confidence"] == "exact":
            break

    return {
        "start_label": start["label"],
        "start_cycle": start["cycle"],
        "start_distance": best_action_distance(start),
        "end_cycle": current["cycle"],
        "end_distance": best_action_distance(current),
        "end_classification": current["classification"],
        "end_confidence": current["confidence"],
        "steps_taken": len(path) - 1,
        "reached_exact_target": current["classification"] == "action-cell" and current["confidence"] == "exact",
        "path": path,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    exact = sum(1 for r in rows if r["reached_exact_target"])
    return {
        "count": total,
        "reached_exact_count": exact,
        "reached_exact_rate": (exact / total) if total else 0.0,
        "failed_count": total - exact,
        "failed_rate": ((total - exact) / total) if total else 0.0,
        "avg_steps": (sum(r["steps_taken"] for r in rows) / total) if total else 0.0,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--top-first", type=int, default=8)
    ap.add_argument("--top-second", type=int, default=8)
    args = ap.parse_args()

    payload = load_json(args.input)
    seed = payload["seed_cycle"]
    vocab = unique_preserve_order(payload["vocab"])
    depth = payload.get("sample_depth", 4)
    sample_size = payload.get("sample_size", 300)
    random_seed = payload.get("random_seed", 17)
    max_steps = payload.get("max_steps", 10)

    starts = sample_family_starts(
        seed=seed,
        vocab=vocab,
        family="action-cell",
        depth=depth,
        sample_size=sample_size,
        random_seed=random_seed,
        r=args.r,
    )

    starts = [
        s for s in starts
        if not (s["classification"] == "action-cell" and s["confidence"] == "exact")
    ]

    walks = [
        walk_two_step(
            start=s,
            vocab=vocab,
            r=args.r,
            max_steps=max_steps,
            top_first=args.top_first,
            top_second=args.top_second,
        )
        for s in starts
    ]

    out = {
        "seed_cycle": seed,
        "target_family": "action-cell",
        "sample_depth": depth,
        "family_start_count": len(starts),
        "policy": "two_step_lookahead",
        "top_first": args.top_first,
        "top_second": args.top_second,
        "summary": summarize(walks),
        "walks": walks,
        "failed_walks": [w for w in walks if not w["reached_exact_target"]],
        "failed_walk_count": sum(1 for w in walks if not w["reached_exact_target"]),
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    s = out["summary"]
    print(f"starts={out['family_start_count']}")
    print(f"exact={s['reached_exact_count']}/{s['count']}")
    print(f"rate={s['reached_exact_rate']:.6f}")
    print(f"failed={out['failed_walk_count']}")
    print(f"avg_steps={s['avg_steps']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
