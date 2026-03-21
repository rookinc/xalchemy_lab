from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Literal

from xalchemy_lab.trurtle.vertex_controller import Arrival, VertexController


Handedness = Literal["left", "right"]
Status = Literal["active", "halted"]


@dataclass
class Edge:
    edge_id: str
    endpoints: tuple[str, str]
    touch_count: int = 0
    trurtle_ids: list[str] = field(default_factory=list)
    classes_present: list[int] = field(default_factory=list)

    def other_vertex(self, vertex_id: str) -> str:
        a, b = self.endpoints
        if vertex_id == a:
            return b
        if vertex_id == b:
            return a
        raise ValueError(f"vertex {vertex_id} not incident to edge {self.edge_id}")


@dataclass
class Trurtle:
    trurtle_id: str
    trurtle_class: int
    current_vertex: str
    incoming_edge: str
    handedness: Handedness
    status: Status = "active"
    step_count: int = 0


@dataclass
class TrurtleEvent:
    tick: int
    trurtle_id: str
    event_type: str
    vertex_id: str | None = None
    incoming_edge: str | None = None
    outgoing_edge: str | None = None
    note: str = ""


def build_toy_network() -> tuple[dict[str, VertexController], dict[str, Edge]]:
    edges = {
        "e01": Edge("e01", ("v0", "v1")),
        "e02": Edge("e02", ("v0", "v2")),
        "e12": Edge("e12", ("v1", "v2")),
        "e13": Edge("e13", ("v1", "v3")),
        "e23": Edge("e23", ("v2", "v3")),
    }

    incident = {
        "v0": ["e01", "e02"],
        "v1": ["e01", "e12", "e13"],
        "v2": ["e02", "e12", "e23"],
        "v3": ["e13", "e23"],
    }

    controllers = {
        "v0": VertexController(
            vertex_id="v0",
            incident_edges=incident["v0"],
            routing_bias="polarity_under_load",
            load_override_threshold=1,
            yield_cooldown_ticks=2,
        ),
        "v1": VertexController(
            vertex_id="v1",
            incident_edges=incident["v1"],
            routing_bias="handedness_first",
            load_override_threshold=1,
            yield_cooldown_ticks=2,
        ),
        "v2": VertexController(
            vertex_id="v2",
            incident_edges=incident["v2"],
            routing_bias="least_used",
            load_override_threshold=1,
            yield_cooldown_ticks=2,
        ),
        "v3": VertexController(
            vertex_id="v3",
            incident_edges=incident["v3"],
            routing_bias="polarity_under_load",
            load_override_threshold=2,
            yield_cooldown_ticks=2,
        ),
    }

    return controllers, edges


def apply_edge_traversal(edge: Edge, trurtle: Trurtle) -> None:
    edge.touch_count += 1
    edge.trurtle_ids.append(trurtle.trurtle_id)
    edge.classes_present.append(trurtle.trurtle_class)


def step_trurtle(
    tick: int,
    trurtle: Trurtle,
    controllers: dict[str, VertexController],
    edges: dict[str, Edge],
) -> list[TrurtleEvent]:
    events: list[TrurtleEvent] = []

    if trurtle.status != "active":
        return events

    controller = controllers[trurtle.current_vertex]
    arrival = Arrival(
        trurtle_id=trurtle.trurtle_id,
        trurtle_class=trurtle.trurtle_class,
        incoming_edge=trurtle.incoming_edge,
        handedness=trurtle.handedness,
        previous_vertex=None,
        step_count=trurtle.step_count,
    )

    decision = controller.route(arrival)

    events.append(
        TrurtleEvent(
            tick=tick,
            trurtle_id=trurtle.trurtle_id,
            event_type="arrive",
            vertex_id=trurtle.current_vertex,
            incoming_edge=trurtle.incoming_edge,
            outgoing_edge=decision.outgoing_edge,
            note=decision.notes,
        )
    )

    if decision.action != "route" or decision.outgoing_edge is None:
        trurtle.status = "halted"
        events.append(
            TrurtleEvent(
                tick=tick,
                trurtle_id=trurtle.trurtle_id,
                event_type="halt",
                vertex_id=trurtle.current_vertex,
                incoming_edge=trurtle.incoming_edge,
                note=decision.notes,
            )
        )
        return events

    outgoing_edge = edges[decision.outgoing_edge]
    apply_edge_traversal(outgoing_edge, trurtle)

    next_vertex = outgoing_edge.other_vertex(trurtle.current_vertex)

    events.append(
        TrurtleEvent(
            tick=tick,
            trurtle_id=trurtle.trurtle_id,
            event_type="traverse",
            vertex_id=trurtle.current_vertex,
            incoming_edge=trurtle.incoming_edge,
            outgoing_edge=decision.outgoing_edge,
            note=f"to={next_vertex}",
        )
    )

    trurtle.current_vertex = next_vertex
    trurtle.incoming_edge = decision.outgoing_edge
    trurtle.handedness = decision.handedness_update or trurtle.handedness
    trurtle.step_count += 1

    events.append(
        TrurtleEvent(
            tick=tick,
            trurtle_id=trurtle.trurtle_id,
            event_type="depart",
            vertex_id=next_vertex,
            incoming_edge=trurtle.incoming_edge,
            note=f"hand={trurtle.handedness}; steps={trurtle.step_count}",
        )
    )

    return events


def idle_all_controllers(controllers: dict[str, VertexController]) -> None:
    for controller in controllers.values():
        controller.idle_tick()


def summarize_edges(edges: dict[str, Edge]) -> dict[str, dict]:
    return {
        edge_id: {
            "endpoints": list(edge.endpoints),
            "touch_count": edge.touch_count,
            "trurtle_ids": list(edge.trurtle_ids),
            "classes_present": list(edge.classes_present),
        }
        for edge_id, edge in edges.items()
    }


def summarize_controllers(controllers: dict[str, VertexController]) -> dict[str, dict]:
    return {
        vertex_id: {
            "routing_bias": c.routing_bias,
            "threshold": c.load_override_threshold,
            "yield_cooldown": c.yield_cooldown_ticks,
            "classes_seen": sorted(c.classes_seen),
            "coupling_count": c.coupling_count,
            "switch_state": c.switch_state,
            "cooldown_left": c.switch_cooldown_remaining,
            "route_counts": dict(c.route_counts),
            "controller_events": [asdict(e) for e in c.controller_events],
        }
        for vertex_id, c in controllers.items()
    }


def summarize_trurtles(trurtles: list[Trurtle]) -> list[dict]:
    return [
        {
            "id": t.trurtle_id,
            "class": t.trurtle_class,
            "current_vertex": t.current_vertex,
            "incoming_edge": t.incoming_edge,
            "handedness": t.handedness,
            "status": t.status,
            "step_count": t.step_count,
        }
        for t in trurtles
    ]
