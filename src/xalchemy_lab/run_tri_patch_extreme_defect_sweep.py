from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


N_CYCLES = 6
MAX_AMP = 50


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


def stabilized_offset(
    start_node: str,
    sign: str,
    base_stress: tuple[int, int, int],
    base_mismatch: tuple[int, int, int],
    *,
    add_stress: tuple[int, int, int] = (0, 0, 0),
    add_mismatch: tuple[int, int, int] = (0, 0, 0),
) -> dict[str, object]:
    baseline = make_world(start_node, sign, base_stress, base_mismatch)
    perturbed = make_world(start_node, sign, base_stress, base_mismatch)

    for name, idx in (("L1", 0), ("L2", 1), ("R1", 2)):
        perturbed.turtles[name].carried_stress += add_stress[idx]
        perturbed.turtles[name].mismatch_count += add_mismatch[idx]

    last_ds = (0, 0, 0)
    last_dm = (0, 0, 0)
    cycle_records: list[dict[str, object]] = []
    stress_deltas: list[tuple[int, int, int]] = []
    mismatch_deltas: list[tuple[int, int, int]] = []

    prev_stress_base = stress_vec(baseline)
    prev_stress_pert = stress_vec(perturbed)
    prev_mismatch_base = mismatch_vec(baseline)
    prev_mismatch_pert = mismatch_vec(perturbed)

    for _ in range(N_CYCLES):
        rec_base = full_cycle(baseline, start_node)
        rec_pert = full_cycle(perturbed, start_node)

        last_ds = sub_vec(rec_pert["stress"], rec_base["stress"])      # type: ignore[arg-type]
        last_dm = sub_vec(rec_pert["mismatch"], rec_base["mismatch"])  # type: ignore[arg-type]

        growth_base_s = sub_vec(rec_base["stress"], prev_stress_base)        # type: ignore[arg-type]
        growth_pert_s = sub_vec(rec_pert["stress"], prev_stress_pert)        # type: ignore[arg-type]
        growth_base_m = sub_vec(rec_base["mismatch"], prev_mismatch_base)    # type: ignore[arg-type]
        growth_pert_m = sub_vec(rec_pert["mismatch"], prev_mismatch_pert)    # type: ignore[arg-type]

        stress_deltas.append(sub_vec(growth_pert_s, growth_base_s))
        mismatch_deltas.append(sub_vec(growth_pert_m, growth_base_m))
        cycle_records.append(rec_pert)

        prev_stress_base = rec_base["stress"]        # type: ignore[assignment]
        prev_stress_pert = rec_pert["stress"]        # type: ignore[assignment]
        prev_mismatch_base = rec_base["mismatch"]    # type: ignore[assignment]
        prev_mismatch_pert = rec_pert["mismatch"]    # type: ignore[assignment]

    relock_cycle = None
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
        offset_ok = (
            stress_deltas[i] == stress_deltas[i - 1]
            and mismatch_deltas[i] == mismatch_deltas[i - 1]
            and stress_deltas[i] == (0, 0, 0)
            and mismatch_deltas[i] == (0, 0, 0)
        )
        if faces_ok and signs_ok and offset_ok:
            relock_cycle = i + 1
            break

    return {
        "delta_stress": last_ds,
        "delta_mismatch": last_dm,
        "relock_cycle": relock_cycle,
        "final_signs": cycle_records[-1]["signs"],
        "final_faces": (
            cycle_records[-1]["first_face"],
            cycle_records[-1]["opposite_face"],
            cycle_records[-1]["return_face"],
        ),
    }


def scan_family(
    label: str,
    start_node: str,
    sign: str,
    *,
    stress_mode: tuple[int, int, int],
    mismatch_mode: tuple[int, int, int],
) -> None:
    base_stress = (8, 8, 8)
    base_mismatch = (4, 4, 4)

    print("\n====================")
    print(f"SCAN: {label}")
    print("====================")
    print(f"start_node         = {start_node}")
    print(f"stress_mode        = {stress_mode}")
    print(f"mismatch_mode      = {mismatch_mode}")

    first_failure = None

    for amp in range(MAX_AMP + 1):
        add_stress = tuple(amp * x for x in stress_mode)
        add_mismatch = tuple(amp * x for x in mismatch_mode)

        result = stabilized_offset(
            start_node,
            sign,
            base_stress,
            base_mismatch,
            add_stress=add_stress,      # type: ignore[arg-type]
            add_mismatch=add_mismatch,  # type: ignore[arg-type]
        )

        ds_ok = result["delta_stress"] == add_stress
        dm_ok = result["delta_mismatch"] == add_mismatch
        relock_ok = result["relock_cycle"] == 2
        sign_ok = result["final_signs"] == ((sign, sign, sign))

        ok = ds_ok and dm_ok and relock_ok and sign_ok

        print(
            f"amp={amp:02d} "
            f"ds={result['delta_stress']} "
            f"dm={result['delta_mismatch']} "
            f"relock={result['relock_cycle']} "
            f"signs={result['final_signs']} "
            f"ok={ok}"
        )

        if not ok and first_failure is None:
            first_failure = {
                "amp": amp,
                "result": result,
                "expected_ds": add_stress,
                "expected_dm": add_mismatch,
            }

    print("\nsummary")
    if first_failure is None:
        print(f"  no failure detected up to amp={MAX_AMP}")
    else:
        print(f"  first failure at amp={first_failure['amp']}")
        print(f"  expected_ds       = {first_failure['expected_ds']}")
        print(f"  expected_dm       = {first_failure['expected_dm']}")
        print(f"  observed          = {first_failure['result']}")


def main() -> None:
    print("\n====================")
    print("EXTREME DEFECT SWEEP")
    print("====================")
    print(f"Testing amplitudes 0..{MAX_AMP} for exact offset transport and re-lock persistence.")

    scans = [
        ("u1R_stress_L1", "u1R", "+", (1, 0, 0), (0, 0, 0)),
        ("u1R_mismatch_L1", "u1R", "+", (0, 0, 0), (1, 0, 0)),
        ("u1R_stress_L1_mismatch_R1", "u1R", "+", (1, 0, 0), (0, 0, 1)),
        ("u1R_stress_all", "u1R", "+", (1, 1, 1), (0, 0, 0)),
        ("d1R_stress_L1", "d1R", "-", (1, 0, 0), (0, 0, 0)),
        ("d1R_mismatch_L1", "d1R", "-", (0, 0, 0), (1, 0, 0)),
        ("d1R_stress_L1_mismatch_R1", "d1R", "-", (1, 0, 0), (0, 0, 1)),
        ("d1R_stress_all", "d1R", "-", (1, 1, 1), (0, 0, 0)),
    ]

    for label, start_node, sign, stress_mode, mismatch_mode in scans:
        scan_family(
            label=label,
            start_node=start_node,
            sign=sign,
            stress_mode=stress_mode,
            mismatch_mode=mismatch_mode,
        )


if __name__ == "__main__":
    main()
