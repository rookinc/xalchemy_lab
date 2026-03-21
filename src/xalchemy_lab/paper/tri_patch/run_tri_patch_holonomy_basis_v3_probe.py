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


def add6(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))


def scale6(k: int, v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(k * x for x in v)


def flatten(ds: tuple[int, int, int], dm: tuple[int, int, int]) -> tuple[int, int, int, int, int, int]:
    return ds + dm


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


def find_small_integer_representation(
    target: tuple[int, ...],
    basis_vectors: dict[str, tuple[int, ...]],
    coeff_bound: int = 3,
) -> tuple[int, ...] | None:
    basis_names = tuple(basis_vectors.keys())
    ranges = [range(-coeff_bound, coeff_bound + 1) for _ in basis_names]
    zero = (0, 0, 0, 0, 0, 0)

    for coeffs in product(*ranges):
        current = zero
        for k, name in zip(coeffs, basis_names):
            current = add6(current, scale6(k, basis_vectors[name]))
        if current == target:
            return tuple(coeffs)
    return None


def main() -> None:
    print("\n====================")
    print("HOLONOMY BASIS V3 PROBE")
    print("====================")
    print("Test candidate basis {U, A, B, S_L1, S_L2, S_R1, M_L2R1} against all enumerated classes.\n")

    vectors = {name: route_vector(name) for name in ROUTES}

    print("ENUMERATED CLASS VECTORS")
    for name, vec in vectors.items():
        print(f"  {name:20s} = {vec}")

    U = vectors["hold_all"]
    A = vectors["advance_L1_R1"]
    B = vectors["advance_L1_L2"]

    S_L1 = tuple(a - u for a, u in zip(vectors["advance_L1"], U))
    S_L2 = tuple(a - u for a, u in zip(vectors["advance_L2"], U))
    S_R1 = tuple(a - u for a, u in zip(vectors["advance_R1"], U))
    M_L2R1 = tuple(a - u for a, u in zip(vectors["advance_L2_R1"], U))

    basis = {
        "U": U,
        "A": A,
        "B": B,
        "S_L1": S_L1,
        "S_L2": S_L2,
        "S_R1": S_R1,
        "M_L2R1": M_L2R1,
    }

    print("\nPROPOSED BASIS V3")
    for name, vec in basis.items():
        print(f"  {name:7s} = {vec}")

    print("\nINTERPRETATION CHECKS")
    print(f"  S_L1   = advance_L1   - hold_all = {S_L1}")
    print(f"  S_L2   = advance_L2   - hold_all = {S_L2}")
    print(f"  S_R1   = advance_R1   - hold_all = {S_R1}")
    print(f"  M_L2R1 = advance_L2_R1 - hold_all = {M_L2R1}")

    print("\nRECOVERY OF ENUMERATED CLASSES")
    all_ok = True
    for name, vec in vectors.items():
        coeffs = find_small_integer_representation(vec, basis, coeff_bound=3)
        ok = coeffs is not None
        all_ok = all_ok and ok
        print(f"  {name:20s} coeffs={coeffs} generated={ok}")

    print(f"\nall_enumerated_classes_generated = {all_ok}")


if __name__ == "__main__":
    main()
