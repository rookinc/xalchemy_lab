from __future__ import annotations

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


def route_once(A: int, sigma: int, tau: int, hand: str) -> str | None:
    controller = VertexController(
        vertex_id=f"vc_{A}{sigma}{tau}",
        incident_edges=["e_in", "e_left", "e_right"],
        routing_bias="state_sensitive",
        anchored_chart=A,
        sigma_state=sigma,
        tau_state=tau,
    )
    decision = controller.route(
        Arrival(
            trurtle_id=hand[:1].upper(),
            trurtle_class=1,
            incoming_edge="e_in",
            handedness=hand,
        )
    )
    return decision.outgoing_edge


def main() -> None:
    print("HELLO STATE-SENSITIVE TABLE")
    print()
    print("Current controller behavior table")
    print()

    for A, sigma, tau in STATE_ORDER:
        left_out = route_once(A, sigma, tau, "left")
        right_out = route_once(A, sigma, tau, "right")

        print(
            f"state={A}{sigma}{tau} "
            f"left->{left_out} "
            f"right->{right_out}"
        )


if __name__ == "__main__":
    main()
