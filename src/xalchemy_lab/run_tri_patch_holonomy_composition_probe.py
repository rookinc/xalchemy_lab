from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


BASE_CASES = [
    ("u1R_clean_locked", "u1R", "+", (8, 8, 8), (4, 4, 4)),
    ("d1R_clean_locked", "d1R", "-", (8, 8, 8), (4, 4, 4)),
]

ROUTES = {
    "bundled_all": ("L1", "L2", "R1"),
    "split_LR_hold_L2": ("L1", "R1"),
    "split_LL_hold_R1": ("L1", "L2"),
    "singleton_L1_only": ("L1",),
    "singleton_R1_only": ("R1",),
}

COMPOSITIONS = [
    ("A_then_B", "split_LR_hold_L2", "split_LL_hold_R1"),
    ("B_then_A", "split_LL_hold_R1", "split_LR_hold_L2"),
    ("A_then_C", "split_LR_hold_L2", "singleton_L1_only"),
    ("C_then_A", "singleton_L1_only", "split_LR_hold_L2"),
    ("C_then_D", "singleton_L1_only", "singleton_R1_only"),
    ("D_then_C", "singleton_R1_only", "singleton_L1_only"),
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
    return tuple(world.turtles[n].carried_stress for n in ("L1", "L2", "R1"))


def mismatch_vec(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[n].mismatch_count for n in ("L1", "L2", "R1"))


def sign_vec(world: World) -> tuple[str | None, str | None, str | None]:
    return tuple(world.turtles[n].carry_sign for n in ("L1", "L2", "R1"))


def nodes_vec(world: World) -> tuple[str, str, str]:
    return tuple(world.turtles[n].node for n in ("L1", "L2", "R1"))  # type: ignore[return-value]


def sub_vec(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add_vec(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def run_route_once(
    world: World,
    start_node: str,
    advancers: tuple[str, ...],
) -> None:
    if start_node == "u1R":
        first_hub = "u1R"
        opposite_hub = "d1R"
    else:
        first_hub = "d1R"
        opposite_hub = "u1R"

    step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})
    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})

    middle_moves = {}
    for name in ("L1", "L2", "R1"):
        middle_moves[name] = opposite_hub if name in advancers else "mR"
    step(world, middle_moves)

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})


def run_route_sequence(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    sequence: list[str],
) -> dict[str, object]:
    world = make_world(start_node, sign, stress, mismatch)
    for route_name in sequence:
        run_route_once(world, start_node, ROUTES[route_name])

    return {
        "nodes": nodes_vec(world),
        "signs": sign_vec(world),
        "stress": stress_vec(world),
        "mismatch": mismatch_vec(world),
    }


def single_route_correction(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    route_name: str,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    bundled = run_route_sequence(start_node, sign, stress, mismatch, ["bundled_all"])
    route = run_route_sequence(start_node, sign, stress, mismatch, [route_name])
    return (
        sub_vec(route["stress"], bundled["stress"]),        # type: ignore[arg-type]
        sub_vec(route["mismatch"], bundled["mismatch"]),    # type: ignore[arg-type]
    )


def main() -> None:
    print("\n====================")
    print("HOLONOMY COMPOSITION PROBE")
    print("====================")
    print("Compare sequential route deviations against the sum of their single-route holonomy vectors.")

    for label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"\nCASE: {label}")
        print(f"  start_node         = {start_node}")
        print(f"  initial_signs      = {(sign, sign, sign)}")
        print(f"  initial_stress     = {stress}")
        print(f"  initial_mismatch   = {mismatch}")

        bundled_twice = run_route_sequence(start_node, sign, stress, mismatch, ["bundled_all", "bundled_all"])

        for comp_label, r1, r2 in COMPOSITIONS:
            single_1 = single_route_correction(start_node, sign, stress, mismatch, r1)
            single_2 = single_route_correction(start_node, sign, stress, mismatch, r2)

            seq = run_route_sequence(start_node, sign, stress, mismatch, [r1, r2])

            actual_ds = sub_vec(seq["stress"], bundled_twice["stress"])        # type: ignore[arg-type]
            actual_dm = sub_vec(seq["mismatch"], bundled_twice["mismatch"])    # type: ignore[arg-type]

            expected_ds = add_vec(single_1[0], single_2[0])
            expected_dm = add_vec(single_1[1], single_2[1])

            print(f"\n  composition        = {comp_label}")
            print(f"    routes           = ({r1}, {r2})")
            print(f"    final_nodes      = {seq['nodes']}")
            print(f"    final_signs      = {seq['signs']}")
            print(f"    actual_ds        = {actual_ds}")
            print(f"    actual_dm        = {actual_dm}")
            print(f"    expected_ds      = {expected_ds}")
            print(f"    expected_dm      = {expected_dm}")
            print(f"    stress_additive  = {actual_ds == expected_ds}")
            print(f"    mismatch_additive= {actual_dm == expected_dm}")


if __name__ == "__main__":
    main()
