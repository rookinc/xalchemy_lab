from __future__ import annotations

import json
from pathlib import Path


def transition_sign(a: str, b: str) -> int:
    return 1 if a == b else -1


def invariant(chart_trace: list[str]) -> dict:
    if len(chart_trace) < 2:
        return {"transition_signs": [], "H": 1}
    signs = [transition_sign(chart_trace[i], chart_trace[i + 1]) for i in range(len(chart_trace) - 1)]
    H = 1
    for s in signs:
        H *= s
    return {"transition_signs": signs, "H": H}


def main() -> None:
    src = Path("specs/app/framed_return_probe_v0_1.json")
    data = json.loads(src.read_text())

    out = {
        "name": "framed_return_invariant_v0_1",
        "source": src.name,
        "loops": [],
    }

    print("HELLO FRAMED RETURN INVARIANT")
    print()

    for loop in data["loops"]:
        inv = invariant(loop["chart_trace"])
        row = {
            "name": loop["name"],
            "chart_trace": loop["chart_trace"],
            "transition_signs": inv["transition_signs"],
            "H": inv["H"],
        }
        out["loops"].append(row)
        print(f"{row['name']}: trace={row['chart_trace']} signs={row['transition_signs']} H={row['H']}")

    outpath = Path("specs/app/framed_return_invariant_v0_1.json")
    outpath.write_text(json.dumps(out, indent=2))
    print()
    print(f"Wrote {outpath}")


if __name__ == "__main__":
    main()
