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
            trurtle_id="H1",
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


def summarize_controller(c: VertexController) -> dict:
    return {
        "vertex_id": c.vertex_id,
        "A": c.anchored_chart,
        "sigma": c.sigma_state,
        "tau": c.tau_state,
        "switch_state": c.switch_state,
        "cooldown_left": c.switch_cooldown_remaining,
        "route_counts": dict(c.route_counts),
        "event_count": len(c.controller_events),
    }


def run_loop(name: str, controller_specs: list[tuple[str, int, int, int]], hand_sequence: list[str]) -> dict:
    controllers = [make_controller(*spec) for spec in controller_specs]
    steps = []

    for i, (controller, hand) in enumerate(zip(controllers, hand_sequence), start=1):
        steps.append(run_route(controller, hand, i))

    return {
        "name": name,
        "controller_specs": [
            {"vertex_id": c.vertex_id, "A": c.anchored_chart, "sigma": c.sigma_state, "tau": c.tau_state}
            for c in controllers
        ],
        "hand_sequence": hand_sequence,
        "steps": steps,
        "physical_trace": [s["physical_exit"] for s in steps],
        "chart_trace": [s["chart_exit"] for s in steps],
        "controller_summaries": [summarize_controller(c) for c in controllers],
    }


def main() -> None:
    print("HELLO MULTI-CONTROLLER HOLONOMY PROBE")
    print()

    hand_sequence = ["left", "right", "left"]

    loop_a = run_loop(
        "loop_A",
        [
            ("vA1", 0, 1, 1),
            ("vA2", 0, 1, 1),
            ("vA3", 0, 1, 1),
        ],
        hand_sequence,
    )

    loop_b = run_loop(
        "loop_B",
        [
            ("vB1", 1, 1, 1),
            ("vB2", 1, 1, 1),
            ("vB3", 1, 1, 1),
        ],
        hand_sequence,
    )

    loop_c = run_loop(
        "loop_C_mixed_chart",
        [
            ("vC1", 0, 1, 1),
            ("vC2", 1, 1, 1),
            ("vC3", 0, 1, 1),
        ],
        hand_sequence,
    )

    payload = {
        "name": "multi_controller_holonomy_probe_v0_1",
        "loops": [loop_a, loop_b, loop_c],
    }

    for loop in payload["loops"]:
        print(f"=== {loop['name']} ===")
        print("physical_trace =", loop["physical_trace"])
        print("chart_trace    =", loop["chart_trace"])
        print()

    outpath = Path("export/multi_controller_holonomy_probe_v0_1.json")
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {outpath}")


if __name__ == "__main__":
    main()
