from __future__ import annotations

from itertools import product

from xalchemy_lab.tri_patch_core import World, Turtle, step


BASE_CASES = [
    ("u1R_clean_locked", "u1R", "+", (8, 8, 8), (4, 4, 4)),
    ("d1R_clean_locked", "d1R", "-", (8, 8, 8), (4, 4, 4)),
]

CARRIERS = ("L1", "L2", "R1")

# Factorized basis from current note:
# A = split_LR_hold_L2
# B = split_LL_hold_R1
# U = singleton_L1_only
# S_L2 = D - C
# S_R1 = E - C


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


def sign_vec(world: World) -> tuple[str | None, str | None, str | None]:
    return tuple(world.turtles[n].carry_sign for n in CARRIERS)


def nodes_vec(world: World) -> tuple[str, str, str]:
    return tuple(world.turtles[n].node for n in CARRIERS)  # type: ignore[return-value]


def sub3(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add6(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))


def scale6(k: int, v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(k * x for x in v)


def flatten(ds: tuple[int, int, int], dm: tuple[int, int, int]) -> tuple[int, int, int, int, int, int]:
    return ds + dm


def do_step(world: World, moves: dict[str, str]) -> tuple[str | None, str | None, str | None]:
    before = len(world.collisions)
    step(world, moves)
    if len(world.collisions) == before:
        return None, None, None
    c = world.collisions[-1]
    return c.node, c.kind, c.face_event


def run_middle_route(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    advancers: tuple[str, ...],
) -> dict[str, object]:
    world = make_world(start_node, sign, stress, mismatch)

    if start_node == "u1R":
        first_hub = "u1R"
        opposite_hub = "d1R"
    else:
        first_hub = "d1R"
        opposite_hub = "u1R"

    events: list[tuple[str | None, str | None, str | None]] = []

    events.append(do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub}))
    events.append(do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"}))

    middle_moves = {}
    for name in CARRIERS:
        middle_moves[name] = opposite_hub if name in advancers else "mR"
    events.append(do_step(world, middle_moves))

    events.append(do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"}))
    events.append(do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub}))

    return {
        "events": events,
        "nodes": nodes_vec(world),
        "signs": sign_vec(world),
        "stress": stress_vec(world),
        "mismatch": mismatch_vec(world),
    }


def all_advancer_subsets() -> list[tuple[str, ...]]:
    out = []
    for bits in product([0, 1], repeat=3):
        subset = tuple(name for bit, name in zip(bits, CARRIERS) if bit)
        out.append(subset)
    return out


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


def subset_label(advancers: tuple[str, ...]) -> str:
    if not advancers:
        return "hold_all"
    return "advance_" + "_".join(advancers)


def main() -> None:
    print("\n====================")
    print("MIDDLE ROUTE ENUMERATOR")
    print("====================")
    print("Enumerate all middle-route advance subsets, compute holonomy, and test factorization in the current basis.")

    subsets = all_advancer_subsets()

    # Build basis from the positive clean case.
    _, start_node0, sign0, stress0, mismatch0 = BASE_CASES[0]
    bundled0 = run_middle_route(start_node0, sign0, stress0, mismatch0, ("L1", "L2", "R1"))

    def holonomy_for_subset(case, advancers):
        _, start_node, sign, stress, mismatch = case
        res = run_middle_route(start_node, sign, stress, mismatch, advancers)
        ds = sub3(res["stress"], bundled0["stress"]) if case == BASE_CASES[0] else None
        dm = sub3(res["mismatch"], bundled0["mismatch"]) if case == BASE_CASES[0] else None
        return res, ds, dm

    # Primitive factor basis from current theory
    A_res = run_middle_route(start_node0, sign0, stress0, mismatch0, ("L1", "R1"))
    B_res = run_middle_route(start_node0, sign0, stress0, mismatch0, ("L1", "L2"))
    C_res = run_middle_route(start_node0, sign0, stress0, mismatch0, ("L1",))
    D_res = run_middle_route(start_node0, sign0, stress0, mismatch0, ("L2",))
    E_res = run_middle_route(start_node0, sign0, stress0, mismatch0, ("R1",))

    A = flatten(sub3(A_res["stress"], bundled0["stress"]), sub3(A_res["mismatch"], bundled0["mismatch"]))  # type: ignore[arg-type]
    B = flatten(sub3(B_res["stress"], bundled0["stress"]), sub3(B_res["mismatch"], bundled0["mismatch"]))  # type: ignore[arg-type]
    C = flatten(sub3(C_res["stress"], bundled0["stress"]), sub3(C_res["mismatch"], bundled0["mismatch"]))  # type: ignore[arg-type]
    D = flatten(sub3(D_res["stress"], bundled0["stress"]), sub3(D_res["mismatch"], bundled0["mismatch"]))  # type: ignore[arg-type]
    E = flatten(sub3(E_res["stress"], bundled0["stress"]), sub3(E_res["mismatch"], bundled0["mismatch"]))  # type: ignore[arg-type]

    basis_vectors = {
        "A": A,
        "B": B,
        "U": C,
        "S_L2": tuple(d - c for d, c in zip(D, C)),
        "S_R1": tuple(e - c for e, c in zip(E, C)),
    }

    print("\nCURRENT FACTORIZED BASIS")
    for name, vec in basis_vectors.items():
        print(f"  {name:4s} = {vec}")

    class_buckets: dict[tuple[int, int, int, int, int, int], list[str]] = {}

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"\n====================")
        print(f"CASE: {case_label}")
        print("====================")
        bundled = run_middle_route(start_node, sign, stress, mismatch, ("L1", "L2", "R1"))

        for advancers in subsets:
            label = subset_label(advancers)
            res = run_middle_route(start_node, sign, stress, mismatch, advancers)

            ds = sub3(res["stress"], bundled["stress"])        # type: ignore[arg-type]
            dm = sub3(res["mismatch"], bundled["mismatch"])    # type: ignore[arg-type]
            flat = flatten(ds, dm)

            coeffs = None
            if case_label == "u1R_clean_locked":
                coeffs = find_small_integer_representation(flat, basis_vectors, coeff_bound=3)

            class_buckets.setdefault(flat, []).append(f"{case_label}:{label}")

            print(f"\n  route              = {label}")
            print(f"    advancers        = {advancers}")
            print(f"    middle_event     = {res['events'][2]}")
            print(f"    final_nodes      = {res['nodes']}")
            print(f"    final_signs      = {res['signs']}")
            print(f"    delta_stress     = {ds}")
            print(f"    delta_mismatch   = {dm}")
            if coeffs is not None:
                print(f"    factor_coeffs    = A:{coeffs[0]} B:{coeffs[1]} U:{coeffs[2]} S_L2:{coeffs[3]} S_R1:{coeffs[4]}")
                print(f"    factorized       = {coeffs is not None}")

    print("\n====================")
    print("DISCOVERED HOLONOMY CLASSES")
    print("====================")
    for idx, (flat, members) in enumerate(sorted(class_buckets.items()), start=1):
        print(f"\nclass {idx}")
        print(f"  vector             = {flat}")
        print("  members:")
        for member in members:
            print(f"    - {member}")


if __name__ == "__main__":
    main()
