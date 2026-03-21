from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from xalchemy_lab.tri_patch_core import World, Turtle, step


ROUTES: dict[str, tuple[str, ...]] = {
    "hold_all": (),
    "advance_L1": ("L1",),
    "advance_L2": ("L2",),
    "advance_R1": ("R1",),
    "advance_L1_L2": ("L1", "L2"),
    "advance_L1_R1": ("L1", "R1"),
    "advance_L2_R1": ("L2", "R1"),
    "advance_L1_L2_R1": ("L1", "L2", "R1"),
}

LOCAL_WORDS: dict[str, tuple[str, ...]] = {
    "w_bundled": ("advance_L1_L2_R1",),
    "w_hold": ("hold_all",),
    "w_LR_1": ("advance_L1_R1",),
    "w_LR_2": ("advance_L2_R1",),
    "w_LL": ("advance_L1_L2",),
    "w_single_L1": ("advance_L1",),
    "w_single_L2": ("advance_L2",),
    "w_single_R1": ("advance_R1",),
    "w_hold_then_LR": ("hold_all", "advance_L1_R1"),
    "w_LR_then_hold": ("advance_L1_R1", "hold_all"),
    "w_LL_then_LR": ("advance_L1_L2", "advance_L1_R1"),
    "w_two_LR": ("advance_L1_R1", "advance_L2_R1"),
}

GLOBAL_LOOPS: dict[str, dict[str, Any]] = {
    "global_square": {
        "description": "User-supplied global loop",
        "cocycle": 0,
    },
    "global_twist": {
        "description": "User-supplied global loop",
        "cocycle": 1,
    },
    "global_return": {
        "description": "User-supplied global loop",
        "cocycle": 0,
    },
}

BRIDGE_PAIRS: list[tuple[str, str]] = [
    ("w_bundled", "global_square"),
    ("w_hold", "global_twist"),
    ("w_LR_1", "global_twist"),
    ("w_LR_2", "global_twist"),
    ("w_LL", "global_return"),
]


@dataclass
class LiftState:
    world: World
    lift_bit: int = 0


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
    return tuple(world.turtles[name].carried_stress for name in ("L1", "L2", "R1"))


def mismatch_vec(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[name].mismatch_count for name in ("L1", "L2", "R1"))


def sign_vec(world: World) -> tuple[str | None, str | None, str | None]:
    return tuple(world.turtles[name].carry_sign for name in ("L1", "L2", "R1"))


def node_vec(world: World) -> tuple[str, str, str]:
    return tuple(world.turtles[name].node for name in ("L1", "L2", "R1"))  # type: ignore[return-value]


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


def maybe_toggle_lift_bit(state: LiftState, route_name: str) -> None:
    advancers = ROUTES[route_name]
    is_stall = len(advancers) == 0
    is_two_advancer_lr = (
        len(advancers) == 2
        and "R1" in advancers
        and len(set(advancers) & {"L1", "L2"}) == 1
    )
    if is_stall or is_two_advancer_lr:
        state.lift_bit ^= 1


def run_route_once(
    state: LiftState,
    start_node: str,
    advancers: tuple[str, ...],
    route_name: str,
) -> None:
    world = state.world

    if start_node == "u1R":
        first_hub = "u1R"
        opposite_hub = "d1R"
    elif start_node == "d1R":
        first_hub = "d1R"
        opposite_hub = "u1R"
    else:
        raise ValueError(f"Unexpected start node: {start_node}")

    do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})
    do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})

    middle_moves = {}
    for name in ("L1", "L2", "R1"):
        middle_moves[name] = opposite_hub if name in advancers else "mR"
    do_step(world, middle_moves)

    maybe_toggle_lift_bit(state, route_name)

    do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub})


def run_local_word(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    word: tuple[str, ...],
) -> dict[str, Any]:
    state = LiftState(
        world=make_world(start_node, sign, stress, mismatch),
        lift_bit=0,
    )

    for route_name in word:
        run_route_once(state, start_node, ROUTES[route_name], route_name)

    return {
        "final_nodes": node_vec(state.world),
        "final_signs": sign_vec(state.world),
        "final_stress": stress_vec(state.world),
        "final_mismatch": mismatch_vec(state.world),
        "lift_bit": state.lift_bit,
    }


def local_holonomy_data(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    word: tuple[str, ...],
) -> dict[str, Any]:
    bundled_word = ("advance_L1_L2_R1",) * len(word)
    base = run_local_word(start_node, sign, stress, mismatch, bundled_word)
    run = run_local_word(start_node, sign, stress, mismatch, word)

    ds = sub3(run["final_stress"], base["final_stress"])      # type: ignore[arg-type]
    dm = sub3(run["final_mismatch"], base["final_mismatch"])  # type: ignore[arg-type]

    return {
        "word": word,
        "delta_stress": ds,
        "delta_mismatch": dm,
        "mismatch_parity": total_mismatch_parity(dm),
        "lift_bit": run["lift_bit"],
        "final_nodes": run["final_nodes"],
        "final_signs": run["final_signs"],
    }


def global_cocycle_value(loop_label: str, loop_info: dict[str, Any]) -> int | None:
    return loop_info.get("cocycle")


def format_triple(x: tuple[int, int, int]) -> str:
    return f"({x[0]},{x[1]},{x[2]})"


def main() -> None:
    print("\n====================")
    print("TRI-PATCH GLOBAL BRIDGE TABLE")
    print("====================")
    print("First explicit local/global comparison table using your named global loop bits.")

    for case_label, start_node, sign, stress, mismatch in [
        ("u1R_clean_locked", "u1R", "+", (8, 8, 8), (4, 4, 4)),
        ("d1R_clean_locked", "d1R", "-", (8, 8, 8), (4, 4, 4)),
    ]:
        print(f"\n====================")
        print(f"LOCAL CASE: {case_label}")
        print("====================")

        local_cache: dict[str, dict[str, Any]] = {}
        for local_label, word in LOCAL_WORDS.items():
            local_cache[local_label] = local_holonomy_data(
                start_node, sign, stress, mismatch, word
            )

        print("\nBRIDGE PAIR TABLE")
        for local_label, global_label in BRIDGE_PAIRS:
            local_data = local_cache[local_label]
            global_info = GLOBAL_LOOPS[global_label]
            global_bit = global_cocycle_value(global_label, global_info)

            print(f"  local={local_label:16s} <-> global={global_label}")
            print(f"    local_delta_s    = {format_triple(local_data['delta_stress'])}")
            print(f"    local_delta_m    = {format_triple(local_data['delta_mismatch'])}")
            print(f"    local_dm_parity  = {local_data['mismatch_parity']}")
            print(f"    local_lift_bit   = {local_data['lift_bit']}")
            print(f"    global_cocycle   = {global_bit}")
            print(f"    global_note      = {global_info.get('description', '')}")

        print("\nREADING")
        print("  mismatch_parity is the kernel channel.")
        print("  lift_bit is the bridge candidate channel.")


if __name__ == "__main__":
    main()
