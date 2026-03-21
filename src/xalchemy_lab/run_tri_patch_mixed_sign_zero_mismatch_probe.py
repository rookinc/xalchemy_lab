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
            "L1": Turtle(name="L1", chirality="L", node="u1R"),
            "L2": Turtle(name="L2", chirality="L", node="mR"),
            "R1": Turtle(name="R1", chirality="R", node="u1R"),
        }
    )


def scenario_mixed_sign_zero_mismatch_probe():
    print("\n====================")
    print("SCENARIO: mixed_sign_zero_mismatch_probe")
    print("====================")
    world = make_world()

    # Artificially prepare the strongest possible probe:
    # mixed incoming signs, but zero mismatch on all turtles.
    world.turtles["L1"].carry_sign = "-"
    world.turtles["L1"].mismatch_count = 0

    world.turtles["L2"].carry_sign = "+"
    world.turtles["L2"].mismatch_count = 0

    world.turtles["R1"].carry_sign = "-"
    world.turtles["R1"].mismatch_count = 0

    print_state("initial (artificial mixed sign, zero mismatch state)", world)

    # Bring the third turtle in so the triad assembles at u1R.
    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    print_state("after tick 1 (forced mixed-sign, zero-mismatch triad at u1R)", world)

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    print_state("after tick 2 (post-event export)", world)


def main():
    scenario_mixed_sign_zero_mismatch_probe()


if __name__ == "__main__":
    main()
