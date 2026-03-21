from __future__ import annotations

from itertools import product

from xalchemy_lab.tri_patch_core import World, Turtle, step


BASE_CASE = ("u1R", "+", (8, 8, 8), (4, 4, 4))

PRIMITIVES = {
    "A": ("L1", "R1"),        # split_LR_hold_L2
    "B": ("L1", "L2"),        # split_LL_hold_R1
    "C": ("L1",),             # singleton_L1_only
    "D": ("L2",),             # singleton_L2_only
    "E": ("R1",),             # singleton_R1_only
}

TARGET_WORDS = {
    "A": ["A"],
    "B": ["B"],
    "C": ["C"],
    "D": ["D"],
    "E": ["E"],
    "A+B": ["A", "B"],
    "A+C": ["A", "C"],
    "C+E": ["C", "E"],
    "A+B+A": ["A", "B", "A"],
    "C+A+E": ["C", "A", "E"],
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


def sub_vec(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add6(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))


def scale6(k: int, v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(k * x for x in v)


def flatten(ds: tuple[int, int, int], dm: tuple[int, int, int]) -> tuple[int, int, int, int, int, int]:
    return ds + dm


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


def run_sequence(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    sequence: list[tuple[str, ...]],
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    world = make_world(start_node, sign, stress, mismatch)
    for advancers in sequence:
        run_route_once(world, start_node, advancers)
    return stress_vec(world), mismatch_vec(world)


def primitive_vector(name: str) -> tuple[int, int, int, int, int, int]:
    start_node, sign, stress, mismatch = BASE_CASE
    bundled_s, bundled_m = run_sequence(start_node, sign, stress, mismatch, [("L1", "L2", "R1")])
    route_s, route_m = run_sequence(start_node, sign, stress, mismatch, [PRIMITIVES[name]])
    ds = sub_vec(route_s, bundled_s)
    dm = sub_vec(route_m, bundled_m)
    return flatten(ds, dm)


def target_vector(word: list[str]) -> tuple[int, int, int, int, int, int]:
    start_node, sign, stress, mismatch = BASE_CASE
    bundled_s, bundled_m = run_sequence(start_node, sign, stress, mismatch, [("L1", "L2", "R1")] * len(word))
    seq = [PRIMITIVES[name] for name in word]
    route_s, route_m = run_sequence(start_node, sign, stress, mismatch, seq)
    ds = sub_vec(route_s, bundled_s)
    dm = sub_vec(route_m, bundled_m)
    return flatten(ds, dm)


def find_small_integer_representation(
    target: tuple[int, ...],
    basis_names: tuple[str, ...],
    basis_vectors: dict[str, tuple[int, ...]],
    coeff_bound: int = 4,
) -> tuple[int, ...] | None:
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
    print("HOLONOMY REBASIS PROBE")
    print("====================")
    print("Test the rebased generating set {A, B, C, D-C, E-C}.")

    prim_vecs = {name: primitive_vector(name) for name in PRIMITIVES}

    rebased = {
        "A": prim_vecs["A"],
        "B": prim_vecs["B"],
        "C": prim_vecs["C"],
        "D_minus_C": tuple(d - c for d, c in zip(prim_vecs["D"], prim_vecs["C"])),
        "E_minus_C": tuple(e - c for e, c in zip(prim_vecs["E"], prim_vecs["C"])),
    }

    print("\nPRIMITIVE VECTORS")
    for name in ("A", "B", "C", "D", "E"):
        print(f"  {name} = {prim_vecs[name]}")

    print("\nREBASED GENERATORS")
    for name, vec in rebased.items():
        print(f"  {name:10s} = {vec}")

    print("\nRECOVER PRIMITIVES FROM REBASED BASIS")
    recovery_targets = {
        "A": prim_vecs["A"],
        "B": prim_vecs["B"],
        "C": prim_vecs["C"],
        "D": prim_vecs["D"],
        "E": prim_vecs["E"],
    }
    basis_names = ("A", "B", "C", "D_minus_C", "E_minus_C")
    for label, vec in recovery_targets.items():
        coeffs = find_small_integer_representation(vec, basis_names, rebased, coeff_bound=2)
        print(f"  {label}: coeffs={coeffs} recovered={coeffs is not None}")

    print("\nGENERATE OBSERVED TARGET WORDS")
    target_vecs = {label: target_vector(word) for label, word in TARGET_WORDS.items()}
    for label, vec in target_vecs.items():
        coeffs = find_small_integer_representation(vec, basis_names, rebased, coeff_bound=4)
        print(f"  {label:6s} vec={vec} coeffs={coeffs} generated={coeffs is not None}")

    print("\nINTERPRETATION CHECKS")
    print("  D - C should be pure stress-direction:")
    print(f"    {rebased['D_minus_C']}")
    print("  E - C should be pure stress-direction:")
    print(f"    {rebased['E_minus_C']}")


if __name__ == "__main__":
    main()
