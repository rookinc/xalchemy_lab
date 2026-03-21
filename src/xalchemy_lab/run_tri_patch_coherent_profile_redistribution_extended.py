from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


CASES = [
    (3, 0, 0),
    (3, 0, 3),
    (3, 3, 0),
    (3, 3, 3),
    (4, 2, 0),
    (4, 2, 1),
    (4, 3, 1),
    (4, 4, 4),
]


def make_world(stress_vec: tuple[int, int, int]) -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node="u1R", carry_sign="+", carried_stress=stress_vec[0]),
            "L2": Turtle(name="L2", chirality="L", node="u1R", carry_sign="+", carried_stress=stress_vec[1]),
            "R1": Turtle(name="R1", chirality="R", node="u1R", carry_sign="+", carried_stress=stress_vec[2]),
        }
    )


def expected_after_closure(stress_vec: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(max(s - 1, 0) for s in stress_vec)


def run_case(stress_vec: tuple[int, int, int]) -> None:
    world = make_world(stress_vec)

    incoming_stress = {name: world.turtles[name].carried_stress for name in sorted(world.turtles)}
    incoming_mismatch = {name: world.turtles[name].mismatch_count for name in sorted(world.turtles)}

    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    closure = world.collisions[-1]
    after_closure = tuple(world.turtles[name].carried_stress for name in ("L1", "L2", "R1"))

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    after_export = tuple(world.turtles[name].carried_stress for name in ("L1", "L2", "R1"))

    expected = expected_after_closure(stress_vec)
    ok = after_closure == expected

    ledger = world.hub_ledger["u1R"]

    print(f"\ncase: s{stress_vec[0]}{stress_vec[1]}{stress_vec[2]}")
    print(f"  incoming_mismatch   = {incoming_mismatch}")
    print(f"  incoming_stress     = {incoming_stress}")
    print(f"  closure_class       = {closure.face_event}")
    print(f"  expected_closure    = {expected}")
    print(f"  actual_closure      = {after_closure}")
    print(f"  match               = {ok}")
    print(f"  after_export        = {after_export}")
    print(f"  deposited_stress    = {ledger.deposited_stress}")
    print(f"  stress_energy       = {ledger.stress_energy}")
    print(f"  stored_tension      = {ledger.stored_tension}")


def main() -> None:
    print("\n====================")
    print("COHERENT PROFILE REDISTRIBUTION EXTENDED")
    print("====================")
    print("Testing conjecture: s' = max(s-1, 0) componentwise on coherent zero-burden closure")

    for case in CASES:
        run_case(case)


if __name__ == "__main__":
    main()
