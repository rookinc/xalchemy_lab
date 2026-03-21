from __future__ import annotations

from itertools import product

from xalchemy_lab.tri_patch_core import World, Turtle, step


BASE_CASE = ("u1R", "+", (8, 8, 8), (4, 4, 4))
CARRIERS = ("L1", "L2", "R1")

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

COORD_NAMES = (
    "ds_L1",
    "ds_L2",
    "ds_R1",
    "dm_L1",
    "dm_L2",
    "dm_R1",
)


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
    return tuple(world.turtles[n].carried_stress for n in CARRIERS)


def mismatch_vec(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[n].mismatch_count for n in CARRIERS)


def sub3(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def flatten(ds: tuple[int, int, int], dm: tuple[int, int, int]) -> tuple[int, int, int, int, int, int]:
    return ds + dm


def mod2(v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x % 2 for x in v)


def dot_mod2(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum((x & 1) * (y & 1) for x, y in zip(a, b)) % 2


def run_route_once(world: World, start_node: str, advancers: tuple[str, ...]) -> None:
    if start_node == "u1R":
        first_hub = "u1R"
        opposite_hub = "d1R"
    else:
        first_hub = "d1R"
        opposite_hub = "u1R"

    step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})
    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})

    middle_moves = {}
    for name in CARRIERS:
        middle_moves[name] = opposite_hub if name in advancers else "mR"
    step(world, middle_moves)

    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})


def route_vector(route_name: str) -> tuple[int, int, int, int, int, int]:
    start_node, sign, stress, mismatch = BASE_CASE
    bundled = make_world(start_node, sign, stress, mismatch)
    route = make_world(start_node, sign, stress, mismatch)

    run_route_once(bundled, start_node, ROUTES["advance_L1_L2_R1"])
    run_route_once(route, start_node, ROUTES[route_name])

    ds = sub3(stress_vec(route), stress_vec(bundled))
    dm = sub3(mismatch_vec(route), mismatch_vec(bundled))
    return flatten(ds, dm)


def format_functional(w: tuple[int, ...]) -> str:
    terms = [name for bit, name in zip(w, COORD_NAMES) if bit]
    if not terms:
        return "0 = 0 (trivial)"
    return " + ".join(terms) + " = 0 mod 2"


def main() -> None:
    print("\n====================")
    print("HOLONOMY PARITY FUNCTIONAL PROBE")
    print("====================")
    print("Solve for binary linear functionals whose kernel contains the reachable holonomy image mod 2.\n")

    vectors = {name: route_vector(name) for name in ROUTES}
    mod2_vectors = {name: mod2(vec) for name, vec in vectors.items()}

    print("REACHABLE MOD 2 CLASS VECTORS")
    distinct_reachable = sorted(set(mod2_vectors.values()))
    for vec in distinct_reachable:
        members = [name for name, v in mod2_vectors.items() if v == vec]
        print(f"  {vec}")
        for m in members:
            print(f"    - {m}")

    nonzero_functionals = [
        tuple(bits) for bits in product([0, 1], repeat=6) if any(bits)
    ]

    annihilators = []
    for w in nonzero_functionals:
        if all(dot_mod2(w, v) == 0 for v in distinct_reachable):
            annihilators.append(w)

    print("\nANNIHILATING MOD 2 FUNCTIONALS")
    for w in annihilators:
        print(f"  w = {w}   ->   {format_functional(w)}")

    print(f"\nnumber_of_nonzero_annihilators = {len(annihilators)}")

    if len(annihilators) == 1:
        w = annihilators[0]
        print("\nUNIQUE PARITY LAW")
        print(f"  {format_functional(w)}")

        print("\nCHECK ON REACHABLE VECTORS")
        for vec in distinct_reachable:
            print(f"  vec={vec}  value={dot_mod2(w, vec)}")

        print("\nCHECK ON SAMPLE UNREACHABLE VECTORS")
        sample_unreachable = [
            (0, 0, 0, 0, 0, 1),
            (0, 0, 0, 0, 1, 0),
            (0, 0, 0, 1, 0, 0),
            (0, 0, 0, 1, 1, 1),
        ]
        for vec in sample_unreachable:
            print(f"  vec={vec}  value={dot_mod2(w, vec)}")
    else:
        print("\nNo unique nonzero annihilator found; either the reachable image has smaller rank than expected or multiple equivalent parity laws exist.")


if __name__ == "__main__":
    main()
