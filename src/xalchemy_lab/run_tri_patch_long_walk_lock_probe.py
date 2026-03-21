from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


def make_locked_world(start_node: str, sign: str, stress: tuple[int, int, int], mismatch: tuple[int, int, int]) -> World:
    return World(
        turtles={
            "L1": Turtle(
                name="L1",
                chirality="L",
                node=start_node,
                carry_sign=sign,
                carried_stress=stress[0],
                mismatch_count=mismatch[0],
            ),
            "L2": Turtle(
                name="L2",
                chirality="L",
                node=start_node,
                carry_sign=sign,
                carried_stress=stress[1],
                mismatch_count=mismatch[1],
            ),
            "R1": Turtle(
                name="R1",
                chirality="R",
                node=start_node,
                carry_sign=sign,
                carried_stress=stress[2],
                mismatch_count=mismatch[2],
            ),
        }
    )


def stress_vec(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[name].carried_stress for name in ("L1", "L2", "R1"))


def mismatch_vec(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[name].mismatch_count for name in ("L1", "L2", "R1"))


def sign_vec(world: World) -> tuple[str | None, str | None, str | None]:
    return tuple(world.turtles[name].carry_sign for name in ("L1", "L2", "R1"))


def print_state(world: World, label: str) -> None:
    print(label)
    print(f"  signs      = {sign_vec(world)}")
    print(f"  stress     = {stress_vec(world)}")
    print(f"  mismatch   = {mismatch_vec(world)}")


def do_step(world: World, label: str, moves: dict[str, str]) -> None:
    step(world, moves)
    collision = world.collisions[-1] if world.collisions else None
    print(f"\n{label}")
    print(f"  moves      = {moves}")
    if collision is not None:
        print(f"  face_event = {collision.face_event}")
        print(f"  node       = {collision.node}")
        print(f"  kind       = {collision.kind}")
    print_state(world, "  state")


def run_positive_long_walk() -> None:
    print("\n====================")
    print("POSITIVE LONG WALK")
    print("====================")

    # Start from a representative locked state found by the basin map.
    world = make_locked_world(
        start_node="u1R",
        sign="+",
        stress=(8, 8, 8),
        mismatch=(4, 4, 4),
    )
    print_state(world, "initial locked state @ u1R")

    # Standard cycle skeleton, repeated further than before.
    schedule = [
        ("cycle A: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle A: hit d1R", {"L1": "d1R", "L2": "d1R", "R1": "d1R"}),
        ("cycle A: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle A: return to u1R", {"L1": "u1R", "L2": "u1R", "R1": "u1R"}),

        ("cycle B: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle B: hit d1R", {"L1": "d1R", "L2": "d1R", "R1": "d1R"}),
        ("cycle B: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle B: return to u1R", {"L1": "u1R", "L2": "u1R", "R1": "u1R"}),

        ("cycle C: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle C: hit d1R", {"L1": "d1R", "L2": "d1R", "R1": "d1R"}),
        ("cycle C: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle C: return to u1R", {"L1": "u1R", "L2": "u1R", "R1": "u1R"}),
    ]

    for label, moves in schedule:
        do_step(world, label, moves)

    print("\nfinal ledger snapshot")
    for hub in ("u1R", "d1R"):
        ledger = world.hub_ledger[hub]
        print(
            f"  {hub}: stress_energy={ledger.stress_energy} "
            f"stored_tension={ledger.stored_tension} "
            f"deposited={ledger.deposited_stress} "
            f"clean={ledger.clean_closures} "
            f"tension={ledger.tension_closures}"
        )


def run_negative_long_walk() -> None:
    print("\n====================")
    print("NEGATIVE LONG WALK")
    print("====================")

    world = make_locked_world(
        start_node="d1R",
        sign="-",
        stress=(8, 8, 8),
        mismatch=(4, 4, 4),
    )
    print_state(world, "initial locked state @ d1R")

    schedule = [
        ("cycle A: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle A: hit u1R", {"L1": "u1R", "L2": "u1R", "R1": "u1R"}),
        ("cycle A: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle A: return to d1R", {"L1": "d1R", "L2": "d1R", "R1": "d1R"}),

        ("cycle B: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle B: hit u1R", {"L1": "u1R", "L2": "u1R", "R1": "u1R"}),
        ("cycle B: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle B: return to d1R", {"L1": "d1R", "L2": "d1R", "R1": "d1R"}),

        ("cycle C: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle C: hit u1R", {"L1": "u1R", "L2": "u1R", "R1": "u1R"}),
        ("cycle C: export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
        ("cycle C: return to d1R", {"L1": "d1R", "L2": "d1R", "R1": "d1R"}),
    ]

    for label, moves in schedule:
        do_step(world, label, moves)

    print("\nfinal ledger snapshot")
    for hub in ("u1R", "d1R"):
        ledger = world.hub_ledger[hub]
        print(
            f"  {hub}: stress_energy={ledger.stress_energy} "
            f"stored_tension={ledger.stored_tension} "
            f"deposited={ledger.deposited_stress} "
            f"clean={ledger.clean_closures} "
            f"tension={ledger.tension_closures}"
        )


def main() -> None:
    print("\n====================")
    print("LONG WALK LOCK PROBE")
    print("====================")
    print("Follow already-locked states through several additional admissible transport rounds.")
    run_positive_long_walk()
    run_negative_long_walk()


if __name__ == "__main__":
    main()
