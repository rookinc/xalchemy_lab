from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    p = Path("specs/tree_gauge_representative_v1.json")
    data = json.loads(p.read_text())

    status = data.get("status", "missing")
    source_kind = data.get("source_kind", "missing")
    edge_cocycle = data.get("edge_cocycle", {})

    missing = [k for k, v in edge_cocycle.items() if v is None]

    print("\n====================")
    print("TREE-GAUGE STATUS")
    print("====================\n")
    print(f"status      = {status}")
    print(f"source_kind = {source_kind}")
    print(f"n_edges     = {len(edge_cocycle)}")
    print(f"n_missing   = {len(missing)}")

    if missing:
        print("missing_keys =", ", ".join(missing))

    if source_kind == "smoke_test":
        print("\nREADING:")
        print("  current cocycle is a smoke-test representative only")
    elif source_kind == "independent":
        print("\nREADING:")
        print("  current cocycle claims to come from independent signed-lift data")
    elif source_kind == "derived_from_signed_lift_source":
        print("\nREADING:")
        print("  current cocycle is derived from the signed_lift_source_v1 seed")
        print("  this is a derivation step, but not yet full G15 data unless source coverage is complete")
    else:
        print("\nREADING:")
        print("  source kind is unspecified")

    print()


if __name__ == "__main__":
    main()
