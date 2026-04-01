#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

data = json.loads(Path("artifacts/frame2_o_anchor_residue_frame2_d1.json").read_text())
rows = data["rows"]

prefix2_counter = Counter()
prefix3_counter = Counter()
full_cycles = Counter()

o4_s0_rows = []
o4_s4_rows = []
other_rows = []

for row in rows:
    cyc = row["normalized_cycle"]
    p2 = tuple(cyc[:2])
    p3 = tuple(cyc[:3])

    prefix2_counter[p2] += 1
    prefix3_counter[p3] += 1
    full_cycles[tuple(cyc)] += 1

    if p2 == ("o4", "s0"):
        o4_s0_rows.append(cyc)
    elif p2 == ("o4", "s4"):
        o4_s4_rows.append(cyc)
    else:
        other_rows.append(cyc)

summary = {
    "row_count": len(rows),
    "prefix2_counter": {str(list(k)): v for k, v in sorted(prefix2_counter.items())},
    "prefix3_counter": {str(list(k)): v for k, v in sorted(prefix3_counter.items())},
    "o4_s0_count": len(o4_s0_rows),
    "o4_s4_count": len(o4_s4_rows),
    "other_prefix_count": len(other_rows),
}

out = {
    "summary": summary,
    "o4_s4_examples": o4_s4_rows[:20],
    "other_prefix_examples": other_rows[:20],
    "distinct_full_cycles": [list(k) for k in sorted(full_cycles.keys())],
}

outpath = Path("artifacts/frame2_d1_orientation_verification.json")
outpath.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

print(f"wrote {outpath}")
print(json.dumps(summary, indent=2))
