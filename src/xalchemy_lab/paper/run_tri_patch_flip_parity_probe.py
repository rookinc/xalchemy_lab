from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


N_CYCLES = 6
MAX_FLIPS = 4


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
    _ = world.collisions[-1].face_event

    step(world, {"L1": opposite_hub, "L2": opposite_hub, "R1": opposite_hub})
    opposite_face = world.collisions[-1].face_event

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    _ = world.collisions[-1].face_event

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


def flip_carrier(world: World, carrier: str, n_flips: int) -> None:
    for _ in range(n_flips):
        current = world.turtles[carrier].carry_sign
        if current not in {"+", "-"}:
            raise ValueError(f"Cannot flip sign {current!r} on {carrier}")
        world.turtles[carrier].carry_sign = "-" if current == "+" else "+"


def stabilized_offset(
    start_node: str,
    sign: str,
    base_stress: tuple[int, int, int],
    base_mismatch: tuple[int, int, int],
    carrier: str,
    n_flips: int,
) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[str | None, str | None, str | None]]:
    baseline = make_world(start_node, sign, base_stress, base_mismatch)
    perturbed = make_world(start_node, sign, base_stress, base_mismatch)

    flip_carrier(perturbed, carrier, n_flips)

    ds = (0, 0, 0)
    dm = (0, 0, 0)
    final_signs = sign_vec(perturbed)

    for _ in range(N_CYCLES):
        full_cycle(baseline, start_node)
        full_cycle(perturbed, start_node)
        ds = sub_vec(stress_vec(perturbed), stress_vec(baseline))
        dm = sub_vec(mismatch_vec(perturbed), mismatch_vec(baseline))
        final_signs = sign_vec(perturbed)

    return ds, dm, final_signs


def run_family(start_node: str, sign: str, carrier: str) -> None:
    base_stress = (8, 8, 8)
    base_mismatch = (4, 4, 4)

    print(f"\n====================")
    print(f"FAMILY: {start_node}_{carrier}")
    print("====================")
    print(f"base_sign          = {sign}")
    print(f"base_stress        = {base_stress}")
    print(f"base_mismatch      = {base_mismatch}")

    for n_flips in range(MAX_FLIPS + 1):
        ds, dm, final_signs = stabilized_offset(
            start_node=start_node,
            sign=sign,
            base_stress=base_stress,
            base_mismatch=base_mismatch,
            carrier=carrier,
            n_flips=n_flips,
        )
        print(f"\nflips: {n_flips}")
        print(f"  parity            = {'odd' if n_flips % 2 else 'even'}")
        print(f"  delta_stress      = {ds}")
        print(f"  delta_mismatch    = {dm}")
        print(f"  final_signs       = {final_signs}")


def main() -> None:
    print("\n====================")
    print("FLIP PARITY PROBE")
    print("====================")
    print("Repeat sign flips on a single carrier before re-lock and measure stabilized offsets.")

    families = [
        ("u1R", "+", "L1"),
        ("u1R", "+", "L2"),
        ("u1R", "+", "R1"),
        ("d1R", "-", "L1"),
        ("d1R", "-", "L2"),
        ("d1R", "-", "R1"),
    ]

    for start_node, sign, carrier in families:
        run_family(start_node, sign, carrier)


if __name__ == "__main__":
    main()
