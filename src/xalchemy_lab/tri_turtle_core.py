from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Tuple


NodeName = Literal[
    "u3L", "u2L", "u1T", "u2R", "u3R",
    "d1T",
    "d2L", "d3L", "d2R", "d3R",
]

Chirality = Literal["L", "R"]


# Rooted 1-2-3 scaffold
# u3L -- u2L \       / u2R -- u3R
#              \ u1T /
#                |
#               d1T
#              /   \
#           d2L     d2R
#           /         \
#         d3L         d3R
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

    def visit(self) -> None:
        if self.node not in self.seen_nodes:
            self.seen_nodes.append(self.node)


@dataclass
class Collision:
    tick: int
    node: NodeName
    kind: str
    turtles: List[str]


@dataclass
class World:
    turtles: Dict[str, Turtle]
    tick: int = 0
    collisions: List[Collision] = field(default_factory=list)

    def snapshot(self) -> Dict[str, Tuple[NodeName, Optional[NodeName]]]:
        return {name: (t.node, t.heading) for name, t in self.turtles.items()}


def inward_move(node: NodeName) -> NodeName:
    """Minimal v0 rule: move toward the class-1 spine if possible."""
    if node in ("u3L",):
        return "u2L"
    if node in ("u2L",):
        return "u1T"
    if node in ("u3R",):
        return "u2R"
    if node in ("u2R",):
        return "u1T"
    if node in ("d3L",):
        return "d2L"
    if node in ("d2L",):
        return "d1T"
    if node in ("d3R",):
        return "d2R"
    if node in ("d2R",):
        return "d1T"
    return node  # hubs hold by default


def apply_collision(world: World, node: NodeName, names: List[str]) -> None:
    kinds = "".join(sorted(world.turtles[n].chirality for n in names))
    if kinds == "LL":
        kind = "LL"
    elif kinds == "LR":
        kind = "LR"
    elif kinds == "LLR":
        kind = "LLR"
    else:
        kind = kinds

    union_seen: List[NodeName] = []
    for n in names:
        for s in world.turtles[n].seen_nodes:
            if s not in union_seen:
                union_seen.append(s)

    token = f"{kind}@{node}"
    for n in names:
        t = world.turtles[n]
        t.bumps += 1
        t.shared_tokens.append(token)
        t.seen_nodes = union_seen.copy()

    world.collisions.append(Collision(
        tick=world.tick,
        node=node,
        kind=kind,
        turtles=names.copy(),
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

    # choose moves
    for name, turtle in world.turtles.items():
        turtle.visit()
        if scripted and name in scripted:
            target = scripted[name]
            if target not in ADJ[turtle.node] and target != turtle.node:
                raise ValueError(f"Illegal scripted move for {name}: {turtle.node} -> {target}")
            turtle.heading = target
        else:
            turtle.heading = inward_move(turtle.node)

    # commit moves
    for turtle in world.turtles.values():
        if turtle.heading is not None:
            turtle.node = turtle.heading
            turtle.visit()

    detect_collisions(world)


def default_world() -> World:
    turtles = {
        "L1": Turtle(name="L1", chirality="L", node="u3L"),
        "L2": Turtle(name="L2", chirality="L", node="u3R"),
        "R1": Turtle(name="R1", chirality="R", node="d1T"),
    }
    return World(turtles=turtles)
