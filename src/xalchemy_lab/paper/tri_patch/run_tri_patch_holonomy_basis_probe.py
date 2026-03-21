from __future__ import annotations

from itertools import combinations

from xalchemy_lab.tri_patch_core import World, Turtle, step


BASE_CASE = ("u1R", "+", (8, 8, 8), (4, 4, 4))

PRIMITIVES = {
    "A_split_LR_hold_L2": ("L1", "R1"),
    "B_split_LL_hold_R1": ("L1", "L2"),
    "C_singleton_L1_only": ("L1",),
    "D_singleton_L2_only": ("L2",),
    "E_singleton_R1_only": ("R1",),
}

# previously observed target words to test generation
TARGET_WORDS = {
    "A": ["A_split_LR_hold_L2"],
    "B": ["B_split_LL_hold_R1"],
    "C": ["C_singleton_L1_only"],
    "D": ["D_singleton_L2_only"],
    "E": ["E_singleton_R1_only"],
    "A+B": ["A_split_LR_hold_L2", "B_split_LL_hold_R1"],
    "A+C": ["A_split_LR_hold_L2", "C_singleton_L1_only"],
    "C+E": ["C_singleton_L1_only", "E_singleton_R1_only"],
    "A+B+A": ["A_split_LR_hold_L2", "B_split_LL_hold_R1", "A_split_LR_hold_L2"],
    "C+A+E": ["C_singleton_L1_only", "A_split_LR_hold_L2", "E_singleton_R1_only"],
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
    coeff_bound: int = 3,
) -> tuple[int, ...] | None:
    if not basis_names:
        return () if target == (0, 0, 0, 0, 0, 0) else None

    # brute force over small coefficients
    ranges = [range(-coeff_bound, coeff_bound + 1) for _ in basis_names]

    def rec(idx: int, current: tuple[int, ...], coeffs: list[int]) -> tuple[int, ...] | None:
        if idx == len(basis_names):
            return tuple(coeffs) if current == target else None
        name = basis_names[idx]
        vec = basis_vectors[name]
        for k in ranges[idx]:
            nxt = add6(current, scale6(k, vec))
            coeffs.append(k)
            out = rec(idx + 1, nxt, coeffs)
            if out is not None:
                return out
            coeffs.pop()
        return None

    return rec(0, (0, 0, 0, 0, 0, 0), [])


def main() -> None:
    print("\n====================")
    print("HOLONOMY BASIS PROBE")
    print("====================")
    print("Extract primitive holonomy vectors and test whether observed route words are generated by a smaller basis.")

    prim_vecs = {name: primitive_vector(name) for name in PRIMITIVES}

    print("\nPRIMITIVE CLASS VECTORS")
    for name, vec in prim_vecs.items():
        print(f"  {name}: {vec}")

    print("\nPAIRWISE DIFFERENCES")
    for a, b in combinations(PRIMITIVES.keys(), 2):
        diff = tuple(x - y for x, y in zip(prim_vecs[a], prim_vecs[b]))
        print(f"  {a} - {b} = {diff}")

    candidate_bases = [
        ("A_split_LR_hold_L2", "B_split_LL_hold_R1", "C_singleton_L1_only", "D_singleton_L2_only", "E_singleton_R1_only"),
        ("A_split_LR_hold_L2", "C_singleton_L1_only", "D_singleton_L2_only", "E_singleton_R1_only"),
        ("B_split_LL_hold_R1", "C_singleton_L1_only", "D_singleton_L2_only", "E_singleton_R1_only"),
        ("A_split_LR_hold_L2", "B_split_LL_hold_R1", "C_singleton_L1_only", "E_singleton_R1_only"),
    ]

    print("\nGENERATION TESTS")
    target_vecs = {label: target_vector(word) for label, word in TARGET_WORDS.items()}

    for basis in candidate_bases:
        print(f"\nbasis: {basis}")
        all_ok = True
        for label, vec in target_vecs.items():
            coeffs = find_small_integer_representation(vec, basis, prim_vecs, coeff_bound=3)
            ok = coeffs is not None
            all_ok = all_ok and ok
            print(f"  target={label:6s} vec={vec} generated={ok} coeffs={coeffs}")
        print(f"  basis_spans_targets = {all_ok}")


if __name__ == "__main__":
    main()
