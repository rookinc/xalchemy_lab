from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Tuple


NodeName = Literal[
    "u3L", "u2L", "u1T", "u2R", "u3R",
    "d1T",
    "d2L", "d3L", "d2R", "d3R",
]

Chirality = Literal["L", "R"]


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
class World:
    turtles: Dict[str, Turtle]
    tick: int = 0
    collisions: List[Collision] = field(default_factory=list)

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


def face_event_for(kind: str, node: NodeName) -> str:
    cls = NODE_CLASS[node]
    if kind == "LL" and cls == 1:
        return "B_stabilized"
    if kind == "LR" and cls == 1:
        return "sign_transfer"
    if kind == "LLR" and cls == 1:
        return "ABC_closed"
    if kind == "LL":
        return "support_pair"
    if kind == "LR":
        return "complement_exchange"
    if kind == "LLR":
        return "triadic_closure"
    return "unknown"


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

    token = f"{kind}@{node}"
    face_event = face_event_for(kind, node)
    face_token = f"{face_event}@{node}"

    for n in names:
        t = world.turtles[n]
        t.bumps += 1
        t.shared_tokens.append(token)
        t.seen_nodes = union_seen.copy()
        if face_token not in union_faces:
            union_faces.append(face_token)
        t.face_tokens = union_faces.copy()

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
