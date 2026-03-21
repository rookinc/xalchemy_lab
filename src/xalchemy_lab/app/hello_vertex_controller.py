from __future__ import annotations

from xalchemy_lab.trurtle.vertex_controller import Arrival, VertexController


def print_controller_state(controller: VertexController) -> None:
    print("\nCONTROLLER STATE")
    print(f"  vertex_id      = {controller.vertex_id}")
    print(f"  incident_edges = {controller.incident_edges}")
    print(f"  routing_bias   = {controller.routing_bias}")
    print(f"  threshold      = {controller.load_override_threshold}")
    print(f"  yield_cooldown = {controller.yield_cooldown_ticks}")
    print(f"  classes_seen   = {sorted(controller.classes_seen)}")
    print(f"  coupling_count = {controller.coupling_count}")
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


def run_demo(routing_bias: str, threshold: int = 1, cooldown: int = 0) -> None:
    controller = VertexController(
        vertex_id="v0",
        incident_edges=["e0", "e1", "e2"],
        routing_bias=routing_bias,
        load_override_threshold=threshold,
        yield_cooldown_ticks=cooldown,
    )

    print(f"\n==============================")
    print(f"ROUTING BIAS: {routing_bias} (threshold={threshold}, cooldown={cooldown})")
    print(f"==============================")

    print("\n=== SINGLE ARRIVAL ===")
    a1 = Arrival(
        trurtle_id="T1",
        trurtle_class=1,
        incoming_edge="e0",
        handedness="left",
        previous_vertex="v_prev",
        step_count=1,
    )
    d1 = controller.route(a1)
    print(
        f"{a1.trurtle_id} arrives on {a1.incoming_edge} hand={a1.handedness} "
        f"-> action={d1.action} outgoing={d1.outgoing_edge} note={d1.notes}"
    )
    print_controller_state(controller)

    print("\n=== SINGLE ARRIVAL, OPPOSITE HAND ===")
    a2 = Arrival(
        trurtle_id="T2",
        trurtle_class=2,
        incoming_edge="e1",
        handedness="right",
        previous_vertex="v_prev",
        step_count=1,
    )
    d2 = controller.route(a2)
    print(
        f"{a2.trurtle_id} arrives on {a2.incoming_edge} hand={a2.handedness} "
        f"-> action={d2.action} outgoing={d2.outgoing_edge} note={d2.notes}"
    )
    print_controller_state(controller)

    print("\n=== SIMULTANEOUS ARRIVALS ===")
    arrivals = [
        Arrival(
            trurtle_id="T3",
            trurtle_class=3,
            incoming_edge="e0",
            handedness="left",
            previous_vertex="v_prev",
            step_count=2,
        ),
        Arrival(
            trurtle_id="T4",
            trurtle_class=2,
            incoming_edge="e2",
            handedness="right",
            previous_vertex="v_prev",
            step_count=2,
        ),
    ]
    results = controller.resolve_simultaneous_arrivals(arrivals)
    for arrival, decision in results:
        print(
            f"{arrival.trurtle_id} arrives on {arrival.incoming_edge} "
            f"class={arrival.trurtle_class} hand={arrival.handedness} "
            f"-> action={decision.action} outgoing={decision.outgoing_edge} "
            f"hand_update={decision.handedness_update} note={decision.notes}"
        )
    print_controller_state(controller)

    print("\n=== STRESS ARRIVALS ===")
    stress_arrivals = [
        Arrival(
            trurtle_id="T5",
            trurtle_class=1,
            incoming_edge="e0",
            handedness="left",
            previous_vertex="v_prev",
            step_count=3,
        ),
        Arrival(
            trurtle_id="T6",
            trurtle_class=3,
            incoming_edge="e2",
            handedness="right",
            previous_vertex="v_prev",
            step_count=3,
        ),
    ]
    for arrival in stress_arrivals:
        decision = controller.route(arrival)
        print(
            f"{arrival.trurtle_id} arrives on {arrival.incoming_edge} "
            f"class={arrival.trurtle_class} hand={arrival.handedness} "
            f"-> action={decision.action} outgoing={decision.outgoing_edge} "
            f"note={decision.notes}"
        )
    print_controller_state(controller)

    print("\n=== RECOVERY IDLE TICKS ===")
    for tick in range(1, cooldown + 2):
        controller.idle_tick()
        print(f"idle_tick={tick}")
        print_controller_state(controller)

    print_controller_events(controller)


def main() -> None:
    print("HELLO VERTEX CONTROLLER")

    run_demo("handedness_first")
    run_demo("least_used")
    run_demo("polarity_under_load", threshold=1, cooldown=2)
    run_demo("polarity_under_load", threshold=2, cooldown=2)


if __name__ == "__main__":
    main()
