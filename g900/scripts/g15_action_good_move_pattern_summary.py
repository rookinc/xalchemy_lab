#!/data/data/com.termux/files/usr/bin/python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


SEED = ["o2", "s2", "t0", "s0", "t3", "s3"]


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def species(x: str) -> str:
    return x[0]


def index(x: str) -> int:
    return int(x[1:])


def parse_move_sig(sig: str) -> list[dict]:
    edits = []
    if not sig:
        return edits
    for part in sig.split("|"):
        pos_str, rest = part.split(":", 1)
        frm, to = rest.split("->", 1)
        edits.append({
            "position": int(pos_str),
            "from": frm,
            "to": to,
        })
    edits.sort(key=lambda e: e["position"])
    return edits


def summarize_rows(rows: list[dict]) -> dict:
    by_position = defaultdict(lambda: {"count": 0, "exact_count": 0})
    by_species = defaultdict(lambda: {"count": 0, "exact_count": 0})
    by_index_mode = defaultdict(lambda: {"count": 0, "exact_count": 0})
    by_seed_restore = defaultdict(lambda: {"count": 0, "exact_count": 0})
    by_move = defaultdict(lambda: {"count": 0, "exact_count": 0, "steps_sum": 0})

    for row in rows:
        for move in row.get("best_moves", []):
            move_sig = move["first_move"]
            exact = bool(move["exact"])
            steps = move["steps_taken"]

            edits = parse_move_sig(move_sig)
            if len(edits) != 1:
                continue
            e = edits[0]

            pos = e["position"]
            frm = e["from"]
            to = e["to"]

            sp_key = f"{species(frm)}->{species(to)}"
            idx_key = "index_preserved" if index(frm) == index(to) else "index_shifted"
            restore_key = "restores_seed" if to == SEED[pos] else "does_not_restore_seed"

            by_position[pos]["count"] += 1
            by_species[sp_key]["count"] += 1
            by_index_mode[idx_key]["count"] += 1
            by_seed_restore[restore_key]["count"] += 1
            by_move[move_sig]["count"] += 1
            by_move[move_sig]["steps_sum"] += steps

            if exact:
                by_position[pos]["exact_count"] += 1
                by_species[sp_key]["exact_count"] += 1
                by_index_mode[idx_key]["exact_count"] += 1
                by_seed_restore[restore_key]["exact_count"] += 1
                by_move[move_sig]["exact_count"] += 1

    def finalize(bucket: dict) -> list[dict]:
        out = []
        for key in sorted(bucket):
            row = bucket[key]
            count = row["count"]
            exact_count = row["exact_count"]
            item = {
                "key": key,
                "count": count,
                "exact_count": exact_count,
                "exact_rate": (exact_count / count) if count else 0.0,
            }
            if "steps_sum" in row:
                item["avg_steps"] = (row["steps_sum"] / count) if count else 0.0
            out.append(item)
        out.sort(key=lambda x: (-x["exact_rate"], -x["count"], str(x["key"])))
        return out

    return {
        "by_position": finalize(by_position),
        "by_species": finalize(by_species),
        "by_index_mode": finalize(by_index_mode),
        "by_seed_restore": finalize(by_seed_restore),
        "by_move": finalize(by_move),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-json")
    args = ap.parse_args()

    data = load_json(args.input)
    summary = summarize_rows(data["oracle_rows"])

    payload = {
        "source": args.input,
        "summary": summary,
    }

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")

    print("BY POSITION")
    print("position  count  exact%")
    print("--------  -----  ------")
    for row in summary["by_position"]:
        print(f"{row['key']:>8}  {row['count']:>5}  {100.0*row['exact_rate']:>5.1f}%")
    print()

    print("BY SPECIES")
    print("species   count  exact%")
    print("--------  -----  ------")
    for row in summary["by_species"]:
        print(f"{row['key']:<8}  {row['count']:>5}  {100.0*row['exact_rate']:>5.1f}%")
    print()

    print("BY INDEX MODE")
    print("mode            count  exact%")
    print("--------------  -----  ------")
    for row in summary["by_index_mode"]:
        print(f"{row['key']:<14}  {row['count']:>5}  {100.0*row['exact_rate']:>5.1f}%")
    print()

    print("BY SEED RESTORE")
    print("mode                count  exact%")
    print("------------------  -----  ------")
    for row in summary["by_seed_restore"]:
        print(f"{row['key']:<18}  {row['count']:>5}  {100.0*row['exact_rate']:>5.1f}%")
    print()

    print("TOP MOVES")
    print("move              count  exact%  avg_steps")
    print("----------------  -----  ------  ---------")
    for row in summary["by_move"][:20]:
        print(
            f"{row['key']:<16}  "
            f"{row['count']:>5}  "
            f"{100.0*row['exact_rate']:>5.1f}%  "
            f"{row['avg_steps']:>9.3f}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
