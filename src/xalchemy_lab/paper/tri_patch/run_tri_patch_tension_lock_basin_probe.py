from __future__ import annotations

from itertools import product

from xalchemy_lab.tri_patch_core import World, Turtle, step


N_CYCLES = 5


def make_world(
    start_node: str,
    signs: tuple[str, str, str],
    mismatch: tuple[int, int, int],
    stress: tuple[int, int, int],
) -> World:
    return World(
        turtles={
            "L1": Turtle(
                name="L1",
                chirality="L",
                node=start_node,
                carry_sign=signs[0],
                mismatch_count=mismatch[0],
                carried_stress=stress[0],
            ),
            "L2": Turtle(
                name="L2",
                chirality="L",
                node=start_node,
                carry_sign=signs[1],
                mismatch_count=mismatch[1],
                carried_stress=stress[1],
            ),
            "R1": Turtle(
                name="R1",
                chirality="R",
                node=start_node,
                carry_sign=signs[2],
                mismatch_count=mismatch[2],
                carried_stress=stress[2],
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


def classify_seed(
    label: str,
    start_node: str,
    signs: tuple[str, str, str],
    mismatch: tuple[int, int, int],
    stress: tuple[int, int, int],
) -> None:
    world = make_world(start_node, signs, mismatch, stress)

    prev_stress = stress_vec(world)
    prev_mismatch = mismatch_vec(world)

    cycle_records: list[dict[str, object]] = []
    stress_deltas: list[tuple[int, int, int]] = []
    mismatch_deltas: list[tuple[int, int, int]] = []

    for _ in range(N_CYCLES):
        rec = full_cycle(world, start_node)
        curr_stress = rec["stress"]  # type: ignore[assignment]
        curr_mismatch = rec["mismatch"]  # type: ignore[assignment]

        stress_deltas.append(sub_vec(curr_stress, prev_stress))
        mismatch_deltas.append(sub_vec(curr_mismatch, prev_mismatch))
        cycle_records.append(rec)

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
            lock_cycle = i + 1
            inferred_stress_delta = stress_deltas[i]
            inferred_mismatch_delta = mismatch_deltas[i]
            break

    final = cycle_records[-1]
    print(f"\nseed: {label}")
    print(f"  start_node          = {start_node}")
    print(f"  initial_signs       = {signs}")
    print(f"  initial_mismatch    = {mismatch}")
    print(f"  initial_stress      = {stress}")
    print(f"  lock_cycle          = {lock_cycle}")
    print(f"  stress_growth       = {inferred_stress_delta}")
    print(f"  mismatch_growth     = {inferred_mismatch_delta}")
    print(f"  final_signs         = {final['signs']}")
    print(f"  final_stress        = {final['stress']}")
    print(f"  final_mismatch      = {final['mismatch']}")
    print(f"  final_faces         = ({final['first_face']}, {final['opposite_face']}, {final['return_face']})")


def main() -> None:
    print("\n====================")
    print("TENSION LOCK BASIN PROBE")
    print("====================")
    print("Testing whether non-coherent and partially burdened seeds enter the affine tension-locked regime.")

    seeds = [
        ("u1R_coherent_pos_clean", "u1R", ("+", "+", "+"), (0, 0, 0), (1, 1, 1)),
        ("d1R_coherent_neg_clean", "d1R", ("-", "-", "-"), (0, 0, 0), (1, 1, 1)),

        ("u1R_mixed_zero_mismatch", "u1R", ("-", "+", "-"), (0, 0, 0), (1, 1, 1)),
        ("d1R_mixed_zero_mismatch", "d1R", ("+", "-", "+"), (0, 0, 0), (1, 1, 1)),

        ("u1R_coherent_low_mismatch", "u1R", ("+", "+", "+"), (1, 0, 0), (1, 1, 1)),
        ("d1R_coherent_low_mismatch", "d1R", ("-", "-", "-"), (1, 0, 0), (1, 1, 1)),

        ("u1R_coherent_high_mismatch", "u1R", ("+", "+", "+"), (2, 1, 2), (1, 1, 1)),
        ("d1R_coherent_high_mismatch", "d1R", ("-", "-", "-"), (2, 1, 2), (1, 1, 1)),

        ("u1R_mixed_with_mismatch", "u1R", ("-", "+", "-"), (2, 0, 1), (1, 1, 1)),
        ("d1R_mixed_with_mismatch", "d1R", ("+", "-", "+"), (2, 0, 1), (1, 1, 1)),

        ("u1R_mixed_stress_skew", "u1R", ("-", "+", "-"), (0, 0, 0), (4, 2, 1)),
        ("d1R_mixed_stress_skew", "d1R", ("+", "-", "+"), (0, 0, 0), (4, 2, 1)),

        ("u1R_coherent_skew_stress", "u1R", ("+", "+", "+"), (0, 0, 0), (4, 2, 1)),
        ("d1R_coherent_skew_stress", "d1R", ("-", "-", "-"), (0, 0, 0), (4, 2, 1)),
    ]

    for seed in seeds:
        classify_seed(*seed)


if __name__ == "__main__":
    main()
