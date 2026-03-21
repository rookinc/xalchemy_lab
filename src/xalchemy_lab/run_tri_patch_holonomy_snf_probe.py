from __future__ import annotations

from math import gcd
from itertools import combinations

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


def flatten(ds: tuple[int, int, int], dm: tuple[int, int, int]) -> tuple[int, int, int, int, int, int]:
    return ds + dm


def det_bareiss(mat: list[list[int]]) -> int:
    n = len(mat)
    if n == 0:
        return 1
    a = [row[:] for row in mat]
    sign = 1
    prev = 1
    for k in range(n - 1):
        pivot = a[k][k]
        if pivot == 0:
            swap_row = None
            for i in range(k + 1, n):
                if a[i][k] != 0:
                    swap_row = i
                    break
            if swap_row is None:
                return 0
            a[k], a[swap_row] = a[swap_row], a[k]
            sign *= -1
            pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * pivot - a[i][k] * a[k][j]) // prev
        prev = pivot
        for i in range(k + 1, n):
            a[i][k] = 0
        for j in range(k + 1, n):
            a[k][j] = 0
    return sign * a[n - 1][n - 1]


def gcd_list(values: list[int]) -> int:
    g = 0
    for v in values:
        g = gcd(g, abs(v))
    return g


def minors_gcd(matrix: list[list[int]], k: int) -> int:
    rows = len(matrix)
    cols = len(matrix[0]) if matrix else 0
    vals: list[int] = []
    for row_idx in combinations(range(rows), k):
        for col_idx in combinations(range(cols), k):
            sub = [[matrix[r][c] for c in col_idx] for r in row_idx]
            vals.append(det_bareiss(sub))
    return gcd_list(vals)


def smith_invariants_from_minors(matrix: list[list[int]]) -> list[int]:
    rows = len(matrix)
    cols = len(matrix[0]) if matrix else 0
    max_k = min(rows, cols)
    d_prev = 1
    invs: list[int] = []
    for k in range(1, max_k + 1):
        d_k = minors_gcd(matrix, k)
        if d_k == 0:
            break
        invs.append(d_k // d_prev)
        d_prev = d_k
    return invs


def rank_over_q(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    a = [row[:] for row in matrix]
    m = len(a)
    n = len(a[0])
    r = 0
    c = 0
    while r < m and c < n:
        pivot = None
        for i in range(r, m):
            if a[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            c += 1
            continue
        a[r], a[pivot] = a[pivot], a[r]
        piv = a[r][c]
        for i in range(r + 1, m):
            if a[i][c] == 0:
                continue
            ai = a[i][c]
            # integer elimination via lcm-style step
            g = gcd(abs(piv), abs(ai))
            mul_r = ai // g
            mul_i = piv // g
            for j in range(c, n):
                a[i][j] = a[i][j] * mul_i - a[r][j] * mul_r
        r += 1
        c += 1
    # count nonzero rows
    rk = 0
    for row in a:
        if any(v != 0 for v in row):
            rk += 1
    return rk


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


def main() -> None:
    print("\n====================")
    print("HOLONOMY SNF PROBE")
    print("====================")
    print("Compute integer lattice invariants for the enumerated holonomy class vectors.\n")

    vectors = {name: route_vector(name) for name in ROUTES}

    print("ENUMERATED CLASS VECTORS")
    ordered_names = list(ROUTES.keys())
    for name in ordered_names:
        print(f"  {name:20s} = {vectors[name]}")

    nonzero_names = [name for name in ordered_names if any(vectors[name])]
    matrix_rows = [list(vectors[name]) for name in nonzero_names]

    print("\nMATRIX (rows = nonzero class vectors)")
    for name, row in zip(nonzero_names, matrix_rows):
        print(f"  {name:20s} {tuple(row)}")

    rk = rank_over_q(matrix_rows)
    invs = smith_invariants_from_minors(matrix_rows)

    print("\nLATTICE INVARIANTS")
    print(f"  rank_over_Q        = {rk}")
    print(f"  smith_invariants   = {tuple(invs)}")

    print("\nMINORS GCD CHAIN")
    d_prev = 1
    for k in range(1, min(len(matrix_rows), 6) + 1):
        d_k = minors_gcd(matrix_rows, k)
        if d_k == 0:
            print(f"  Delta_{k}           = 0")
            break
        print(f"  Delta_{k}           = {d_k}   (invariant factor contribution = {d_k // d_prev})")
        d_prev = d_k

    print("\nQUICK READ")
    if invs:
        torsion_free = all(x == 1 for x in invs)
        print(f"  torsion_free       = {torsion_free}")
        print(f"  lattice_rank       = {len(invs)}")
    else:
        print("  No nonzero invariants found.")


if __name__ == "__main__":
    main()
