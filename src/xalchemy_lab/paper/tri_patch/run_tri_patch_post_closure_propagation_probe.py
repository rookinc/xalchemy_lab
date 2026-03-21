from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List

from xalchemy_lab.tri_patch_core import World, Turtle, step


@dataclass
class ProbeCase:
    name: str
    initial_signs: Dict[str, str]
    initial_mismatch: Dict[str, int]
    initial_stress: Dict[str, int]
    scripted_steps: List[Dict[str, str]]


def print_state(label: str, world: World) -> None:
    print(f"\n{label}")
    print(f"tick={world.tick}")
    for name, t in sorted(world.turtles.items()):
        print(
            f"  {name}: node={t.node} sign={t.carry_sign} stress={t.carried_stress} "
            f"mismatch={t.mismatch_count} tokens={t.shared_tokens}"
        )
    if world.collisions:
        print("  collisions:")
        for c in world.collisions:
            print(
                f"    tick={c.tick} node={c.node} kind={c.kind} face={c.face_event} turtles={c.turtles}\n"
                f"      in_sign={c.incoming_signs} out_sign={c.outgoing_signs}\n"
                f"      in_stress={c.incoming_stress} out_stress={c.outgoing_stress}\n"
                f"      in_mismatch={c.incoming_mismatch} out_mismatch={c.outgoing_mismatch}"
            )
    print("  hub ledger:")
    for hub, ledger in sorted(world.hub_ledger.items()):
        print(
            f"    {hub}: stress_energy={ledger.stress_energy} stored_tension={ledger.stored_tension} "
            f"deposited={ledger.deposited_stress} clean={ledger.clean_closures} tension={ledger.tension_closures}"
        )


def make_closed_world(
    signs: Dict[str, str],
    mismatches: Dict[str, int],
    stress: Dict[str, int],
) -> World:
    """
    Build a world already sitting at a clean coherent triad on u1R so we can
    probe post-closure propagation while varying only transported stress.
    """
    world = World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node="u1R"),
            "L2": Turtle(name="L2", chirality="L", node="u1R"),
            "R1": Turtle(name="R1", chirality="R", node="u1R"),
        }
    )

    for name, turtle in world.turtles.items():
        turtle.carry_sign = signs[name]
        turtle.mismatch_count = mismatches[name]
        turtle.carried_stress = stress[name]

    return world


def summarize(world: World) -> None:
    print("\nsummary")
    print("-------")
    face_counts = Counter(c.face_event for c in world.collisions)
    node_counts = Counter(c.node for c in world.collisions)

    print(f"total_collisions={len(world.collisions)}")
    print(f"face_counts={dict(sorted(face_counts.items()))}")
    print(f"node_counts={dict(sorted(node_counts.items()))}")

    print("final turtles:")
    for name, t in sorted(world.turtles.items()):
        print(
            f"  {name}: node={t.node} sign={t.carry_sign} "
            f"stress={t.carried_stress} mismatch={t.mismatch_count}"
        )

    print("final hub ledger:")
    for hub, ledger in sorted(world.hub_ledger.items()):
        print(
            f"  {hub}: stress_energy={ledger.stress_energy} stored_tension={ledger.stored_tension} "
            f"deposited={ledger.deposited_stress} clean={ledger.clean_closures} tension={ledger.tension_closures}"
        )


def run_case(case: ProbeCase) -> None:
    print("\n====================")
    print(f"SCENARIO: {case.name}")
    print("====================")

    world = make_closed_world(
        signs=case.initial_signs,
        mismatches=case.initial_mismatch,
        stress=case.initial_stress,
    )
    print_state("initial (already assembled coherent triad on u1R)", world)

    # Tick 1: force the triad to close at u1R under the chosen incoming stress profile.
    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    print_state("after tick 1 (closure at u1R)", world)

    # Remaining scripted transport probes.
    for idx, moves in enumerate(case.scripted_steps, start=2):
        step(world, moves)
        print_state(f"after tick {idx}", world)

    summarize(world)


def main() -> None:
    # Hold closure class fixed: coherent + signs, zero mismatch.
    # Vary only incoming stress profile, then compare downstream histories.
    cases = [
        ProbeCase(
            name="post_closure_stress_000",
            initial_signs={"L1": "+", "L2": "+", "R1": "+"},
            initial_mismatch={"L1": 0, "L2": 0, "R1": 0},
            initial_stress={"L1": 0, "L2": 0, "R1": 0},
            scripted_steps=[
                {"L1": "mR", "L2": "mR", "R1": "mR"},
                {"L1": "d1R", "L2": "mL", "R1": "u1R"},
                {"L1": "mR", "L2": "u1L", "R1": "mR"},
                {"L1": "u1R", "L2": "u2L", "R1": "u1R"},
            ],
        ),
        ProbeCase(
            name="post_closure_stress_111",
            initial_signs={"L1": "+", "L2": "+", "R1": "+"},
            initial_mismatch={"L1": 0, "L2": 0, "R1": 0},
            initial_stress={"L1": 1, "L2": 1, "R1": 1},
            scripted_steps=[
                {"L1": "mR", "L2": "mR", "R1": "mR"},
                {"L1": "d1R", "L2": "mL", "R1": "u1R"},
                {"L1": "mR", "L2": "u1L", "R1": "mR"},
                {"L1": "u1R", "L2": "u2L", "R1": "u1R"},
            ],
        ),
        ProbeCase(
            name="post_closure_stress_222",
            initial_signs={"L1": "+", "L2": "+", "R1": "+"},
            initial_mismatch={"L1": 0, "L2": 0, "R1": 0},
            initial_stress={"L1": 2, "L2": 2, "R1": 2},
            scripted_steps=[
                {"L1": "mR", "L2": "mR", "R1": "mR"},
                {"L1": "d1R", "L2": "mL", "R1": "u1R"},
                {"L1": "mR", "L2": "u1L", "R1": "mR"},
                {"L1": "u1R", "L2": "u2L", "R1": "u1R"},
            ],
        ),
        ProbeCase(
            name="post_closure_stress_asymmetric_300",
            initial_signs={"L1": "+", "L2": "+", "R1": "+"},
            initial_mismatch={"L1": 0, "L2": 0, "R1": 0},
            initial_stress={"L1": 3, "L2": 0, "R1": 0},
            scripted_steps=[
                {"L1": "mR", "L2": "mR", "R1": "mR"},
                {"L1": "d1R", "L2": "mL", "R1": "u1R"},
                {"L1": "mR", "L2": "u1L", "R1": "mR"},
                {"L1": "u1R", "L2": "u2L", "R1": "u1R"},
            ],
        ),
    ]

    for case in cases:
        run_case(case)


if __name__ == "__main__":
    main()
