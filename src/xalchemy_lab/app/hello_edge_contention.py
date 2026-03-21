from __future__ import annotations

from xalchemy_lab.trurtle.batched_vertex_walk import (
    Edge,
    Trurtle,
    batch_step,
    idle_all_controllers,
    summarize_controllers,
    summarize_edges,
    summarize_trurtles,
)
from xalchemy_lab.trurtle.vertex_controller import VertexController


def build_contention_network():
    edges = {
        "e12": Edge("e12", ("v1", "v2")),
    }

    controllers = {
        "v1": VertexController(
            vertex_id="v1",
            incident_edges=["e12"],
            routing_bias="handedness_first",
            load_override_threshold=1,
            yield_cooldown_ticks=1,
        ),
        "v2": VertexController(
            vertex_id="v2",
            incident_edges=["e12"],
            routing_bias="handedness_first",
            load_override_threshold=1,
            yield_cooldown_ticks=1,
        ),
    }

    trurtles = [
        Trurtle("T1", 1, "v1", "stub_v1", "left"),
        Trurtle("T2", 2, "v2", "stub_v2", "right"),
    ]

    return controllers, edges, trurtles


def print_trurtles(trurtles):
    print("\nTRURTLES")
    for t in trurtles:
        print(
            f"  {t.trurtle_id}: class={t.trurtle_class} "
            f"vertex={t.current_vertex} in={t.incoming_edge} "
            f"hand={t.handedness} status={t.status} steps={t.step_count}"
        )


def print_edges(edge_summary):
    print("\nEDGES")
    for edge_id, data in sorted(edge_summary.items()):
        print(
            f"  {edge_id}: endpoints={data['endpoints']} "
            f"touches={data['touch_count']} contention={data['contention_count']} "
            f"classes={data['classes_present']}"
        )


def print_controllers(controller_summary):
    print("\nCONTROLLERS")
    for vertex_id, data in sorted(controller_summary.items()):
        print(
            f"  {vertex_id}: bias={data['routing_bias']} "
            f"state={data['switch_state']} cooldown={data['cooldown_left']} "
            f"routes={data['route_counts']} coupling={data['coupling_count']}"
        )


def run_demo(channel_rule: str) -> None:
    controllers, edges, trurtles = build_contention_network()

    print(f"\n========================================")
    print(f"ROUND 1. FIGHT! channel_rule={channel_rule}")
    print(f"========================================")
    print_trurtles(trurtles)

    events = batch_step(
        tick=1,
        trurtles=trurtles,
        controllers=controllers,
        edges=edges,
        channel_rule=channel_rule,
    )
    for e in events:
        print(
            f"{e.tick:02d} | {e.trurtle_id:>2} | {e.event_type:<14} "
            f"| vertex={e.vertex_id} in={e.incoming_edge} out={e.outgoing_edge} "
            f"| {e.note}"
        )

    idle_all_controllers(controllers)

    print_trurtles(trurtles)
    print_edges(summarize_edges(edges))
    print_controllers(summarize_controllers(controllers))


def main() -> None:
    print("HELLO EDGE CONTENTION")
    for channel_rule in (
        "bidirectional_ok",
        "same_direction_only",
        "contention_creates_coupling",
        "single_occupancy",
    ):
        run_demo(channel_rule)


if __name__ == "__main__":
    main()
