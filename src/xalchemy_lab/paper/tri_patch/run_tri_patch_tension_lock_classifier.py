from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


SEEDS = [
    ("u1R_pos_s000", "u1R", "+", (0, 0, 0)),
    ("u1R_pos_s111", "u1R", "+", (1, 1, 1)),
    ("u1R_pos_s300", "u1R", "+", (3, 0, 0)),
    ("u1R_pos_s421", "u1R", "+", (4, 2, 1)),
    ("u1R_pos_s444", "u1R", "+", (4, 4, 4)),
    ("d1R_neg_s000", "d1R", "-", (0, 0, 0)),
    ("d1R_neg_s111", "d1R", "-", (1, 1, 1)),
    ("d1R_neg_s300", "d1R", "-", (3, 0, 0)),
    ("d1R_neg_s421", "d1R", "-", (4, 2, 1)),
    ("d1R_neg_s444", "d1R", "-", (4, 4, 4)),
]

N_CYCLES = 8


def make_world(start_node: str, sign: str, stress_vec: tuple[int, int, int]) -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=start_node, carry_sign=sign, carried_stress=stress_vec[0]),
            "L2": Turtle(name="L2", chirality="L", node=start_node, carry_sign=sign, carried_stress=stress_vec[1]),
            "R1": Turtle(name="R1", chirality="R", node=start_node, carry_sign=sign, carried_stress=stress_vec[2]),
        }
    )


def stress_vec(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[name].carried_stress for name in ("L1", "L2", "R1"))


def mismatch_vec(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[name].mismatch_count for name in ("L1", "L2", "R1"))


def sign_vec(world: World) -> tuple[str | None, str | None, str | None]:
    return tuple(world.turtles[name].carry_sign for name in ("L1", "L2", "R1"))


def add_vec(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


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


def main() -> None:
    print("\n====================")
    print("TENSION LOCK CLASSIFIER")
    print("====================")
    print("Detect first cycle where the orbit appears to enter a stable affine tension regime.")

    for label, start_node, sign, seed in SEEDS:
        world = make_world(start_node, sign, seed)
        print(f"\nseed: {label}")
        print(f"  start_node          = {start_node}")
        print(f"  initial_sign        = {sign}")
        print(f"  initial_stress      = {seed}")

        prev_stress = stress_vec(world)
        prev_mismatch = mismatch_vec(world)

        stress_deltas: list[tuple[int, int, int]] = []
        mismatch_deltas: list[tuple[int, int, int]] = []
        cycle_records: list[dict[str, object]] = []

        for cycle in range(1, N_CYCLES + 1):
            result = full_cycle(world, start_node)
            curr_stress = result["stress"]  # type: ignore[assignment]
            curr_mismatch = result["mismatch"]  # type: ignore[assignment]

            ds = sub_vec(curr_stress, prev_stress)
            dm = sub_vec(curr_mismatch, prev_mismatch)

            stress_deltas.append(ds)
            mismatch_deltas.append(dm)
            cycle_records.append(result)

            print(f"  cycle {cycle}")
            print(f"    first_face        = {result['first_face']}")
            print(f"    opposite_face     = {result['opposite_face']}")
            print(f"    return_face       = {result['return_face']}")
            print(f"    signs             = {result['signs']}")
            print(f"    stress            = {curr_stress}")
            print(f"    mismatch          = {curr_mismatch}")
            print(f"    delta_stress      = {ds}")
            print(f"    delta_mismatch    = {dm}")

            prev_stress = curr_stress
            prev_mismatch = curr_mismatch

        lock_cycle = None
        inferred_stress_delta = None
        inferred_mismatch_delta = None

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
                lock_cycle = i  # first cycle index after which regime appears stable
                inferred_stress_delta = stress_deltas[i]
                inferred_mismatch_delta = mismatch_deltas[i]
                break

        print("  summary")
        print(f"    lock_cycle        = {lock_cycle}")
        print(f"    stress_growth     = {inferred_stress_delta}")
        print(f"    mismatch_growth   = {inferred_mismatch_delta}")


if __name__ == "__main__":
    main()
