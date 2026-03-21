from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


BASE_CASE = ("u1R", "+", (8, 8, 8), (4, 4, 4))

PRIMITIVES = {
    "A_split_LR_hold_L2": ("L1", "R1"),
    "B_split_LL_hold_R1": ("L1", "L2"),
    "C_singleton_L1_only": ("L1",),
    "D_singleton_L2_only": ("L2",),
    "E_singleton_R1_only": ("R1",),
}

# Proposed factorization pieces
# Universal singleton penalty:
#   C = U_singleton + S_L1
#   D = U_singleton + S_L2
#   E = U_singleton + S_R1
#
# with
#   U_singleton := C
#   S_L1 := 0
#   S_L2 := D - C
#   S_R1 := E - C
#
# Dyadic classes are left as their own "U" candidates for now.
TARGETS = {
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


def sub3(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add3(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def scale3(k: int, v: tuple[int, int, int]) -> tuple[int, int, int]:
    return (k * v[0], k * v[1], k * v[2])


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


def primitive_vector(name: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    start_node, sign, stress, mismatch = BASE_CASE
    bundled_s, bundled_m = run_sequence(start_node, sign, stress, mismatch, [("L1", "L2", "R1")])
    route_s, route_m = run_sequence(start_node, sign, stress, mismatch, [PRIMITIVES[name]])
    return sub3(route_s, bundled_s), sub3(route_m, bundled_m)


def target_vector(word: list[str]) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    start_node, sign, stress, mismatch = BASE_CASE
    bundled_s, bundled_m = run_sequence(start_node, sign, stress, mismatch, [("L1", "L2", "R1")] * len(word))
    seq = [PRIMITIVES[name] for name in word]
    route_s, route_m = run_sequence(start_node, sign, stress, mismatch, seq)
    return sub3(route_s, bundled_s), sub3(route_m, bundled_m)


def main() -> None:
    print("\n====================")
    print("HOLONOMY FACTORIZATION PROBE")
    print("====================")
    print("Test whether observed route classes factor into a universal arity/receipt part plus pure stress-direction anisotropy.\n")

    prim = {name: primitive_vector(name) for name in PRIMITIVES}

    A = prim["A_split_LR_hold_L2"]
    B = prim["B_split_LL_hold_R1"]
    C = prim["C_singleton_L1_only"]
    D = prim["D_singleton_L2_only"]
    E = prim["E_singleton_R1_only"]

    U_singleton = C
    S_L1 = ((0, 0, 0), (0, 0, 0))
    S_L2 = (sub3(D[0], C[0]), sub3(D[1], C[1]))
    S_R1 = (sub3(E[0], C[0]), sub3(E[1], C[1]))

    print("PRIMITIVE HOLONOMY CLASSES")
    for name, (ds, dm) in prim.items():
        print(f"  {name}")
        print(f"    ds = {ds}")
        print(f"    dm = {dm}")

    print("\nPROPOSED FACTORIZATION PIECES")
    print("  U_singleton")
    print(f"    ds = {U_singleton[0]}")
    print(f"    dm = {U_singleton[1]}")
    print("  S_L1")
    print(f"    ds = {S_L1[0]}")
    print(f"    dm = {S_L1[1]}")
    print("  S_L2 = D - C")
    print(f"    ds = {S_L2[0]}")
    print(f"    dm = {S_L2[1]}")
    print("  S_R1 = E - C")
    print(f"    ds = {S_R1[0]}")
    print(f"    dm = {S_R1[1]}")

    print("\nSINGLETON FACTORIZATION CHECK")
    singleton_checks = {
        "C": (C, add3(U_singleton[0], S_L1[0]), add3(U_singleton[1], S_L1[1])),
        "D": (D, add3(U_singleton[0], S_L2[0]), add3(U_singleton[1], S_L2[1])),
        "E": (E, add3(U_singleton[0], S_R1[0]), add3(U_singleton[1], S_R1[1])),
    }
    for label, (actual, pred_s, pred_m) in singleton_checks.items():
        print(f"  {label}")
        print(f"    actual_ds = {actual[0]}")
        print(f"    actual_dm = {actual[1]}")
        print(f"    pred_ds   = {pred_s}")
        print(f"    pred_dm   = {pred_m}")
        print(f"    match     = {actual[0] == pred_s and actual[1] == pred_m}")

    print("\nMISMATCH CONTENT CHECK")
    print("  D - C should be pure stress:")
    print(f"    {flatten(*S_L2)}")
    print("  E - C should be pure stress:")
    print(f"    {flatten(*S_R1)}")

    print("\nTARGET WORD DECOMPOSITIONS")
    for label, word in TARGETS.items():
        actual_ds, actual_dm = target_vector(word)

        nA = word.count("A_split_LR_hold_L2")
        nB = word.count("B_split_LL_hold_R1")
        nC = word.count("C_singleton_L1_only")
        nD = word.count("D_singleton_L2_only")
        nE = word.count("E_singleton_R1_only")

        pred_ds = (0, 0, 0)
        pred_dm = (0, 0, 0)

        pred_ds = add3(pred_ds, scale3(nA, A[0]))
        pred_dm = add3(pred_dm, scale3(nA, A[1]))

        pred_ds = add3(pred_ds, scale3(nB, B[0]))
        pred_dm = add3(pred_dm, scale3(nB, B[1]))

        n_singletons = nC + nD + nE
        pred_ds = add3(pred_ds, scale3(n_singletons, U_singleton[0]))
        pred_dm = add3(pred_dm, scale3(n_singletons, U_singleton[1]))

        pred_ds = add3(pred_ds, scale3(nD, S_L2[0]))
        pred_dm = add3(pred_dm, scale3(nD, S_L2[1]))

        pred_ds = add3(pred_ds, scale3(nE, S_R1[0]))
        pred_dm = add3(pred_dm, scale3(nE, S_R1[1]))

        print(f"  {label}")
        print(f"    word       = {word}")
        print(f"    actual_ds  = {actual_ds}")
        print(f"    actual_dm  = {actual_dm}")
        print(f"    pred_ds    = {pred_ds}")
        print(f"    pred_dm    = {pred_dm}")
        print(f"    match      = {actual_ds == pred_ds and actual_dm == pred_dm}")
        print(
            f"    coeffs     = "
            f"A:{nA} B:{nB} U:{n_singletons} S_L2:{nD} S_R1:{nE}"
        )


if __name__ == "__main__":
    main()
