from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


def make_world(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
) -> World:
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


def sub_vec(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def print_state(world: World, label: str) -> None:
    print(label)
    print(f"  nodes      = {tuple(world.turtles[name].node for name in ('L1', 'L2', 'R1'))}")
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


def predicted_rail_after_one_loop(
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    return (
        (stress[0] + 2, stress[1] + 2, stress[2] + 2),
        (mismatch[0] + 2, mismatch[1] + 2, mismatch[2] + 2),
    )


def run_case(
    label: str,
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    defect_note: str,
) -> None:
    print("\n====================")
    print(f"CASE: {label}")
    print("====================")
    print(f"start_node   = {start_node}")
    print(f"defect_note  = {defect_note}")

    world = make_world(start_node, sign, stress, mismatch)
    print_state(world, "initial")

    pred_s, pred_m = predicted_rail_after_one_loop(stress, mismatch)
    print("\npredicted standard-rail one-loop result")
    print(f"  predicted_stress   = {pred_s}")
    print(f"  predicted_mismatch = {pred_m}")

    if start_node == "u1R":
        # Standard would be u1R -> mR -> d1R -> mR -> u1R
        # Escape: break bundle by holding L2 at mR while L1,R1 continue.
        schedule = [
            ("hit u1R", {"L1": "u1R", "L2": "u1R", "R1": "u1R"}),
            ("export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
            ("escape split: L1,R1 to d1R; L2 holds at mR", {"L1": "d1R", "L2": "mR", "R1": "d1R"}),
            ("partial return: L1,R1 back to mR; L2 still at mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
            ("rejoin at u1R", {"L1": "u1R", "L2": "u1R", "R1": "u1R"}),
        ]
    else:
        # Standard would be d1R -> mR -> u1R -> mR -> d1R
        schedule = [
            ("hit d1R", {"L1": "d1R", "L2": "d1R", "R1": "d1R"}),
            ("export to mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
            ("escape split: L1,R1 to u1R; L2 holds at mR", {"L1": "u1R", "L2": "mR", "R1": "u1R"}),
            ("partial return: L1,R1 back to mR; L2 still at mR", {"L1": "mR", "L2": "mR", "R1": "mR"}),
            ("rejoin at d1R", {"L1": "d1R", "L2": "d1R", "R1": "d1R"}),
        ]

    for step_label, moves in schedule:
        do_step(world, step_label, moves)

    actual_s = stress_vec(world)
    actual_m = mismatch_vec(world)

    print("\ncomparison to standard rail prediction")
    print(f"  actual_stress      = {actual_s}")
    print(f"  actual_mismatch    = {actual_m}")
    print(f"  delta_vs_pred_s    = {sub_vec(actual_s, pred_s)}")
    print(f"  delta_vs_pred_m    = {sub_vec(actual_m, pred_m)}")
    print(f"  final_signs        = {sign_vec(world)}")
    print(f"  final_nodes        = {tuple(world.turtles[name].node for name in ('L1', 'L2', 'R1'))}")

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
    print("OPERATOR ESCAPE PROBE")
    print("====================")
    print("Deliberately break the standard locked bundle mid-rail and compare the outcome to the rail operator prediction.")

    cases = [
        (
            "u1R_clean_locked",
            "u1R",
            "+",
            (8, 8, 8),
            (4, 4, 4),
            "baseline locked positive rail",
        ),
        (
            "u1R_locked_with_defect",
            "u1R",
            "+",
            (9, 8, 10),
            (5, 4, 6),
            "positive rail with carried stress/mismatch offsets",
        ),
        (
            "d1R_clean_locked",
            "d1R",
            "-",
            (8, 8, 8),
            (4, 4, 4),
            "baseline locked negative rail",
        ),
        (
            "d1R_locked_with_defect",
            "d1R",
            "-",
            (9, 8, 10),
            (5, 4, 6),
            "negative rail with carried stress/mismatch offsets",
        ),
    ]

    for case in cases:
        run_case(*case)


if __name__ == "__main__":
    main()
