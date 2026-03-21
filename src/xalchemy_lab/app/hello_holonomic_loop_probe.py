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


def route_once(controller: VertexController, hand: str, step: int) -> dict:
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
        "handedness": hand,
        "physical_exit": decision.outgoing_edge,
        "chart_exit": to_chart_coordinate(controller.anchored_chart, decision.outgoing_edge),
        "switch_state": decision.switch_state_update,
        "notes": decision.notes,
    }


def controller_payload(name: str, A: int, sigma: int, tau: int) -> VertexController:
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


def main() -> None:
    print("HELLO HOLONOMIC LOOP PROBE")
    print()

    # same physical-looking mixed reopening at two different charts
    v011 = controller_payload("v011", 0, 1, 1)
    v111 = controller_payload("v111", 1, 1, 1)

    sequence = ["left", "right", "left"]

    out = {
        "name": "holonomic_loop_probe_v0_1",
        "sequence": sequence,
        "controllers": {},
    }

    for controller in [v011, v111]:
        print(f"=== {controller.vertex_id} : (A,sigma,tau)=({controller.anchored_chart},{controller.sigma_state},{controller.tau_state}) ===")
        routes = []
        for i, hand in enumerate(sequence, start=1):
            rec = route_once(controller, hand, i)
            routes.append(rec)
            print(
                f"step={i} hand={hand:<5} "
                f"physical={rec['physical_exit']:<7} "
                f"chart={rec['chart_exit']:<11} "
                f"state={rec['switch_state']}"
            )
        summary = summarize_controller(controller)
        out["controllers"][controller.vertex_id] = {
            "routes": routes,
            "summary": summary,
        }
        print("summary =", summary)
        print()

    outpath = Path("export/holonomic_loop_probe_v0_1.json")
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(json.dumps(out, indent=2))
    print(f"Wrote {outpath}")


if __name__ == "__main__":
    main()
