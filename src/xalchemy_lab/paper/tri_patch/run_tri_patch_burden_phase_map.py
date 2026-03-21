from __future__ import annotations

from itertools import product
from typing import Dict, Iterable, List, Tuple

from xalchemy_lab.tri_patch_core import HUB_SIGN, World, Turtle, apply_collision


SIGNS = ["+", "-"]
MISMATCH_VALUES = [0, 1, 2]
STRESS_VALUES = [0, 1, 2]


def make_world(
    node: str,
    signs: Dict[str, str],
    mismatches: Dict[str, int],
    stress: Dict[str, int],
) -> World:
    world = World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=node),
            "L2": Turtle(name="L2", chirality="L", node=node),
            "R1": Turtle(name="R1", chirality="R", node=node),
        }
    )
    for name, turtle in world.turtles.items():
        turtle.carry_sign = signs[name]
        turtle.mismatch_count = mismatches[name]
        turtle.carried_stress = stress[name]
    return world


def burden_for(node: str, signs: Dict[str, str], mismatches: Dict[str, int]) -> int:
    hub_sign = HUB_SIGN[node]
    sign_penalty = sum(1 for s in signs.values() if s != hub_sign)
    mismatch_burden = sum(mismatches.values())
    return sign_penalty + mismatch_burden


def signature(signs: Dict[str, str]) -> str:
    return "".join(signs[name] for name in ("L1", "L2", "R1"))


def run_case(
    node: str,
    signs: Dict[str, str],
    mismatches: Dict[str, int],
    stress: Dict[str, int],
) -> Tuple[str, int, int]:
    world = make_world(node=node, signs=signs, mismatches=mismatches, stress=stress)
    apply_collision(world, node, ["L1", "L2", "R1"])
    event = world.collisions[-1]
    total_stress = sum(stress.values())
    burden = burden_for(node, signs, mismatches)
    return event.face_event, burden, total_stress


def all_sign_patterns() -> Iterable[Dict[str, str]]:
    for vals in product(SIGNS, repeat=3):
        yield {"L1": vals[0], "L2": vals[1], "R1": vals[2]}


def all_mismatch_patterns() -> Iterable[Dict[str, int]]:
    for vals in product(MISMATCH_VALUES, repeat=3):
        yield {"L1": vals[0], "L2": vals[1], "R1": vals[2]}


def all_stress_patterns() -> Iterable[Dict[str, int]]:
    for vals in product(STRESS_VALUES, repeat=3):
        yield {"L1": vals[0], "L2": vals[1], "R1": vals[2]}


def print_summary_for_node(node: str) -> None:
    print("\n====================")
    print(f"BURDEN PHASE MAP @ {node}")
    print("====================")

    rows: List[Tuple[str, int, int, str, Dict[str, int], Dict[str, int]]] = []

    for signs in all_sign_patterns():
        for mismatches in all_mismatch_patterns():
            for stress in all_stress_patterns():
                face_event, burden, total_stress = run_case(
                    node=node,
                    signs=signs,
                    mismatches=mismatches,
                    stress=stress,
                )
                rows.append(
                    (
                        signature(signs),
                        burden,
                        total_stress,
                        face_event,
                        mismatches,
                        stress,
                    )
                )

    rows.sort(key=lambda r: (r[0], r[1], r[2], r[3]))

    current_sig = None
    current_burden = None
    current_stress = None
    bucket: List[Tuple[str, int, int, str, Dict[str, int], Dict[str, int]]] = []

    def flush_bucket(bucket_rows: List[Tuple[str, int, int, str, Dict[str, int], Dict[str, int]]]) -> None:
        if not bucket_rows:
            return

        sign_sig, burden, total_stress, _, _, _ = bucket_rows[0]
        face_classes = sorted({r[3] for r in bucket_rows})

        print(f"\nsigns={sign_sig} burden={burden} total_stress={total_stress}")
        print(f"  closure_classes={face_classes}")

        examples = bucket_rows[:3]
        for _, _, _, face_event, mismatches, stress in examples:
            print(
                f"  example mismatch={mismatches} stress={stress} -> {face_event}"
            )

        if len(bucket_rows) > 3:
            print(f"  ... {len(bucket_rows) - 3} more examples")

    for row in rows:
        sign_sig, burden, total_stress, _, _, _ = row
        key = (sign_sig, burden, total_stress)

        if (current_sig, current_burden, current_stress) != key:
            flush_bucket(bucket)
            bucket = []
            current_sig, current_burden, current_stress = key

        bucket.append(row)

    flush_bucket(bucket)


def print_transition_summary(node: str) -> None:
    print("\n====================")
    print(f"TRANSITION SUMMARY @ {node}")
    print("====================")

    summary: Dict[Tuple[str, int, int], Dict[str, int]] = {}

    for signs in all_sign_patterns():
        for mismatches in all_mismatch_patterns():
            for stress in all_stress_patterns():
                face_event, burden, total_stress = run_case(
                    node=node,
                    signs=signs,
                    mismatches=mismatches,
                    stress=stress,
                )
                key = (signature(signs), burden, total_stress)
                summary.setdefault(key, {})
                summary[key][face_event] = summary[key].get(face_event, 0) + 1

    for key in sorted(summary):
        sign_sig, burden, total_stress = key
        counts = summary[key]
        print(
            f"signs={sign_sig} burden={burden} total_stress={total_stress} "
            f"counts={counts}"
        )


def main() -> None:
    print_summary_for_node("u1R")
    print_transition_summary("u1R")

    print_summary_for_node("d1R")
    print_transition_summary("d1R")


if __name__ == "__main__":
    main()
