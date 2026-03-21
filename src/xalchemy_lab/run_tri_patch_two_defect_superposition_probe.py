from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


N_CYCLES = 6


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


def add_vec(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


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
    _export_1 = world.collisions[-1].face_event

    step(world, {"L1": opposite_hub, "L2": opposite_hub, "R1": opposite_hub})
    opposite_face = world.collisions[-1].face_event

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    _export_2 = world.collisions[-1].face_event

    step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})
    return_face = world.collisions[-1].face_event

    return {
        "first_face": first_face,
        "opposite_face": opposite_face,
        "return_face": return_face,
        "stress": stress_vec(world),
        "mismatch": mismatch_vec(world),
        "signs": sign_vec(world),
    }


def apply_perturbation(world: World, perturbation: str) -> None:
    if perturbation == "none":
        return
    if perturbation == "stress_plus_one_on_L1":
        world.turtles["L1"].carried_stress += 1
        return
    if perturbation == "stress_plus_two_on_R1":
        world.turtles["R1"].carried_stress += 2
        return
    if perturbation == "mismatch_plus_one_on_L1":
        world.turtles["L1"].mismatch_count += 1
        return
    if perturbation == "mismatch_plus_two_on_R1":
        world.turtles["R1"].mismatch_count += 2
        return
    if perturbation == "flip_sign_on_L1":
        current = world.turtles["L1"].carry_sign
        world.turtles["L1"].carry_sign = "-" if current == "+" else "+"
        return
    if perturbation == "stress_plus_one_on_L1__mismatch_plus_two_on_R1":
        world.turtles["L1"].carried_stress += 1
        world.turtles["R1"].mismatch_count += 2
        return
    if perturbation == "stress_plus_two_on_R1__mismatch_plus_one_on_L1":
        world.turtles["R1"].carried_stress += 2
        world.turtles["L1"].mismatch_count += 1
        return
    if perturbation == "flip_sign_on_L1__stress_plus_two_on_R1":
        current = world.turtles["L1"].carry_sign
        world.turtles["L1"].carry_sign = "-" if current == "+" else "+"
        world.turtles["R1"].carried_stress += 2
        return
    raise ValueError(f"Unknown perturbation: {perturbation}")


def stabilized_offset(
    start_node: str,
    sign: str,
    base_stress: tuple[int, int, int],
    base_mismatch: tuple[int, int, int],
    perturbation: str,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    baseline = make_world(start_node, sign, base_stress, base_mismatch)
    perturbed = make_world(start_node, sign, base_stress, base_mismatch)
    apply_perturbation(perturbed, perturbation)

    last_ds = None
    last_dm = None

    for _ in range(N_CYCLES):
        rec_base = full_cycle(baseline, start_node)
        rec_pert = full_cycle(perturbed, start_node)
        ds = sub_vec(rec_pert["stress"], rec_base["stress"])      # type: ignore[arg-type]
        dm = sub_vec(rec_pert["mismatch"], rec_base["mismatch"])  # type: ignore[arg-type]
        last_ds = ds
        last_dm = dm

    assert last_ds is not None and last_dm is not None
    return last_ds, last_dm


def run_family(
    start_node: str,
    sign: str,
    base_stress: tuple[int, int, int],
    base_mismatch: tuple[int, int, int],
    p1: str,
    p2: str,
    combo: str,
) -> None:
    ds1, dm1 = stabilized_offset(start_node, sign, base_stress, base_mismatch, p1)
    ds2, dm2 = stabilized_offset(start_node, sign, base_stress, base_mismatch, p2)
    dsc, dmc = stabilized_offset(start_node, sign, base_stress, base_mismatch, combo)

    expected_ds = add_vec(ds1, ds2)
    expected_dm = add_vec(dm1, dm2)

    print(f"\nfamily: {start_node}_{combo}")
    print(f"  base_sign           = {sign}")
    print(f"  p1                  = {p1}")
    print(f"    ds1               = {ds1}")
    print(f"    dm1               = {dm1}")
    print(f"  p2                  = {p2}")
    print(f"    ds2               = {ds2}")
    print(f"    dm2               = {dm2}")
    print(f"  combo               = {combo}")
    print(f"    ds_combo          = {dsc}")
    print(f"    dm_combo          = {dmc}")
    print(f"  expected_sum_ds     = {expected_ds}")
    print(f"  expected_sum_dm     = {expected_dm}")
    print(f"  stress_superposes   = {dsc == expected_ds}")
    print(f"  mismatch_superposes = {dmc == expected_dm}")


def main() -> None:
    print("\n====================")
    print("TWO DEFECT SUPERPOSITION PROBE")
    print("====================")
    print("Compare stabilized transported offsets for single defects versus combined defects.")

    base_stress = (8, 8, 8)
    base_mismatch = (4, 4, 4)

    families = [
        ("u1R", "+", "stress_plus_one_on_L1", "mismatch_plus_two_on_R1", "stress_plus_one_on_L1__mismatch_plus_two_on_R1"),
        ("u1R", "+", "stress_plus_two_on_R1", "mismatch_plus_one_on_L1", "stress_plus_two_on_R1__mismatch_plus_one_on_L1"),
        ("u1R", "+", "flip_sign_on_L1", "stress_plus_two_on_R1", "flip_sign_on_L1__stress_plus_two_on_R1"),
        ("d1R", "-", "stress_plus_one_on_L1", "mismatch_plus_two_on_R1", "stress_plus_one_on_L1__mismatch_plus_two_on_R1"),
        ("d1R", "-", "stress_plus_two_on_R1", "mismatch_plus_one_on_L1", "stress_plus_two_on_R1__mismatch_plus_one_on_L1"),
        ("d1R", "-", "flip_sign_on_L1", "stress_plus_two_on_R1", "flip_sign_on_L1__stress_plus_two_on_R1"),
    ]

    for start_node, sign, p1, p2, combo in families:
        run_family(
            start_node=start_node,
            sign=sign,
            base_stress=base_stress,
            base_mismatch=base_mismatch,
            p1=p1,
            p2=p2,
            combo=combo,
        )


if __name__ == "__main__":
    main()
