#!/data/data/com.termux/files/usr/bin/python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
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


def parse_start_label(label: str) -> tuple[list[str], list[dict[str, Any]]]:
    seed = ["o2", "s2", "t0", "s0", "t3", "s3"]
    cycle = seed[:]
    edits: list[dict[str, Any]] = []

    for part in label.split("__"):
        if not part.startswith("edit_pos"):
            continue
        rest = part[len("edit_pos"):]
        digits = []
        i = 0
        while i < len(rest) and rest[i].isdigit():
            digits.append(rest[i])
            i += 1
        pos = int("".join(digits))
        tail = rest[i + 1:] if i < len(rest) and rest[i] == "_" else rest[i:]
        frm, to = tail.split("_to_", 1)
        cycle[pos] = to
        edits.append({"position": pos, "from": frm, "to": to})

    edits.sort(key=lambda x: x["position"])
    return cycle, edits


def support_and_transition(label: str) -> tuple[str, str]:
    edits = []
    for part in label.split("__"):
        if not part.startswith("edit_pos"):
            continue
        rest = part[len("edit_pos"):]
        digits = []
        i = 0
        while i < len(rest) and rest[i].isdigit():
            digits.append(rest[i])
            i += 1
        pos = int("".join(digits))
        tail = rest[i + 1:] if i < len(rest) and rest[i] == "_" else rest[i:]
        frm, to = tail.split("_to_", 1)
        edits.append((pos, frm, to))
    edits.sort()
    support = "|".join(str(pos) for pos, _, _ in edits)
    transition = "|".join(f"{pos}:{frm}->{to}" for pos, frm, to in edits)
    return support, transition


def first_move_signature(row: dict[str, Any]) -> str:
    bits = []
    for e in sorted(row.get("edits", []), key=lambda x: x["position"]):
        bits.append(f"{e['position']}:{e['from']}->{e['to']}")
    return "|".join(bits)


def greedy_after_forced_first_move(start: dict[str, Any], first_move: dict[str, Any], vocab: list[str], r: int, max_steps: int) -> dict[str, Any]:
    path = [start, first_move]
    seen = {tuple(start["cycle"]), tuple(first_move["cycle"])}
    current = first_move

    for _ in range(max_steps - 1):
        current_distance = current["distance_summary"].get("best_action_distance")
        candidates = []

        for item in one_edit_variants(current["cycle"], vocab):
            row = classify_row(item["cycle"], r, item["label"], item["edits"])
            d = row["distance_summary"].get("best_action_distance", 10**9)
            candidates.append((d, row["label"], row))

        if not candidates:
            break

        candidates.sort(key=lambda x: (x[0], x[1]))
        nxt = candidates[0][2]
        nxt_d = nxt["distance_summary"].get("best_action_distance")

        if current_distance is None or nxt_d is None or nxt_d > current_distance:
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
        "reached_exact_target": current["classification"] == "action-cell" and current["confidence"] == "exact",
        "steps_taken": len(path) - 1,
        "end_classification": current["classification"],
        "end_confidence": current["confidence"],
        "end_distance": current["distance_summary"].get("best_action_distance"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--payload", required=True)
    ap.add_argument("--delta", required=True)
    ap.add_argument("--mode", choices=["rescued", "broken", "both"], default="both")
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--max-steps", type=int, default=10)
    args = ap.parse_args()

    payload = load_json(args.payload)
    delta = load_json(args.delta)

    vocab = unique_preserve_order(payload["vocab"])

    labels: list[str] = []
    if args.mode in ("rescued", "both"):
        labels.extend(row["start_label"] for row in delta.get("rescued_examples", []))
    if args.mode in ("broken", "both"):
        labels.extend(row["start_label"] for row in delta.get("broken_examples", []))

    labels = sorted(dict.fromkeys(labels))

    out_rows = []
    for label in labels:
        cycle, edits = parse_start_label(label)
        start = classify_row(cycle, args.r, label, edits)
        support, transition = support_and_transition(label)

        move_rows = []
        for item in one_edit_variants(start["cycle"], vocab):
            forced = classify_row(item["cycle"], args.r, item["label"], item["edits"])
            move_sig = first_move_signature(forced)
            result = greedy_after_forced_first_move(
                start=start,
                first_move=forced,
                vocab=vocab,
                r=args.r,
                max_steps=args.max_steps,
            )
            move_rows.append({
                "first_move": move_sig,
                "exact": result["reached_exact_target"],
                "steps_taken": result["steps_taken"],
                "end_classification": result["end_classification"],
                "end_confidence": result["end_confidence"],
                "end_distance": result["end_distance"],
            })

        move_rows.sort(key=lambda x: (-int(x["exact"]), x["steps_taken"], x["first_move"]))

        out_rows.append({
            "start_label": label,
            "support": support,
            "transition": transition,
            "start_classification": start["classification"],
            "start_confidence": start["confidence"],
            "start_distance": start["distance_summary"].get("best_action_distance"),
            "best_moves": move_rows[:12],
        })

    out = {
        "payload": args.payload,
        "delta": args.delta,
        "mode": args.mode,
        "count": len(out_rows),
        "oracle_rows": out_rows,
    }

    Path(args.out_json).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out_json}")
    print(f"count={len(out_rows)}")
    print()
    for row in out_rows:
        print(f"{row['support']} :: {row['transition']}")
        for move in row["best_moves"][:5]:
            print(
                f"  {move['first_move']} "
                f"exact={move['exact']} "
                f"steps={move['steps_taken']} "
                f"end={move['end_classification']}/{move['end_confidence']} "
                f"d={move['end_distance']}"
            )
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
