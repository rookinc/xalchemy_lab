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

CARRIERS = ("L1", "L2", "R1")

# Enumerate all primitive middle-route subsets as the current local chart
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
            "L1": Turtle(name="L1", chirality="L", node=start_node, carry_sign=sign, carried_stress=stress[0], mismatch_count=mismatch[0]),
            "L2": Turtle(name="L2", chirality="L", node=start_node, carry_sign=sign, carried_stress=stress[1], mismatch_count=mismatch[1]),
            "R1": Turtle(name="R1", chirality="R", node=start_node, carry_sign=sign, carried_stress=stress[2], mismatch_count=mismatch[2]),
        }
    )


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
    for name in CARRIERS:
        middle_moves[name] = opposite_hub if name in advancers else "mR"
    middle_event = do_step(world, middle_moves)

    maybe_toggle_lift_bit(state, middle_event, route_name)

    do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})

    return middle_event


def chirality_rule(route_name: str, middle_event: tuple[str | None, str | None, str | None]) -> int:
    node, kind, face = middle_event
    return int(route_name == "hold_all" or kind == "LR")


def main() -> None:
    print("\n====================")
    print("LARGER CHART LIFT RULE PROBE")
    print("====================")
    print("Check that the chirality-based lift rule remains the correct primitive classifier across the full enumerated middle-route chart.\n")

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"CASE: {case_label}")

        mismatches = []

        for route_name, advancers in ROUTES.items():
            state = LiftState(world=make_world(start_node, sign, stress, mismatch), lift_bit=0)
            middle_event = run_route_once(state, start_node, advancers, route_name)
            predicted = chirality_rule(route_name, middle_event)
            actual = state.lift_bit

            print(
                f"  {route_name:20s} "
                f"middle_event={middle_event} "
                f"pred={predicted} "
                f"actual={actual} "
                f"match={predicted == actual}"
            )

            if predicted != actual:
                mismatches.append((route_name, middle_event, predicted, actual))

        print(f"\nall_routes_match_chirality_rule = {len(mismatches) == 0}")
        if mismatches:
            print("mismatches:")
            for row in mismatches:
                print(f"  {row}")

        print("\nsummary note")
        print("  If the chart stays clean here, the current local binary law is stable on the full primitive middle-route family.")
        print()


if __name__ == "__main__":
    main()
