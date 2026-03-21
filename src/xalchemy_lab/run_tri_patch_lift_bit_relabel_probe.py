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


def primitive_feature_under_relabel(route_name: str, mapping: dict[str, str]) -> str:
    route = ROUTES[route_name]
    relabeled = relabel_route(route, mapping)

    if len(relabeled) == 0:
        return "hold_all"
    if len(relabeled) == 1:
        return f"singleton_{relabeled[0]}"
    if len(relabeled) == 2:
        return f"dyad_{'_'.join(relabeled)}"
    return "triad_all"


def main() -> None:
    print("\n====================")
    print("LIFT BIT RELABEL PROBE")
    print("====================")
    print("Test whether the primitive lift-bit rule is coordinate-dependent or reflects a genuine asymmetry of the patch.")

    perms = list(permutations(BASE_CARRIERS))
    mappings = []
    for perm in perms:
        mapping = dict(zip(BASE_CARRIERS, perm))
        mappings.append(mapping)

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"\n====================")
        print(f"CASE: {case_label}")
        print("====================")

        base_rows = []
        for route_name in ROUTES:
            state = LiftState(world=make_world(start_node, sign, stress, mismatch), lift_bit=0)
            middle_event = run_route_once(state, start_node, ROUTES[route_name], route_name)
            base_rows.append((route_name, state.lift_bit, middle_event))

        print("\nBASE PRIMITIVE TABLE")
        for route_name, bit, middle_event in base_rows:
            print(f"  {route_name:20s} lift_bit={bit} middle_event={middle_event}")

        print("\nRELABEL ANALYSIS")
        for mapping in mappings:
            print(f"\n  mapping = {mapping}")
            for route_name, bit, middle_event in base_rows:
                feature = primitive_feature_under_relabel(route_name, mapping)
                print(
                    f"    base_route={route_name:20s} "
                    f"relabel_feature={feature:18s} "
                    f"lift_bit={bit}"
                )

        print("\nsummary note")
        print("  If the bit is always attached to the image of base R1 under relabeling, then the current law is coordinate-dependent. If instead it collapses to a relabel-invariant route property, then the asymmetry is geometric rather than nominal.")


if __name__ == "__main__":
    main()
