from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    data = json.loads(Path("specs/bridge_edge_aliases_v1.json").read_text())
    aliases = data["aliases"]

    print("\n====================")
    print("BRIDGE EDGE ALIAS STATUS")
    print("====================\n")

    missing = [k for k, v in aliases.items() if v is None]
    for k in sorted(aliases):
        print(f"{k:3s} -> {aliases[k]}")

    print()
    print(f"missing = {len(missing)}")
    if missing:
        print("missing_keys =", ", ".join(missing))
    print()


if __name__ == "__main__":
    main()
