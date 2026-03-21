from __future__ import annotations

from copy import deepcopy

from xalchemy_lab.tri_patch_core import World, Turtle, apply_collision


def make_world() -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node="d1R", carry_sign="-"),
            "L2": Turtle(name="L2", chirality="L", node="d1R", carry_sign="-"),
            "R1": Turtle(name="R1", chirality="R", node="d1R", carry_sign="-"),
        }
    )


def configure_case(world: World, stress_triplet: tuple[int, int, int]) -> None:
    names = ["L1", "L2", "R1"]
    for name, stress in zip(names, stress_triplet):
        t = world.turtles[name]
        t.mismatch_count = 0
        t.carried_stress = stress
        t.shared_tokens = []
        t.face_tokens = []
        t.seen_nodes = ["d1R"]


def print_case_result(
    label: str,
    stress_triplet: tuple[int, int, int],
    world_before: World,
    world_after: World,
) -> None:
    c = world_after.collisions[-1]
    ledger_before = world_before.hub_ledger["d1R"]
    ledger_after = world_after.hub_ledger["d1R"]

    print(f"\ncase: {label}")
    print(f"  incoming_signs    = {c.incoming_signs}")
    print(f"  incoming_mismatch = {c.incoming_mismatch}")
    print(f"  incoming_stress   = {c.incoming_stress}")
    print(f"  total_stress      = {sum(stress_triplet)}")
    print(f"  closure_class     = {c.face_event}")
    print(f"  outgoing_stress   = {c.outgoing_stress}")
    print(
        "  ledger_delta      = "
        f"stress_energy {ledger_before.stress_energy}->{ledger_after.stress_energy}, "
        f"stored_tension {ledger_before.stored_tension}->{ledger_after.stored_tension}, "
        f"deposited {ledger_before.deposited_stress}->{ledger_after.deposited_stress}, "
        f"clean {ledger_before.clean_closures}->{ledger_after.clean_closures}, "
        f"tension {ledger_before.tension_closures}->{ledger_after.tension_closures}"
    )


def main() -> None:
    cases = [
        ("s000", (0, 0, 0)),
        ("s100", (1, 0, 0)),
        ("s110", (1, 1, 0)),
        ("s111", (1, 1, 1)),
        ("s222", (2, 2, 2)),
        ("s333", (3, 3, 3)),
    ]

    print("\n====================")
    print("SCENARIO: pure_overload_probe_negative")
    print("====================")
    print("All cases are sign-coherent (-,-,-) with zero mismatch at d1R.")
    print("Only incoming carried stress is varied.")

    for label, stress_triplet in cases:
        world = make_world()
        configure_case(world, stress_triplet)
        before = deepcopy(world)
        apply_collision(world, "d1R", ["L1", "L2", "R1"])
        print_case_result(label, stress_triplet, before, world)


if __name__ == "__main__":
    main()
