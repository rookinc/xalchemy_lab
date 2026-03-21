from __future__ import annotations

from itertools import permutations
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

BASE_CARRIERS = ("L1", "L2", "R1")
BASE_CHIRALITY = {
    "L1": "L",
    "L2": "L",
    "R1": "R",
}

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
    for name in BASE_CARRIERS:
        middle_moves[name] = opposite_hub if name in advancers else "mR"
    middle_event = do_step(world, middle_moves)

    maybe_toggle_lift_bit(state, middle_event, route_name)

    do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})

    return middle_event


def relabel_route(route: tuple[str, ...], mapping: dict[str, str]) -> tuple[str, ...]:
    return tuple(sorted(mapping[name] for name in route))


def relabeled_chirality(mapping: dict[str, str]) -> dict[str, str]:
    # Push forward the base chirality labels onto the renamed carriers.
    out: dict[str, str] = {}
    for old_name, new_name in mapping.items():
        out[new_name] = BASE_CHIRALITY[old_name]
    return out


def dyad_chirality_type(relabeled_route: tuple[str, ...], pushed_chirality: dict[str, str]) -> str:
    if len(relabeled_route) != 2:
        return "not_dyad"
    c1 = pushed_chirality[relabeled_route[0]]
    c2 = pushed_chirality[relabeled_route[1]]
    return "".join(sorted((c1, c2)))  # LL, LR, RR


def route_feature_under_relabel(
    route_name: str,
    mapping: dict[str, str],
) -> dict[str, object]:
    relabeled = relabel_route(ROUTES[route_name], mapping)
    pushed = relabeled_chirality(mapping)
    return {
        "relabeled_route": relabeled,
        "is_hold_all": len(relabeled) == 0,
        "is_singleton": len(relabeled) == 1,
        "is_dyad": len(relabeled) == 2,
        "is_triad": len(relabeled) == 3,
        "dyad_type": dyad_chirality_type(relabeled, pushed),
        "is_mixed_dyad": dyad_chirality_type(relabeled, pushed) == "LR",
    }


def main() -> None:
    print("\n====================")
    print("LIFT BIT CHIRALITY INVARIANT PROBE")
    print("====================")
    print("Test whether the lift-bit rule is better stated as: hold_all OR chirality-mixed dyad.\n")

    perms = list(permutations(BASE_CARRIERS))
    mappings = [dict(zip(BASE_CARRIERS, perm)) for perm in perms]

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"CASE: {case_label}")

        base_rows = []
        for route_name in ROUTES:
            state = LiftState(world=make_world(start_node, sign, stress, mismatch), lift_bit=0)
            middle_event = run_route_once(state, start_node, ROUTES[route_name], route_name)
            base_rows.append((route_name, state.lift_bit, middle_event))

        print("\nBASE PRIMITIVE TABLE")
        for route_name, bit, middle_event in base_rows:
            print(f"  {route_name:20s} lift_bit={bit} middle_event={middle_event}")

        print("\nRELABEL + CHIRALITY ANALYSIS")
        all_ok = True
        for mapping in mappings:
            print(f"\n  mapping = {mapping}")
            pushed = relabeled_chirality(mapping)
            print(f"    pushed_chirality = {pushed}")
            for route_name, bit, _ in base_rows:
                feat = route_feature_under_relabel(route_name, mapping)
                predicted = int(feat["is_hold_all"] or feat["is_mixed_dyad"])
                ok = (predicted == bit)
                all_ok = all_ok and ok
                print(
                    f"    base_route={route_name:20s} "
                    f"relabeled_route={feat['relabeled_route']!s:18s} "
                    f"dyad_type={feat['dyad_type']:8s} "
                    f"is_hold_all={int(feat['is_hold_all'])} "
                    f"is_mixed_dyad={int(feat['is_mixed_dyad'])} "
                    f"pred={predicted} "
                    f"lift_bit={bit} "
                    f"match={ok}"
                )

        print(f"\nall_relabels_match_hold_or_mixed_dyad = {all_ok}")
        print("\nsummary note")
        print("  If true, the current lift bit is not 'contains R1' in any absolute sense; it is 'stall or chirality-mixed dyad' in the pushed-forward chirality structure.")

        print()


if __name__ == "__main__":
    main()
