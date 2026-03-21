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


def turtle_state(world: World) -> dict[str, tuple[str | None, int, int]]:
    return {
        name: (
            world.turtles[name].carry_sign,
            world.turtles[name].carried_stress,
            world.turtles[name].mismatch_count,
        )
        for name in ("L1", "L2", "R1")
    }


def run_case(label: str, stress_vec: tuple[int, int, int]) -> None:
    world = make_world(stress_vec)

    print(f"\ncase: {label}")
    print(f"  incoming_stress      = {dict(zip(('L1','L2','R1'), stress_vec))}")
    print(f"  initial_state        = {turtle_state(world)}")

    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    closure = world.collisions[-1]
    print(f"  closure_face         = {closure.face_event}")
    print(f"  post_closure_state   = {turtle_state(world)}")

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    export = world.collisions[-1]
    print(f"  export_face          = {export.face_event}")
    print(f"  post_export_state    = {turtle_state(world)}")

    step(world, {"L1": "d1R", "L2": "d1R", "R1": "d1R"})
    downstream = world.collisions[-1]
    print(f"  downstream_face      = {downstream.face_event}")
    print(f"  post_downstream      = {turtle_state(world)}")

    ledger_u1r = world.hub_ledger["u1R"]
    ledger_d1r = world.hub_ledger["d1R"]
    print(
        "  u1R_ledger           = "
        f"stress_energy={ledger_u1r.stress_energy} "
        f"stored_tension={ledger_u1r.stored_tension} "
        f"deposited={ledger_u1r.deposited_stress} "
        f"clean={ledger_u1r.clean_closures} "
        f"tension={ledger_u1r.tension_closures}"
    )
    print(
        "  d1R_ledger           = "
        f"stress_energy={ledger_d1r.stress_energy} "
        f"stored_tension={ledger_d1r.stored_tension} "
        f"deposited={ledger_d1r.deposited_stress} "
        f"clean={ledger_d1r.clean_closures} "
        f"tension={ledger_d1r.tension_closures}"
    )


def main() -> None:
    print("\n====================")
    print("STRESS PAYLOAD PROBE")
    print("====================")
    print("Same coherent branch, varying incoming stress.")
    print("Check whether stress changes routing/export/downstream recurrence without changing branch selection.")

    for label, stress_vec in CASES:
        run_case(label, stress_vec)


if __name__ == "__main__":
    main()
