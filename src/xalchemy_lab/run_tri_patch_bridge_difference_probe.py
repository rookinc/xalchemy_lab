from __future__ import annotations

from itertools import combinations

from xalchemy_lab.tri_patch_core import World, Turtle, step


BASE_CASES = [
    ("u1R_clean_locked", "u1R", "+", (8, 8, 8), (4, 4, 4)),
    ("d1R_clean_locked", "d1R", "-", (8, 8, 8), (4, 4, 4)),
]

ROUTES = {
    "hold_all": (),
    "advance_L1": ("L1",),
    "advance_L2": ("L2",),
    "advance_R1": ("R1",),
    "advance_L1_L2": ("L1", "L2"),
    "advance_L1_R1": ("L1", "R1"),
    "advance_L2_R1": ("L2", "R1"),
    "advance_L1_L2_R1": ("L1", "L2", "R1"),
}


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


def sub3(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def flatten(ds: tuple[int, int, int], dm: tuple[int, int, int]) -> tuple[int, int, int, int, int, int]:
    return ds + dm


def mod2(v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x % 2 for x in v)


def total_mismatch_parity(dm: tuple[int, int, int]) -> int:
    return (dm[0] + dm[1] + dm[2]) % 2


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


def run_route(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    route_name: str,
) -> dict[str, object]:
    world = make_world(start_node, sign, stress, mismatch)
    run_route_once(world, start_node, ROUTES[route_name])
    return {
        "nodes": nodes_vec(world),
        "signs": sign_vec(world),
        "stress": stress_vec(world),
        "mismatch": mismatch_vec(world),
    }


def holonomy_vector(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    route_name: str,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    bundled = run_route(start_node, sign, stress, mismatch, "advance_L1_L2_R1")
    route = run_route(start_node, sign, stress, mismatch, route_name)
    ds = sub3(route["stress"], bundled["stress"])        # type: ignore[arg-type]
    dm = sub3(route["mismatch"], bundled["mismatch"])    # type: ignore[arg-type]
    return ds, dm


def main() -> None:
    print("\n====================")
    print("BRIDGE DIFFERENCE PROBE")
    print("====================")
    print("Compare differences of local holonomy classes with the binary parity shadow. This tests whether the bridge target should be route-difference data rather than raw local classes.")

    route_names = list(ROUTES.keys())

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"\n====================")
        print(f"CASE: {case_label}")
        print("====================")
        print(f"start_node          = {start_node}")
        print(f"initial_signs       = {(sign, sign, sign)}")
        print(f"initial_stress      = {stress}")
        print(f"initial_mismatch    = {mismatch}")

        cached = {
            name: holonomy_vector(start_node, sign, stress, mismatch, name)
            for name in route_names
        }

        for r1, r2 in combinations(route_names, 2):
            ds1, dm1 = cached[r1]
            ds2, dm2 = cached[r2]

            dds = sub3(ds1, ds2)
            ddm = sub3(dm1, dm2)
            flat = flatten(dds, ddm)
            flat_mod2 = mod2(flat)

            print(f"\nroute_pair           = ({r1}, {r2})")
            print(f"  delta_delta_s      = {dds}")
            print(f"  delta_delta_m      = {ddm}")
            print(f"  mod2_signature     = {flat_mod2}")
            print(f"  mismatch_parity    = {total_mismatch_parity(ddm)}")
            print(f"  even_mismatch_ok   = {total_mismatch_parity(ddm) == 0}")

        print("\nsummary note")
        print("  If a local–global Z2 bridge exists, it is more plausible that it lives on differences between route histories (loop-like comparison data) than on raw local class vectors.")


if __name__ == "__main__":
    main()
