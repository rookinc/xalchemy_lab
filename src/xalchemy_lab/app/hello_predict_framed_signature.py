from __future__ import annotations

import json
from pathlib import Path


def predicted_chart_exit(A: int, sigma: int, tau: int, hand: str) -> str:
    # base chart law
    if A == 0:
        base = "chart_left" if hand == "left" else "chart_right"
    else:
        base = "chart_right" if hand == "left" else "chart_left"

    # unary collapse operators
    if sigma == 1 and tau == 0:
        return "chart_left"
    if sigma == 0 and tau == 1:
        return "chart_right"

    # mixed reopening in chart-relative coordinates
    if sigma == 1 and tau == 1:
        if A == 0:
            return "chart_right" if hand == "left" else "chart_left"
        return "chart_left" if hand == "left" else "chart_right"

    return base


def transition_sign(a: str, b: str) -> int:
    return 1 if a == b else -1


def chart_value(symbol: str) -> int:
    if symbol == "chart_left":
        return -1
    if symbol == "chart_right":
        return 1
    raise ValueError(f"unknown chart symbol: {symbol}")


def signature_from_predicted_trace(trace: list[str]) -> tuple[list[int], int, int]:
    if not trace:
        return [], 1, 0

    signs: list[int] = []
    H = 1
    for i in range(len(trace) - 1):
        s = transition_sign(trace[i], trace[i + 1])
        signs.append(s)
        H *= s

    S = sum(chart_value(x) for x in trace)
    return signs, H, S


def main() -> None:
    src = Path("specs/app/native_framed_accumulator_v0_1.json")
    data = json.loads(src.read_text())

    out = {
        "name": "predicted_framed_signature_v0_1",
        "source": src.name,
        "loops": [],
    }

    print("HELLO PREDICT FRAMED SIGNATURE")
    print()

    for loop in data["loops"]:
        specs = loop["controller_specs"]
        hands = loop["hand_sequence"]

        predicted_trace = [
            predicted_chart_exit(spec["A"], spec["sigma"], spec["tau"], hand)
            for spec, hand in zip(specs, hands)
        ]
        signs, H, S = signature_from_predicted_trace(predicted_trace)

        observed_sig = loop["signature"]
        observed_trace = [step["chart_exit"] for step in loop["steps"]]

        row = {
            "name": loop["name"],
            "predicted_chart_trace": predicted_trace,
            "predicted_transition_signs": signs,
            "predicted_H": H,
            "predicted_S": S,
            "observed_chart_trace": observed_trace,
            "observed_signature": observed_sig,
            "matches": {
                "chart_trace": predicted_trace == observed_trace,
                "signature": [H, S] == observed_sig,
            },
        }
        out["loops"].append(row)

        print(
            f"{row['name']}: "
            f"trace_match={row['matches']['chart_trace']} "
            f"sig_match={row['matches']['signature']} "
            f"pred=({H},{S}) obs={tuple(observed_sig)}"
        )

    outpath = Path("specs/app/predicted_framed_signature_v0_1.json")
    outpath.write_text(json.dumps(out, indent=2))
    print()
    print(f"Wrote {outpath}")


if __name__ == "__main__":
    main()
