#!/data/data/com.termux/files/usr/bin/python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def support_from_label(label: str) -> str:
    posns = []
    for part in label.split("__"):
        if part.startswith("edit_pos"):
            rest = part[len("edit_pos"):]
            digits = []
            for ch in rest:
                if ch.isdigit():
                    digits.append(ch)
                else:
                    break
            if digits:
                posns.append(int("".join(digits)))
    posns = sorted(set(posns))
    return "|".join(str(p) for p in posns)


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
    same_exact = []
    same_fail = []

    for key in shared:
        b = base_map[key]
        c = cand_map[key]
        be = bool(b["reached_exact_target"])
        ce = bool(c["reached_exact_target"])

        row = {
            "start_label": key,
            "support": support_from_label(key),
            "baseline_exact": be,
            "candidate_exact": ce,
            "baseline_steps": b["steps_taken"],
            "candidate_steps": c["steps_taken"],
            "start_cycle": b.get("start_cycle", c.get("start_cycle")),
        }

        if (not be) and ce:
            rescued.append(row)
        elif be and (not ce):
            broken.append(row)
        elif be and ce:
            same_exact.append(row)
        else:
            same_fail.append(row)

    def bucket(rows: list[dict]) -> list[dict]:
        counts = defaultdict(int)
        for r in rows:
            counts[r["support"]] += 1
        out = []
        for k in sorted(counts):
            out.append({"support": k, "count": counts[k]})
        return out

    payload = {
        "baseline": args.baseline,
        "candidate": args.candidate,
        "shared_count": len(shared),
        "rescued_count": len(rescued),
        "broken_count": len(broken),
        "same_exact_count": len(same_exact),
        "same_fail_count": len(same_fail),
        "rescued_by_support": bucket(rescued),
        "broken_by_support": bucket(broken),
        "rescued_examples": rescued[:25],
        "broken_examples": broken[:25],
    }

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")

    print(f"shared={payload['shared_count']}")
    print(f"rescued={payload['rescued_count']}")
    print(f"broken={payload['broken_count']}")
    print(f"same_exact={payload['same_exact_count']}")
    print(f"same_fail={payload['same_fail_count']}")
    print()

    print("rescued_by_support")
    for row in payload["rescued_by_support"]:
        print(f"  {row['support']}: {row['count']}")
    print()

    print("broken_by_support")
    for row in payload["broken_by_support"]:
        print(f"  {row['support']}: {row['count']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
