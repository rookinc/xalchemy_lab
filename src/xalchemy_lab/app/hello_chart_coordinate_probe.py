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


def main() -> None:
    s011_left = route_once(0, 1, 1, "left")
    s011_right = route_once(0, 1, 1, "right")
    s111_left = route_once(1, 1, 1, "left")
    s111_right = route_once(1, 1, 1, "right")

    print("HELLO CHART COORDINATE PROBE")
    print()
    print(f"011 physical -> left={s011_left} right={s011_right}")
    print(
        f"011 chart    -> left={to_chart_coordinate(0, s011_left)} "
        f"right={to_chart_coordinate(0, s011_right)}"
    )
    print()
    print(f"111 physical -> left={s111_left} right={s111_right}")
    print(
        f"111 chart    -> left={to_chart_coordinate(1, s111_left)} "
        f"right={to_chart_coordinate(1, s111_right)}"
    )
    print()

    a_left = to_chart_coordinate(0, s011_left)
    a_right = to_chart_coordinate(0, s011_right)
    b_left = to_chart_coordinate(1, s111_left)
    b_right = to_chart_coordinate(1, s111_right)

    if a_left == b_left and a_right == b_right:
        print("chart-coordinate comparison: identical")
        print("mixed reopening is chart-stable")
    elif a_left == b_right and a_right == b_left:
        print("chart-coordinate comparison: reversed")
        print("mixed reopening is chart-reversed")
    else:
        print("chart-coordinate comparison: mixed")
        print("mixed reopening differs in chart coordinates too")


if __name__ == "__main__":
    main()
