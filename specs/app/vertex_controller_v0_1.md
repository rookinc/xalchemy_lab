# Vertex Controller v0.1

## Purpose

A **vertex controller** is the local routing locus of a trurtle system.

A trurtle traverses an edge, arrives at a vertex, and is routed onward by the local state of that vertex together with the state of the incident edges.

This gives the transport split:

- trurtle = moving informative agent
- edge = residue-bearing channel
- vertex = routing controller
- sector / face / cell = embedding context

Canonical sentence:

Informative transport is routed at vertices, inscribed on edges, and embedded in sectors.

## 1. Definition

A **vertex controller** is a finite local control object attached to a graph vertex or sheet junction.
It receives arriving trurtles through incident edges, evaluates local routing law, and selects lawful outgoing edges.

A vertex controller may also accumulate local memory of arrivals, class interactions, coupling events, burden overrides, and switch state.

## 2. Core role

A vertex controller is responsible for:

- receiving arrivals from incident edges
- resolving simultaneous arrivals
- selecting outgoing routes
- mediating class interaction
- recording local coupling history
- applying local switching or bias rules
- responding to local burden
- contributing to informative action by altering future local transport

The edge remembers that transport happened.
The vertex determines where transport can go next.

## 3. Design principle

The vertex controller should use local information only.

It may inspect:

- the incoming edge
- the incident outgoing edges
- current edge residues on those edges
- recent arrivals at the vertex
- classes present
- coupling state
- boundary or sector tags
- current switch state
- relative burden on candidate exits

It should not require global path planning.

Canonical principle:

The vertex is the traffic controller of informative transport.

## 4. Minimal object model

    VertexController
      id
      incident_edges
      routing_bias
      burden_threshold
      classes_seen
      recent_arrivals
      coupling_count
      switch_state
      route_counts
      tags

Field meanings:

- `id` — unique vertex identifier
- `incident_edges` — edges meeting at the vertex
- `routing_bias` — local preference relation such as handedness-first, least-used, or polarity-under-load
- `burden_threshold` — minimum excess burden on the preferred exit required before polarity may be overridden
- `classes_seen` — set of trurtle classes observed at this vertex
- `recent_arrivals` — bounded memory of recent arrival events
- `coupling_count` — count of coupling events witnessed at this vertex
- `switch_state` — small internal state controlling routing
- `route_counts` — local per-edge route counts
- `tags` — optional labels such as `boundary`, `junction`, `coupling_site`, `seed_site`, or `terminal`

## 5. Relation to edges

A vertex controller does not replace edge memory.

Edge responsibilities:

- touch count
- classes present
- trurtles present
- semantic kind
- reinforcement level
- optional decay or freshness

Vertex responsibilities:

- arrival history
- conflict state
- coupling events
- switch phase
- routing bias
- burden-sensitive override
- temporary lock or cooldown

Canonical sentence:

The edge carries residue; the vertex decides flow.

## 6. Arrival model

A trurtle step should be interpreted as:

1. traverse an edge
2. arrive at a vertex
3. vertex controller inspects local state
4. outgoing edge is selected
5. traversal is committed
6. edge and vertex memory are updated
7. event is logged

## 7. Trurtle input to the controller

    Arrival
      trurtle_id
      trurtle_class
      incoming_edge
      handedness
      previous_vertex
      step_count
      local_flags

## 8. Output of the controller

    RoutingDecision
      outgoing_edge
      action
      handedness_update
      switch_state_update
      notes

Possible actions:

- `route`
- `halt`
- `wait`
- `couple`
- `flip`
- `reject`

## 9. Minimal routing laws

Supported controller personalities:

- `handedness_first`
- `least_used`
- `polarity_under_load`

### Handedness-first

Routes by local polarity preference.

### Least-used

Routes toward the lesser-burdened candidate edge.

### Polarity-under-load

Routes by handedness unless the burden on the preferred exit exceeds the burden threshold relative to an available alternative, at which point routing is diverted toward the lesser-burdened channel.

Canonical sentence:

Route by handedness unless handedness would deepen a local imbalance.

## 10. Burden threshold

The burden threshold is a controller parameter that sets how strongly polarity is preserved under load.

Interpretation:

- lower threshold = softer controller, earlier rerouting
- higher threshold = stiffer controller, later rerouting

Examples:

- threshold 1: rapid equalization under stress
- threshold 2: longer polarity loyalty before yielding

Canonical sentence:

The burden threshold tunes when polarity yields to load.

## 11. Simultaneous arrivals

If two or more trurtles arrive at the same vertex on the same tick:

- record a `meet`
- update `classes_seen`
- increment `coupling_count` if distinct classes are present
- apply deterministic precedence or coexistence law
- optionally flip handedness for all arrivals
- return routed outcomes for each trurtle or halt some of them

For v0.1, the simplest lawful strategy is:

- all arrivals succeed
- all arrivals emit `meet`
- all arrivals flip handedness once
- controller increments `coupling_count` if classes differ

## 12. Switch state

Suggested minimal switch states:

- `neutral`
- `flipped`
- `alternating`
- `locked`
- `cooldown`

For v0.1 burden-sensitive routing:

- `neutral` means no burden override occurred on the current routing decision
- `flipped` means burden override occurred and polarity yielded

This is where anti-loop and anti-congestion behavior can live.

## 13. Coupling at the vertex

A vertex is the natural place to register coupling as a routing phenomenon.

A vertex coupling event occurs when:

- two or more distinct trurtle classes arrive simultaneously, or
- a trurtle arrives at a vertex marked as a coupling site, or
- controller state detects a cross-class routing interaction through local edge residues

Possible effects:

- increment `coupling_count`
- add new class to `classes_seen`
- flip switch state
- alter handedness preference
- bias routing away from repetition
- emit a `couple` event

Canonical sentence:

Coupling is not merely a crossing of traces; it is a routed interaction witnessed at a vertex.

## 14. Anti-loop role

The vertex controller is the cleanest place to prevent pathological local loops.

A controller may use:

- recent-arrival memory
- immediate-backtrack exclusion
- least-used-edge preference
- cooldown on recently used exits
- alternation under repeated arrivals
- burden-sensitive rerouting

Canonical principle:

Loop suppression belongs more naturally to the controller than to the agent.

## 15. Minimal memory model

Suggested v0.1 memory:

    recent_arrivals: bounded list of recent arrival records
    classes_seen: set
    coupling_count: integer
    switch_state: small finite state
    route_counts: per-edge small counters
    burden_threshold: integer

## 16. Event logging

Suggested event types:

- `arrive`
- `route`
- `meet`
- `couple`
- `flip`
- `halt`
- `lock`
- `release`
- `switch`
- `override`

Minimal event record:

    VertexEvent
      tick
      vertex_id
      trurtle_id
      event_type
      incoming_edge
      outgoing_edge
      switch_state
      note

Canonical principle:

The controller log is the audit trail of local routing law.

## 17. Invariants

A valid vertex controller should satisfy:

- locality
- determinism
- incident legality
- state coherence
- coupling consistency
- finite-state clarity

## 18. Minimal formal definition

A vertex controller is a finite local routing object attached to a vertex of a transport substrate. It receives arriving trurtles through incident edges, applies deterministic local routing law using controller state and incident edge residue, and selects lawful outgoing edges while recording locally informative transport events.

## 19. Minimal Python-shaped schema

    from dataclasses import dataclass, field
    from typing import Literal

    SwitchState = Literal["neutral", "flipped", "alternating", "locked", "cooldown"]

    @dataclass
    class VertexController:
        vertex_id: str
        incident_edges: list[str]
        routing_bias: str = "handedness_first"
        load_override_threshold: int = 1
        classes_seen: set[int] = field(default_factory=set)
        recent_arrivals: list[dict] = field(default_factory=list)
        coupling_count: int = 0
        switch_state: SwitchState = "neutral"
        route_counts: dict[str, int] = field(default_factory=dict)
        tags: set[str] = field(default_factory=set)

## 20. Short canonical definitions

A vertex controller is the local traffic controller of informative transport.

A vertex controller routes trurtles, witnesses coupling, and regulates local flow.

Informative transport is routed at vertices, inscribed on edges, and embedded in sectors.
