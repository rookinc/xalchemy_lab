#!/data/data/com.termux/files/usr/bin/python3
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


SEED = ["o2", "s2", "t0", "s0", "t3", "s3"]


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
    cycle = SEED[:]
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


def move_signature(row: dict[str, Any]) -> str:
    bits = []
    for e in sorted(row.get("edits", []), key=lambda x: x["position"]):
        bits.append(f"{e['position']}:{e['from']}->{e['to']}")
    return "|".join(bits)


def greedy_from_state(start: dict[str, Any], vocab: list[str], r: int, max_steps: int) -> dict[str, Any]:
    path = [start]
    seen = {tuple(start["cycle"])}
    current = start

    for _ in range(max_steps):
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


def best_first_moves_from_targeted_oracle(oracle_row: dict[str, Any], top_first: int) -> list[str]:
    return [m["first_move"] for m in oracle_row.get("best_moves", [])[:top_first]]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--payload", required=True)
    ap.add_argument("--targeted-oracle", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--max-steps", type=int, default=10)
    ap.add_argument("--top-first", type=int, default=3)
    ap.add_argument("--top-second", type=int, default=6)
    args = ap.parse_args()

    payload = load_json(args.payload)
    oracle = load_json(args.targeted_oracle)
    vocab = unique_preserve_order(payload["vocab"])

    out_rows = []
    for row in oracle["oracle_rows"]:
        label = row["start_label"]
        cycle, edits = parse_start_label(label)
        start = classify_row(cycle, args.r, label, edits)
        support, transition = support_and_transition(label)

        allowed_first = set(best_first_moves_from_targeted_oracle(row, args.top_first))

        first_level = []
        for item1 in one_edit_variants(start["cycle"], vocab):
            first = classify_row(item1["cycle"], args.r, item1["label"], item1["edits"])
            first_sig = move_signature(first)
            if first_sig not in allowed_first:
                continue

            second_candidates = []
            for item2 in one_edit_variants(first["cycle"], vocab):
                second = classify_row(item2["cycle"], args.r, item2["label"], item2["edits"])
                d = second["distance_summary"].get("best_action_distance", 10**9)
                second_candidates.append((d, move_signature(second), second))
            second_candidates.sort(key=lambda x: (x[0], x[1]))
            second_candidates = second_candidates[:args.top_second]

            second_level = []
            for _, second_sig, second in second_candidates:
                tail = greedy_from_state(second, vocab=vocab, r=args.r, max_steps=max(0, args.max_steps - 2))
                total_steps = 2 + tail["steps_taken"]
                second_level.append({
                    "second_move": second_sig,
                    "exact": tail["reached_exact_target"],
                    "total_steps": total_steps,
                    "end_classification": tail["end_classification"],
                    "end_confidence": tail["end_confidence"],
                    "end_distance": tail["end_distance"],
                })

            second_level.sort(key=lambda x: (-int(x["exact"]), x["total_steps"], x["second_move"]))
            first_level.append({
                "first_move": first_sig,
                "best_second_moves": second_level,
            })

        first_level.sort(
            key=lambda x: (
                -int(x["best_second_moves"][0]["exact"]) if x["best_second_moves"] else 0,
                x["best_second_moves"][0]["total_steps"] if x["best_second_moves"] else 10**9,
                x["first_move"],
            )
        )

        out_rows.append({
            "start_label": label,
            "support": support,
            "transition": transition,
            "start_distance": start["distance_summary"].get("best_action_distance"),
            "two_step_motifs": first_level,
        })

    out = {
        "payload": args.payload,
        "targeted_oracle": args.targeted_oracle,
        "count": len(out_rows),
        "oracle_rows": out_rows,
    }

    Path(args.out_json).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out_json}")
    print(f"count={len(out_rows)}")
    print()

    for row in out_rows:
        print(f"{row['support']} :: {row['transition']}")
        for motif in row["two_step_motifs"][:3]:
            best2 = motif["best_second_moves"][0] if motif["best_second_moves"] else None
            if not best2:
                continue
            print(
                f"  first={motif['first_move']} "
                f"then={best2['second_move']} "
                f"exact={best2['exact']} "
                f"steps={best2['total_steps']} "
                f"end={best2['end_classification']}/{best2['end_confidence']} "
                f"d={best2['end_distance']}"
            )
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
