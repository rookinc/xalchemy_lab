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
                    "edit": {
                        "position": pos,
                        "from": original,
                        "to": candidate,
                    },
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


def classify_row(cycle: list[str], r: int, label: str = "state", edit: dict[str, Any] | None = None) -> dict[str, Any]:
    c = classify_cycle(cycle, r)
    return {
        "label": label,
        "cycle": cycle,
        "edit": edit,
        "classification": c["classification"],
        "confidence": c["confidence"],
        "distance_summary": c["distance_summary"],
    }


def select_parents(seed: list[str], family: str, parent_confidence: str | None, vocab: list[str], r: int) -> list[dict[str, Any]]:
    rows = []
    for item in one_edit_variants(seed, vocab):
        row = classify_row(item["cycle"], r, label=item["label"], edit=item["edit"])
        if row["classification"] != family:
            continue
        if parent_confidence is not None and row["confidence"] != parent_confidence:
            continue
        rows.append(row)
    return rows


def choose_best_child(current: dict[str, Any], family: str, vocab: list[str], r: int) -> dict[str, Any] | None:
    metric = metric_key_for_family(family)
    current_distance = current["distance_summary"].get(metric)
    current_cycle = tuple(current["cycle"])

    candidates = []
    for item in one_edit_variants(current["cycle"], vocab):
        if tuple(item["cycle"]) == current_cycle:
            continue
        row = classify_row(item["cycle"], r, label=item["label"], edit=item["edit"])
        child_distance = row["distance_summary"].get(metric)

        exact_bonus = 1 if row["classification"] == family and row["confidence"] == "exact" else 0
        family_bonus = 1 if row["classification"] == family else 0

        candidates.append(
            (
                child_distance if child_distance is not None else 10**9,
                -exact_bonus,
                -family_bonus,
                row["confidence"] != "exact",
                row["label"],
                row,
            )
        )

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[:5])
    best = candidates[0][-1]

    best_distance = best["distance_summary"].get(metric)
    if current_distance is None or best_distance is None:
        return None

    if best_distance > current_distance:
        return None

    if best_distance == current_distance and tuple(best["cycle"]) == current_cycle:
        return None

    return best


def greedy_walk_from_parent(
    parent: dict[str, Any],
    family: str,
    vocab: list[str],
    r: int,
    max_steps: int,
) -> dict[str, Any]:
    metric = metric_key_for_family(family)

    path = [parent]
    seen = {tuple(parent["cycle"])}
    current = parent

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

    start_distance = parent["distance_summary"].get(metric)
    end_distance = current["distance_summary"].get(metric)

    return {
        "parent_label": parent["label"],
        "start_cycle": parent["cycle"],
        "start_classification": parent["classification"],
        "start_confidence": parent["confidence"],
        "start_distance": start_distance,
        "end_cycle": current["cycle"],
        "end_classification": current["classification"],
        "end_confidence": current["confidence"],
        "end_distance": end_distance,
        "steps_taken": max(0, len(path) - 1),
        "reached_exact_target": current["classification"] == family and current["confidence"] == "exact",
        "improved": (end_distance is not None and start_distance is not None and end_distance < start_distance),
        "path": path,
    }


def summarize_walks(walks: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(walks)
    if total == 0:
        return {
            "count": 0,
            "reached_exact_count": 0,
            "improved_count": 0,
            "stalled_count": 0,
            "avg_start_distance": None,
            "avg_end_distance": None,
            "avg_steps_taken": None,
        }

    start_distances = [w["start_distance"] for w in walks if w["start_distance"] is not None]
    end_distances = [w["end_distance"] for w in walks if w["end_distance"] is not None]
    steps = [w["steps_taken"] for w in walks]

    reached_exact_count = sum(1 for w in walks if w["reached_exact_target"])
    improved_count = sum(1 for w in walks if w["improved"])
    stalled_count = total - improved_count

    def avg(xs: list[float]) -> float | None:
        if not xs:
            return None
        return sum(xs) / len(xs)

    return {
        "count": total,
        "reached_exact_count": reached_exact_count,
        "reached_exact_rate": reached_exact_count / total,
        "improved_count": improved_count,
        "improved_rate": improved_count / total,
        "stalled_count": stalled_count,
        "stalled_rate": stalled_count / total,
        "avg_start_distance": avg(start_distances),
        "avg_end_distance": avg(end_distances),
        "avg_steps_taken": avg(steps),
    }


def greedy_feedback_summary(
    seed: list[str],
    family: str,
    parent_confidence: str | None,
    vocab: list[str],
    r: int,
    max_steps: int,
    parent_limit: int | None = None,
) -> dict[str, Any]:
    parents = select_parents(seed, family, parent_confidence, vocab, r)
    if parent_limit is not None:
        parents = parents[:parent_limit]

    walks = [
        greedy_walk_from_parent(parent, family, vocab, r, max_steps=max_steps)
        for parent in parents
    ]

    return {
        "seed_cycle": seed,
        "target_family": family,
        "parent_confidence_filter": parent_confidence,
        "vocab_size": len(vocab),
        "parent_count": len(parents),
        "max_steps": max_steps,
        "summary": summarize_walks(walks),
        "walks": walks[:50],
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 scripts/g15_greedy_feedback_probe.py")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--seed-cycle", help="comma-separated cycle entries")
    group.add_argument("--input", help="JSON input with seed_cycle")
    p.add_argument("--family", choices=["subjective-state", "objective-state", "action-cell"])
    p.add_argument("--parent-confidence", choices=["exact", "nearest", "ambiguous"])
    p.add_argument("--r", type=int, default=1)
    p.add_argument("--vocab", help="comma-separated replacement vocabulary")
    p.add_argument("--max-steps", type=int, default=6)
    p.add_argument("--parent-limit", type=int)
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
        parent_confidence = payload.get("parent_confidence", args.parent_confidence)
        max_steps = payload.get("max_steps", args.max_steps)
        parent_limit = payload.get("parent_limit", args.parent_limit)
    else:
        seed = parse_cycle(args.seed_cycle)
        vocab = parse_cycle(args.vocab) if args.vocab else None
        family = args.family
        parent_confidence = args.parent_confidence
        max_steps = args.max_steps
        parent_limit = args.parent_limit

    if family is None:
        raise SystemExit("family is required either via --family or inside the input JSON")

    if vocab is None:
        vocab = default_vocab_for_cycle(seed, args.r)
    else:
        vocab = unique_preserve_order(vocab)

    result = greedy_feedback_summary(
        seed=seed,
        family=family,
        parent_confidence=parent_confidence,
        vocab=vocab,
        r=args.r,
        max_steps=max_steps,
        parent_limit=parent_limit,
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
