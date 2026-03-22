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


def compose_traces(trace1: list[str], trace2: list[str]) -> list[str]:
    return trace1 + trace2


def join_term(trace1: list[str], trace2: list[str]) -> int:
    if not trace1 or not trace2:
        return 1
    return transition_sign(trace1[-1], trace2[0])


def main() -> None:
    src = Path("specs/app/framed_signature_v0_1.json")
    data = json.loads(src.read_text())

    loops = {row["name"]: row["chart_trace"] for row in data["loops"]}

    pairs = [
        ("return_A", "return_B"),
        ("return_A", "return_C_mixed_chart"),
        ("return_B", "return_D_unary_mixed"),
        ("return_C_mixed_chart", "return_D_unary_mixed"),
    ]

    out = {
        "name": "framed_signature_composition_v0_1",
        "source": src.name,
        "pairs": [],
    }

    print("HELLO FRAMED SIGNATURE COMPOSITION")
    print()

    for left_name, right_name in pairs:
        t1 = loops[left_name]
        t2 = loops[right_name]

        sig1 = signature_from_trace(t1)
        sig2 = signature_from_trace(t2)

        combined = compose_traces(t1, t2)
        sig_total = signature_from_trace(combined)

        jt = join_term(t1, t2)
        predicted_H = sig1["H"] * sig2["H"] * jt
        predicted_S = sig1["S"] + sig2["S"]

        row = {
            "left": {
                "name": left_name,
                "trace": t1,
                "H": sig1["H"],
                "S": sig1["S"],
            },
            "right": {
                "name": right_name,
                "trace": t2,
                "H": sig2["H"],
                "S": sig2["S"],
            },
            "join_term": jt,
            "combined_trace": combined,
            "combined": {
                "H": sig_total["H"],
                "S": sig_total["S"],
            },
            "predicted": {
                "H": predicted_H,
                "S": predicted_S,
            },
            "matches": {
                "H": sig_total["H"] == predicted_H,
                "S": sig_total["S"] == predicted_S,
            },
        }
        out["pairs"].append(row)

        print(f"{left_name} + {right_name}")
        print(f"  H1={sig1['H']} S1={sig1['S']}")
        print(f"  H2={sig2['H']} S2={sig2['S']}")
        print(f"  join_term={jt}")
        print(f"  combined H={sig_total['H']} predicted H={predicted_H} match={row['matches']['H']}")
        print(f"  combined S={sig_total['S']} predicted S={predicted_S} match={row['matches']['S']}")
        print()

    outpath = Path("specs/app/framed_signature_composition_v0_1.json")
    outpath.write_text(json.dumps(out, indent=2))
    print(f"Wrote {outpath}")


if __name__ == "__main__":
    main()
