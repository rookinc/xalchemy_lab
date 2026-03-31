#!/data/data/com.termux/files/usr/bin/python3
from __future__ import annotations

import json
import sys
from pathlib import Path

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: ./scripts/g15_extract_stalls.py <result.json> [more.json ...]", file=sys.stderr)
        return 1

    for arg in sys.argv[1:]:
        p = Path(arg)
        data = json.loads(p.read_text(encoding="utf-8"))
        family = data.get("target_family", "unknown")

        if "failed_walks" in data:
            stalls = data["failed_walks"]
            source_mode = "failed_walks"
        else:
            walks = data.get("walks", [])
            stalls = [w for w in walks if not w.get("reached_exact_target", False)]
            source_mode = "walks_fallback"

        out = {
            "source_file": str(p),
            "target_family": family,
            "stall_count": len(stalls),
            "source_mode": source_mode,
            "stalls": stalls,
        }

        out_path = p.with_name(p.stem + "_stalls.json")
        out_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out_path}")
        print(f"family={family} stalls={len(stalls)} source_mode={source_mode}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
