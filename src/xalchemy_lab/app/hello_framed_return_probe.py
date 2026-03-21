from __future__ import annotations

import json
from pathlib import Path

from xalchemy_lab.trurtle.vertex_controller import Arrival, VertexController


def to_chart_coordinate(A: int, edge: str | None) -> str | None:
    if edge is None:
        return None
    if A == 0:
        if edge == "e_left":
            return "chart_left"
        if edge == "e_right":
            return "chart_right"
    else:
        if edge == "e_right":
            return "chart_left"
        if edge == "e_left":
            return "chart_right"
    return f"unknown:{edge}"


def transition_sign(prev_chart: str | None, curr_chart: str | None) -> int | None:
    if prev_chart is None or curr_chart is None:
        return None
    return 1 if prev_chart == curr_chart else -1


def classify_return(initial_frame: str, final_frame: str) -> str:
    if initial_frame == final_frame:
        return "same"
    if {initial_frame, final_frame} == {"chart_left", "chart_right"}:
        return "reversed"
    if initial_frame.startswith("unknown") or final_frame.startswith("unknown"):
        return "ambiguous"
    return "shifted"


def make_controller(name: str, A: int, sigma: int, tau: int) -> VertexController:
    return VertexController(
        vertex_id=name,
        incident_edges=["e_in", "e_left", "e_right"],
        routing_bias="state_sensitive_under_load",
        load_override_threshold=1,
        yield_cooldown_ticks=2,
        anchored_chart=A,
        sigma_state=sigma,
        tau_state=tau,
    )


def run_route(controller: VertexController, hand: str, step: int) -> dict:
    decision = controller.route(
        Arrival(
            trurtle_id="R1",
            trurtle_class=1,
            incoming_edge="e_in",
            handedness=hand,
            step_count=step,
        )
    )
    return {
        "vertex_id": controller.vertex_id,
        "A": controller.anchored_chart,
        "sigma": controller.sigma_state,
        "tau": controller.tau_state,
        "handedness": hand,
        "physical_exit": decision.outgoing_edge,
        "chart_exit": to_chart_coordinate(controller.anchored_chart, decision.outgoing_edge),
        "switch_state": decision.switch_state_update,
        "notes": decision.notes,
    }


def run_loop(name: str, controller_specs: list[tuple[str, int, int, int]], hand_sequence: list[str]) -> dict:
    controllers = [make_controller(*spec) for spec in controller_specs]
    steps = []

    running_H = 1
    previous_chart: str | None = None

    for i, (controller, hand) in enumerate(zip(controllers, hand_sequence), start=1):
        step = run_route(controller, hand, i)
        curr_chart = step["chart_exit"]
        omega = transition_sign(previous_chart, curr_chart)

        if omega is None:
            running_H = 1
        else:
            running_H *= omega

        step["transition_sign"] = omega
        step["running_H"] = running_H

        steps.append(step)
        previous_chart = curr_chart

    chart_trace = [s["chart_exit"] for s in steps]
    physical_trace = [s["physical_exit"] for s in steps]
    transition_signs = [s["transition_sign"] for s in steps if s["transition_sign"] is not None]

    initial_frame = chart_trace[0] if chart_trace else "ambiguous"
    final_frame = chart_trace[-1] if chart_trace else "ambiguous"
    return_class = classify_return(initial_frame, final_frame)

    return {
        "name": name,
        "controller_specs": [
            {"vertex_id": c.vertex_id, "A": c.anchored_chart, "sigma": c.sigma_state, "tau": c.tau_state}
            for c in controllers
        ],
        "hand_sequence": hand_sequence,
        "steps": steps,
        "physical_trace": physical_trace,
        "chart_trace": chart_trace,
        "transition_signs": transition_signs,
        "H": running_H,
        "initial_frame": initial_frame,
        "final_frame": final_frame,
        "return_class": return_class,
    }


def main() -> None:
    print("HELLO FRAMED RETURN PROBE")
    print()

    loops = [
        run_loop(
            "return_A",
            [("rA1", 0, 1, 1), ("rA2", 0, 1, 1), ("rA3", 0, 1, 1)],
            ["left", "right", "left"],
        ),
        run_loop(
            "return_B",
            [("rB1", 1, 1, 1), ("rB2", 1, 1, 1), ("rB3", 1, 1, 1)],
            ["left", "right", "left"],
        ),
        run_loop(
            "return_C_mixed_chart",
            [("rC1", 0, 1, 1), ("rC2", 1, 1, 1), ("rC3", 0, 1, 1)],
            ["left", "right", "left"],
        ),
        run_loop(
            "return_D_unary_mixed",
            [("rD1", 0, 0, 1), ("rD2", 1, 1, 0), ("rD3", 0, 1, 1)],
            ["left", "left", "right"],
        ),
    ]

    payload = {
        "name": "framed_return_probe_v0_1",
        "loops": loops,
    }

    outpath = Path("specs/app/framed_return_probe_v0_1.json")
    outpath.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {outpath}")
    print()

    for loop in loops:
        print(f"=== {loop['name']} ===")
        print("physical_trace =", loop["physical_trace"])
        print("chart_trace    =", loop["chart_trace"])
        print("transition_signs =", loop["transition_signs"])
        print("H              =", loop["H"])
        print("initial_frame  =", loop["initial_frame"])
        print("final_frame    =", loop["final_frame"])
        print("return_class   =", loop["return_class"])
        print()


if __name__ == "__main__":
    main()
