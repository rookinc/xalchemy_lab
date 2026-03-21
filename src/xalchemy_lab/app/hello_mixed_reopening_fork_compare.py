from __future__ import annotations

import json
from pathlib import Path

STATE_ORDER = ["000","001","010","011","100","101","110","111"]

M1 = {
    "000": {"left": "e_left",  "right": "e_right"},
    "001": {"left": "e_right", "right": "e_right"},
    "010": {"left": "e_left",  "right": "e_left"},
    "011": {"left": "e_right", "right": "e_left"},
    "100": {"left": "e_right", "right": "e_left"},
    "101": {"left": "e_left",  "right": "e_left"},
    "110": {"left": "e_right", "right": "e_right"},
    "111": {"left": "e_right", "right": "e_left"},
}

M2 = {
    "000": {"left": "e_left",  "right": "e_right"},
    "001": {"left": "e_right", "right": "e_right"},
    "010": {"left": "e_left",  "right": "e_left"},
    "011": {"left": "e_right", "right": "e_left"},
    "100": {"left": "e_right", "right": "e_left"},
    "101": {"left": "e_left",  "right": "e_left"},
    "110": {"left": "e_right", "right": "e_right"},
    "111": {"left": "e_left",  "right": "e_right"},
}

def summarize_differences(a: dict, b: dict) -> list[dict]:
    out = []
    for state in STATE_ORDER:
        if a[state] != b[state]:
            out.append({
                "state": state,
                "law_a": a[state],
                "law_b": b[state],
            })
    return out

def main() -> None:
    payload = {
        "name": "mixed_reopening_fork_comparison_v0_1",
        "laws": {
            "M1_chart_blind_mixed_reopening": M1,
            "M2_chart_sensitive_mixed_reopening": M2,
        },
        "differences": summarize_differences(M1, M2),
        "question": "Should A reverse the mixed reopening state 111, or only the unary/chart base frame?"
    }

    outpath = Path("specs/app/mixed_reopening_fork_comparison_v0_1.json")
    outpath.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {outpath}")
    print()
    print("Differences:")
    for row in payload["differences"]:
        print(
            f"state={row['state']} "
            f"M1={row['law_a']} "
            f"M2={row['law_b']}"
        )

if __name__ == "__main__":
    main()
