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


def two_edit_variants(seed: list[str], vocab: list[str]) -> list[dict[str, Any]]:
    out = []
    seen_cycles = set()

    for i in range(len(seed)):
        for j in range(i + 1, len(seed)):
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


def scan_seed(seed: list[str], vocab: list[str], r: int, limit: int | None = None) -> dict[str, Any]:
    seed_result = classify_cycle(seed, r)
    variants = two_edit_variants(seed, vocab)
    if limit is not None:
        variants = variants[:limit]

    results = []
    for item in variants:
        c = classify_cycle(item["cycle"], r)
        results.append(
            {
                "label": item["label"],
                "edits": item["edits"],
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
        "scan_depth": 2,
        "vocab_size": len(vocab),
        "summary": summarize(results),
        "results": results,
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 scripts/g15_depth2_basin_scan.py")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--seed-cycle", help="comma-separated cycle entries")
    group.add_argument("--input", help="JSON input with a 'seed_cycle' field")
    p.add_argument("--r", type=int, default=1)
    p.add_argument("--vocab", help="comma-separated replacement vocabulary")
    p.add_argument("--limit", type=int, help="optional cap on number of variants")
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
        limit = payload.get("limit", args.limit)
    else:
        seed = parse_cycle(args.seed_cycle)
        vocab = parse_cycle(args.vocab) if args.vocab else None
        limit = args.limit

    if vocab is None:
        vocab = default_vocab_for_cycle(seed, args.r)
    else:
        vocab = unique_preserve_order(vocab)

    result = scan_seed(seed=seed, vocab=vocab, r=args.r, limit=limit)
    text = json.dumps(result, indent=2)

    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
