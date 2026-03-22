from __future__ import annotations

import json
from pathlib import Path


def chart_value(symbol: str) -> int:
    if symbol == "chart_left":
        return -1
    if symbol == "chart_right":
        return 1
    raise ValueError(f"unknown chart symbol: {symbol}")


def displacement(trace: list[str]) -> dict:
    values = [chart_value(x) for x in trace]
    S = sum(values)
    return {
        "chart_values": values,
        "S": S,
    }


def main() -> None:
    src = Path("specs/app/framed_return_probe_v0_1.json")
    data = json.loads(src.read_text())

    out = {
        "name": "signed_framed_displacement_v0_1",
        "source": src.name,
        "loops": [],
    }

    print("HELLO SIGNED FRAMED DISPLACEMENT")
    print()

    for loop in data["loops"]:
        disp = displacement(loop["chart_trace"])
        row = {
            "name": loop["name"],
            "chart_trace": loop["chart_trace"],
            "chart_values": disp["chart_values"],
            "S": disp["S"],
        }
        out["loops"].append(row)
        print(
            f"{row['name']}: trace={row['chart_trace']} "
            f"values={row['chart_values']} S={row['S']}"
        )

    outpath = Path("specs/app/signed_framed_displacement_v0_1.json")
    outpath.write_text(json.dumps(out, indent=2))
    print()
    print(f"Wrote {outpath}")


if __name__ == "__main__":
    main()
