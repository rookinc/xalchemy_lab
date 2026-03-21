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

WORD_LEN = 2


def make_world(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
) -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=start_node, carry_sign=sign, carried_stress=stress[0], mismatch_count=mismatch[0]),
            "L2": Turtle(name="L2", chirality="L", node=start_node, carry_sign=sign, carried_stress=stress[1], mismatch_count=mismatch[1]),
            "R1": Turtle(name="R1", chirality="R", node=start_node, carry_sign=sign, carried_stress=stress[2], mismatch_count=mismatch[2]),
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


def total_mismatch_parity(dm: tuple[int, int, int]) -> int:
    return (dm[0] + dm[1] + dm[2]) % 2


def do_step(world: World, moves: dict[str, str]) -> tuple[str | None, str | None, str | None]:
    before = len(world.collisions)
    step(world, moves)
    if len(world.collisions) == before:
        return None, None, None
    c = world.collisions[-1]
    return c.node, c.kind, c.face_event


def maybe_toggle_lift_bit(state: LiftState, middle_event: tuple[str | None, str | None, str | None], route_name: str) -> None:
    node, kind, face = middle_event
    if kind == "LR" and face in {"sign_transfer+", "sign_transfer-"}:
        state.lift_bit ^= 1
        return
    if route_name == "hold_all":
        state.lift_bit ^= 1
        return


def run_route_once(state: LiftState, start_node: str, advancers: tuple[str, ...], route_name: str) -> None:
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


def run_word(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    word: tuple[str, ...],
) -> dict[str, object]:
    state = LiftState(world=make_world(start_node, sign, stress, mismatch), lift_bit=0)
    for route_name in word:
        run_route_once(state, start_node, ROUTES[route_name], route_name)
    return {
        "nodes": nodes_vec(state.world),
        "signs": sign_vec(state.world),
        "stress": stress_vec(state.world),
        "mismatch": mismatch_vec(state.world),
        "lift_bit": state.lift_bit,
        "mismatch_parity": total_mismatch_parity(mismatch_vec(state.world)),
    }


def main() -> None:
    print("\n====================")
    print("LIFT BIT VS HOLONOMY TABLE")
    print("====================")
    print("Tabulate local route words, holonomy vectors, mismatch parity, and lift_bit in one place.")

    route_names = tuple(ROUTES.keys())

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"\n====================")
        print(f"CASE: {case_label}")
        print("====================")

        bundled_1 = run_word(start_node, sign, stress, mismatch, ("advance_L1_L2_R1",))
        print("\nPRIMITIVES")
        for route_name in route_names:
            res = run_word(start_node, sign, stress, mismatch, (route_name,))
            ds = sub3(res["stress"], bundled_1["stress"])      # type: ignore[arg-type]
            dm = sub3(res["mismatch"], bundled_1["mismatch"])  # type: ignore[arg-type]
            print(
                f"  {route_name:20s} "
                f"ds={ds} dm={dm} "
                f"dm_parity={sum(dm)%2} "
                f"lift_bit={res['lift_bit']}"
            )

        print(f"\nWORDS OF LENGTH {WORD_LEN}")
        bundled_w = run_word(start_node, sign, stress, mismatch, ("advance_L1_L2_R1",) * WORD_LEN)
        words = list(product(route_names, repeat=WORD_LEN))
        for word in words:
            res = run_word(start_node, sign, stress, mismatch, word)
            ds = sub3(res["stress"], bundled_w["stress"])      # type: ignore[arg-type]
            dm = sub3(res["mismatch"], bundled_w["mismatch"])  # type: ignore[arg-type]
            print(
                f"  word={word} "
                f"ds={ds} dm={dm} "
                f"dm_parity={sum(dm)%2} "
                f"lift_bit={res['lift_bit']}"
            )


if __name__ == "__main__":
    main()
