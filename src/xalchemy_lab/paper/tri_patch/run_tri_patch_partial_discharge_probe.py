from __future__ import annotations

from copy import deepcopy

from xalchemy_lab.tri_patch_core import World, Turtle, apply_collision


def make_world(node: str, sign: str) -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=node, carry_sign=sign),
            "L2": Turtle(name="L2", chirality="L", node=node, carry_sign=sign),
            "R1": Turtle(name="R1", chirality="R", node=node, carry_sign=sign),
        }
    )


def configure_case(world: World, stress_triplet: tuple[int, int, int]) -> None:
    for name, stress in zip(["L1", "L2", "R1"], stress_triplet):
        t = world.turtles[name]
        t.mismatch_count = 0
        t.carried_stress = stress
        t.shared_tokens = []
        t.face_tokens = []
        t.seen_nodes = [t.node]


def expected_partial_discharge(stress_triplet: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(max(s - 1, 0) for s in stress_triplet)


def print_case_result(
    label: str,
    hub: str,
    sign: str,
    stress_triplet: tuple[int, int, int],
    world_before: World,
    world_after: World,
) -> None:
    c = world_after.collisions[-1]
    ledger_before = world_before.hub_ledger[hub]
    ledger_after = world_after.hub_ledger[hub]
    expected = expected_partial_discharge(stress_triplet)
    observed = (
        c.outgoing_stress["L1"],
        c.outgoing_stress["L2"],
        c.outgoing_stress["R1"],
    )

    print("")
    print(f"case: {label}")
    print(f"  hub               = {hub}")
    print(f"  coherent_sign     = {sign}")
    print(f"  incoming_stress   = {c.incoming_stress}")
    print(f"  expected_out      = {expected}")
    print(f"  observed_out      = {observed}")
    print(f"  closure_class     = {c.face_event}")
    print(f"  discharge_matches = {observed == expected}")
    print(
        "  ledger_delta      = "
        f"stress_energy {ledger_before.stress_energy}->{ledger_after.stress_energy}, "
        f"stored_tension {ledger_before.stored_tension}->{ledger_after.stored_tension}, "
        f"deposited {ledger_before.deposited_stress}->{ledger_after.deposited_stress}, "
        f"clean {ledger_before.clean_closures}->{ledger_after.clean_closures}, "
        f"tension {ledger_before.tension_closures}->{ledger_after.tension_closures}"
    )


def run_suite(hub: str, sign: str) -> None:
    cases = [
        ("s200", (2, 0, 0)),
        ("s310", (3, 1, 0)),
        ("s521", (5, 2, 1)),
        ("s404", (4, 0, 4)),
        ("s710", (7, 1, 0)),
        ("s123", (1, 2, 3)),
    ]

    print("")
    print("====================")
    print(f"PARTIAL DISCHARGE SUITE @ {hub}")
    print("====================")
    print(f"All cases are coherent {sign}{sign}{sign} with zero mismatch.")
    print("Probe: outgoing_stress_i == max(incoming_stress_i - 1, 0)")

    for label, stress_triplet in cases:
        world = make_world(hub, sign)
        configure_case(world, stress_triplet)
        before = deepcopy(world)
        apply_collision(world, hub, ["L1", "L2", "R1"])
        print_case_result(label, hub, sign, stress_triplet, before, world)


def main() -> None:
    print("\n====================")
    print("SCENARIO: partial_discharge_probe")
    print("====================")
    run_suite("u1R", "+")
    run_suite("d1R", "-")


if __name__ == "__main__":
    main()
