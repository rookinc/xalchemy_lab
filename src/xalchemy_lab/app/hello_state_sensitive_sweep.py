from __future__ import annotations

import json
from pathlib import Path

from xalchemy_lab.trurtle.vertex_controller import Arrival, VertexController


STATE_ORDER = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1),
]


def run_state_sensitive_case(A: int, sigma: int, tau: int) -> dict:
    controller = VertexController(
        vertex_id=f"vc_{A}{sigma}{tau}",
        incident_edges=["e_in", "e_left", "e_right"],
        routing_bias="state_sensitive",
        anchored_chart=A,
        sigma_state=sigma,
        tau_state=tau,
        load_override_threshold=1,
        yield_cooldown_ticks=2,
    )

    left = controller.route(
        Arrival(
            trurtle_id="L",
            trurtle_class=1,
            incoming_edge="e_in",
            handedness="left",
        )
    )
    right = controller.route(
        Arrival(
            trurtle_id="R",
            trurtle_class=1,
            incoming_edge="e_in",
            handedness="right",
        )
    )

    return {
        "state": f"{A}{sigma}{tau}",
        "mode": "state_sensitive",
        "left": {
            "outgoing_edge": left.outgoing_edge,
            "action": left.action,
            "switch_state": left.switch_state_update,
            "notes": left.notes,
        },
        "right": {
            "outgoing_edge": right.outgoing_edge,
            "action": right.action,
            "switch_state": right.switch_state_update,
            "notes": right.notes,
        },
        "route_counts": dict(controller.route_counts),
        "final_switch_state": controller.switch_state,
        "event_count": len(controller.controller_events),
    }


def run_under_load_case(A: int, sigma: int, tau: int) -> dict:
    controller = VertexController(
        vertex_id=f"vc_{A}{sigma}{tau}_load",
        incident_edges=["e_in", "e_left", "e_right"],
        routing_bias="state_sensitive_under_load",
        anchored_chart=A,
        sigma_state=sigma,
        tau_state=tau,
        load_override_threshold=1,
        yield_cooldown_ticks=2,
    )

    arrivals = [
        Arrival("T1", 1, "e_in", "left"),
        Arrival("T2", 1, "e_in", "left"),
        Arrival("T3", 1, "e_in", "right"),
    ]

    decisions = []
    for arrival in arrivals:
        d = controller.route(arrival)
        decisions.append(
            {
                "trurtle_id": arrival.trurtle_id,
                "handedness": arrival.handedness,
                "outgoing_edge": d.outgoing_edge,
                "action": d.action,
                "switch_state": d.switch_state_update,
                "notes": d.notes,
            }
        )

    override_events = [
        {
            "seq": e.seq,
            "event_type": e.event_type,
            "incoming_edge": e.incoming_edge,
            "outgoing_edge": e.outgoing_edge,
            "switch_state": e.switch_state,
            "note": e.note,
        }
        for e in controller.controller_events
        if e.event_type in {"override", "switch_to_flipped", "cooldown_tick", "switch_to_neutral"}
    ]

    return {
        "state": f"{A}{sigma}{tau}",
        "mode": "state_sensitive_under_load",
        "decisions": decisions,
        "route_counts": dict(controller.route_counts),
        "final_switch_state": controller.switch_state,
        "cooldown_left": controller.switch_cooldown_remaining,
        "override_trace": override_events,
        "event_count": len(controller.controller_events),
    }


def main() -> None:
    print("HELLO STATE-SENSITIVE SWEEP")

    payload = {
        "name": "state_sensitive_routing_sweep_v0_1",
        "version": "0.1",
        "states": [],
    }

    for A, sigma, tau in STATE_ORDER:
        payload["states"].append(
            {
                "state": f"{A}{sigma}{tau}",
                "structural_register": {
                    "A": A,
                    "sigma": sigma,
                    "tau": tau,
                },
                "state_sensitive": run_state_sensitive_case(A, sigma, tau),
                "state_sensitive_under_load": run_under_load_case(A, sigma, tau),
            }
        )

    outdir = Path("specs/app")
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "state_sensitive_routing_sweep_v0_1.json"
    outpath.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {outpath}")

    print()
    print("SUMMARY")
    for entry in payload["states"]:
        s = entry["state"]
        ss = entry["state_sensitive"]
        ul = entry["state_sensitive_under_load"]
        print(
            f"state={s} "
            f"base[L->{ss['left']['outgoing_edge']},R->{ss['right']['outgoing_edge']}] "
            f"load_final={ul['final_switch_state']} "
            f"routes={ul['route_counts']}"
        )


if __name__ == "__main__":
    main()
