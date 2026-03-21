from __future__ import annotations

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


def maybe_toggle_lift_bit(state: LiftState, middle_event: tuple[str | None, str | None, str | None], route_name: str) -> None:
    node, kind, face = middle_event

    # Candidate rule set for a missing cocycle-like bit:
    # Toggle on non-bundled dyadic middle events only.
    # This is deliberately minimal and exploratory.
    if kind == "LR" and face in {"sign_transfer+", "sign_transfer-"}:
        state.lift_bit ^= 1
        return

    # Optional second toggle family: holding everyone at mR can also be treated as
    # a sheet-sensitive stalled routing event.
    if route_name == "hold_all":
        state.lift_bit ^= 1
        return


def run_route_once(state: LiftState, start_node: str, advancers: tuple[str, ...], route_name: str) -> tuple[str | None, str | None, str | None]:
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


def run_route(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    route_name: str,
) -> dict[str, object]:
    state = LiftState(world=make_world(start_node, sign, stress, mismatch), lift_bit=0)
    middle_event = run_route_once(state, start_node, ROUTES[route_name], route_name)

    return {
        "nodes": nodes_vec(state.world),
        "signs": sign_vec(state.world),
        "stress": stress_vec(state.world),
        "mismatch": mismatch_vec(state.world),
        "mismatch_parity": total_mismatch_parity(mismatch_vec(state.world)),
        "lift_bit": state.lift_bit,
        "middle_event": middle_event,
    }


def main() -> None:
    print("\n====================")
    print("LIFT BIT PROBE")
    print("====================")
    print("Augment local transport with an explicit binary lift register and test whether it can distinguish route classes while the old even-mismatch kernel remains intact.")

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"\n====================")
        print(f"CASE: {case_label}")
        print("====================")
        print(f"start_node          = {start_node}")
        print(f"initial_signs       = {(sign, sign, sign)}")
        print(f"initial_stress      = {stress}")
        print(f"initial_mismatch    = {mismatch}")

        for route_name in ROUTES:
            result = run_route(start_node, sign, stress, mismatch, route_name)

            print(f"\nroute               = {route_name}")
            print(f"  middle_event      = {result['middle_event']}")
            print(f"  final_nodes       = {result['nodes']}")
            print(f"  final_signs       = {result['signs']}")
            print(f"  final_stress      = {result['stress']}")
            print(f"  final_mismatch    = {result['mismatch']}")
            print(f"  mismatch_parity   = {result['mismatch_parity']}")
            print(f"  lift_bit          = {result['lift_bit']}")

        print("\nsummary note")
        print("  In a successful augmented model, mismatch parity should stay even while lift_bit provides a second binary channel that can separate route classes.")


if __name__ == "__main__":
    main()
