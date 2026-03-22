from __future__ import annotations

import json
from dataclasses import asdict, dataclass
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


def chart_value(symbol: str | None) -> int:
    if symbol == "chart_left":
        return -1
    if symbol == "chart_right":
        return 1
    return 0


def transition_sign(prev_chart: str | None, curr_chart: str | None) -> int | None:
    if prev_chart is None or curr_chart is None:
        return None
    return 1 if prev_chart == curr_chart else -1


@dataclass
class FramedAccumulator:
    prev_chart: str | None = None
    H: int = 1
    S: int = 0

    def update(self, curr_chart: str | None) -> dict:
        omega = transition_sign(self.prev_chart, curr_chart)
        if omega is not None:
            self.H *= omega
        self.S += chart_value(curr_chart)
        self.prev_chart = curr_chart
        return {
            "transition_sign": omega,
            "running_H": self.H,
            "running_S": self.S,
            "prev_chart": self.prev_chart,
        }


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


def run_route(controller: VertexController, hand: str, step: int, acc: FramedAccumulator) -> dict:
    decision = controller.route(
        Arrival(
            trurtle_id="N1",
            trurtle_class=1,
            incoming_edge="e_in",
            handedness=hand,
            step_count=step,
        )
    )
    chart_exit = to_chart_coordinate(controller.anchored_chart, decision.outgoing_edge)
    acc_update = acc.update(chart_exit)

    return {
        "vertex_id": controller.vertex_id,
        "A": controller.anchored_chart,
        "sigma": controller.sigma_state,
        "tau": controller.tau_state,
        "handedness": hand,
        "physical_exit": decision.outgoing_edge,
        "chart_exit": chart_exit,
        "switch_state": decision.switch_state_update,
        "notes": decision.notes,
        **acc_update,
    }


def run_loop(name: str, controller_specs: list[tuple[str, int, int, int]], hand_sequence: list[str]) -> dict:
    controllers = [make_controller(*spec) for spec in controller_specs]
    acc = FramedAccumulator()
    steps = []

    for i, (controller, hand) in enumerate(zip(controllers, hand_sequence), start=1):
        steps.append(run_route(controller, hand, i, acc))

    return {
        "name": name,
        "controller_specs": [
            {"vertex_id": c.vertex_id, "A": c.anchored_chart, "sigma": c.sigma_state, "tau": c.tau_state}
            for c in controllers
        ],
        "hand_sequence": hand_sequence,
        "steps": steps,
        "final_accumulator": asdict(acc),
        "signature": [acc.H, acc.S],
    }


def main() -> None:
    print("HELLO NATIVE FRAMED ACCUMULATOR")
    print()

    loops = [
        run_loop(
            "return_A",
            [("a1", 0, 1, 1), ("a2", 0, 1, 1), ("a3", 0, 1, 1)],
            ["left", "right", "left"],
        ),
        run_loop(
            "return_B",
            [("b1", 1, 1, 1), ("b2", 1, 1, 1), ("b3", 1, 1, 1)],
            ["left", "right", "left"],
        ),
        run_loop(
            "return_C_mixed_chart",
            [("c1", 0, 1, 1), ("c2", 1, 1, 1), ("c3", 0, 1, 1)],
            ["left", "right", "left"],
        ),
        run_loop(
            "return_D_unary_mixed",
            [("d1", 0, 0, 1), ("d2", 1, 1, 0), ("d3", 0, 1, 1)],
            ["left", "left", "right"],
        ),
    ]

    payload = {
        "name": "native_framed_accumulator_v0_1",
        "loops": loops,
    }

    outpath = Path("specs/app/native_framed_accumulator_v0_1.json")
    outpath.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {outpath}")
    print()

    for loop in loops:
        print(f"{loop['name']}: signature={tuple(loop['signature'])} final_acc={loop['final_accumulator']}")

if __name__ == "__main__":
    main()
