from __future__ import annotations

from dataclasses import dataclass

from xalchemy_lab.tri_patch_core import World, Turtle, step


@dataclass
class ProbeRow:
    route_name: str
    advancers: tuple[str, ...]
    middle_event: tuple[str | None, str | None, str | None]
    is_sign_transfer: int
    predicted_by_route_only: int
    match: bool


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

CHIRALITY = {
    "L1": "L",
    "L2": "L",
    "R1": "R",
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


def do_step(world: World, moves: dict[str, str]) -> tuple[str | None, str | None, str | None]:
    before = len(world.collisions)
    step(world, moves)
    if len(world.collisions) == before:
        return None, None, None
    c = world.collisions[-1]
    return c.node, c.kind, c.face_event


def run_middle_event(
    start_node: str,
    sign: str,
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
    advancers: tuple[str, ...],
) -> tuple[str | None, str | None, str | None]:
    world = make_world(start_node, sign, stress, mismatch)

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
    return do_step(world, middle_moves)


def route_only_predictor(advancers: tuple[str, ...]) -> int:
    # Candidate intrinsic rule:
    # sign_transfer occurs exactly for 2-advancer routes that contain the unique R-chiral carrier.
    if len(advancers) != 2:
        return 0
    n_r = sum(1 for name in advancers if CHIRALITY[name] == "R")
    return int(n_r == 1)


def describe_route(advancers: tuple[str, ...]) -> str:
    if not advancers:
        return "stall"
    ch = "".join(sorted(CHIRALITY[a] for a in advancers))
    return f"{len(advancers)}-advancer/{ch}"


def main() -> None:
    print("\n====================")
    print("SIGN-TRANSFER PREDICTOR PROBE")
    print("====================")
    print("Test whether LR sign-transfer can be recognized from primitive route structure alone, without using the face-event label.")

    for case_label, start_node, sign, stress, mismatch in BASE_CASES:
        print(f"\n====================")
        print(f"CASE: {case_label}")
        print("====================")

        rows: list[ProbeRow] = []
        for route_name, advancers in ROUTES.items():
            middle_event = run_middle_event(start_node, sign, stress, mismatch, advancers)
            node, kind, face = middle_event
            is_sign_transfer = int(kind == "LR" and face in {"sign_transfer+", "sign_transfer-"})
            predicted = route_only_predictor(advancers)
            rows.append(
                ProbeRow(
                    route_name=route_name,
                    advancers=advancers,
                    middle_event=middle_event,
                    is_sign_transfer=is_sign_transfer,
                    predicted_by_route_only=predicted,
                    match=(is_sign_transfer == predicted),
                )
            )

        all_ok = True
        for row in rows:
            all_ok = all_ok and row.match
            print(
                f"{row.route_name:20s} "
                f"advancers={row.advancers!s:16s} "
                f"type={describe_route(row.advancers):16s} "
                f"middle_event={row.middle_event!s:36s} "
                f"actual={row.is_sign_transfer} "
                f"pred={row.predicted_by_route_only} "
                f"match={row.match}"
            )

        print(f"\nall_routes_match_route_only_predictor = {all_ok}")
        print("\nsummary note")
        print("  If True, then LR sign-transfer is not an opaque engine label here; it is exactly the 2-advancer route containing the unique R-chiral carrier.")

    print("\nworking candidate")
    print("  sign_transfer predictor = 1 exactly for 2-advancer routes with chirality pattern LR.")


if __name__ == "__main__":
    main()
