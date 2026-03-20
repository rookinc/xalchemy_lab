from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Tuple


NodeName = Literal[
    "u3L", "u2L", "u1T", "u2R", "u3R",
    "d1T",
    "d2L", "d3L", "d2R", "d3R",
]

Chirality = Literal["L", "R"]
Sign = Literal["+", "-"]


ADJ: Dict[NodeName, List[NodeName]] = {
    "u3L": ["u2L"],
    "u2L": ["u3L", "u1T"],
    "u1T": ["u2L", "u2R", "d1T"],
    "u2R": ["u1T", "u3R"],
    "u3R": ["u2R"],
    "d1T": ["u1T", "d2L", "d2R"],
    "d2L": ["d1T", "d3L"],
    "d3L": ["d2L"],
    "d2R": ["d1T", "d3R"],
    "d3R": ["d2R"],
}

NODE_CLASS: Dict[NodeName, int] = {
    "u3L": 3, "u2L": 2, "u1T": 1, "u2R": 2, "u3R": 3,
    "d1T": 1,
    "d2L": 2, "d3L": 3, "d2R": 2, "d3R": 3,
}

HUB_SIGN: Dict[NodeName, Sign] = {
    "u1T": "+",
    "d1T": "-",
}


@dataclass
class Turtle:
    name: str
    chirality: Chirality
    node: NodeName
    heading: Optional[NodeName] = None
    seen_nodes: List[NodeName] = field(default_factory=list)
    bumps: int = 0
    shared_tokens: List[str] = field(default_factory=list)
    face_tokens: List[str] = field(default_factory=list)
    carry_sign: Optional[Sign] = None
    site_sign_history: List[Sign] = field(default_factory=list)
    mismatch_count: int = 0
    carried_stress: int = 0

    def visit(self) -> None:
        if self.node not in self.seen_nodes:
            self.seen_nodes.append(self.node)


@dataclass
class Collision:
    tick: int
    node: NodeName
    kind: str
    turtles: List[str]
    face_event: str


@dataclass
class HubLedger:
    plus_arrivals: int = 0
    minus_arrivals: int = 0
    unsigned_arrivals: int = 0
    mismatch_events: int = 0
    transfers: int = 0
    clean_closures: int = 0
    tension_closures: int = 0
    stored_tension: int = 0
    stress_energy: int = 0


@dataclass
class World:
    turtles: Dict[str, Turtle]
    tick: int = 0
    collisions: List[Collision] = field(default_factory=list)
    hub_ledger: Dict[NodeName, HubLedger] = field(
        default_factory=lambda: {
            "u1T": HubLedger(),
            "d1T": HubLedger(),
        }
    )

    def snapshot(self) -> Dict[str, Tuple[NodeName, Optional[NodeName]]]:
        return {name: (t.node, t.heading) for name, t in self.turtles.items()}


def inward_move(node: NodeName) -> NodeName:
    if node == "u3L":
        return "u2L"
    if node == "u2L":
        return "u1T"
    if node == "u3R":
        return "u2R"
    if node == "u2R":
        return "u1T"
    if node == "d3L":
        return "d2L"
    if node == "d2L":
        return "d1T"
    if node == "d3R":
        return "d2R"
    if node == "d2R":
        return "d1T"
    return node


def classify_collision(names: List[str], world: World) -> str:
    kinds = "".join(sorted(world.turtles[n].chirality for n in names))
    if kinds == "LL":
        return "LL"
    if kinds == "LR":
        return "LR"
    if kinds == "LLR":
        return "LLR"
    return kinds


def closure_event(node: NodeName, names: List[str], world: World) -> str:
    sign = HUB_SIGN.get(node)
    if sign is None:
        return "triadic_closure"

    any_tension = any(world.turtles[n].mismatch_count > 0 for n in names)
    if any_tension:
        return f"ABC{sign}_tension"
    return f"ABC{sign}_closed"


def face_event_for(kind: str, node: NodeName, names: List[str], world: World) -> str:
    cls = NODE_CLASS[node]
    sign = HUB_SIGN.get(node)

    if cls == 1 and sign is not None:
        if kind == "LL":
            return f"B{sign}"
        if kind == "LR":
            return f"sign_transfer{sign}"
        if kind == "LLR":
            return closure_event(node, names, world)

    if kind == "LL":
        return "support_pair"
    if kind == "LR":
        return "complement_exchange"
    if kind == "LLR":
        return "triadic_closure"
    return "unknown"


def update_site_sign_and_mismatch(world: World, node: NodeName, names: List[str]) -> None:
    hub_sign = HUB_SIGN.get(node)
    if hub_sign is None:
        return

    ledger = world.hub_ledger[node]

    for n in names:
        t = world.turtles[n]
        t.site_sign_history.append(hub_sign)

        if t.carry_sign == "+":
            ledger.plus_arrivals += 1
        elif t.carry_sign == "-":
            ledger.minus_arrivals += 1
        else:
            ledger.unsigned_arrivals += 1

        if t.carry_sign is not None and t.carry_sign != hub_sign:
            t.mismatch_count += 1
            ledger.mismatch_events += 1
            ledger.stress_energy += 1


def mutate_signs(world: World, node: NodeName, names: List[str], kind: str) -> None:
    hub_sign = HUB_SIGN.get(node)
    if hub_sign is None:
        return

    turtles = [world.turtles[n] for n in names]

    if kind == "LL":
        for t in turtles:
            t.carry_sign = hub_sign
        return

    if kind == "LR":
        carried = None
        for t in turtles:
            if t.carry_sign is not None:
                carried = t.carry_sign
                break
        if carried is None:
            carried = hub_sign
        for t in turtles:
            t.carry_sign = carried
        world.hub_ledger[node].transfers += 1
        return

    if kind == "LLR":
        for t in turtles:
            t.carry_sign = hub_sign
        return


def propagate_stress_to_turtles(world: World, names: List[str], face_event: str) -> None:
    if face_event.endswith("_tension"):
        for n in names:
            world.turtles[n].carried_stress += 1
    elif face_event.endswith("_closed"):
        for n in names:
            if world.turtles[n].carried_stress > 0:
                world.turtles[n].carried_stress -= 1


def update_hub_closure_stats(world: World, node: NodeName, face_event: str) -> None:
    if node not in world.hub_ledger:
        return

    ledger = world.hub_ledger[node]

    if face_event.endswith("_closed"):
        ledger.clean_closures += 1
        if ledger.stored_tension > 0:
            ledger.stored_tension -= 1
        if ledger.stress_energy > 0:
            ledger.stress_energy -= 1
    elif face_event.endswith("_tension"):
        ledger.tension_closures += 1
        ledger.stored_tension += 1
        ledger.stress_energy += 1


def apply_collision(world: World, node: NodeName, names: List[str]) -> None:
    kind = classify_collision(names, world)

    union_seen: List[NodeName] = []
    union_faces: List[str] = []
    for n in names:
        for s in world.turtles[n].seen_nodes:
            if s not in union_seen:
                union_seen.append(s)
        for f in world.turtles[n].face_tokens:
            if f not in union_faces:
                union_faces.append(f)

    update_site_sign_and_mismatch(world, node, names)
    mutate_signs(world, node, names, kind)

    token = f"{kind}@{node}"
    face_event = face_event_for(kind, node, names, world)
    face_token = f"{face_event}@{node}"

    for n in names:
        t = world.turtles[n]
        t.bumps += 1
        t.shared_tokens.append(token)
        t.seen_nodes = union_seen.copy()
        if face_token not in union_faces:
            union_faces.append(face_token)
        t.face_tokens = union_faces.copy()

    propagate_stress_to_turtles(world, names, face_event)
    update_hub_closure_stats(world, node, face_event)

    world.collisions.append(Collision(
        tick=world.tick,
        node=node,
        kind=kind,
        turtles=names.copy(),
        face_event=face_event,
    ))


def detect_collisions(world: World) -> None:
    by_node: Dict[NodeName, List[str]] = {}
    for name, turtle in world.turtles.items():
        by_node.setdefault(turtle.node, []).append(name)

    for node, names in by_node.items():
        if len(names) >= 2:
            apply_collision(world, node, sorted(names))


def step(world: World, scripted: Optional[Dict[str, NodeName]] = None) -> None:
    world.tick += 1

    for name, turtle in world.turtles.items():
        turtle.visit()
        if scripted and name in scripted:
            target = scripted[name]
            if target not in ADJ[turtle.node] and target != turtle.node:
                raise ValueError(f"Illegal scripted move for {name}: {turtle.node} -> {target}")
            turtle.heading = target
        else:
            turtle.heading = inward_move(turtle.node)

    for turtle in world.turtles.values():
        if turtle.heading is not None:
            turtle.node = turtle.heading
            turtle.visit()

    detect_collisions(world)
