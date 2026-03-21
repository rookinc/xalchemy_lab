from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


Handedness = Literal["left", "right"]
SwitchState = Literal["neutral", "flipped", "alternating", "locked", "cooldown"]


@dataclass
class Arrival:
    trurtle_id: str
    trurtle_class: int
    incoming_edge: str
    handedness: Handedness
    previous_vertex: str | None = None
    step_count: int = 0
    local_flags: dict = field(default_factory=dict)


@dataclass
class RoutingDecision:
    outgoing_edge: str | None
    action: str
    handedness_update: Handedness | None = None
    switch_state_update: SwitchState | None = None
    notes: str = ""


@dataclass
class ControllerEvent:
    seq: int
    vertex_id: str
    event_type: str
    trurtle_id: str | None = None
    incoming_edge: str | None = None
    outgoing_edge: str | None = None
    switch_state: SwitchState | None = None
    note: str = ""


@dataclass
class VertexController:
    vertex_id: str
    incident_edges: list[str]
    routing_bias: str = "handedness_first"
    load_override_threshold: int = 1
    yield_cooldown_ticks: int = 0
    classes_seen: set[int] = field(default_factory=set)
    recent_arrivals: list[dict] = field(default_factory=list)
    coupling_count: int = 0
    switch_state: SwitchState = "neutral"
    switch_cooldown_remaining: int = 0
    route_counts: dict[str, int] = field(default_factory=dict)
    controller_events: list[ControllerEvent] = field(default_factory=list)
    _event_seq: int = 0
    tags: set[str] = field(default_factory=set)

    def emit_event(
        self,
        event_type: str,
        *,
        trurtle_id: str | None = None,
        incoming_edge: str | None = None,
        outgoing_edge: str | None = None,
        note: str = "",
    ) -> None:
        self._event_seq += 1
        self.controller_events.append(
            ControllerEvent(
                seq=self._event_seq,
                vertex_id=self.vertex_id,
                event_type=event_type,
                trurtle_id=trurtle_id,
                incoming_edge=incoming_edge,
                outgoing_edge=outgoing_edge,
                switch_state=self.switch_state,
                note=note,
            )
        )

    def record_arrival(self, arrival: Arrival) -> None:
        self.recent_arrivals.append(
            {
                "trurtle_id": arrival.trurtle_id,
                "trurtle_class": arrival.trurtle_class,
                "incoming_edge": arrival.incoming_edge,
                "handedness": arrival.handedness,
                "previous_vertex": arrival.previous_vertex,
                "step_count": arrival.step_count,
                "local_flags": dict(arrival.local_flags),
            }
        )
        self.classes_seen.add(arrival.trurtle_class)
        self.emit_event(
            "arrive",
            trurtle_id=arrival.trurtle_id,
            incoming_edge=arrival.incoming_edge,
            note=f"class={arrival.trurtle_class}; hand={arrival.handedness}",
        )

    def legal_outgoing_edges(self, incoming_edge: str) -> list[str]:
        return [edge for edge in self.incident_edges if edge != incoming_edge]

    def _handedness_choice(self, candidates: list[str], handedness: Handedness) -> str:
        ordered = sorted(candidates)
        return ordered[0] if handedness == "left" else ordered[-1]

    def _least_used_choice(self, candidates: list[str]) -> str:
        ordered = sorted(candidates)
        return min(ordered, key=lambda e: (self.route_counts.get(e, 0), e))

    def _polarity_under_load_choice(
        self,
        candidates: list[str],
        handedness: Handedness,
    ) -> tuple[str, bool]:
        preferred = self._handedness_choice(candidates, handedness)
        alternates = [e for e in candidates if e != preferred]
        if not alternates:
            return preferred, False

        alternate = self._least_used_choice(alternates)
        preferred_count = self.route_counts.get(preferred, 0)
        alternate_count = self.route_counts.get(alternate, 0)

        if preferred_count - alternate_count >= self.load_override_threshold:
            return alternate, True
        return preferred, False

    def choose_outgoing_edge(self, arrival: Arrival) -> tuple[str | None, bool]:
        candidates = self.legal_outgoing_edges(arrival.incoming_edge)
        if not candidates:
            return None, False

        if self.routing_bias == "handedness_first":
            return self._handedness_choice(candidates, arrival.handedness), False

        if self.routing_bias == "least_used":
            return self._least_used_choice(candidates), False

        if self.routing_bias in {"handedness_then_least_used", "polarity_under_load"}:
            return self._polarity_under_load_choice(candidates, arrival.handedness)

        return sorted(candidates)[0], False

    def _tick_switch_recovery(self) -> None:
        if self.switch_cooldown_remaining > 0:
            self.switch_cooldown_remaining -= 1
            self.emit_event(
                "cooldown_tick",
                note=f"cooldown_remaining={self.switch_cooldown_remaining}",
            )
            if self.switch_cooldown_remaining == 0 and self.switch_state != "neutral":
                self.switch_state = "neutral"
                self.emit_event("switch_to_neutral", note="cooldown expired")

    def idle_tick(self) -> None:
        self.emit_event("idle", note="no arrival")
        self._tick_switch_recovery()

    def _apply_override_state(self, overridden: bool, arrival: Arrival) -> None:
        if overridden:
            was_state = self.switch_state
            self.switch_state = "flipped"
            self.switch_cooldown_remaining = self.yield_cooldown_ticks
            self.emit_event(
                "override",
                trurtle_id=arrival.trurtle_id,
                incoming_edge=arrival.incoming_edge,
                note=(
                    f"preferred exit over burden threshold={self.load_override_threshold}; "
                    f"cooldown={self.yield_cooldown_ticks}"
                ),
            )
            if was_state != "flipped":
                self.emit_event(
                    "switch_to_flipped",
                    trurtle_id=arrival.trurtle_id,
                    incoming_edge=arrival.incoming_edge,
                    note="polarity yielded under burden",
                )
        else:
            self._tick_switch_recovery()

    def route(self, arrival: Arrival) -> RoutingDecision:
        self.record_arrival(arrival)
        outgoing, overridden = self.choose_outgoing_edge(arrival)
        self._apply_override_state(overridden, arrival)

        if outgoing is None:
            self.emit_event(
                "halt",
                trurtle_id=arrival.trurtle_id,
                incoming_edge=arrival.incoming_edge,
                note="no legal outgoing edge",
            )
            return RoutingDecision(
                outgoing_edge=None,
                action="halt",
                handedness_update=arrival.handedness,
                switch_state_update=self.switch_state,
                notes="no legal outgoing edge",
            )

        self.route_counts[outgoing] = self.route_counts.get(outgoing, 0) + 1
        self.emit_event(
            "route",
            trurtle_id=arrival.trurtle_id,
            incoming_edge=arrival.incoming_edge,
            outgoing_edge=outgoing,
            note=f"override={str(overridden).lower()}",
        )
        return RoutingDecision(
            outgoing_edge=outgoing,
            action="route",
            handedness_update=arrival.handedness,
            switch_state_update=self.switch_state,
            notes=(
                f"routed from {arrival.incoming_edge} to {outgoing}; "
                f"threshold={self.load_override_threshold}; "
                f"override={str(overridden).lower()}"
            ),
        )

    def resolve_simultaneous_arrivals(
        self,
        arrivals: list[Arrival],
    ) -> list[tuple[Arrival, RoutingDecision]]:
        if not arrivals:
            return []

        distinct_classes = {a.trurtle_class for a in arrivals}
        if len(distinct_classes) > 1:
            self.coupling_count += 1
            self.emit_event(
                "couple",
                note=f"distinct_classes={sorted(distinct_classes)}",
            )

        results: list[tuple[Arrival, RoutingDecision]] = []
        for arrival in arrivals:
            self.record_arrival(arrival)
            outgoing, overridden = self.choose_outgoing_edge(arrival)
            self._apply_override_state(overridden, arrival)
            flipped: Handedness = "right" if arrival.handedness == "left" else "left"
            self.emit_event(
                "flip",
                trurtle_id=arrival.trurtle_id,
                incoming_edge=arrival.incoming_edge,
                note=f"{arrival.handedness}->{flipped}",
            )

            if outgoing is None:
                self.emit_event(
                    "halt",
                    trurtle_id=arrival.trurtle_id,
                    incoming_edge=arrival.incoming_edge,
                    note="simultaneous arrival; no legal outgoing edge",
                )
                decision = RoutingDecision(
                    outgoing_edge=None,
                    action="halt",
                    handedness_update=flipped,
                    switch_state_update=self.switch_state,
                    notes="simultaneous arrival; no legal outgoing edge",
                )
            else:
                self.route_counts[outgoing] = self.route_counts.get(outgoing, 0) + 1
                self.emit_event(
                    "route",
                    trurtle_id=arrival.trurtle_id,
                    incoming_edge=arrival.incoming_edge,
                    outgoing_edge=outgoing,
                    note=f"simultaneous; override={str(overridden).lower()}",
                )
                decision = RoutingDecision(
                    outgoing_edge=outgoing,
                    action="route",
                    handedness_update=flipped,
                    switch_state_update=self.switch_state,
                    notes=(
                        f"simultaneous arrival; flipped to {flipped}; "
                        f"threshold={self.load_override_threshold}; "
                        f"override={str(overridden).lower()}"
                    ),
                )
            results.append((arrival, decision))
        return results
