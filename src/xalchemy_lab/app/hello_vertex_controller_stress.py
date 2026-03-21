from __future__ import annotations

from xalchemy_lab.trurtle.vertex_controller import Arrival, VertexController


def print_controller_state(controller: VertexController) -> None:
    print("\nCONTROLLER STATE")
    print(f"  vertex_id      = {controller.vertex_id}")
    print(f"  incident_edges = {controller.incident_edges}")
    print(f"  routing_bias   = {controller.routing_bias}")
    print(f"  threshold      = {controller.load_override_threshold}")
    print(f"  yield_cooldown = {controller.yield_cooldown_ticks}")
    print(f"  switch_state   = {controller.switch_state}")
    print(f"  cooldown_left  = {controller.switch_cooldown_remaining}")
    print(f"  route_counts   = {controller.route_counts}")
    print(f"  recent_arrivals= {len(controller.recent_arrivals)}")
    print(f"  controller_events = {len(controller.controller_events)}")


def print_controller_events(controller: VertexController) -> None:
    print("\n=== CONTROLLER EVENTS ===")
    for e in controller.controller_events:
        print(
            f"{e.seq:02d} | {e.event_type:<18} | trurtle={e.trurtle_id} "
            f"| in={e.incoming_edge} out={e.outgoing_edge} "
            f"| state={e.switch_state} | {e.note}"
        )


def main() -> None:
    controller = VertexController(
        vertex_id="v_stress",
        incident_edges=["e_in", "e_left", "e_right"],
        routing_bias="polarity_under_load",
        load_override_threshold=1,
        yield_cooldown_ticks=2,
    )

    print("HELLO VERTEX CONTROLLER STRESS")
    print("\nGoal: force polarity-under-load override and cooldown recovery.")

    arrivals = [
        Arrival("S1", 1, "e_in", "left", "v_prev", 1),
        Arrival("S2", 1, "e_in", "left", "v_prev", 2),
        Arrival("S3", 1, "e_in", "left", "v_prev", 3),
        Arrival("S4", 1, "e_in", "left", "v_prev", 4),
    ]

    print("\n=== STRESS ARRIVALS ===")
    for arrival in arrivals:
        decision = controller.route(arrival)
        print(
            f"{arrival.trurtle_id} arrives on {arrival.incoming_edge} "
            f"hand={arrival.handedness} -> action={decision.action} "
            f"outgoing={decision.outgoing_edge} state={decision.switch_state_update} "
            f"note={decision.notes}"
        )
        print_controller_state(controller)

    print("\n=== IDLE RECOVERY ===")
    for tick in range(1, 5):
        controller.idle_tick()
        print(f"idle_tick={tick}")
        print_controller_state(controller)

    print_controller_events(controller)


if __name__ == "__main__":
    main()
