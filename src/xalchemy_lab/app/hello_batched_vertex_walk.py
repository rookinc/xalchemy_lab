from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from xalchemy_lab.trurtle.batched_vertex_walk import (
    Trurtle,
    batch_step,
    build_toy_network,
    idle_all_controllers,
    summarize_controllers,
    summarize_edges,
    summarize_trurtles,
)


def print_trurtles(trurtles: list[Trurtle]) -> None:
    print("\nTRURTLES")
    for t in trurtles:
        print(
            f"  {t.trurtle_id}: class={t.trurtle_class} "
            f"vertex={t.current_vertex} in={t.incoming_edge} "
            f"hand={t.handedness} status={t.status} steps={t.step_count}"
        )


def print_edges(edge_summary: dict[str, dict]) -> None:
    print("\nEDGES")
    for edge_id, data in sorted(edge_summary.items()):
        print(
            f"  {edge_id}: endpoints={data['endpoints']} "
            f"touches={data['touch_count']} classes={data['classes_present']}"
        )


def print_controllers(controller_summary: dict[str, dict]) -> None:
    print("\nCONTROLLERS")
    for vertex_id, data in sorted(controller_summary.items()):
        print(
            f"  {vertex_id}: bias={data['routing_bias']} "
            f"threshold={data['threshold']} state={data['switch_state']} "
            f"cooldown={data['cooldown_left']} routes={data['route_counts']} "
            f"coupling={data['coupling_count']}"
        )


def main() -> None:
    controllers, edges = build_toy_network()
    trurtles = [
        Trurtle("T1", 1, "v0", "e02", "left"),
        Trurtle("T2", 2, "v1", "e12", "right"),
        Trurtle("T3", 3, "v2", "e23", "left"),
    ]

    all_trurtle_events: list[dict] = []

    print("HELLO BATCHED VERTEX WALK")
    print_trurtles(trurtles)

    max_ticks = 8
    for tick in range(1, max_ticks + 1):
        print(f"\n==================== TICK {tick} ====================")

        events = batch_step(tick, trurtles, controllers, edges)
        for e in events:
            all_trurtle_events.append(asdict(e))
            print(
                f"{e.tick:02d} | {e.trurtle_id:>2} | {e.event_type:<12} "
                f"| vertex={e.vertex_id} in={e.incoming_edge} out={e.outgoing_edge} "
                f"| {e.note}"
            )

        idle_all_controllers(controllers)

        print_trurtles(trurtles)
        print_edges(summarize_edges(edges))
        print_controllers(summarize_controllers(controllers))

        if all(t.status == "halted" for t in trurtles):
            print("\nAll trurtles halted.")
            break

    outdir = Path("export")
    outdir.mkdir(exist_ok=True)

    summary = {
        "name": "batched_vertex_walk_demo",
        "ticks": max_ticks,
        "trurtles": summarize_trurtles(trurtles),
        "edges": summarize_edges(edges),
        "controllers": summarize_controllers(controllers),
        "trurtle_events": all_trurtle_events,
    }

    outpath = outdir / "batched_vertex_walk_demo.json"
    outpath.write_text(json.dumps(summary, indent=2))
    print(f"\nWrote {outpath}")


if __name__ == "__main__":
    main()
