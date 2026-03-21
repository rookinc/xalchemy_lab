from __future__ import annotations

from itertools import product

from xalchemy_lab.tri_patch_core import World, Turtle, step


def stress_gate_class(total_stress: int, k: int) -> str:
    return "ABC+_tension" if total_stress >= k else "ABC+_closed"


def support_gate_class(stress_vec: tuple[int, int, int], support_threshold: int) -> str:
    occupied = sum(1 for s in stress_vec if s > 0)
    return "ABC+_tension" if occupied >= support_threshold else "ABC+_closed"


def make_world(stress_vec: tuple[int, int, int]) -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node="u1R", carry_sign="+", carried_stress=stress_vec[0]),
            "L2": Turtle(name="L2", chirality="L", node="u1R", carry_sign="+", carried_stress=stress_vec[1]),
            "R1": Turtle(name="R1", chirality="R", node="u1R", carry_sign="+", carried_stress=stress_vec[2]),
        }
    )


def run_case(stress_vec: tuple[int, int, int]) -> None:
    world = make_world(stress_vec)

    incoming_stress = {name: world.turtles[name].carried_stress for name in ("L1", "L2", "R1")}
    total_stress = sum(stress_vec)
    occupied = sum(1 for s in stress_vec if s > 0)

    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    closure = world.collisions[-1]
    actual = closure.face_event

    print(f"\ncase: s{stress_vec[0]}{stress_vec[1]}{stress_vec[2]}")
    print(f"  incoming_stress      = {incoming_stress}")
    print(f"  total_stress         = {total_stress}")
    print(f"  occupied_channels    = {occupied}")
    print(f"  current_law          = {actual}")
    print(f"  stress_gate(k=1)     = {stress_gate_class(total_stress, 1)}")
    print(f"  stress_gate(k=3)     = {stress_gate_class(total_stress, 3)}")
    print(f"  stress_gate(k=6)     = {stress_gate_class(total_stress, 6)}")
    print(f"  stress_gate(k=9)     = {stress_gate_class(total_stress, 9)}")
    print(f"  support_gate(n>=1)   = {support_gate_class(stress_vec, 1)}")
    print(f"  support_gate(n>=2)   = {support_gate_class(stress_vec, 2)}")
    print(f"  support_gate(n>=3)   = {support_gate_class(stress_vec, 3)}")


def main() -> None:
    print("\n====================")
    print("STRESS PROMOTION SWEEP")
    print("====================")
    print("Coherent zero-mismatch triads at u1R")
    print("Compare current law against possible stress-promotion gates")

    cases = [
        (0, 0, 0),
        (1, 0, 0),
        (1, 1, 0),
        (1, 1, 1),
        (2, 0, 0),
        (2, 1, 0),
        (2, 1, 1),
        (2, 2, 2),
        (3, 0, 0),
        (3, 1, 0),
        (3, 1, 1),
        (3, 3, 0),
        (3, 3, 3),
        (4, 0, 0),
        (4, 2, 0),
        (4, 2, 1),
        (4, 4, 4),
        (6, 0, 0),
        (6, 1, 0),
        (6, 3, 0),
        (6, 3, 3),
    ]

    for case in cases:
        run_case(case)


if __name__ == "__main__":
    main()
