from __future__ import annotations

from xalchemy_lab.tri_turtle_core import World, Turtle, step


def print_state(label, world):
    print(f"\n{label}")
    print(f"tick={world.tick}")
    for name, t in sorted(world.turtles.items()):
        print(
            f"  {name}: node={t.node} chirality={t.chirality} "
            f"bumps={t.bumps} seen={t.seen_nodes} "
            f"tokens={t.shared_tokens} faces={t.face_tokens}"
        )
    if world.collisions:
        print("  collisions:")
        for c in world.collisions:
            print(
                f"    tick={c.tick} node={c.node} kind={c.kind} "
                f"face_event={c.face_event} turtles={c.turtles}"
            )


def make_world(l1_node: str, l2_node: str, r1_node: str) -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=l1_node),
            "L2": Turtle(name="L2", chirality="L", node=l2_node),
            "R1": Turtle(name="R1", chirality="R", node=r1_node),
        }
    )


def scenario_default():
    print("\n====================")
    print("SCENARIO: default")
    print("====================")
    world = make_world("u3L", "u3R", "d1T")
    print_state("initial", world)

    step(world, scripted={"L1": "u2L", "L2": "u2R", "R1": "d1T"})
    print_state("after tick 1", world)

    step(world, scripted={"L1": "u1T", "L2": "u1T", "R1": "d1T"})
    print_state("after tick 2", world)

    step(world, scripted={"L1": "u1T", "L2": "u1T", "R1": "u1T"})
    print_state("after tick 3", world)


def scenario_mirror():
    print("\n====================")
    print("SCENARIO: mirror")
    print("====================")
    world = make_world("d3L", "d3R", "u1T")
    print_state("initial", world)

    step(world, scripted={"L1": "d2L", "L2": "d2R", "R1": "u1T"})
    print_state("after tick 1", world)

    step(world, scripted={"L1": "d1T", "L2": "d1T", "R1": "u1T"})
    print_state("after tick 2", world)

    step(world, scripted={"L1": "d1T", "L2": "d1T", "R1": "d1T"})
    print_state("after tick 3", world)


def scenario_split():
    print("\n====================")
    print("SCENARIO: split")
    print("====================")
    world = make_world("u3L", "u3R", "d1T")
    print_state("initial", world)

    step(world, scripted={"L1": "u2L", "L2": "u2R", "R1": "d1T"})
    print_state("after tick 1", world)

    step(world, scripted={"L1": "u1T", "L2": "u1T", "R1": "d1T"})
    print_state("after tick 2", world)

    step(world, scripted={"L1": "d1T", "L2": "u1T", "R1": "d1T"})
    print_state("after tick 3", world)


def main():
    scenario_default()
    scenario_mirror()
    scenario_split()


if __name__ == "__main__":
    main()
