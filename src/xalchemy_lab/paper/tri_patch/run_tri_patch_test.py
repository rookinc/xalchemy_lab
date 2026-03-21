from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


def print_state(label, world):
    print(f"\n{label}")
    print(f"tick={world.tick}")
    for name, t in sorted(world.turtles.items()):
        print(
            f"  {name}: node={t.node} sign={t.carry_sign} stress={t.carried_stress} "
            f"mismatch={t.mismatch_count} tokens={t.shared_tokens}"
        )
    if world.collisions:
        print("  collisions:")
        for c in world.collisions:
            print(
                f"    tick={c.tick} node={c.node} kind={c.kind} face={c.face_event} turtles={c.turtles}\n"
                f"      in_sign={c.incoming_signs} out_sign={c.outgoing_signs}\n"
                f"      in_stress={c.incoming_stress} out_stress={c.outgoing_stress}\n"
                f"      in_mismatch={c.incoming_mismatch} out_mismatch={c.outgoing_mismatch}"
            )
    print("  hub ledger:")
    for hub, ledger in sorted(world.hub_ledger.items()):
        print(
            f"    {hub}: stress_energy={ledger.stress_energy} stored_tension={ledger.stored_tension} "
            f"deposited={ledger.deposited_stress} clean={ledger.clean_closures} tension={ledger.tension_closures}"
        )


def make_cross_world():
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node="u3L"),
            "L2": Turtle(name="L2", chirality="L", node="u2L"),
            "R1": Turtle(name="R1", chirality="R", node="d2R"),
        }
    )


def scenario_cross_patch_stress_transport():
    print("\n====================")
    print("SCENARIO: cross_patch_stress_transport")
    print("====================")
    world = make_cross_world()
    print_state("initial", world)

    step(world, {"L1": "u2L", "L2": "u1L", "R1": "d1R"})
    print_state("after tick 1", world)

    step(world, {"L1": "u1L", "L2": "u1L", "R1": "d1R"})
    print_state("after tick 2 (LL at u1L)", world)

    step(world, {"L1": "mL", "L2": "mL", "R1": "d1R"})
    print_state("after tick 3 (into mL)", world)

    step(world, {"L1": "mR", "L2": "mR", "R1": "d1R"})
    print_state("after tick 4 (cross to mR)", world)

    step(world, {"L1": "d1R", "L2": "mR", "R1": "d1R"})
    print_state("after tick 5 (LR at d1R)", world)

    step(world, {"L1": "d1R", "L2": "d1R", "R1": "d1R"})
    print_state("after tick 6 (LLR tension at d1R)", world)

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    print_state("after tick 7 (stressed packet leaves d1R)", world)

    step(world, {"L1": "u1R", "L2": "mR", "R1": "u1R"})
    print_state("after tick 8 (LR at u1R)", world)

    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    print_state("after tick 9 (LLR at u1R)", world)


def main():
    scenario_cross_patch_stress_transport()


if __name__ == "__main__":
    main()
