from __future__ import annotations

from copy import deepcopy

from xalchemy_lab.tri_patch_core import World, Turtle, apply_collision


def make_world(node: str = "u1R") -> World:
    world = World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=node, carry_sign="+"),
            "L2": Turtle(name="L2", chirality="L", node=node, carry_sign="+"),
            "R1": Turtle(name="R1", chirality="R", node=node, carry_sign="+"),
        }
    )
    return world


def set_state(world: World, stress_triplet: tuple[int, int, int], mismatch_triplet: tuple[int, int, int]) -> None:
    for name, s, m in zip(("L1", "L2", "R1"), stress_triplet, mismatch_triplet):
        world.turtles[name].carried_stress = s
        world.turtles[name].mismatch_count = m


def run_event(world: World) -> tuple[tuple[int, int, int], tuple[int, int, int, int, int]]:
    world.tick += 1
    apply_collision(world, "u1R", ["L1", "L2", "R1"])
    stress_out = tuple(world.turtles[name].carried_stress for name in ("L1", "L2", "R1"))
    ledger = world.hub_ledger["u1R"]
    ledger_tuple = (
        ledger.stress_energy,
        ledger.stored_tension,
        ledger.deposited_stress,
        ledger.clean_closures,
        ledger.tension_closures,
    )
    return stress_out, ledger_tuple


def run_single(stress_triplet: tuple[int, int, int]) -> tuple[tuple[int, int, int], tuple[int, int, int, int, int]]:
    world = make_world()
    set_state(world, stress_triplet, (0, 0, 0))
    return run_event(world)


def run_split(
    first_triplet: tuple[int, int, int],
    second_triplet: tuple[int, int, int],
) -> tuple[
    tuple[int, int, int],
    tuple[int, int, int, int, int],
    tuple[int, int, int],
    tuple[int, int, int, int, int],
]:
    world = make_world()
    set_state(world, first_triplet, (0, 0, 0))
    mid_stress, mid_ledger = run_event(world)

    set_state(world, second_triplet, (0, 0, 0))
    final_stress, final_ledger = run_event(world)
    return mid_stress, mid_ledger, final_stress, final_ledger


def fmt_ledger(x: tuple[int, int, int, int, int]) -> str:
    return (
        f"(stress_energy={x[0]}, stored_tension={x[1]}, deposited={x[2]}, "
        f"clean={x[3]}, tension={x[4]})"
    )


def main() -> None:
    print("\n====================")
    print("LEDGER ADDITIVITY PROBE")
    print("====================")

    cases = [
        {
            "name": "equal_split_222_vs_111_111",
            "single": (2, 2, 2),
            "split_a": (1, 1, 1),
            "split_b": (1, 1, 1),
        },
        {
            "name": "boundary_split_321_vs_210_111",
            "single": (3, 2, 1),
            "split_a": (2, 1, 0),
            "split_b": (1, 1, 1),
        },
        {
            "name": "asymmetric_split_420_vs_210_210",
            "single": (4, 2, 0),
            "split_a": (2, 1, 0),
            "split_b": (2, 1, 0),
        },
    ]

    for case in cases:
        print(f"\ncase: {case['name']}")
        print(f"  single input      = {case['single']}")
        print(f"  split inputs      = {case['split_a']} then {case['split_b']}")

        single_stress, single_ledger = run_single(case["single"])
        mid_stress, mid_ledger, split_stress, split_ledger = run_split(case["split_a"], case["split_b"])

        print(f"  single final S    = {single_stress}")
        print(f"  single final L    = {fmt_ledger(single_ledger)}")

        print(f"  split mid S       = {mid_stress}")
        print(f"  split mid L       = {fmt_ledger(mid_ledger)}")
        print(f"  split final S     = {split_stress}")
        print(f"  split final L     = {fmt_ledger(split_ledger)}")

        print(f"  carrier matches   = {single_stress == split_stress}")
        print(f"  ledger matches    = {single_ledger == split_ledger}")

        delta = tuple(b - a for a, b in zip(single_ledger, split_ledger))
        print(f"  ledger delta      = {delta}")


if __name__ == "__main__":
    main()
