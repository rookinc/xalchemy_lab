from __future__ import annotations

from itertools import product

from dataclasses import dataclass

from xalchemy_lab.tri_patch_core import World, Turtle, step


@dataclass
class LiftState:
    world: World
    lift_bit: int = 0


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

WORD_LENGTHS = (1, 2, 3, 4)


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


def total_mismatch_parity(dm: tuple[int, int, int]) -> int:
    return (dm[0] + dm[1] + dm[2]) % 2


def do_step(world: World, moves: dict[str, str]) -> tuple[str | None, str | None, str | None]:
    before = len(world.collisions)
    step(world, moves)
    if len(world.collisions) == before:
        return None, None, None
    c = world.collisions[-1]
    return c.node, c.kind, c.face_event


def maybe_toggle_lift_bit(
    state: LiftState,
    middle_event: tuple[str | None, str | None, str | None],
    route_name: str,
) -> None:
    node, kind, face = middle_event

    if kind == "LR" and face in {"sign_transfer+", "sign_transfer-"}:
        state.lift_bit ^= 1
        return

    if route_name == "hold_all":
        state.lift_bit ^= 1
        return


def run_route_once(
    state: LiftState,
    start_node: str,
    advancers: tuple[str, ...],
    route_name: str,
) -> tuple[str | None, str | None, str | None]:
    world = state.world

    if start_node == "u1R":
        first_hub = "u1R"
        opposite_hub = "d1R"
    else:
        first_hub = "d1R"
        opposite_hub = "u1R"

    do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})
    do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})

    middle_moves = {}
    for name in ("L1", "L2", "R1"):
        middle_moves[name] = opposite_hub if name in advancers else "mR"
    middle_event = do_step(world, middle_moves)

    maybe_toggle_lift_bit(state, middle_event, route_name)

    do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})

    return middle_event


def run_word(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    word: tuple[str, ...],
) -> dict[str, object]:
    state = LiftState(world=make_world(start_node, sign, stress, mismatch), lift_bit=0)
    middle_events: list[tuple[str | None, str | None, str | None]] = []

    for route_name in word:
        middle_events.append(run_route_once(state, start_node, ROUTES[route_name], route_name))

    return {
        "nodes": nodes_vec(state.world),
        "signs": sign_vec(state.world),
        "stress": stress_vec(state.world),
        "mismatch": mismatch_vec(state.world),
        "mismatch_parity": total_mismatch_parity(mismatch_vec(state.world)),
        "lift_bit": state.lift_bit,
        "middle_events": middle_events,
    }


def main() -> None:
    print("\n====================")
    print("LIFT BIT COMPOSITION PROBE EXTENDED")
    print("====================")
    print("Test whether lift_bit remains additive mod 2 for longer route words while mismatch parity stays even.")

    route_names = tuple(ROUTES.keys())

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"\n====================")
        print(f"CASE: {case_label}")
        print("====================")
        print(f"start_node          = {start_node}")

        singles = {
            name: run_word(start_node, sign, stress, mismatch, (name,))
            for name in route_names
        }

        print("\nSINGLE-STEP LIFT BITS")
        for name in route_names:
            print(f"  {name:20s} -> {singles[name]['lift_bit']}")

        for word_length in WORD_LENGTHS:
            words = list(product(route_names, repeat=word_length))
            checked = 0
            composition_failures: list[str] = []
            odd_mismatch_failures: list[str] = []

            for word in words:
                res = run_word(start_node, sign, stress, mismatch, word)

                expected = 0
                for route_name in word:
                    expected ^= singles[route_name]["lift_bit"]  # type: ignore[index]

                actual = res["lift_bit"]  # type: ignore[assignment]
                checked += 1

                if actual != expected and len(composition_failures) < 20:
                    composition_failures.append(
                        f"word={word} actual={actual} expected={expected} "
                        f"middle_events={res['middle_events']} final_nodes={res['nodes']} final_signs={res['signs']}"
                    )

                if res["mismatch_parity"] != 0 and len(odd_mismatch_failures) < 20:
                    odd_mismatch_failures.append(
                        f"word={word} mismatch={res['mismatch']} mismatch_parity={res['mismatch_parity']} "
                        f"lift_bit={res['lift_bit']}"
                    )

            print(f"\nword_length         = {word_length}")
            print(f"  checked_words     = {checked}")
            print(f"  composition_failures = {len(composition_failures)}")
            print(f"  odd_mismatch_failures = {len(odd_mismatch_failures)}")

            if composition_failures:
                print("  COMPOSITION FAILURE EXAMPLES")
                for line in composition_failures:
                    print(f"    {line}")
            else:
                print("  lift_bit stayed additive mod 2 on all tested words.")

            if odd_mismatch_failures:
                print("  ODD MISMATCH FAILURE EXAMPLES")
                for line in odd_mismatch_failures:
                    print(f"    {line}")
            else:
                print("  mismatch parity stayed even on all tested words.")

        print("\nsummary note")
        print("  If both properties hold through length 4, the augmented local model has a stable kernel/cocycle split on the tested semigroup.")


if __name__ == "__main__":
    main()
