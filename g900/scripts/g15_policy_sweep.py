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


POLICIES = [
    "distance_only",
    "distance_then_exact_then_family",
    "distance_then_family_then_exact",
    "family_then_distance_then_exact",
]


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
                    "edits": [{"position": pos, "from": original, "to": candidate}],
                }
            )
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


def policy_score(row: dict[str, Any], family: str, policy: str) -> tuple:
    metric = metric_key_for_family(family)
    d = row["distance_summary"].get(metric, 10**9)
    exact = 1 if row["classification"] == family and row["confidence"] == "exact" else 0
    fam = 1 if row["classification"] == family else 0

    if policy == "distance_only":
        return (d, row["label"])

    if policy == "distance_then_exact_then_family":
        return (d, -exact, -fam, row["label"])

    if policy == "distance_then_family_then_exact":
        return (d, -fam, -exact, row["label"])

    if policy == "family_then_distance_then_exact":
        return (-fam, d, -exact, row["label"])

    raise ValueError(f"unknown policy: {policy}")


def choose_best_child(current: dict[str, Any], family: str, vocab: list[str], r: int, policy: str) -> dict[str, Any] | None:
    metric = metric_key_for_family(family)
    current_distance = current["distance_summary"].get(metric)

    candidates = []
    for item in one_edit_variants(current["cycle"], vocab):
        row = classify_row(item["cycle"], r, item["label"], item["edits"])
        candidates.append((policy_score(row, family, policy), row))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0])
    best = candidates[0][1]
    best_distance = best["distance_summary"].get(metric)

    if current_distance is None or best_distance is None:
        return None
    if best_distance > current_distance:
        return None

    return best


def run_policy(start_cycle: list[str], family: str, vocab: list[str], r: int, policy: str, max_steps: int) -> dict[str, Any]:
    start = classify_row(start_cycle, r, label="start", edits=[])
    current = start
    path = [start]
    seen = {tuple(start_cycle)}

    if current["classification"] == family and current["confidence"] == "exact":
        return {
            "policy": policy,
            "start_cycle": start_cycle,
            "reached_exact_target": True,
            "steps_taken": 0,
            "end_classification": current["classification"],
            "end_confidence": current["confidence"],
            "end_distance": current["distance_summary"].get(metric_key_for_family(family)),
            "path": path,
        }

    for _ in range(max_steps):
        nxt = choose_best_child(current, family, vocab, r, policy)
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

    return {
        "policy": policy,
        "start_cycle": start_cycle,
        "reached_exact_target": current["classification"] == family and current["confidence"] == "exact",
        "steps_taken": len(path) - 1,
        "end_classification": current["classification"],
        "end_confidence": current["confidence"],
        "end_distance": current["distance_summary"].get(metric_key_for_family(family)),
        "path": path,
    }


def summarize_policy_runs(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    recovered = sum(1 for r in results if r["reached_exact_target"])
    avg_steps = (sum(r["steps_taken"] for r in results) / total) if total else 0.0
    return {
        "count": total,
        "recovered_count": recovered,
        "recovered_rate": (recovered / total) if total else 0.0,
        "avg_steps": avg_steps,
    }


def main() -> int:
    ap = argparse.ArgumentParser(prog="python3 scripts/g15_policy_sweep.py")
    ap.add_argument("--input", required=True, help="*_stalls.json file")
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--max-steps", type=int, default=10)
    ap.add_argument("--out")
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    family = data["target_family"]
    stalls = data.get("stalls", [])

    results_by_policy = {}

    for policy in POLICIES:
        policy_results = []
        for stall in stalls:
            start_cycle = stall["start_cycle"]
            vocab = default_vocab_for_cycle(start_cycle, args.r)
            policy_results.append(
                run_policy(
                    start_cycle=start_cycle,
                    family=family,
                    vocab=vocab,
                    r=args.r,
                    policy=policy,
                    max_steps=args.max_steps,
                )
            )
        results_by_policy[policy] = {
            "summary": summarize_policy_runs(policy_results),
            "results": policy_results,
        }

    out = {
        "source_file": args.input,
        "target_family": family,
        "stall_count": len(stalls),
        "policies": results_by_policy,
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
