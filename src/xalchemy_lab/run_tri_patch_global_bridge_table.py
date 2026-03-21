from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
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

BRIDGE_PAIRS: list[tuple[str, str]] = [
    ("w_bundled", "global_square"),
    ("w_hold", "global_twist"),
    ("w_LR_1", "global_twist"),
    ("w_LR_2", "global_twist"),
    ("w_LL", "global_return"),

    # diagnostic stress-test rows
    ("w_single_L1", "global_square"),
    ("w_single_L2", "global_square"),
    ("w_single_R1", "global_square"),
    ("w_hold_then_LR", "global_return"),
    ("w_LR_then_hold", "global_return"),
    ("w_LL_then_LR", "global_twist"),
    ("w_two_LR", "global_return"),

    # break-search rows
    ("w_hold_then_LR", "global_return"),
    ("w_LR_then_hold", "global_return"),
    ("w_two_LR", "global_return"),
    ("w_LL_then_LR", "global_twist"),
]


@dataclass
class LiftState:
    world: World
    lift_bit: int = 0


def load_global_loops() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    spec_path = Path("specs/signed_lift_bridge_loops_v1.json")
    data = json.loads(spec_path.read_text())
    loops = {}
    for loop in data.get("loops", []):
        loops[loop["name"]] = loop
    alphabet = data.get("symbol_alphabet", {})
    return loops, alphabet


def load_actual_loop_artifacts() -> dict[str, dict[str, Any]]:
    artifact_path = Path("specs/signed_lift_actual_loop_artifacts_v1.json")
    if not artifact_path.exists():
        return {}
    data = json.loads(artifact_path.read_text())
    loops = {}
    for loop in data.get("loops", []):
        loops[loop["name"]] = loop
    return loops


GLOBAL_LOOPS, SYMBOL_ALPHABET = load_global_loops()
ACTUAL_LOOP_ARTIFACTS = load_actual_loop_artifacts()


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
    return tuple(world.turtles[name].node for name in ("L1", "L2", "R1"))


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

    ds = sub3(run["final_stress"], base["final_stress"])
    dm = sub3(run["final_mismatch"], base["final_mismatch"])

    return {
        "word": word,
        "delta_stress": ds,
        "delta_mismatch": dm,
        "mismatch_parity": total_mismatch_parity(dm),
        "lift_bit": run["lift_bit"],
        "final_nodes": run["final_nodes"],
        "final_signs": run["final_signs"],
    }


def global_cocycle_value(loop_name: str, loop_info: dict[str, Any]) -> tuple[int | None, str]:
    actual_artifact = ACTUAL_LOOP_ARTIFACTS.get(loop_name)
    if actual_artifact is not None and actual_artifact.get("actual_cocycle") is not None:
        return int(actual_artifact["actual_cocycle"]), "actual_signed_lift_artifact"

    actual = loop_info.get("actual_cocycle")
    if actual is not None:
        return int(actual), "loop_spec_actual"

    rtype = loop_info.get("representation_type")
    path = loop_info.get("path")
    path_1 = loop_info.get("path_1")
    path_2 = loop_info.get("path_2")

    if rtype == "symbolic_closed_walk" and path == ["x", "x^-1"]:
        return 0, "provisional_symbolic"
    if rtype == "symbolic_closed_walk" and path == ["s1", "s2", "s3", "s4"]:
        return 0, "provisional_symbolic"
    if rtype == "symbolic_two_path_loop" and path_1 == ["a", "b"] and path_2 == ["c", "d"]:
        return 1, "provisional_symbolic"

    return None, "missing"


def summarize_loop(loop_name: str, loop_info: dict[str, Any]) -> str:
    artifact = ACTUAL_LOOP_ARTIFACTS.get(loop_name, {})
    if artifact.get("base_walk_type") == "symbolic_closed_walk" and artifact.get("base_walk") is not None:
        return f"{artifact['base_walk_type']} path={artifact.get('base_walk', [])}"
    if artifact.get("base_walk_type") == "symbolic_two_path_loop":
        return (
            f"{artifact['base_walk_type']} "
            f"path_1={artifact.get('path_1', [])} "
            f"path_2={artifact.get('path_2', [])}"
        )

    rtype = loop_info.get("representation_type", "unknown")
    start = loop_info.get("start_object", "?")
    if rtype == "symbolic_closed_walk":
        return f"{rtype} start={start} path={loop_info.get('path', [])}"
    if rtype == "symbolic_two_path_loop":
        return (
            f"{rtype} start={start} "
            f"path_1={loop_info.get('path_1', [])} "
            f"path_2={loop_info.get('path_2', [])}"
        )
    return repr(loop_info)


def interpret_loop(loop_name: str, loop_info: dict[str, Any]) -> str:
    artifact = ACTUAL_LOOP_ARTIFACTS.get(loop_name, {})
    if artifact.get("base_meaning"):
        return str(artifact["base_meaning"])

    rtype = loop_info.get("representation_type", "unknown")
    start = loop_info.get("start_object", "?")

    if rtype == "symbolic_closed_walk":
        path = loop_info.get("path", [])
        if path == ["x", "x^-1"]:
            return "explicit out-and-back walk: q0 -> q1 -> q0"
        if path == ["s1", "s2", "s3", "s4"]:
            return "explicit small cycle walk: q0 -> q1 -> q2 -> q4 -> q0"
        return f"closed walk from {start} with symbolic path {path}"

    if rtype == "symbolic_two_path_loop":
        path_1 = loop_info.get("path_1", [])
        path_2 = loop_info.get("path_2", [])
        if path_1 == ["a", "b"] and path_2 == ["c", "d"]:
            return "explicit two-path comparison: path_1 is q0 -> q1 -> q2, path_2 is q0 -> q3 -> q2"
        return (
            f"two-path comparison loop from {start}: "
            f"go out by {path_1}, return by comparing against {path_2}"
        )

    return "uninterpreted symbolic loop"


def format_triple(x: tuple[int, int, int]) -> str:
    return f"({x[0]},{x[1]},{x[2]})"


def main() -> None:
    print("\n====================")
    print("TRI-PATCH GLOBAL BRIDGE TABLE")
    print("====================")
    print("Bridge table prefers actual signed-lift artifact values and falls back to the provisional symbolic evaluator.")
    print()

    for case_label, start_node, sign, stress, mismatch in [
        ("u1R_clean_locked", "u1R", "+", (0, 0, 0), (0, 0, 0)),
        ("d1R_clean_locked", "d1R", "-", (0, 0, 0), (0, 0, 0)),
    ]:
        print("====================")
        print(f"LOCAL CASE: {case_label}")
        print("====================\n")
        print("BRIDGE PAIR TABLE")

        for local_word_name, global_loop_name in BRIDGE_PAIRS:
            hol = local_holonomy_data(
                start_node=start_node,
                sign=sign,
                stress=stress,
                mismatch=mismatch,
                word=LOCAL_WORDS[local_word_name],
            )

            ginfo = GLOBAL_LOOPS[global_loop_name]
            gcocycle, gsource = global_cocycle_value(global_loop_name, ginfo)

            print(f"  local={local_word_name:18s} <-> global={global_loop_name}")
            print(f"    local_delta_s    = {format_triple(hol['delta_stress'])}")
            print(f"    local_delta_m    = {format_triple(hol['delta_mismatch'])}")
            print(f"    local_dm_parity  = {hol['mismatch_parity']}")
            print(f"    local_lift_bit   = {hol['lift_bit']}")
            print(f"    global_repr      = {summarize_loop(global_loop_name, ginfo)}")
            print(f"    global_meaning   = {interpret_loop(global_loop_name, ginfo)}")
            print(f"    global_cocycle   = {gcocycle}")
            print(f"    global_source    = {gsource}")

            if gcocycle is None:
                print("    bridge_status    = VALUE_PENDING")
            else:
                print(f"    bridge_status    = {'MATCH' if hol['lift_bit'] == gcocycle else 'MISMATCH'}")
            print()

        print()

    print("Summary:")
    print("  mismatch parity remains the kernel channel")
    print("  lift_bit remains the current local bridge candidate")
    print("  symbolic global loop bodies are now present")
    print("  global_return and global_square now have minimal formal interpretations")
    print("  bridge table now prefers actual signed-lift artifact values")
    print("  provisional symbolic cocycle evaluation remains the fallback")
    print()


if __name__ == "__main__":
    main()
