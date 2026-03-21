from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Literal

from xalchemy_lab.trurtle.vertex_controller import Arrival, VertexController


Handedness = Literal["left", "right"]
Status = Literal["active", "halted"]
ChannelRule = Literal[
    "bidirectional_ok",
    "single_occupancy",
    "same_direction_only",
    "contention_creates_coupling",
]


@dataclass
class Edge:
    edge_id: str
    endpoints: tuple[str, str]
    touch_count: int = 0
    trurtle_ids: list[str] = field(default_factory=list)
    classes_present: list[int] = field(default_factory=list)
    contention_count: int = 0

    def other_vertex(self, vertex_id: str) -> str:
        a, b = self.endpoints
        if vertex_id == a:
            return b
        if vertex_id == b:
            return a
        raise ValueError(f"vertex {vertex_id} not incident to edge {self.edge_id}")

    def direction_label(self, from_vertex: str, to_vertex: str) -> str:
        return f"{from_vertex}->{to_vertex}"


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


@dataclass
class PendingMove:
    trurtle_id: str
    from_vertex: str
    to_vertex: str
    incoming_edge_next: str
    handedness_next: Handedness
    outgoing_edge: str


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


def _resolve_edge_claims(
    tick: int,
    pending_moves: list[PendingMove],
    trurtle_map: dict[str, Trurtle],
    edges: dict[str, Edge],
    channel_rule: ChannelRule,
) -> tuple[list[PendingMove], list[TrurtleEvent]]:
    events: list[TrurtleEvent] = []
    approved: list[PendingMove] = []

    claims_by_edge: dict[str, list[PendingMove]] = {}
    for move in pending_moves:
        claims_by_edge.setdefault(move.outgoing_edge, []).append(move)

    for edge_id, claims in claims_by_edge.items():
        edge = edges[edge_id]

        if len(claims) == 1:
            approved.append(claims[0])
            continue

        dirs = {edge.direction_label(c.from_vertex, c.to_vertex) for c in claims}
        distinct_sources = {c.from_vertex for c in claims}

        if channel_rule == "bidirectional_ok":
            approved.extend(claims)
            continue

        if channel_rule == "single_occupancy":
            chosen = sorted(claims, key=lambda c: c.trurtle_id)[0]
            approved.append(chosen)
            edge.contention_count += len(claims) - 1
            for claim in claims[1:]:
                trurtle = trurtle_map[claim.trurtle_id]
                trurtle.status = "halted"
                events.append(
                    TrurtleEvent(
                        tick=tick,
                        trurtle_id=claim.trurtle_id,
                        event_type="edge_blocked",
                        vertex_id=claim.from_vertex,
                        outgoing_edge=edge_id,
                        note=f"single_occupancy; winner={chosen.trurtle_id}",
                    )
                )
            continue

        if channel_rule == "same_direction_only":
            if len(dirs) == 1:
                approved.extend(claims)
            else:
                chosen = sorted(claims, key=lambda c: c.trurtle_id)[0]
                approved.append(chosen)
                edge.contention_count += len(claims) - 1
                for claim in claims[1:]:
                    trurtle = trurtle_map[claim.trurtle_id]
                    trurtle.status = "halted"
                    events.append(
                        TrurtleEvent(
                            tick=tick,
                            trurtle_id=claim.trurtle_id,
                            event_type="edge_blocked",
                            vertex_id=claim.from_vertex,
                            outgoing_edge=edge_id,
                            note=f"same_direction_only; winner={chosen.trurtle_id}",
                        )
                    )
            continue

        if channel_rule == "contention_creates_coupling":
            edge.contention_count += 1
            classes = sorted({trurtle_map[c.trurtle_id].trurtle_class for c in claims})
            for claim in claims:
                approved.append(claim)
                events.append(
                    TrurtleEvent(
                        tick=tick,
                        trurtle_id=claim.trurtle_id,
                        event_type="edge_coupling",
                        vertex_id=claim.from_vertex,
                        outgoing_edge=edge_id,
                        note=(
                            f"claims={len(claims)} dirs={sorted(dirs)} "
                            f"sources={sorted(distinct_sources)} classes={classes}"
                        ),
                    )
                )
            continue

    return approved, events


def batch_step(
    tick: int,
    trurtles: list[Trurtle],
    controllers: dict[str, VertexController],
    edges: dict[str, Edge],
    channel_rule: ChannelRule = "bidirectional_ok",
) -> list[TrurtleEvent]:
    events: list[TrurtleEvent] = []
    trurtle_map = {t.trurtle_id: t for t in trurtles}

    arrivals_by_vertex: dict[str, list[tuple[Trurtle, Arrival]]] = {}
    for trurtle in trurtles:
        if trurtle.status != "active":
            continue
        arrival = Arrival(
            trurtle_id=trurtle.trurtle_id,
            trurtle_class=trurtle.trurtle_class,
            incoming_edge=trurtle.incoming_edge,
            handedness=trurtle.handedness,
            previous_vertex=None,
            step_count=trurtle.step_count,
        )
        arrivals_by_vertex.setdefault(trurtle.current_vertex, []).append((trurtle, arrival))

    pending_moves: list[PendingMove] = []

    for vertex_id, batch in arrivals_by_vertex.items():
        controller = controllers[vertex_id]

        if len(batch) == 1:
            trurtle, arrival = batch[0]
            decision = controller.route(arrival)

            events.append(
                TrurtleEvent(
                    tick=tick,
                    trurtle_id=trurtle.trurtle_id,
                    event_type="arrive",
                    vertex_id=vertex_id,
                    incoming_edge=arrival.incoming_edge,
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
                        vertex_id=vertex_id,
                        incoming_edge=arrival.incoming_edge,
                        note=decision.notes,
                    )
                )
                continue

            outgoing_edge = edges[decision.outgoing_edge]
            next_vertex = outgoing_edge.other_vertex(vertex_id)
            pending_moves.append(
                PendingMove(
                    trurtle_id=trurtle.trurtle_id,
                    from_vertex=vertex_id,
                    to_vertex=next_vertex,
                    incoming_edge_next=decision.outgoing_edge,
                    handedness_next=decision.handedness_update or trurtle.handedness,
                    outgoing_edge=decision.outgoing_edge,
                )
            )
            events.append(
                TrurtleEvent(
                    tick=tick,
                    trurtle_id=trurtle.trurtle_id,
                    event_type="propose_move",
                    vertex_id=vertex_id,
                    incoming_edge=arrival.incoming_edge,
                    outgoing_edge=decision.outgoing_edge,
                    note=f"to={next_vertex}",
                )
            )
        else:
            arrivals = [arrival for _, arrival in batch]
            results = controller.resolve_simultaneous_arrivals(arrivals)

            for trurtle, arrival in batch:
                matching = None
                for arrival_res, decision in results:
                    if arrival_res.trurtle_id == trurtle.trurtle_id:
                        matching = decision
                        break
                assert matching is not None

                events.append(
                    TrurtleEvent(
                        tick=tick,
                        trurtle_id=trurtle.trurtle_id,
                        event_type="arrive_batch",
                        vertex_id=vertex_id,
                        incoming_edge=arrival.incoming_edge,
                        outgoing_edge=matching.outgoing_edge,
                        note=matching.notes,
                    )
                )

                if matching.action != "route" or matching.outgoing_edge is None:
                    trurtle.status = "halted"
                    events.append(
                        TrurtleEvent(
                            tick=tick,
                            trurtle_id=trurtle.trurtle_id,
                            event_type="halt",
                            vertex_id=vertex_id,
                            incoming_edge=arrival.incoming_edge,
                            note=matching.notes,
                        )
                    )
                    continue

                outgoing_edge = edges[matching.outgoing_edge]
                next_vertex = outgoing_edge.other_vertex(vertex_id)
                pending_moves.append(
                    PendingMove(
                        trurtle_id=trurtle.trurtle_id,
                        from_vertex=vertex_id,
                        to_vertex=next_vertex,
                        incoming_edge_next=matching.outgoing_edge,
                        handedness_next=matching.handedness_update or trurtle.handedness,
                        outgoing_edge=matching.outgoing_edge,
                    )
                )
                events.append(
                    TrurtleEvent(
                        tick=tick,
                        trurtle_id=trurtle.trurtle_id,
                        event_type="propose_move",
                        vertex_id=vertex_id,
                        incoming_edge=arrival.incoming_edge,
                        outgoing_edge=matching.outgoing_edge,
                        note=f"to={next_vertex}",
                    )
                )

    approved_moves, edge_events = _resolve_edge_claims(
        tick=tick,
        pending_moves=pending_moves,
        trurtle_map=trurtle_map,
        edges=edges,
        channel_rule=channel_rule,
    )
    events.extend(edge_events)

    approved_ids = {m.trurtle_id for m in approved_moves}

    for move in pending_moves:
        if move.trurtle_id not in approved_ids and trurtle_map[move.trurtle_id].status == "active":
            trurtle_map[move.trurtle_id].status = "halted"
            events.append(
                TrurtleEvent(
                    tick=tick,
                    trurtle_id=move.trurtle_id,
                    event_type="halt",
                    vertex_id=move.from_vertex,
                    outgoing_edge=move.outgoing_edge,
                    note=f"edge claim rejected under {channel_rule}",
                )
            )

    for move in approved_moves:
        trurtle = trurtle_map[move.trurtle_id]
        edge = edges[move.outgoing_edge]
        apply_edge_traversal(edge, trurtle)

        events.append(
            TrurtleEvent(
                tick=tick,
                trurtle_id=trurtle.trurtle_id,
                event_type="traverse",
                vertex_id=move.from_vertex,
                incoming_edge=trurtle.incoming_edge,
                outgoing_edge=move.outgoing_edge,
                note=f"to={move.to_vertex}",
            )
        )

        trurtle.current_vertex = move.to_vertex
        trurtle.incoming_edge = move.incoming_edge_next
        trurtle.handedness = move.handedness_next
        trurtle.step_count += 1

        events.append(
            TrurtleEvent(
                tick=tick,
                trurtle_id=trurtle.trurtle_id,
                event_type="depart",
                vertex_id=move.to_vertex,
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
            "contention_count": edge.contention_count,
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
