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


def flatten(ds: tuple[int, int, int], dm: tuple[int, int, int]) -> tuple[int, int, int, int, int, int]:
    return ds + dm


def mod2(v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x % 2 for x in v)


def add_mod2(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x + y) % 2 for x, y in zip(a, b))


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


def gf2_rank(rows: list[tuple[int, ...]]) -> int:
    if not rows:
        return 0
    a = [list(r) for r in rows]
    m = len(a)
    n = len(a[0])
    r = 0
    c = 0
    while r < m and c < n:
        pivot = None
        for i in range(r, m):
            if a[i][c] % 2 != 0:
                pivot = i
                break
        if pivot is None:
            c += 1
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(m):
            if i != r and a[i][c] % 2 != 0:
                for j in range(c, n):
                    a[i][j] = (a[i][j] + a[r][j]) % 2
        r += 1
        c += 1
    return r


def in_span_mod2(target: tuple[int, ...], gens: list[tuple[int, ...]]) -> bool:
    if not gens:
        return all(x == 0 for x in target)
    zero = tuple(0 for _ in target)
    seen = {zero}
    frontier = [zero]
    for g in gens:
        new_seen = set(seen)
        for v in seen:
            new_seen.add(add_mod2(v, g))
        seen = new_seen
    return target in seen


def main() -> None:
    print("\n====================")
    print("HOLONOMY MOD 2 PROBE")
    print("====================")
    print("Reduce the enumerated holonomy classes mod 2 and identify the binary shadow / missing coset.\n")

    vectors = {name: route_vector(name) for name in ROUTES}

    print("ENUMERATED CLASS VECTORS")
    for name, vec in vectors.items():
        print(f"  {name:20s} = {vec}")

    mod2_vectors = {name: mod2(vec) for name, vec in vectors.items()}

    print("\nCLASS VECTORS MOD 2")
    for name, vec in mod2_vectors.items():
        print(f"  {name:20s} = {vec}")

    nonzero_mod2 = [v for v in mod2_vectors.values() if any(v)]
    rank2 = gf2_rank(nonzero_mod2)

    print("\nGF(2) SUMMARY")
    print(f"  mod2_rank          = {rank2}")
    print(f"  nonzero_mod2_count = {len(nonzero_mod2)}")

    distinct = {}
    for name, vec in mod2_vectors.items():
        distinct.setdefault(vec, []).append(name)

    print("\nDISTINCT MOD 2 CLASSES")
    for idx, (vec, members) in enumerate(sorted(distinct.items()), start=1):
        print(f"  class {idx}: {vec}")
        for m in members:
            print(f"    - {m}")

    gens = []
    gen_names = []
    for name in ROUTES:
        v = mod2_vectors[name]
        if not any(v):
            continue
        if not in_span_mod2(v, gens):
            gens.append(v)
            gen_names.append(name)

    print("\nGREEDY MOD 2 GENERATORS")
    for name, vec in zip(gen_names, gens):
        print(f"  {name:20s} = {vec}")

    print("\nSPAN CHECK OVER ALL 64 PARITY VECTORS")
    all_vecs = [tuple(bits) for bits in product([0, 1], repeat=6)]
    reachable = [v for v in all_vecs if in_span_mod2(v, gens)]
    unreachable = [v for v in all_vecs if not in_span_mod2(v, gens)]

    print(f"  reachable_count    = {len(reachable)}")
    print(f"  unreachable_count  = {len(unreachable)}")

    print("\nUNREACHABLE PARITY VECTORS (first 16)")
    for v in unreachable[:16]:
        print(f"  {v}")

    if unreachable:
        witness = unreachable[0]
        print("\nWITNESS MISSING COSET REPRESENTATIVE")
        print(f"  witness            = {witness}")

    print("\nPARITY PATTERN HINT")
    print("  Compare reachable/unreachable vectors to see whether one linear parity condition cuts out the observed lattice image mod 2.")


if __name__ == "__main__":
    main()
