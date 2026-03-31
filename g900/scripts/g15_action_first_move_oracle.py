#!/data/data/com.termux/files/usr/bin/python3
from __future__ import annotations

import argparse
import itertools
import json
import random
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


def start_support_and_transition(label: str) -> tuple[str, str]:
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
    edits = row.get("edits", [])
    bits = []
    for e in sorted(edits, key=lambda x: x["position"]):
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
        "path": path,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-json")
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

    oracle = defaultdict(lambda: {
        "start_count": 0,
        "forced_moves": defaultdict(lambda: {
            "count": 0,
            "exact_count": 0,
            "steps_sum": 0,
            "examples": [],
        }),
    })

    for start in starts:
        support, transition = start_support_and_transition(start["label"])
        key = (support, transition)
        oracle[key]["start_count"] += 1

        for item in one_edit_variants(start["cycle"], vocab):
            forced = classify_row(item["cycle"], args.r, item["label"], item["edits"])
            move_sig = first_move_signature(forced)

            result = greedy_after_forced_first_move(
                start=start,
                first_move=forced,
                vocab=vocab,
                r=args.r,
                max_steps=max_steps,
            )

            bucket = oracle[key]["forced_moves"][move_sig]
            bucket["count"] += 1
            if result["reached_exact_target"]:
                bucket["exact_count"] += 1
            bucket["steps_sum"] += result["steps_taken"]

            if len(bucket["examples"]) < 3:
                bucket["examples"].append({
                    "start_label": start["label"],
                    "forced_first_move": move_sig,
                    "reached_exact_target": result["reached_exact_target"],
                    "steps_taken": result["steps_taken"],
                    "end_classification": result["end_classification"],
                    "end_confidence": result["end_confidence"],
                })

    out_rows = []
    for (support, transition) in sorted(oracle):
        forced_rows = []
        for move_sig in sorted(oracle[(support, transition)]["forced_moves"]):
            b = oracle[(support, transition)]["forced_moves"][move_sig]
            forced_rows.append({
                "first_move": move_sig,
                "count": b["count"],
                "exact_count": b["exact_count"],
                "exact_rate": (b["exact_count"] / b["count"]) if b["count"] else 0.0,
                "avg_steps": (b["steps_sum"] / b["count"]) if b["count"] else 0.0,
                "examples": b["examples"],
            })

        forced_rows.sort(key=lambda x: (-x["exact_rate"], x["avg_steps"], x["first_move"]))

        out_rows.append({
            "support": support,
            "transition": transition,
            "start_count": oracle[(support, transition)]["start_count"],
            "best_first_moves": forced_rows[:12],
        })

    payload_out = {
        "source": args.input,
        "target_family": "action-cell",
        "signature_oracle": out_rows,
    }

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(payload_out, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")

    print("support   transition   top_first_moves")
    print("--------  -----------  ---------------")
    for row in out_rows[:20]:
        print(f"{row['support']} :: {row['transition']}")
        for move in row["best_first_moves"][:5]:
            print(
                f"  {move['first_move']} "
                f"exact%={100.0*move['exact_rate']:.1f} "
                f"count={move['count']} "
                f"avg_steps={move['avg_steps']:.3f}"
            )
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
