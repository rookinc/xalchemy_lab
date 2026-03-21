from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


CASES = [
    ("u1R_clean_locked", "u1R", "+", (8, 8, 8), (4, 4, 4)),
    ("u1R_with_defect", "u1R", "+", (9, 8, 10), (5, 4, 6)),
    ("d1R_clean_locked", "d1R", "-", (8, 8, 8), (4, 4, 4)),
    ("d1R_with_defect", "d1R", "-", (9, 8, 10), (5, 4, 6)),
]

ROUTES = [
    ("bundled_all", ("L1", "L2", "R1")),
    ("split_LR_hold_L2", ("L1", "R1")),
    ("split_LL_hold_R1", ("L1", "L2")),
    ("singleton_L1_only", ("L1",)),
    ("singleton_L2_only", ("L2",)),
    ("singleton_R1_only", ("R1",)),
]


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


def sub_vec(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def do_step(world: World, moves: dict[str, str]) -> tuple[str | None, str | None, str | None]:
    before = len(world.collisions)
    step(world, moves)
    if len(world.collisions) == before:
        return None, None, None
    c = world.collisions[-1]
    return c.node, c.kind, c.face_event


def run_route(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    advancers: tuple[str, ...],
) -> dict[str, object]:
    world = make_world(start_node, sign, stress, mismatch)

    if start_node == "u1R":
        first_hub = "u1R"
        opposite_hub = "d1R"
    else:
        first_hub = "d1R"
        opposite_hub = "u1R"

    events: list[tuple[str | None, str | None, str | None]] = []

    events.append(do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub}))
    events.append(do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"}))

    middle_moves = {}
    for name in ("L1", "L2", "R1"):
        middle_moves[name] = opposite_hub if name in advancers else "mR"
    events.append(do_step(world, middle_moves))

    events.append(do_step(world, {"L1": "mR", "L2": "mR", "R1": "mR"}))
    events.append(do_step(world, {"L1": first_hub, "L2": first_hub, "R1": first_hub}))

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
) -> list[tuple[tuple[int, int, int], tuple[int, int, int], str]]:
    bundled = run_route(start_node, sign, stress, mismatch, ("L1", "L2", "R1"))
    holonomy_rows: list[tuple[tuple[int, int, int], tuple[int, int, int], str]] = []

    print("\n====================")
    print(f"CASE: {label}")
    print("====================")
    print(f"start_node          = {start_node}")
    print(f"initial_signs       = {(sign, sign, sign)}")
    print(f"initial_stress      = {stress}")
    print(f"initial_mismatch    = {mismatch}")

    for route_label, advancers in ROUTES:
        result = run_route(start_node, sign, stress, mismatch, advancers)
        delta_s = sub_vec(result["stress"], bundled["stress"])        # type: ignore[arg-type]
        delta_m = sub_vec(result["mismatch"], bundled["mismatch"])    # type: ignore[arg-type]

        same_nodes = result["nodes"] == bundled["nodes"]
        same_signs = result["signs"] == bundled["signs"]

        holonomy_rows.append((delta_s, delta_m, f"{label}:{route_label}"))

        print(f"\n  route              = {route_label}")
        print(f"    advancers        = {advancers}")
        print(f"    final_nodes      = {result['nodes']}")
        print(f"    final_signs      = {result['signs']}")
        print(f"    final_stress     = {result['stress']}")
        print(f"    final_mismatch   = {result['mismatch']}")
        print(f"    delta_stress     = {delta_s}")
        print(f"    delta_mismatch   = {delta_m}")
        print(f"    same_nodes       = {same_nodes}")
        print(f"    same_signs       = {same_signs}")
        print(f"    middle_event     = {result['events'][2]}")

    return holonomy_rows


def main() -> None:
    print("\n====================")
    print("HOLONOMY CLASS MAP")
    print("====================")
    print("Compare admissible middle-route patterns against bundled transport and bucket correction vectors.\n")

    class_buckets: dict[tuple[tuple[int, int, int], tuple[int, int, int]], list[str]] = {}

    for case in CASES:
        rows = compare_case(*case)
        for delta_s, delta_m, member in rows:
            key = (delta_s, delta_m)
            class_buckets.setdefault(key, []).append(member)

    print("\n====================")
    print("HOLONOMY CLASSES")
    print("====================")
    for idx, (key, members) in enumerate(
        sorted(class_buckets.items(), key=lambda kv: (kv[0][0], kv[0][1])),
        start=1,
    ):
        ds, dm = key
        print(f"\nclass {idx}")
        print(f"  delta_stress       = {ds}")
        print(f"  delta_mismatch     = {dm}")
        print("  members:")
        for member in members:
            print(f"    - {member}")


if __name__ == "__main__":
    main()
