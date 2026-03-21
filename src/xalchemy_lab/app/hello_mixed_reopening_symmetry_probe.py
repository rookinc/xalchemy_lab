from __future__ import annotations

from xalchemy_lab.trurtle.vertex_controller import Arrival, VertexController


def route_once(A: int, sigma: int, tau: int, hand: str) -> str | None:
    controller = VertexController(
        vertex_id=f"vc_{A}{sigma}{tau}",
        incident_edges=["e_in", "e_left", "e_right"],
        routing_bias="state_sensitive",
        anchored_chart=A,
        sigma_state=sigma,
        tau_state=tau,
    )
    decision = controller.route(Arrival("T", 1, "e_in", hand))
    return decision.outgoing_edge


def main() -> None:
    s011_left = route_once(0, 1, 1, "left")
    s011_right = route_once(0, 1, 1, "right")
    s111_left = route_once(1, 1, 1, "left")
    s111_right = route_once(1, 1, 1, "right")

    print("HELLO MIXED REOPENING SYMMETRY PROBE")
    print()
    print(f"011 -> left={s011_left} right={s011_right}")
    print(f"111 -> left={s111_left} right={s111_right}")
    print()

    if s011_left == s111_left and s011_right == s111_right:
        print("physical-edge comparison: identical")
        print("111 matches 011 in literal edge labels")
    elif s011_left == s111_right and s011_right == s111_left:
        print("physical-edge comparison: reversed")
        print("111 is the literal edge-reversal of 011")
    else:
        print("physical-edge comparison: mixed")
        print("111 differs from 011, but not by a simple literal edge reversal")

    print()
    print("Interpretation note:")
    print("This probe compares literal edge labels only.")
    print("It does not decide chart-relative covariance by itself.")


if __name__ == "__main__":
    main()
