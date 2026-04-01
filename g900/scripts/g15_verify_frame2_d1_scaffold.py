#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

E2 = ["o4", "s0", "t0", "s2", "t2", "s4"]

data = json.loads(Path("artifacts/frame2_o_anchor_residue_frame2_d1.json").read_text())
rows = data["rows"]

prefix1_ok = 0
prefix2_ok = 0
slots_235_ok = 0
slot4_only_ok = 0

slot_mismatch_counter = Counter()
full_mismatch_patterns = Counter()

bad_prefix1 = []
bad_prefix2 = []
bad_slots_235 = []
bad_slot4_only = []

for row in rows:
    cyc = row["normalized_cycle"]

    if cyc[0] == E2[0]:
        prefix1_ok += 1
    else:
        bad_prefix1.append(cyc)

    if cyc[:2] == E2[:2]:
        prefix2_ok += 1
    else:
        bad_prefix2.append(cyc)

    if cyc[2] == E2[2] and cyc[3] == E2[3] and cyc[5] == E2[5]:
        slots_235_ok += 1
    else:
        bad_slots_235.append(cyc)

    mismatches = [i for i, (a, b) in enumerate(zip(cyc, E2)) if a != b]
    full_mismatch_patterns[tuple(mismatches)] += 1
    for i in mismatches:
        slot_mismatch_counter[i] += 1

    if mismatches == [4]:
        slot4_only_ok += 1
    else:
        bad_slot4_only.append(
            {
                "cycle": cyc,
                "mismatches": mismatches,
            }
        )

summary = {
    "row_count": len(rows),
    "E2": E2,
    "prefix1_ok": prefix1_ok,
    "prefix2_ok": prefix2_ok,
    "slots_235_ok": slots_235_ok,
    "slot4_only_ok": slot4_only_ok,
    "slot_mismatch_counter": dict(sorted(slot_mismatch_counter.items())),
    "full_mismatch_patterns": {
        str(list(k)): v for k, v in sorted(full_mismatch_patterns.items())
    },
}

out = {
    "summary": summary,
    "bad_prefix1_examples": bad_prefix1[:20],
    "bad_prefix2_examples": bad_prefix2[:20],
    "bad_slots_235_examples": bad_slots_235[:20],
    "bad_slot4_only_examples": bad_slot4_only[:20],
}

outpath = Path("artifacts/frame2_d1_scaffold_verification.json")
outpath.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

print(f"wrote {outpath}")
print(json.dumps(summary, indent=2))
