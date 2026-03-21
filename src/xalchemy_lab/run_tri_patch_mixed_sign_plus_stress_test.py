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


def make_world():
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node="u3L"),
            "L2": Turtle(name="L2", chirality="L", node="u2L"),
            "R1": Turtle(name="R1", chirality="R", node="u1R"),
        }
    )


def preload_u1r(world: World) -> None:
    ledger = world.hub_ledger["u1R"]
    ledger.stored_tension = 1
    ledger.stress_energy = 1


def plant_resident_plus_at_u1r(world: World) -> None:
    t = world.turtles["R1"]
    t.node = "u1R"
    t.carry_sign = "+"
    t.carried_stress = 1
    t.mismatch_count = 0


def scenario_mixed_sign_plus_stress():
    print("\n====================")
    print("SCENARIO: mixed_sign_plus_stress")
    print("====================")
    world = make_world()
    preload_u1r(world)
    plant_resident_plus_at_u1r(world)
    print_state("initial (u1R preloaded, R1 resident + with stress)", world)

    # Build a +,+ pair on the left
    step(world, {"L1": "u2L", "L2": "u1L", "R1": "u1R"})
    print_state("after tick 1", world)

    step(world, {"L1": "u1L", "L2": "u1L", "R1": "u1R"})
    print_state("after tick 2 (LL at u1L -> +,+)", world)

    # Peel L1 away and manually seed it as stressed negative for gate test
    step(world, {"L1": "mL", "L2": "u1L", "R1": "u1R"})
    print_state("after tick 3 (L1 leaves; L2 holds +)", world)

    step(world, {"L1": "mR", "L2": "u1L", "R1": "u1R"})
    print_state("after tick 4 (L1 crosses toward d1R)", world)

    step(world, {"L1": "d1R", "L2": "u2L", "R1": "u1R"})
    print_state("after tick 5 (L1 reaches d1R)", world)

    world.turtles["L1"].carry_sign = "-"
    world.turtles["L1"].carried_stress = 1
    world.turtles["L1"].mismatch_count = max(world.turtles["L1"].mismatch_count, 1)
    print_state("after manual seed (L1 set to stressed -)", world)

    # Return L1 to u1R, then bring L2 as delayed third
    step(world, {"L1": "mR", "L2": "u1L", "R1": "u1R"})
    print_state("after tick 6 (L1 returns via mR)", world)

    step(world, {"L1": "u1R", "L2": "u1L", "R1": "u1R"})
    print_state("after tick 7 (L1=-,stress meets resident +=,stress)", world)

    step(world, {"L1": "u1R", "L2": "mL", "R1": "u1R"})
    print_state("after tick 8 (L2 into mL)", world)

    step(world, {"L1": "u1R", "L2": "mR", "R1": "u1R"})
    print_state("after tick 9 (L2 into mR)", world)

    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    print_state("after tick 10 (mixed-sign stressed triad at u1R)", world)

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    print_state("after tick 11 (inspect post-event export)", world)


def main():
    scenario_mixed_sign_plus_stress()


if __name__ == "__main__":
    main()
