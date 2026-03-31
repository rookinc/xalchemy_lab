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
    mapping = {
        "subjective-state": "best_subjective_distance",
        "objective-state": "best_objective_distance",
        "action-cell": "best_action_distance",
    }
    return mapping[family]


def classify_row(cycle: list[str], r: int, label: str = "state", edits: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    c = classify_cycle(cycle, r)
    return {
        "label": label,
        "cycle": cycle,
        "edits": edits or [],
        "classification": c["classification"],
        "confidence": c["confidence"],
        "distance_summary": c["distance_summary"],
    }


def score_row(row: dict[str, Any], family: str) -> tuple:
    metric = metric_key_for_family(family)
    d = row["distance_summary"].get(metric, 10**9)
    exact_bonus = 1 if row["classification"] == family and row["confidence"] == "exact" else 0
    family_bonus = 1 if row["classification"] == family else 0
    return (
        d,
        -exact_bonus,
        -family_bonus,
        row["confidence"] != "exact",
        row["label"],
    )


def node_snapshot(node: dict[str, Any]) -> dict[str, Any]:
    return {
        "label": node["label"],
        "cycle": node["cycle"],
        "edits": node.get("edits", []),
        "classification": node["classification"],
        "confidence": node["confidence"],
        "distance_summary": node["distance_summary"],
    }


def result_snapshot(start: dict[str, Any], terminal: dict[str, Any], family: str, beam_width: int, max_steps: int, reached_exact: bool, steps_taken: int) -> dict[str, Any]:
    return {
        "start_cycle": start["cycle"],
        "start_classification": start["classification"],
        "start_confidence": start["confidence"],
        "start_distance": start["distance_summary"].get(metric_key_for_family(family)),
        "reached_exact_target": reached_exact,
        "steps_taken": steps_taken,
        "best_terminal": node_snapshot(terminal),
        "path": [node_snapshot(n) for n in terminal.get("path", [terminal])],
        "beam_width": beam_width,
        "max_steps": max_steps,
    }


def beam_repair(start_cycle: list[str], family: str, vocab: list[str], r: int, beam_width: int, max_steps: int) -> dict[str, Any]:
    start = classify_row(start_cycle, r, label="start")
    start["path"] = [start]

    if start["classification"] == family and start["confidence"] == "exact":
        return result_snapshot(
            start=start,
            terminal=start,
            family=family,
            beam_width=beam_width,
            max_steps=max_steps,
            reached_exact=True,
            steps_taken=0,
        )

    frontier = [start]
    seen = {tuple(start_cycle)}
    best_terminal = start

    for step in range(1, max_steps + 1):
        candidates = []
        for node in frontier:
            parent_path = node["path"]
            for item in one_edit_variants(node["cycle"], vocab):
                key = tuple(item["cycle"])
                if key in seen:
                    continue
                child = classify_row(item["cycle"], r, label=item["label"], edits=item["edits"])
                child["path"] = parent_path + [child]
                seen.add(key)
                candidates.append(child)

        if not candidates:
            break

        candidates.sort(key=lambda row: score_row(row, family))
        frontier = candidates[:beam_width]

        if score_row(frontier[0], family) < score_row(best_terminal, family):
            best_terminal = frontier[0]

        for node in frontier:
            if node["classification"] == family and node["confidence"] == "exact":
                return result_snapshot(
                    start=start,
                    terminal=node,
                    family=family,
                    beam_width=beam_width,
                    max_steps=max_steps,
                    reached_exact=True,
                    steps_taken=step,
                )

    return result_snapshot(
        start=start,
        terminal=best_terminal,
        family=family,
        beam_width=beam_width,
        max_steps=max_steps,
        reached_exact=False,
        steps_taken=len(best_terminal.get("path", [best_terminal])) - 1,
    )


def main() -> int:
    ap = argparse.ArgumentParser(prog="scripts/g15_beam_repair_probe.py")
    ap.add_argument("--input", required=True, help="*_stalls.json file from g15_extract_stalls.py")
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--beam-width", type=int, default=8)
    ap.add_argument("--max-steps", type=int, default=6)
    ap.add_argument("--out")
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    family = data["target_family"]
    stalls = data.get("stalls", [])

    results = []
    for stall in stalls:
        cycle = stall["start_cycle"]
        vocab = default_vocab_for_cycle(cycle, args.r)
        results.append(
            beam_repair(
                start_cycle=cycle,
                family=family,
                vocab=vocab,
                r=args.r,
                beam_width=args.beam_width,
                max_steps=args.max_steps,
            )
        )

    recovered = sum(1 for r in results if r["reached_exact_target"])
    out = {
        "source_file": args.input,
        "target_family": family,
        "beam_width": args.beam_width,
        "max_steps": args.max_steps,
        "stall_count": len(stalls),
        "recovered_count": recovered,
        "recovered_rate": (recovered / len(stalls)) if stalls else 0.0,
        "results": results,
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
