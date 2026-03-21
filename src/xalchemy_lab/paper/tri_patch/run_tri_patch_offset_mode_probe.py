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


def apply_perturbation(world: World, perturbation: str) -> None:
    if perturbation == "none":
        return
    if perturbation == "stress_plus_one_on_L1":
        world.turtles["L1"].carried_stress += 1
        return
    if perturbation == "mismatch_plus_one_on_L1":
        world.turtles["L1"].mismatch_count += 1
        return
    if perturbation == "flip_sign_on_L1":
        current = world.turtles["L1"].carry_sign
        if current == "+":
            world.turtles["L1"].carry_sign = "-"
        elif current == "-":
            world.turtles["L1"].carry_sign = "+"
        else:
            raise ValueError("Cannot flip None sign")
        return
    if perturbation == "stress_plus_two_on_R1":
        world.turtles["R1"].carried_stress += 2
        return
    if perturbation == "mismatch_plus_two_on_R1":
        world.turtles["R1"].mismatch_count += 2
        return
    raise ValueError(f"Unknown perturbation: {perturbation}")


def run_comparison(
    label: str,
    start_node: str,
    sign: str,
    base_stress: tuple[int, int, int],
    base_mismatch: tuple[int, int, int],
    perturbation: str,
) -> None:
    baseline = make_world(start_node, sign, base_stress, base_mismatch)
    perturbed = make_world(start_node, sign, base_stress, base_mismatch)
    apply_perturbation(perturbed, perturbation)

    print("\n====================")
    print(f"CASE: {label}")
    print("====================")
    print(f"start_node          = {start_node}")
    print(f"baseline_signs      = {sign_vec(baseline)}")
    print(f"baseline_stress     = {stress_vec(baseline)}")
    print(f"baseline_mismatch   = {mismatch_vec(baseline)}")
    print(f"perturbation        = {perturbation}")
    print(f"perturbed_signs     = {sign_vec(perturbed)}")
    print(f"perturbed_stress    = {stress_vec(perturbed)}")
    print(f"perturbed_mismatch  = {mismatch_vec(perturbed)}")

    last_ds = None
    last_dm = None

    for cycle in range(1, N_CYCLES + 1):
        rec_base = full_cycle(baseline, start_node)
        rec_pert = full_cycle(perturbed, start_node)

        s_base = rec_base["stress"]  # type: ignore[assignment]
        s_pert = rec_pert["stress"]  # type: ignore[assignment]
        m_base = rec_base["mismatch"]  # type: ignore[assignment]
        m_pert = rec_pert["mismatch"]  # type: ignore[assignment]

        ds = sub_vec(s_pert, s_base)
        dm = sub_vec(m_pert, m_base)

        stable_s = (ds == last_ds) if last_ds is not None else False
        stable_m = (dm == last_dm) if last_dm is not None else False

        print(f"\ncycle {cycle}")
        print(f"  baseline_faces     = ({rec_base['first_face']}, {rec_base['opposite_face']}, {rec_base['return_face']})")
        print(f"  perturbed_faces    = ({rec_pert['first_face']}, {rec_pert['opposite_face']}, {rec_pert['return_face']})")
        print(f"  baseline_signs     = {rec_base['signs']}")
        print(f"  perturbed_signs    = {rec_pert['signs']}")
        print(f"  baseline_stress    = {s_base}")
        print(f"  perturbed_stress   = {s_pert}")
        print(f"  delta_stress       = {ds}")
        print(f"  baseline_mismatch  = {m_base}")
        print(f"  perturbed_mismatch = {m_pert}")
        print(f"  delta_mismatch     = {dm}")
        print(f"  stress_offset_stable_vs_prev   = {stable_s}")
        print(f"  mismatch_offset_stable_vs_prev = {stable_m}")

        last_ds = ds
        last_dm = dm


def main() -> None:
    print("\n====================")
    print("OFFSET MODE PROBE")
    print("====================")
    print("Compare a perturbed locked rail against its unperturbed baseline and track defect offsets.")

    cases = [
        ("u1R_stress_L1", "u1R", "+", (8, 8, 8), (4, 4, 4), "stress_plus_one_on_L1"),
        ("u1R_mismatch_L1", "u1R", "+", (8, 8, 8), (4, 4, 4), "mismatch_plus_one_on_L1"),
        ("u1R_flip_L1", "u1R", "+", (8, 8, 8), (4, 4, 4), "flip_sign_on_L1"),
        ("u1R_stress_R1", "u1R", "+", (8, 8, 8), (4, 4, 4), "stress_plus_two_on_R1"),
        ("u1R_mismatch_R1", "u1R", "+", (8, 8, 8), (4, 4, 4), "mismatch_plus_two_on_R1"),
        ("d1R_stress_L1", "d1R", "-", (8, 8, 8), (4, 4, 4), "stress_plus_one_on_L1"),
        ("d1R_mismatch_L1", "d1R", "-", (8, 8, 8), (4, 4, 4), "mismatch_plus_one_on_L1"),
        ("d1R_flip_L1", "d1R", "-", (8, 8, 8), (4, 4, 4), "flip_sign_on_L1"),
        ("d1R_stress_R1", "d1R", "-", (8, 8, 8), (4, 4, 4), "stress_plus_two_on_R1"),
        ("d1R_mismatch_R1", "d1R", "-", (8, 8, 8), (4, 4, 4), "mismatch_plus_two_on_R1"),
    ]

    for case in cases:
        run_comparison(*case)


if __name__ == "__main__":
    main()
