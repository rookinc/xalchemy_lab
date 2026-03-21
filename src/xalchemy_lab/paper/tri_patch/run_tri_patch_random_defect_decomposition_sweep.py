from __future__ import annotations

import random

from xalchemy_lab.tri_patch_core import World, Turtle, step


N_CYCLES = 6
N_SAMPLES = 120
RANDOM_SEED = 24680


BASIS_PERTURBATIONS = [
    "stress_plus_one_on_L1",
    "stress_plus_one_on_L2",
    "stress_plus_one_on_R1",
    "mismatch_plus_one_on_L1",
    "mismatch_plus_one_on_L2",
    "mismatch_plus_one_on_R1",
    "flip_sign_on_L1",
    "flip_sign_on_L2",
    "flip_sign_on_R1",
]


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


def sub_vec(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add_vec(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def full_cycle(world: World, start_node: str) -> None:
    if start_node == "u1R":
        first_hub = "u1R"
        opposite_hub = "d1R"
    elif start_node == "d1R":
        first_hub = "d1R"
        opposite_hub = "u1R"
    else:
        raise ValueError(f"Unexpected start node: {start_node}")

    step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})
    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    step(world, {"L1": opposite_hub, "L2": opposite_hub, "R1": opposite_hub})
    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})


def apply_one(world: World, perturbation: str) -> None:
    if perturbation == "stress_plus_one_on_L1":
        world.turtles["L1"].carried_stress += 1
        return
    if perturbation == "stress_plus_one_on_L2":
        world.turtles["L2"].carried_stress += 1
        return
    if perturbation == "stress_plus_one_on_R1":
        world.turtles["R1"].carried_stress += 1
        return
    if perturbation == "mismatch_plus_one_on_L1":
        world.turtles["L1"].mismatch_count += 1
        return
    if perturbation == "mismatch_plus_one_on_L2":
        world.turtles["L2"].mismatch_count += 1
        return
    if perturbation == "mismatch_plus_one_on_R1":
        world.turtles["R1"].mismatch_count += 1
        return
    if perturbation == "flip_sign_on_L1":
        world.turtles["L1"].carry_sign = "-" if world.turtles["L1"].carry_sign == "+" else "+"
        return
    if perturbation == "flip_sign_on_L2":
        world.turtles["L2"].carry_sign = "-" if world.turtles["L2"].carry_sign == "+" else "+"
        return
    if perturbation == "flip_sign_on_R1":
        world.turtles["R1"].carry_sign = "-" if world.turtles["R1"].carry_sign == "+" else "+"
        return
    raise ValueError(f"Unknown perturbation: {perturbation}")


def apply_many(world: World, perturbations: list[str]) -> None:
    for p in perturbations:
        apply_one(world, p)


def stabilized_offset(
    start_node: str,
    sign: str,
    base_stress: tuple[int, int, int],
    base_mismatch: tuple[int, int, int],
    perturbations: list[str],
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    baseline = make_world(start_node, sign, base_stress, base_mismatch)
    perturbed = make_world(start_node, sign, base_stress, base_mismatch)

    apply_many(perturbed, perturbations)

    last_ds = None
    last_dm = None

    for _ in range(N_CYCLES):
        full_cycle(baseline, start_node)
        full_cycle(perturbed, start_node)
        last_ds = sub_vec(stress_vec(perturbed), stress_vec(baseline))
        last_dm = sub_vec(mismatch_vec(perturbed), mismatch_vec(baseline))

    assert last_ds is not None and last_dm is not None
    return last_ds, last_dm


def main() -> None:
    rng = random.Random(RANDOM_SEED)

    print("\n====================")
    print("RANDOM DEFECT DECOMPOSITION SWEEP")
    print("====================")
    print(f"samples      = {N_SAMPLES}")
    print(f"cycles       = {N_CYCLES}")
    print(f"random_seed  = {RANDOM_SEED}")
    print("Testing whether random small combined perturbations decompose into sums of primitive basis defects.")

    base_stress = (8, 8, 8)
    base_mismatch = (4, 4, 4)

    summary: dict[str, int] = {}
    examples: list[str] = []

    for sample in range(1, N_SAMPLES + 1):
        start_node = rng.choice(["u1R", "d1R"])
        sign = "+" if start_node == "u1R" else "-"

        k = rng.randint(1, 4)
        perturbations = [rng.choice(BASIS_PERTURBATIONS) for _ in range(k)]

        ds_combo, dm_combo = stabilized_offset(
            start_node, sign, base_stress, base_mismatch, perturbations
        )

        ds_sum = (0, 0, 0)
        dm_sum = (0, 0, 0)
        for p in perturbations:
            ds_p, dm_p = stabilized_offset(
                start_node, sign, base_stress, base_mismatch, [p]
            )
            ds_sum = add_vec(ds_sum, ds_p)
            dm_sum = add_vec(dm_sum, dm_p)

        stress_ok = ds_combo == ds_sum
        mismatch_ok = dm_combo == dm_sum
        ok = stress_ok and mismatch_ok

        bucket = f"ok={ok} start={start_node} k={k}"
        summary[bucket] = summary.get(bucket, 0) + 1

        line = (
            f"sample={sample:03d} "
            f"start={start_node} "
            f"perturbations={perturbations} "
            f"ds_combo={ds_combo} "
            f"dm_combo={dm_combo} "
            f"ds_sum={ds_sum} "
            f"dm_sum={dm_sum} "
            f"stress_ok={stress_ok} "
            f"mismatch_ok={mismatch_ok}"
        )
        if len(examples) < 20:
            examples.append(line)

    print("\nSUMMARY")
    for key, count in sorted(summary.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  count={count:03d}  {key}")

    print("\nEXAMPLES")
    for line in examples:
        print(f"  {line}")


if __name__ == "__main__":
    main()
