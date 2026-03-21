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


def main() -> None:
    print("HELLO STATE-SENSITIVE TABLE")
    print()
    print("Current controller behavior table")
    print()

    for A, sigma, tau in STATE_ORDER:
        controller = VertexController(
            vertex_id=f"vc_{A}{sigma}{tau}",
            incident_edges=["e_in", "e_left", "e_right"],
            routing_bias="state_sensitive",
            anchored_chart=A,
            sigma_state=sigma,
            tau_state=tau,
        )

        left_decision = controller.route(
            Arrival(
                trurtle_id="L",
                trurtle_class=1,
                incoming_edge="e_in",
                handedness="left",
            )
        )
        right_decision = controller.route(
            Arrival(
                trurtle_id="R",
                trurtle_class=1,
                incoming_edge="e_in",
                handedness="right",
            )
        )

        print(
            f"state={A}{sigma}{tau} "
            f"left->{left_decision.outgoing_edge} "
            f"right->{right_decision.outgoing_edge}"
        )


if __name__ == "__main__":
    main()
