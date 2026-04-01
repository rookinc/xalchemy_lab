#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

expected_prefix = ["o4", "s0", "t0", "s2"]
expected_suffix = "s4"
expected_slot4 = {"o4", "s0", "s2", "s3", "s4", "t0", "t3", "t4"}

data = json.loads(Path("artifacts/frame2_o_anchor_residue_frame2_d1.json").read_text())
rows = data["rows"]

observed_slot4 = set()
bad_shape = []

for row in rows:
    cyc = row["normalized_cycle"]
    if cyc[:4] != expected_prefix or cyc[5] != expected_suffix:
        bad_shape.append(cyc)
    observed_slot4.add(cyc[4])

summary = {
    "row_count": len(rows),
    "expected_prefix": expected_prefix,
    "expected_suffix": expected_suffix,
    "observed_slot4": sorted(observed_slot4),
    "expected_slot4": sorted(expected_slot4),
    "shape_ok": len(bad_shape) == 0,
    "slot4_set_ok": observed_slot4 == expected_slot4,
    "bad_shape_count": len(bad_shape),
}

out = {
    "summary": summary,
    "bad_shape_examples": bad_shape[:20],
}

outpath = Path("artifacts/frame2_d1_slot4_family_verification.json")
outpath.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

print(f"wrote {outpath}")
print(json.dumps(summary, indent=2))
