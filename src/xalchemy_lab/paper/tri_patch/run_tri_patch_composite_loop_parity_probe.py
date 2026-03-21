from __future__ import annotations

from itertools import product

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

WORD_LEN = 3


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


def run_word(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    word: tuple[str, ...],
) -> dict[str, object]:
    world = make_world(start_node, sign, stress, mismatch)
    for route_name in word:
        run_route_once(world, start_node, ROUTES[route_name])
    return {
        "nodes": nodes_vec(world),
        "signs": sign_vec(world),
        "stress": stress_vec(world),
        "mismatch": mismatch_vec(world),
    }


def main() -> None:
    print("\n====================")
    print("COMPOSITE LOOP PARITY PROBE")
    print("====================")
    print("Search longer local route-word differences for any odd total mismatch parity.")

    route_names = tuple(ROUTES.keys())
    words = list(product(route_names, repeat=WORD_LEN))

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"\n====================")
        print(f"CASE: {case_label}")
        print("====================")
        print(f"start_node          = {start_node}")
        print(f"word_length         = {WORD_LEN}")
        print(f"total_words         = {len(words)}")

        cache = {
            word: run_word(start_node, sign, stress, mismatch, word)
            for word in words
        }

        odd_examples: list[str] = []
        checked = 0

        for i, w1 in enumerate(words):
            r1 = cache[w1]
            for w2 in words[i + 1:]:
                r2 = cache[w2]

                if r1["nodes"] != r2["nodes"]:
                    continue
                if r1["signs"] != r2["signs"]:
                    continue

                dds = sub3(r1["stress"], r2["stress"])        # type: ignore[arg-type]
                ddm = sub3(r1["mismatch"], r2["mismatch"])    # type: ignore[arg-type]
                checked += 1

                if total_mismatch_parity(ddm) == 1:
                    odd_examples.append(
                        f"w1={w1} w2={w2} "
                        f"delta_delta_s={dds} "
                        f"delta_delta_m={ddm} "
                        f"mod2={mod2(flatten(dds, ddm))}"
                    )
                    if len(odd_examples) >= 20:
                        break
            if len(odd_examples) >= 20:
                break

        print(f"checked_comparable_pairs = {checked}")
        print(f"odd_parity_examples_found = {len(odd_examples)}")

        if odd_examples:
            print("\nODD TOTAL MISMATCH PARITY EXAMPLES")
            for line in odd_examples:
                print(f"  {line}")
        else:
            print("\nNo odd-total-mismatch composite differences found in this search window.")

    print("\nsummary note")
    print("  If odd examples remain absent for longer composite words, the local tri-patch likely realizes the kernel of a larger Z2 observable rather than the observable itself.")


if __name__ == "__main__":
    main()
