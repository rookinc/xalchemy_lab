from __future__ import annotations

import json
from pathlib import Path


def chart_value(symbol: str) -> int:
    if symbol == "chart_left":
        return -1
    if symbol == "chart_right":
        return 1
    raise ValueError(f"unknown chart symbol: {symbol}")


def transition_sign(a: str, b: str) -> int:
    return 1 if a == b else -1


def signature_from_trace(trace: list[str]) -> dict:
    values = [chart_value(x) for x in trace]
    S = sum(values)

    signs = []
    H = 1
    for i in range(len(trace) - 1):
        s = transition_sign(trace[i], trace[i + 1])
        signs.append(s)
        H *= s

    return {
        "chart_values": values,
        "transition_signs": signs,
        "H": H,
        "S": S,
        "signature": [H, S],
    }


def main() -> None:
    src = Path("specs/app/framed_return_probe_v0_1.json")
    data = json.loads(src.read_text())

    out = {
        "name": "framed_signature_v0_1",
        "source": src.name,
        "loops": [],
    }

    print("HELLO FRAMED SIGNATURE")
    print()

    for loop in data["loops"]:
        sig = signature_from_trace(loop["chart_trace"])
        row = {
            "name": loop["name"],
            "chart_trace": loop["chart_trace"],
            "chart_values": sig["chart_values"],
            "transition_signs": sig["transition_signs"],
            "H": sig["H"],
            "S": sig["S"],
            "signature": sig["signature"],
        }
        out["loops"].append(row)
        print(
            f"{row['name']}: "
            f"H={row['H']} S={row['S']} signature={tuple(row['signature'])} "
            f"trace={row['chart_trace']}"
        )

    outpath = Path("specs/app/framed_signature_v0_1.json")
    outpath.write_text(json.dumps(out, indent=2))
    print()
    print(f"Wrote {outpath}")


if __name__ == "__main__":
    main()
