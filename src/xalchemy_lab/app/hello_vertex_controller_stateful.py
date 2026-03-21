from __future__ import annotations

from xalchemy_lab.trurtle.vertex_controller import Arrival, VertexController


def run_demo(name: str, *, A: int, sigma: int, tau: int, bias: str) -> None:
    controller = VertexController(
        vertex_id=name,
        incident_edges=["e_in", "e_left", "e_right"],
        routing_bias=bias,
        load_override_threshold=1,
        yield_cooldown_ticks=2,
        anchored_chart=A,
        sigma_state=sigma,
        tau_state=tau,
    )

    print("\n==============================")
    print(f"STATEFUL CONTROLLER: {name}")
    print(f"(A,sigma,tau)=({A},{sigma},{tau}) bias={bias}")
    print("==============================")

    arrivals = [
        Arrival("T1", 1, "e_in", "left", "v_prev", 1),
        Arrival("T2", 1, "e_in", "left", "v_prev", 2),
        Arrival("T3", 1, "e_in", "right", "v_prev", 3),
    ]

    for arrival in arrivals:
        decision = controller.route(arrival)
        print(
            f"{arrival.trurtle_id}: hand={arrival.handedness} "
            f"-> out={decision.outgoing_edge} state={decision.switch_state_update} "
            f"note={decision.notes}"
        )

    print("route_counts =", controller.route_counts)
    print("switch_state =", controller.switch_state)
    print("events:")
    for e in controller.controller_events:
        print(
            f"  {e.seq:02d} {e.event_type:<18} "
            f"A={e.anchored_chart} sigma={e.sigma_state} tau={e.tau_state} "
            f"in={e.incoming_edge} out={e.outgoing_edge} note={e.note}"
        )


def main() -> None:
    print("HELLO VERTEX CONTROLLER STATEFUL")
    run_demo("vc_001", A=0, sigma=0, tau=1, bias="state_sensitive")
    run_demo("vc_011", A=0, sigma=1, tau=1, bias="state_sensitive")
    run_demo("vc_100", A=1, sigma=0, tau=0, bias="state_sensitive")
    run_demo("vc_111", A=1, sigma=1, tau=1, bias="state_sensitive_under_load")


if __name__ == "__main__":
    main()
