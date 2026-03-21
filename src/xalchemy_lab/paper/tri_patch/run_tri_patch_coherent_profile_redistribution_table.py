from __future__ import annotations

from itertools import product

from xalchemy_lab.tri_patch_core import World, Turtle, step


def print_header() -> None:
    print("\n====================")
    print("COHERENT PROFILE REDISTRIBUTION TABLE")
    print("====================")


def make_world(stress_vec: tuple[int, int, int]) -> World:
    world = World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node="u1R", carry_sign="+", carried_stress=stress_vec[0]),
            "L2": Turtle(name="L2", chirality="L", node="u1R", carry_sign="+", carried_stress=stress_vec[1]),
            "R1": Turtle(name="R1", chirality="R", node="u1R", carry_sign="+", carried_stress=stress_vec[2]),
        }
    )
    return world


def closure_case_name(stress_vec: tuple[int, int, int]) -> str:
    return f"s{stress_vec[0]}{stress_vec[1]}{stress_vec[2]}"


def run_case(stress_vec: tuple[int, int, int]) -> None:
    world = make_world(stress_vec)

    in_signs = {name: t.carry_sign for name, t in sorted(world.turtles.items())}
    in_stress = {name: t.carried_stress for name, t in sorted(world.turtles.items())}
    in_mismatch = {name: t.mismatch_count for name, t in sorted(world.turtles.items())}
    total_in_stress = sum(in_stress.values())

    # Force immediate triadic closure at u1R
    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    closure = world.collisions[-1]
    ledger_after_closure = world.hub_ledger["u1R"]

    out_stress_closure = {name: world.turtles[name].carried_stress for name in sorted(world.turtles)}
    total_out_closure = sum(out_stress_closure.values())

    # Export packet one hop to mR so we can inspect what survives transport
    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    bundle = world.collisions[-1]

    out_stress_export = {name: world.turtles[name].carried_stress for name in sorted(world.turtles)}
    total_out_export = sum(out_stress_export.values())

    deposited = ledger_after_closure.deposited_stress
    stress_energy = ledger_after_closure.stress_energy
    stored_tension = ledger_after_closure.stored_tension

    print(f"\ncase: {closure_case_name(stress_vec)}")
    print(f"  incoming_signs      = {in_signs}")
    print(f"  incoming_mismatch   = {in_mismatch}")
    print(f"  incoming_stress     = {in_stress}")
    print(f"  total_in_stress     = {total_in_stress}")
    print(f"  closure_class       = {closure.face_event}")
    print(f"  closure_out_stress  = {out_stress_closure}")
    print(f"  total_after_closure = {total_out_closure}")
    print(f"  export_face         = {bundle.face_event}")
    print(f"  export_out_stress   = {out_stress_export}")
    print(f"  total_after_export  = {total_out_export}")
    print(f"  deposited_stress    = {deposited}")
    print(f"  stress_energy       = {stress_energy}")
    print(f"  stored_tension      = {stored_tension}")
    print(f"  sorted_profile      = {tuple(sorted(stress_vec, reverse=True))}")
    print(f"  max_minus_min       = {max(stress_vec) - min(stress_vec)}")


def main() -> None:
    print_header()

    # Small systematic table:
    # all coherent zero-mismatch profiles with entries in {0,1,2}
    for stress_vec in product((0, 1, 2), repeat=3):
        run_case(stress_vec)


if __name__ == "__main__":
    main()
