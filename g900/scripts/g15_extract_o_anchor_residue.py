#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
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
            out.append(
                {
                    "label": f"edit_pos{pos}_{original}_to_{candidate}",
                    "cycle": mutated,
                    "position": pos,
                    "from_raw": original,
                    "to_raw": candidate,
                }
            )
    return out


def is_exact_frame2(c: dict[str, Any]) -> bool:
    return (
        c["classification"] == "action-cell"
        and c["confidence"] == "exact"
        and any(m["frame"] == 2 for m in c["action_matches"])
    )


def keep_child(c: dict[str, Any], max_action_distance: int) -> bool:
    d = c["distance_summary"]["best_action_distance"]
    return is_exact_frame2(c) or (d is not None and d <= max_action_distance)


def o_symbols(cycle: list[str]) -> list[str]:
    return [x for x in cycle if x.startswith("o")]


def o_anchor_index(cycle: list[str]) -> int | None:
    osyms = o_symbols(cycle)
    if len(osyms) != 1:
        return None
    return int(osyms[0][1:])


def slot4_value(cycle: list[str]) -> str:
    return normalize_cycle(cycle)[4]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--locked-input", default="artifacts/frame2_witness_reconciliation.json")
    ap.add_argument("--vocab-input", default="artifacts/repair_radius_action_d4.json")
    ap.add_argument("--max-action-distance", type=int, default=3)
    ap.add_argument("--out", default="artifacts/frame2_o_anchor_residue.json")
    args = ap.parse_args()

    locked_data = load_json(args.locked_input)
    vocab_payload = load_json(args.vocab_input)
    vocab = unique_preserve_order(vocab_payload["vocab"])

    starts = [row["start_cycle"] for row in locked_data["results"]]

    retained_rows = []
    o_anchor_hist = Counter()
    o_symbol_hist = Counter()
    slot4_by_o_anchor = defaultdict(Counter)
    bad_rows = []

    for start_idx, start_cycle in enumerate(starts):
        for item in one_edit_variants(start_cycle, vocab):
            child = item["cycle"]
            cc = classify_cycle(child, 1)

            if not keep_child(cc, args.max_action_distance):
                continue

            norm = cc["normalized_cycle"]
            osyms = o_symbols(norm)
            anchor = o_anchor_index(norm)
            s4 = norm[4]

            row = {
                "start_index": start_idx,
                "edit_label": item["label"],
                "position": item["position"],
                "from_raw": item["from_raw"],
                "to_raw": item["to_raw"],
                "normalized_cycle": norm,
                "o_symbols": osyms,
                "o_anchor_index": anchor,
                "slot4": s4,
                "classification": cc["classification"],
                "confidence": cc["confidence"],
                "best_action_distance": cc["distance_summary"]["best_action_distance"],
            }
            retained_rows.append(row)

            for o in osyms:
                o_symbol_hist[o] += 1

            if anchor is None:
                bad_rows.append(row)
            else:
                o_anchor_hist[anchor] += 1
                slot4_by_o_anchor[anchor][s4] += 1

    out = {
        "summary": {
            "retained_row_count": len(retained_rows),
            "o_anchor_histogram": dict(sorted(o_anchor_hist.items())),
            "o_symbol_histogram": dict(sorted(o_symbol_hist.items())),
            "slot4_by_o_anchor": {
                str(k): dict(sorted(v.items()))
                for k, v in sorted(slot4_by_o_anchor.items())
            },
            "non_unique_o_rows": len(bad_rows),
        },
        "non_unique_o_examples": bad_rows[:20],
        "rows": retained_rows,
    }

    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    print(json.dumps(out["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
