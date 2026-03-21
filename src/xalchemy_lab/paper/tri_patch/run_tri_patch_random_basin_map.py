from __future__ import annotations

import random

from xalchemy_lab.tri_patch_core import World, Turtle, step


N_CYCLES = 6
N_SAMPLES = 120
RANDOM_SEED = 12345


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
    start_node: str,
    signs: tuple[str, str, str],
    mismatch: tuple[int, int, int],
    stress: tuple[int, int, int],
) -> dict[str, object]:
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
    return {
        "lock_cycle": lock_cycle,
        "stress_growth": inferred_stress_delta,
        "mismatch_growth": inferred_mismatch_delta,
        "final_signs": final["signs"],
        "final_stress": final["stress"],
        "final_mismatch": final["mismatch"],
        "final_faces": (
            final["first_face"],
            final["opposite_face"],
            final["return_face"],
        ),
    }


def main() -> None:
    rng = random.Random(RANDOM_SEED)

    print("\n====================")
    print("RANDOM BASIN MAP")
    print("====================")
    print(f"samples     = {N_SAMPLES}")
    print(f"cycles      = {N_CYCLES}")
    print(f"random_seed = {RANDOM_SEED}")
    print("signs in {+,-}, mismatch in {0,1,2}, stress in {0,1,2,3,4}")

    summary: dict[str, int] = {}
    lock_examples: list[str] = []
    fail_examples: list[str] = []

    for idx in range(1, N_SAMPLES + 1):
        start_node = rng.choice(["u1R", "d1R"])
        signs = (
            rng.choice(["+", "-"]),
            rng.choice(["+", "-"]),
            rng.choice(["+", "-"]),
        )
        mismatch = (
            rng.randint(0, 2),
            rng.randint(0, 2),
            rng.randint(0, 2),
        )
        stress = (
            rng.randint(0, 4),
            rng.randint(0, 4),
            rng.randint(0, 4),
        )

        result = classify_seed(start_node, signs, mismatch, stress)

        lock_cycle = result["lock_cycle"]
        final_signs = result["final_signs"]
        stress_growth = result["stress_growth"]
        mismatch_growth = result["mismatch_growth"]

        bucket = (
            f"lock={lock_cycle} "
            f"final_signs={final_signs} "
            f"ds={stress_growth} "
            f"dm={mismatch_growth}"
        )
        summary[bucket] = summary.get(bucket, 0) + 1

        line = (
            f"sample={idx:03d} "
            f"start={start_node} "
            f"signs={signs} "
            f"mismatch={mismatch} "
            f"stress={stress} "
            f"-> lock={lock_cycle} "
            f"final_signs={final_signs} "
            f"ds={stress_growth} "
            f"dm={mismatch_growth} "
            f"final_faces={result['final_faces']}"
        )

        if lock_cycle is not None and len(lock_examples) < 12:
            lock_examples.append(line)
        if lock_cycle is None and len(fail_examples) < 12:
            fail_examples.append(line)

    print("\nSUMMARY BUCKETS")
    for key, count in sorted(summary.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  count={count:03d}  {key}")

    print("\nLOCKED EXAMPLES")
    if lock_examples:
        for line in lock_examples:
            print(f"  {line}")
    else:
        print("  none")

    print("\nNON-LOCKED EXAMPLES")
    if fail_examples:
        for line in fail_examples:
            print(f"  {line}")
    else:
        print("  none")


if __name__ == "__main__":
    main()
