from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


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


def nodes_vec(world: World) -> tuple[str, str, str]:
    return tuple(world.turtles[name].node for name in ("L1", "L2", "R1"))  # type: ignore[return-value]


def sub_vec(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def do_step(world: World, moves: dict[str, str]) -> tuple[str | None, str | None, str | None]:
    before = len(world.collisions)
    step(world, moves)
    if len(world.collisions) == before:
        return None, None, None
    c = world.collisions[-1]
    return c.node, c.kind, c.face_event


def run_bundled_route(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
) -> dict[str, object]:
    world = make_world(start_node, sign, stress, mismatch)

    if start_node == "u1R":
        schedule = [
            {"L1": "u1R", "L2": "u1R", "R1": "u1R"},
            {"L1": "mR", "L2": "mR", "R1": "mR"},
            {"L1": "d1R", "L2": "d1R", "R1": "d1R"},
            {"L1": "mR", "L2": "mR", "R1": "mR"},
            {"L1": "u1R", "L2": "u1R", "R1": "u1R"},
        ]
    else:
        schedule = [
            {"L1": "d1R", "L2": "d1R", "R1": "d1R"},
            {"L1": "mR", "L2": "mR", "R1": "mR"},
            {"L1": "u1R", "L2": "u1R", "R1": "u1R"},
            {"L1": "mR", "L2": "mR", "R1": "mR"},
            {"L1": "d1R", "L2": "d1R", "R1": "d1R"},
        ]

    events: list[tuple[str | None, str | None, str | None]] = []
    for moves in schedule:
        events.append(do_step(world, moves))

    return {
        "events": events,
        "nodes": nodes_vec(world),
        "signs": sign_vec(world),
        "stress": stress_vec(world),
        "mismatch": mismatch_vec(world),
    }


def run_split_route(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
) -> dict[str, object]:
    world = make_world(start_node, sign, stress, mismatch)

    if start_node == "u1R":
        schedule = [
            {"L1": "u1R", "L2": "u1R", "R1": "u1R"},
            {"L1": "mR", "L2": "mR", "R1": "mR"},
            {"L1": "d1R", "L2": "mR", "R1": "d1R"},
            {"L1": "mR", "L2": "mR", "R1": "mR"},
            {"L1": "u1R", "L2": "u1R", "R1": "u1R"},
        ]
    else:
        schedule = [
            {"L1": "d1R", "L2": "d1R", "R1": "d1R"},
            {"L1": "mR", "L2": "mR", "R1": "mR"},
            {"L1": "u1R", "L2": "mR", "R1": "u1R"},
            {"L1": "mR", "L2": "mR", "R1": "mR"},
            {"L1": "d1R", "L2": "d1R", "R1": "d1R"},
        ]

    events: list[tuple[str | None, str | None, str | None]] = []
    for moves in schedule:
        events.append(do_step(world, moves))

    return {
        "events": events,
        "nodes": nodes_vec(world),
        "signs": sign_vec(world),
        "stress": stress_vec(world),
        "mismatch": mismatch_vec(world),
    }


def print_events(label: str, events: list[tuple[str | None, str | None, str | None]]) -> None:
    print(label)
    for i, (node, kind, face) in enumerate(events, start=1):
        print(f"  step {i}: node={node} kind={kind} face={face}")


def compare_case(
    label: str,
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
) -> None:
    bundled = run_bundled_route(start_node, sign, stress, mismatch)
    split = run_split_route(start_node, sign, stress, mismatch)

    print("\n====================")
    print(f"CASE: {label}")
    print("====================")
    print(f"start_node          = {start_node}")
    print(f"initial_signs       = {(sign, sign, sign)}")
    print(f"initial_stress      = {stress}")
    print(f"initial_mismatch    = {mismatch}")

    print_events("bundled route events", bundled["events"])  # type: ignore[arg-type]
    print_events("split route events", split["events"])      # type: ignore[arg-type]

    print("\nend state comparison")
    print(f"  bundled_nodes     = {bundled['nodes']}")
    print(f"  split_nodes       = {split['nodes']}")
    print(f"  bundled_signs     = {bundled['signs']}")
    print(f"  split_signs       = {split['signs']}")
    print(f"  bundled_stress    = {bundled['stress']}")
    print(f"  split_stress      = {split['stress']}")
    print(f"  bundled_mismatch  = {bundled['mismatch']}")
    print(f"  split_mismatch    = {split['mismatch']}")
    print(f"  delta_stress      = {sub_vec(split['stress'], bundled['stress'])}")      # type: ignore[arg-type]
    print(f"  delta_mismatch    = {sub_vec(split['mismatch'], bundled['mismatch'])}")  # type: ignore[arg-type]    

    same_nodes = bundled["nodes"] == split["nodes"]
    same_signs = bundled["signs"] == split["signs"]
    same_stress = bundled["stress"] == split["stress"]
    same_mismatch = bundled["mismatch"] == split["mismatch"]

    print("\nroute invariance check")
    print(f"  same_nodes        = {same_nodes}")
    print(f"  same_signs        = {same_signs}")
    print(f"  same_stress       = {same_stress}")
    print(f"  same_mismatch     = {same_mismatch}")


def main() -> None:
    print("\n====================")
    print("ROUTE COMPARISON PROBE")
    print("====================")
    print("Same start state, same end hub, different admissible histories. Compare bundled rail vs split route.")

    cases = [
        ("u1R_clean_locked", "u1R", "+", (8, 8, 8), (4, 4, 4)),
        ("u1R_with_defect", "u1R", "+", (9, 8, 10), (5, 4, 6)),
        ("d1R_clean_locked", "d1R", "-", (8, 8, 8), (4, 4, 4)),
        ("d1R_with_defect", "d1R", "-", (9, 8, 10), (5, 4, 6)),
    ]

    for case in cases:
        compare_case(*case)


if __name__ == "__main__":
    main()
