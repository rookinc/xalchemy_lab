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
    for name in ("L1", "L2", "R1"):
        middle_moves[name] = opposite_hub if name in advancers else "mR"
    middle_event = do_step(world, middle_moves)

    maybe_toggle_lift_bit(state, middle_event, route_name)

    do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})

    return middle_event


def candidate_predicates(route_name: str, middle_event: tuple[str | None, str | None, str | None]) -> dict[str, int]:
    advancers = ROUTES[route_name]
    adv_count = len(advancers)
    node, kind, face = middle_event

    return {
        "stall_or_lr_transfer": int(route_name == "hold_all" or (kind == "LR" and face in {"sign_transfer+", "sign_transfer-"})),
        "not_bundle_compatible": int(route_name == "hold_all" or kind == "LR"),
        "contains_R1_without_full_triad": int(("R1" in advancers) and adv_count < 3),
        "mixed_chirality_or_stall": int(route_name == "hold_all" or kind == "LR"),
        "nontriadic_with_R1": int(adv_count < 3 and "R1" in advancers),
        "hold_or_two_with_R1": int(route_name == "hold_all" or (adv_count == 2 and "R1" in advancers)),
    }


def main() -> None:
    print("\n====================")
    print("LIFT BIT GEOMETRIC PREDICATE PROBE")
    print("====================")
    print("Test more geometric candidate predicates against the invariant lift-bit rule.\n")

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"CASE: {case_label}")

        rows = []
        for route_name in ROUTES:
            state = LiftState(world=make_world(start_node, sign, stress, mismatch), lift_bit=0)
            middle_event = run_route_once(state, start_node, ROUTES[route_name], route_name)
            target = state.lift_bit
            preds = candidate_predicates(route_name, middle_event)
            rows.append((route_name, middle_event, target, preds))

        print("\nROUTE TABLE")
        for route_name, middle_event, target, preds in rows:
            print(f"  {route_name:20s} target={target} middle_event={middle_event}")
            for k, v in preds.items():
                print(f"    {k:24s} = {v}")

        print("\nPREDICATE MATCH CHECK")
        for pred_name in rows[0][3].keys():
            ok = all(preds[pred_name] == target for _, _, target, preds in rows)
            print(f"  {pred_name:24s} match={ok}")

        print()

if __name__ == "__main__":
    main()
