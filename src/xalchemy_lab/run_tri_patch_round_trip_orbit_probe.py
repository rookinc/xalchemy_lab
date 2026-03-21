from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


CASES = [
    ("s000", (0, 0, 0)),
    ("s100", (1, 0, 0)),
    ("s111", (1, 1, 1)),
    ("s300", (3, 0, 0)),
    ("s421", (4, 2, 1)),
    ("s444", (4, 4, 4)),
    ("s633", (6, 3, 3)),
]


def make_world(stress_vec: tuple[int, int, int]) -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node="u1R", carry_sign="+", carried_stress=stress_vec[0]),
            "L2": Turtle(name="L2", chirality="L", node="u1R", carry_sign="+", carried_stress=stress_vec[1]),
            "R1": Turtle(name="R1", chirality="R", node="u1R", carry_sign="+", carried_stress=stress_vec[2]),
        }
    )


def vec(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[name].carried_stress for name in ("L1", "L2", "R1"))


def signs(world: World) -> tuple[str | None, str | None, str | None]:
    return tuple(world.turtles[name].carry_sign for name in ("L1", "L2", "R1"))


def mismatch(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[name].mismatch_count for name in ("L1", "L2", "R1"))


def print_phase(label: str, world: World) -> None:
    print(f"  {label}")
    print(f"    signs     = {signs(world)}")
    print(f"    stress    = {vec(world)}")
    print(f"    mismatch  = {mismatch(world)}")


def run_case(label: str, stress_vec: tuple[int, int, int]) -> None:
    world = make_world(stress_vec)

    print(f"\ncase: {label}")
    print(f"  initial incoming stress @ u1R = {stress_vec}")
    print_phase("state_0", world)

    # Closure at u1R
    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    c1 = world.collisions[-1]
    print(f"  closure_1_face = {c1.face_event}")
    print_phase("after_u1R_closure", world)

    # Export to mR
    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    e1 = world.collisions[-1]
    print(f"  export_1_face  = {e1.face_event}")
    print_phase("after_mR_export_1", world)

    # Re-entry at d1R
    step(world, {"L1": "d1R", "L2": "d1R", "R1": "d1R"})
    c2 = world.collisions[-1]
    print(f"  closure_2_face = {c2.face_event}")
    print_phase("after_d1R_closure", world)

    # Export back through mR
    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    e2 = world.collisions[-1]
    print(f"  export_2_face  = {e2.face_event}")
    print_phase("after_mR_export_2", world)

    # Return to u1R
    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    c3 = world.collisions[-1]
    print(f"  closure_3_face = {c3.face_event}")
    print_phase("after_u1R_return", world)

    initial = stress_vec
    after_first_u1R = (
        tuple(max(s - 1, 0) for s in stress_vec)
        if c1.face_event.endswith("_closed")
        else tuple(s + 1 for s in stress_vec)
    )
    final_vec = vec(world)

    print(f"  summary")
    print(f"    initial_stress        = {initial}")
    print(f"    after_first_u1R       = {after_first_u1R}")
    print(f"    after_round_trip      = {final_vec}")
    print(f"    round_trip_fixed      = {final_vec == initial}")

    ledger_u1r = world.hub_ledger["u1R"]
    ledger_d1r = world.hub_ledger["d1R"]
    print(
        "    u1R_ledger           = "
        f"stress_energy={ledger_u1r.stress_energy} "
        f"stored_tension={ledger_u1r.stored_tension} "
        f"deposited={ledger_u1r.deposited_stress} "
        f"clean={ledger_u1r.clean_closures} "
        f"tension={ledger_u1r.tension_closures}"
    )
    print(
        "    d1R_ledger           = "
        f"stress_energy={ledger_d1r.stress_energy} "
        f"stored_tension={ledger_d1r.stored_tension} "
        f"deposited={ledger_d1r.deposited_stress} "
        f"clean={ledger_d1r.clean_closures} "
        f"tension={ledger_d1r.tension_closures}"
    )


def main() -> None:
    print("\n====================")
    print("ROUND-TRIP ORBIT PROBE")
    print("====================")
    print("u1R closure -> mR export -> d1R closure -> mR export -> u1R return")

    for label, stress_vec in CASES:
        run_case(label, stress_vec)


if __name__ == "__main__":
    main()
