#!/data/data/com.termux/files/usr/bin/python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_start_signature(label: str) -> tuple[str, str]:
    parts = label.split("__")
    edits = []
    positions = []

    for part in parts:
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
        if "_to_" not in tail:
            continue
        frm, to = tail.split("_to_", 1)
        edits.append((pos, frm, to))
        positions.append(pos)

    edits.sort()
    support = "|".join(str(pos) for pos, _, _ in edits)
    transition = "|".join(f"{pos}:{frm}->{to}" for pos, frm, to in edits)
    return support, transition


def first_move_signature(path_rows: list[dict]) -> str | None:
    if len(path_rows) < 2:
        return None
    nxt = path_rows[1]
    edits = nxt.get("edits", [])
    bits = []
    for e in sorted(edits, key=lambda x: x["position"]):
        bits.append(f"{e['position']}:{e['from']}->{e['to']}")
    return "|".join(bits) if bits else None


def summarize_group(rows: list[dict]) -> list[dict]:
    counts = defaultdict(int)
    for r in rows:
        counts[(r["support"], r["transition"])] += 1
    out = []
    for (support, transition), count in sorted(counts.items()):
        out.append({
            "support": support,
            "transition": transition,
            "count": count,
        })
    return out


def summarize_first_moves(rows: list[dict]) -> list[dict]:
    counts = defaultdict(int)
    for r in rows:
        counts[(r["support"], r["baseline_first_move"], r["candidate_first_move"])] += 1
    out = []
    for (support, bmv, cmv), count in sorted(counts.items()):
        out.append({
            "support": support,
            "baseline_first_move": bmv,
            "candidate_first_move": cmv,
            "count": count,
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--out-json")
    args = ap.parse_args()

    base = load_json(args.baseline)
    cand = load_json(args.candidate)

    base_map = {w["start_label"]: w for w in base["walks"] + base["failed_walks"]}
    cand_map = {w["start_label"]: w for w in cand["walks"] + cand["failed_walks"]}

    shared = sorted(set(base_map) & set(cand_map))

    rescued = []
    broken = []

    for key in shared:
        b = base_map[key]
        c = cand_map[key]
        be = bool(b["reached_exact_target"])
        ce = bool(c["reached_exact_target"])

        if be == ce:
            continue

        support, transition = parse_start_signature(key)
        row = {
            "start_label": key,
            "support": support,
            "transition": transition,
            "baseline_exact": be,
            "candidate_exact": ce,
            "baseline_steps": b["steps_taken"],
            "candidate_steps": c["steps_taken"],
            "baseline_first_move": first_move_signature(b["path"]),
            "candidate_first_move": first_move_signature(c["path"]),
            "start_cycle": b.get("start_cycle", c.get("start_cycle")),
        }

        if (not be) and ce:
            rescued.append(row)
        elif be and (not ce):
            broken.append(row)

    payload = {
        "baseline": args.baseline,
        "candidate": args.candidate,
        "shared_count": len(shared),
        "rescued_count": len(rescued),
        "broken_count": len(broken),
        "rescued_by_transition": summarize_group(rescued),
        "broken_by_transition": summarize_group(broken),
        "rescued_by_first_move_delta": summarize_first_moves(rescued),
        "broken_by_first_move_delta": summarize_first_moves(broken),
        "rescued_examples": rescued,
        "broken_examples": broken,
    }

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")

    print(f"shared={payload['shared_count']}")
    print(f"rescued={payload['rescued_count']}")
    print(f"broken={payload['broken_count']}")
    print()

    print("rescued_by_transition")
    for row in payload["rescued_by_transition"]:
        print(f"  {row['support']} :: {row['transition']} :: {row['count']}")
    print()

    print("broken_by_transition")
    for row in payload["broken_by_transition"]:
        print(f"  {row['support']} :: {row['transition']} :: {row['count']}")
    print()

    print("rescued_by_first_move_delta")
    for row in payload["rescued_by_first_move_delta"]:
        print(
            f"  {row['support']} :: "
            f"base[{row['baseline_first_move']}] -> cand[{row['candidate_first_move']}] :: "
            f"{row['count']}"
        )
    print()

    print("broken_by_first_move_delta")
    for row in payload["broken_by_first_move_delta"]:
        print(
            f"  {row['support']} :: "
            f"base[{row['baseline_first_move']}] -> cand[{row['candidate_first_move']}] :: "
            f"{row['count']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
