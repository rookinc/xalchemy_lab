#!/data/data/com.termux/files/usr/bin/python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_possig(psig: str) -> tuple[int, ...]:
    return tuple(sorted(int(x) for x in psig.split("|")))


def rotate_support(psig: str, k: int, mod: int = 6) -> str:
    vals = parse_possig(psig)
    rot = sorted(((x + k) % mod) for x in vals)
    return "|".join(str(x) for x in rot)


def canonical_orbit(psig: str, mod: int = 6) -> str:
    rots = [rotate_support(psig, k, mod=mod) for k in range(mod)]
    return min(rots)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-json")
    args = ap.parse_args()

    data = load_json(args.input)
    rows = data["position_buckets"]

    orbit_buckets = defaultdict(lambda: {
        "count": 0,
        "exact_count": 0,
        "stall_count": 0,
        "steps_weighted_sum": 0.0,
        "members": [],
    })

    for row in rows:
        psig = row["position_signature"]
        orb = canonical_orbit(psig)
        b = orbit_buckets[orb]
        c = row["count"]
        b["count"] += c
        b["exact_count"] += row["exact_count"]
        b["stall_count"] += row["stall_count"]
        b["steps_weighted_sum"] += row["avg_steps"] * c
        b["members"].append({
            "position_signature": psig,
            "count": row["count"],
            "exact_rate": row["exact_rate"],
            "stall_rate": row["stall_rate"],
            "avg_steps": row["avg_steps"],
        })

    out_rows = []
    for orb in sorted(orbit_buckets):
        b = orbit_buckets[orb]
        total = b["count"]
        members = sorted(b["members"], key=lambda x: x["position_signature"])

        exact_rates = [m["exact_rate"] for m in members]
        stall_rates = [m["stall_rate"] for m in members]

        out_rows.append({
            "orbit_canonical": orb,
            "member_count": len(members),
            "total_count": total,
            "aggregate_exact_count": b["exact_count"],
            "aggregate_exact_rate": (b["exact_count"] / total) if total else 0.0,
            "aggregate_stall_count": b["stall_count"],
            "aggregate_stall_rate": (b["stall_count"] / total) if total else 0.0,
            "aggregate_avg_steps": (b["steps_weighted_sum"] / total) if total else 0.0,
            "member_exact_rate_min": min(exact_rates) if exact_rates else None,
            "member_exact_rate_max": max(exact_rates) if exact_rates else None,
            "member_exact_rate_span": (max(exact_rates) - min(exact_rates)) if exact_rates else None,
            "member_stall_rate_min": min(stall_rates) if stall_rates else None,
            "member_stall_rate_max": max(stall_rates) if stall_rates else None,
            "member_stall_rate_span": (max(stall_rates) - min(stall_rates)) if stall_rates else None,
            "members": members,
        })

    payload = {
        "source": args.input,
        "rotation_orbits": out_rows,
    }

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.out_json}")

    print("orbit  members  total  agg_exact%  member_exact_span  agg_stall%  member_stall_span")
    print("-----  -------  -----  ----------  -----------------  ----------  -----------------")
    for row in out_rows:
        print(
            f"{row['orbit_canonical']:<5}  "
            f"{row['member_count']:>7}  "
            f"{row['total_count']:>5}  "
            f"{100.0*row['aggregate_exact_rate']:>9.1f}%  "
            f"{100.0*row['member_exact_rate_span']:>16.1f}%  "
            f"{100.0*row['aggregate_stall_rate']:>9.1f}%  "
            f"{100.0*row['member_stall_rate_span']:>16.1f}%"
        )

    print()
    print("orbit members")
    for row in out_rows:
        print(f"[orbit {row['orbit_canonical']}]")
        for m in row["members"]:
            print(
                f"  {m['position_signature']}: "
                f"count={m['count']} "
                f"exact%={100.0*m['exact_rate']:.1f} "
                f"stall%={100.0*m['stall_rate']:.1f} "
                f"avg_steps={m['avg_steps']:.3f}"
            )
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
