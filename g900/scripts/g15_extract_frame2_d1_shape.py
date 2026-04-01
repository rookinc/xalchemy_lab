#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

data = json.loads(Path("artifacts/frame2_o_anchor_residue_frame2_d1.json").read_text())

rows = data["rows"]

shape_counter = {}
slot4_values = set()

for row in rows:
    cyc = row["normalized_cycle"]
    key = (cyc[0], cyc[1], cyc[2], cyc[3], cyc[5])
    shape_counter[key] = shape_counter.get(key, 0) + 1
    slot4_values.add(cyc[4])

print("row_count:", len(rows))
print("distinct frozen-5 shapes:", len(shape_counter))
for k, v in sorted(shape_counter.items(), key=lambda kv: (-kv[1], kv[0])):
    print(v, ":", k)

print("slot4 values:", sorted(slot4_values))

print("\nfull normalized cycles:")
seen = set()
for row in rows:
    cyc = tuple(row["normalized_cycle"])
    if cyc not in seen:
        seen.add(cyc)
        print(list(cyc))
