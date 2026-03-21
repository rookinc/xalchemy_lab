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


def route_features(route_name: str, middle_event: tuple[str | None, str | None, str | None]) -> dict[str, int]:
    advancers = ROUTES[route_name]
    adv_count = len(advancers)
    has_R1 = int("R1" in advancers)
    has_L1 = int("L1" in advancers)
    has_L2 = int("L2" in advancers)
    is_hold_all = int(adv_count == 0)
    is_singleton = int(adv_count == 1)
    is_dyadic = int(adv_count == 2)
    is_triad = int(adv_count == 3)

    node, kind, face = middle_event
    is_lr_transfer = int(kind == "LR" and face in {"sign_transfer+", "sign_transfer-"})
    is_ll_face = int(kind == "LL")
    is_nonevent = int(kind is None)

    return {
        "is_hold_all": is_hold_all,
        "is_singleton": is_singleton,
        "is_dyadic": is_dyadic,
        "is_triad": is_triad,
        "has_L1": has_L1,
        "has_L2": has_L2,
        "has_R1": has_R1,
        "adv_count_mod2": adv_count % 2,
        "is_lr_transfer": is_lr_transfer,
        "is_ll_face": is_ll_face,
        "is_nonevent": is_nonevent,
    }


def eval_linear_rule(feats: dict[str, int], coeffs: dict[str, int]) -> int:
    total = 0
    for k, c in coeffs.items():
        total ^= (c & 1) & (feats[k] & 1)
    return total


def main() -> None:
    print("\n====================")
    print("LIFT BIT INVARIANT PROBE")
    print("====================")
    print("Search for a simple mod-2 feature rule that reproduces the exploratory lift bit.\n")

    route_names = tuple(ROUTES.keys())
    feature_names = [
        "is_hold_all",
        "is_singleton",
        "is_dyadic",
        "is_triad",
        "has_L1",
        "has_L2",
        "has_R1",
        "adv_count_mod2",
        "is_lr_transfer",
        "is_ll_face",
        "is_nonevent",
    ]

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"CASE: {case_label}")

        rows = []
        for route_name in route_names:
            state = LiftState(world=make_world(start_node, sign, stress, mismatch), lift_bit=0)
            middle_event = run_route_once(state, start_node, ROUTES[route_name], route_name)
            feats = route_features(route_name, middle_event)
            target = state.lift_bit
            rows.append((route_name, feats, target, middle_event))

        print("\nROUTE FEATURES")
        for route_name, feats, target, middle_event in rows:
            print(f"  {route_name:20s} target={target} middle_event={middle_event}")
            print(f"    {feats}")

        matches = []
        for bits in product([0, 1], repeat=len(feature_names)):
            coeffs = dict(zip(feature_names, bits))
            ok = True
            for _, feats, target, _ in rows:
                if eval_linear_rule(feats, coeffs) != target:
                    ok = False
                    break
            if ok:
                matches.append(coeffs)

        print(f"\nmatching_linear_rules = {len(matches)}")
        for coeffs in matches[:10]:
            active = [name for name in feature_names if coeffs[name]]
            print(f"  active_terms = {active}")

        print("\nsummary note")
        print("  A small number of matching linear rules means the current lift bit may admit an invariant feature description rather than requiring explicit event-name toggles.")

        print()

if __name__ == "__main__":
    main()
