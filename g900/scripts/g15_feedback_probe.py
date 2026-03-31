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


def classify_rows(cycles: list[dict[str, Any]], r: int) -> list[dict[str, Any]]:
    rows = []
    for item in cycles:
        c = classify_cycle(item["cycle"], r)
        rows.append(
            {
                "label": item["label"],
                "cycle": item["cycle"],
                "edit": item.get("edit"),
                "classification": c["classification"],
                "confidence": c["confidence"],
                "distance_summary": c["distance_summary"],
            }
        )
    return rows


def metric_key_for_family(family: str) -> str:
    mapping = {
        "subjective-state": "best_subjective_distance",
        "objective-state": "best_objective_distance",
        "action-cell": "best_action_distance",
    }
    if family not in mapping:
        raise ValueError(f"unsupported family: {family}")
    return mapping[family]


def summarize_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        cls = row["classification"]
        counts[cls] = counts.get(cls, 0) + 1
    return counts


def summarize_confidence(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        conf = row["confidence"]
        counts[conf] = counts.get(conf, 0) + 1
    return counts


def select_parents(rows: list[dict[str, Any]], family: str, confidence: str | None) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        if row["classification"] != family:
            continue
        if confidence is not None and row["confidence"] != confidence:
            continue
        out.append(row)
    return out


def second_generation_from_parents(
    parents: list[dict[str, Any]],
    vocab: list[str],
    r: int,
    per_parent_limit: int | None = None,
) -> list[dict[str, Any]]:
    out = []
    for parent in parents:
        variants = one_edit_variants(parent["cycle"], vocab)
        if per_parent_limit is not None:
            variants = variants[:per_parent_limit]
        for item in variants:
            c = classify_cycle(item["cycle"], r)
            out.append(
                {
                    "parent_label": parent["label"],
                    "parent_classification": parent["classification"],
                    "parent_confidence": parent["confidence"],
                    "parent_cycle": parent["cycle"],
                    "parent_distance_summary": parent["distance_summary"],
                    "child_label": item["label"],
                    "child_cycle": item["cycle"],
                    "child_edit": item["edit"],
                    "classification": c["classification"],
                    "confidence": c["confidence"],
                    "distance_summary": c["distance_summary"],
                }
            )
    return out


def average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def feedback_summary(
    seed: list[str],
    family: str,
    parent_confidence: str | None,
    vocab: list[str],
    r: int,
    per_parent_limit: int | None = None,
) -> dict[str, Any]:
    depth1_variants = one_edit_variants(seed, vocab)
    depth1_rows = classify_rows(depth1_variants, r)

    parents = select_parents(depth1_rows, family=family, confidence=parent_confidence)
    depth2_rows = second_generation_from_parents(
        parents=parents,
        vocab=vocab,
        r=r,
        per_parent_limit=per_parent_limit,
    )

    family_metric = metric_key_for_family(family)

    delta_family_distances: list[float] = []
    for row in depth2_rows:
        p = row["parent_distance_summary"].get(family_metric)
        c = row["distance_summary"].get(family_metric)
        if p is not None and c is not None:
            delta_family_distances.append(c - p)

    counts2 = summarize_counts(depth2_rows)
    conf2 = summarize_confidence(depth2_rows)

    total2 = len(depth2_rows)
    retention = 0.0 if total2 == 0 else counts2.get(family, 0) / total2
    objective_rate = 0.0 if total2 == 0 else counts2.get("objective-state", 0) / total2
    subjective_rate = 0.0 if total2 == 0 else counts2.get("subjective-state", 0) / total2
    action_rate = 0.0 if total2 == 0 else counts2.get("action-cell", 0) / total2
    unresolved_rate = 0.0 if total2 == 0 else counts2.get("unresolved", 0) / total2

    return {
        "seed_cycle": seed,
        "target_family": family,
        "parent_confidence_filter": parent_confidence,
        "vocab_size": len(vocab),
        "depth1_total": len(depth1_rows),
        "depth1_parent_count": len(parents),
        "depth2_total": total2,
        "depth2_classification_counts": counts2,
        "depth2_confidence_counts": conf2,
        "conditional_rates": {
            "retention_rate": retention,
            "subjective_rate": subjective_rate,
            "objective_rate": objective_rate,
            "action_rate": action_rate,
            "unresolved_rate": unresolved_rate,
        },
        "distance_feedback": {
            "family_metric": family_metric,
            "avg_child_minus_parent": average(delta_family_distances),
            "sample_count": len(delta_family_distances),
        },
        "parent_examples": parents[:10],
        "child_examples": depth2_rows[:25],
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 scripts/g15_feedback_probe.py")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--seed-cycle", help="comma-separated cycle entries")
    group.add_argument("--input", help="JSON input with seed_cycle")
    p.add_argument("--family", choices=["subjective-state", "objective-state", "action-cell"])
    p.add_argument("--parent-confidence", choices=["exact", "nearest", "ambiguous"])
    p.add_argument("--r", type=int, default=1)
    p.add_argument("--vocab", help="comma-separated replacement vocabulary")
    p.add_argument("--per-parent-limit", type=int)
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
        per_parent_limit = payload.get("per_parent_limit", args.per_parent_limit)
    else:
        seed = parse_cycle(args.seed_cycle)
        vocab = parse_cycle(args.vocab) if args.vocab else None
        family = args.family
        parent_confidence = args.parent_confidence
        per_parent_limit = args.per_parent_limit

    if family is None:
        raise SystemExit("family is required either via --family or inside the input JSON")

    if vocab is None:
        vocab = default_vocab_for_cycle(seed, args.r)
    else:
        vocab = unique_preserve_order(vocab)

    result = feedback_summary(
        seed=seed,
        family=family,
        parent_confidence=parent_confidence,
        vocab=vocab,
        r=args.r,
        per_parent_limit=per_parent_limit,
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
