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
    for pos in range(len(seed)):
        original = seed[pos]
        for candidate in vocab:
            if candidate == original:
                continue
            mutated = seed.copy()
            mutated[pos] = candidate
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


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    classification_counts: dict[str, int] = {}
    confidence_counts: dict[str, int] = {}
    for row in rows:
        cls = row.get("classification", "unknown")
        conf = row.get("confidence", "unknown")
        classification_counts[cls] = classification_counts.get(cls, 0) + 1
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
    return {
        "count": len(rows),
        "classification_counts": classification_counts,
        "confidence_counts": confidence_counts,
    }


def scan_seed(seed: list[str], vocab: list[str], r: int) -> dict[str, Any]:
    seed_result = classify_cycle(seed, r)
    variants = one_edit_variants(seed, vocab)

    results = []
    for item in variants:
        c = classify_cycle(item["cycle"], r)
        results.append(
            {
                "label": item["label"],
                "edit": item["edit"],
                "cycle": item["cycle"],
                "classification": c["classification"],
                "confidence": c["confidence"],
                "distance_summary": c["distance_summary"],
                "normalized_cycle": c["normalized_cycle"],
            }
        )

    return {
        "seed_cycle": seed,
        "seed_classification": seed_result["classification"],
        "seed_confidence": seed_result["confidence"],
        "vocab_size": len(vocab),
        "summary": summarize(results),
        "results": results,
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 scripts/g15_local_basin_scan.py")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--seed-cycle", help="comma-separated cycle entries")
    group.add_argument("--input", help="JSON input with a 'seed_cycle' field")
    p.add_argument("--r", type=int, default=1)
    p.add_argument("--vocab", help="comma-separated replacement vocabulary")
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
    else:
        seed = parse_cycle(args.seed_cycle)
        vocab = parse_cycle(args.vocab) if args.vocab else None

    if vocab is None:
        vocab = default_vocab_for_cycle(seed, args.r)
    else:
        vocab = unique_preserve_order(vocab)

    result = scan_seed(seed=seed, vocab=vocab, r=args.r)
    text = json.dumps(result, indent=2)

    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
