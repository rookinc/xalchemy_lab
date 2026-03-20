from __future__ import annotations

from xalchemy_lab.tri_turtle_core import default_world, step


def print_state(label, world):
    print(f"\n{label}")
    print(f"tick={world.tick}")
    for name, t in sorted(world.turtles.items()):
        print(
            f"  {name}: node={t.node} chirality={t.chirality} "
            f"bumps={t.bumps} seen={t.seen_nodes} tokens={t.shared_tokens}"
        )
    if world.collisions:
        print("  collisions:")
        for c in world.collisions:
            print(f"    tick={c.tick} node={c.node} kind={c.kind} turtles={c.turtles}")


def main():
    world = default_world()
    print_state("initial", world)

    # tick 1: both left turtles move inward, right turtle holds
    step(world, scripted={
        "L1": "u2L",
        "L2": "u2R",
        "R1": "d1T",
    })
    print_state("after tick 1", world)

    # tick 2: left turtles collide at upper class-1 hub
    step(world, scripted={
        "L1": "u1T",
        "L2": "u1T",
        "R1": "d1T",
    })
    print_state("after tick 2", world)

    # tick 3A: right turtle rises to produce triple collision
    step(world, scripted={
        "L1": "u1T",
        "L2": "u1T",
        "R1": "u1T",
    })
    print_state("after tick 3", world)


if __name__ == "__main__":
    main()
