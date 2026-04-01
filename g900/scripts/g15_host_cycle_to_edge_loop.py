#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

from g15_cocycle_decode import EDGES, EDGE_INDEX

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "specs" / "examples" / "g15-host-walk-test.json"

# ---------------------------------------------------------------------
# Fill this map once the host-frame locations v0..v14 are identified
# with the G15 vertices o0..o4, s0..s4, t0..t4.
# ---------------------------------------------------------------------
HOST_TO_G15: Dict[str, str] = {
    "v0": "o0",
    "v1": "o1",
    "v2": "o2",
    "v3": "o3",
    "v4": "o4",
    "v5": "s4",
    "v6": "t2",
    "v7": "s2",
    "v8": "t0",
    "v9": "s0",
    "v10": "t3",
    "v11": "s3",
    "v12": "t1",
    "v13": "t4",
    "v14": "s1",
}


def load_spec(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_host_cycle(spec: dict) -> List[str]:
    subset = spec["move_transition_subset"]
    if len(subset) != 15:
        raise ValueError("expected 15 host-cycle move rows")

    ordered = [row["from_vertex"] for row in subset]
    ordered.append(subset[-1]["to_vertex"])
    return ordered


def edge_label_for_g15_pair(a: str, b: str) -> str:
    key = tuple(sorted((a, b)))
    idx = EDGE_INDEX.get(key)
    if idx is None:
        raise ValueError(f"no G15 edge between {a} and {b}")
    return f"e{idx + 1}"


def main() -> int:
    spec = load_spec(SPEC_PATH)
    host_cycle = build_host_cycle(spec)

    missing = [v for v in host_cycle[:-1] if v not in HOST_TO_G15]
    if missing:
        payload = {
            "status": "awaiting_host_to_g15_map",
            "host_cycle_vertices": host_cycle,
            "missing_vertices": sorted(set(missing)),
            "expected_host_vertices": [f"v{i}" for i in range(15)],
            "g15_vertices": [f"o{i}" for i in range(5)] + [f"s{i}" for i in range(5)] + [f"t{i}" for i in range(5)],
        }
        outpath = ROOT / "artifacts" / "g15_host_cycle_edge_loop.json"
        outpath.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {outpath}")
        print(json.dumps(payload, indent=2))
        return 0

    mapped_cycle = [HOST_TO_G15[v] for v in host_cycle]

    edge_labels: List[str] = []
    edge_pairs: List[Tuple[str, str]] = []
    for a, b in zip(mapped_cycle[:-1], mapped_cycle[1:]):
        edge_pairs.append((a, b))
        edge_labels.append(edge_label_for_g15_pair(a, b))

    payload = {
        "status": "mapped",
        "host_cycle_vertices": host_cycle,
        "mapped_g15_cycle_vertices": mapped_cycle,
        "edge_pairs": edge_pairs,
        "edge_labels": edge_labels,
        "loop_for_parity_probe": ",".join(edge_labels),
    }

    outpath = ROOT / "artifacts" / "g15_host_cycle_edge_loop.json"
    outpath.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {outpath}")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
