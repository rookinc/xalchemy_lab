from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


N_CYCLES = 6


def make_locked_world(
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


def full_cycle(world: World, start_node: str) -> dict[str, object]:
    if start_node == "u1R":
        first_hub = "u1R"
        opposite_hub = "d1R"
    elif start_node == "d1R":
        first_hub = "d1R"
        opposite_hub = "u1R"
    else:
        raise ValueError(f"Unexpected start node: {start_node}")

    step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})
    first_face = world.collisions[-1].face_event

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    export_1 = world.collisions[-1].face_event

    step(world, {"L1": opposite_hub, "L2": opposite_hub, "R1": opposite_hub})
    opposite_face = world.collisions[-1].face_event

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    export_2 = world.collisions[-1].face_event

    step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})
    return_face = world.collisions[-1].face_event

    return {
        "first_face": first_face,
        "export_1": export_1,
        "opposite_face": opposite_face,
        "export_2": export_2,
        "return_face": return_face,
        "stress": stress_vec(world),
        "mismatch": mismatch_vec(world),
        "signs": sign_vec(world),
    }


def detect_relock(cycle_records: list[dict[str, object]], stress_deltas: list[tuple[int, int, int]], mismatch_deltas: list[tuple[int, int, int]]) -> tuple[int | None, tuple[int, int, int] | None, tuple[int, int, int] | None]:
    for i in range(1, len(cycle_records)):
        a = cycle_records[i - 1]
        b = cycle_records[i]

        faces_ok = (
            str(a["first_face"]).endswith("_tension")
            and str(a["opposite_face"]).endswith("_tension")
            and str(a["return_face"]).endswith("_tension")
            and str(b["first_face"]).endswith("_tension")
            and str(b["opposite_face"]).endswith("_tension")
            and str(b["return_face"]).endswith("_tension")
        )

        signs_ok = a["signs"] == b["signs"]
        delta_ok = (
            stress_deltas[i] == stress_deltas[i - 1]
            and mismatch_deltas[i] == mismatch_deltas[i - 1]
        )

        if faces_ok and signs_ok and delta_ok:
            return i + 1, stress_deltas[i], mismatch_deltas[i]

    return None, None, None


def run_case(
    label: str,
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    perturbation: str,
) -> None:
    world = make_locked_world(start_node, sign, stress, mismatch)

    print(f"\n====================")
    print(f"CASE: {label}")
    print("====================")
    print(f"base_start_node     = {start_node}")
    print(f"base_signs          = {sign_vec(world)}")
    print(f"base_stress         = {stress_vec(world)}")
    print(f"base_mismatch       = {mismatch_vec(world)}")
    print(f"perturbation        = {perturbation}")

    # Apply one perturbation in place.
    if perturbation == "stress_plus_one_on_L1":
        world.turtles["L1"].carried_stress += 1
    elif perturbation == "mismatch_plus_one_on_L1":
        world.turtles["L1"].mismatch_count += 1
    elif perturbation == "flip_sign_on_L1":
        current = world.turtles["L1"].carry_sign
        if current == "+":
            world.turtles["L1"].carry_sign = "-"
        elif current == "-":
            world.turtles["L1"].carry_sign = "+"
        else:
            raise ValueError("Cannot flip a None sign")
    elif perturbation == "stress_plus_two_on_R1":
        world.turtles["R1"].carried_stress += 2
    elif perturbation == "mismatch_plus_two_on_R1":
        world.turtles["R1"].mismatch_count += 2
    else:
        raise ValueError(f"Unknown perturbation: {perturbation}")

    print(f"post_perturb_signs  = {sign_vec(world)}")
    print(f"post_perturb_stress = {stress_vec(world)}")
    print(f"post_perturb_mis    = {mismatch_vec(world)}")

    prev_stress = stress_vec(world)
    prev_mismatch = mismatch_vec(world)
    cycle_records: list[dict[str, object]] = []
    stress_deltas: list[tuple[int, int, int]] = []
    mismatch_deltas: list[tuple[int, int, int]] = []

    for cycle in range(1, N_CYCLES + 1):
        rec = full_cycle(world, start_node)
        curr_stress = rec["stress"]  # type: ignore[assignment]
        curr_mismatch = rec["mismatch"]  # type: ignore[assignment]

        ds = sub_vec(curr_stress, prev_stress)
        dm = sub_vec(curr_mismatch, prev_mismatch)

        cycle_records.append(rec)
        stress_deltas.append(ds)
        mismatch_deltas.append(dm)

        print(f"\ncycle {cycle}")
        print(f"  first_face        = {rec['first_face']}")
        print(f"  opposite_face     = {rec['opposite_face']}")
        print(f"  return_face       = {rec['return_face']}")
        print(f"  signs             = {rec['signs']}")
        print(f"  stress            = {curr_stress}")
        print(f"  mismatch          = {curr_mismatch}")
        print(f"  delta_stress      = {ds}")
        print(f"  delta_mismatch    = {dm}")

        prev_stress = curr_stress
        prev_mismatch = curr_mismatch

    relock_cycle, ds_lock, dm_lock = detect_relock(cycle_records, stress_deltas, mismatch_deltas)

    print("\nsummary")
    print(f"  relock_cycle      = {relock_cycle}")
    print(f"  locked_ds         = {ds_lock}")
    print(f"  locked_dm         = {dm_lock}")
    print(f"  final_signs       = {cycle_records[-1]['signs']}")
    print(f"  final_stress      = {cycle_records[-1]['stress']}")
    print(f"  final_mismatch    = {cycle_records[-1]['mismatch']}")


def main() -> None:
    print("\n====================")
    print("RAIL PERTURBATION PROBE")
    print("====================")
    print("Start from locked rail states, inject one asymmetric perturbation, and test for re-lock.")

    cases = [
        ("u1R_locked_stress_L1", "u1R", "+", (8, 8, 8), (4, 4, 4), "stress_plus_one_on_L1"),
        ("u1R_locked_mismatch_L1", "u1R", "+", (8, 8, 8), (4, 4, 4), "mismatch_plus_one_on_L1"),
        ("u1R_locked_flip_L1", "u1R", "+", (8, 8, 8), (4, 4, 4), "flip_sign_on_L1"),
        ("u1R_locked_stress_R1", "u1R", "+", (8, 8, 8), (4, 4, 4), "stress_plus_two_on_R1"),
        ("u1R_locked_mismatch_R1", "u1R", "+", (8, 8, 8), (4, 4, 4), "mismatch_plus_two_on_R1"),

        ("d1R_locked_stress_L1", "d1R", "-", (8, 8, 8), (4, 4, 4), "stress_plus_one_on_L1"),
        ("d1R_locked_mismatch_L1", "d1R", "-", (8, 8, 8), (4, 4, 4), "mismatch_plus_one_on_L1"),
        ("d1R_locked_flip_L1", "d1R", "-", (8, 8, 8), (4, 4, 4), "flip_sign_on_L1"),
        ("d1R_locked_stress_R1", "d1R", "-", (8, 8, 8), (4, 4, 4), "stress_plus_two_on_R1"),
        ("d1R_locked_mismatch_R1", "d1R", "-", (8, 8, 8), (4, 4, 4), "mismatch_plus_two_on_R1"),
    ]

    for case in cases:
        run_case(*case)


if __name__ == "__main__":
    main()
