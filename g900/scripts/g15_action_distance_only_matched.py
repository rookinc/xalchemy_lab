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


def choose_best_child(current: dict[str, Any], vocab: list[str], r: int) -> dict[str, Any] | None:
    current_distance = current["distance_summary"].get("best_action_distance")
    candidates = []

    for item in one_edit_variants(current["cycle"], vocab):
        row = classify_row(item["cycle"], r, item["label"], item["edits"])
        d = row["distance_summary"].get("best_action_distance", 10**9)
        candidates.append((d, row["label"], row))

    if not candidates:
        return None

    candidates.sort(key=lambda x: (x[0], x[1]))
    best = candidates[0][2]
    best_d = best["distance_summary"].get("best_action_distance")

    if current_distance is None or best_d is None:
        return None
    if best_d > current_distance:
        return None
    return best


def walk(start: dict[str, Any], vocab: list[str], r: int, max_steps: int) -> dict[str, Any]:
    path = [start]
    seen = {tuple(start["cycle"])}
    current = start

    for _ in range(max_steps):
        nxt = choose_best_child(current, vocab, r)
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
        "start_distance": start["distance_summary"].get("best_action_distance"),
        "end_cycle": current["cycle"],
        "end_distance": current["distance_summary"].get("best_action_distance"),
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

    walks = [walk(start=s, vocab=vocab, r=args.r, max_steps=max_steps) for s in starts]

    out = {
        "seed_cycle": seed,
        "target_family": "action-cell",
        "sample_depth": depth,
        "family_start_count": len(starts),
        "policy": "distance_only_matched",
        "summary": summarize(walks),
        "walks": walks[:50],
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
