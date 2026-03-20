from __future__ import annotations

from xalchemy_lab.tri_turtle_core import World, Turtle, step


def print_state(label, world):
    print(f"\n{label}")
    print(f"tick={world.tick}")
    for name, t in sorted(world.turtles.items()):
        print(
            f"  {name}: node={t.node} chirality={t.chirality} "
            f"sign={t.carry_sign} carried_stress={t.carried_stress} "
            f"mismatches={t.mismatch_count} site_signs={t.site_sign_history} "
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
    print("  hub ledger:")
    for hub, ledger in sorted(world.hub_ledger.items()):
        print(
            f"    {hub}: +arr={ledger.plus_arrivals} -arr={ledger.minus_arrivals} "
            f"unsigned={ledger.unsigned_arrivals} mismatches={ledger.mismatch_events} "
            f"transfers={ledger.transfers} clean={ledger.clean_closures} "
            f"tension={ledger.tension_closures} stored_tension={ledger.stored_tension} "
            f"stress_energy={ledger.stress_energy} deposited_stress={ledger.deposited_stress}"
        )


def make_world(l1_node: str, l2_node: str, r1_node: str) -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=l1_node),
            "L2": Turtle(name="L2", chirality="L", node=l2_node),
            "R1": Turtle(name="R1", chirality="R", node=r1_node),
        }
    )


def scenario_free_flight_damping():
    print("\n====================")
    print("SCENARIO: free_flight_damping")
    print("====================")
    world = make_world("u3L", "u3R", "d1T")
    print_state("initial", world)

    # Build + at u1T
    step(world, scripted={"L1": "u2L", "L2": "u2R", "R1": "d1T"})
    print_state("after tick 1", world)

    step(world, scripted={"L1": "u1T", "L2": "u1T", "R1": "d1T"})
    print_state("after tick 2", world)

    # Transfer + into - hub
    step(world, scripted={"L1": "d1T", "L2": "u1T", "R1": "d1T"})
    print_state("after tick 3", world)

    # Force tension closure at d1T
    step(world, scripted={"L1": "d1T", "L2": "d1T", "R1": "d1T"})
    print_state("after tick 4 (tension)", world)

    # Separate the turtles so they free-fly without collision
    step(world, scripted={"L1": "d2L", "L2": "d2R", "R1": "u1T"})
    print_state("after tick 5 (separated)", world)

    # More free flight: only L1 continues outward; others hold separated/no collision
    step(world, scripted={"L1": "d3L", "L2": "d2R", "R1": "u1T"})
    print_state("after tick 6 (free flight)", world)

    # Turn L1 back inward; still avoid collisions
    step(world, scripted={"L1": "d2L", "L2": "d2R", "R1": "u1T"})
    print_state("after tick 7 (return leg)", world)


def main():
    scenario_free_flight_damping()


if __name__ == "__main__":
    main()
