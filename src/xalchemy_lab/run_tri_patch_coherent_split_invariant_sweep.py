from __future__ import annotations

from itertools import product

from xalchemy_lab.tri_patch_core import World, Turtle, apply_collision


def make_world(node: str = "u1R") -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=node, carry_sign="+"),
            "L2": Turtle(name="L2", chirality="L", node=node, carry_sign="+"),
            "R1": Turtle(name="R1", chirality="R", node=node, carry_sign="+"),
        }
    )


def set_state(
    world: World,
    stress_triplet: tuple[int, int, int],
    mismatch_triplet: tuple[int, int, int] = (0, 0, 0),
) -> None:
    for name, s, m in zip(("L1", "L2", "R1"), stress_triplet, mismatch_triplet):
        t = world.turtles[name]
        t.carried_stress = s
        t.mismatch_count = m
        t.carry_sign = "+"


def run_event(world: World, node: str = "u1R") -> tuple[tuple[int, int, int], tuple[int, int, int, int, int], str]:
    world.tick += 1
    apply_collision(world, node, ["L1", "L2", "R1"])
    stress_out = tuple(world.turtles[name].carried_stress for name in ("L1", "L2", "R1"))
    ledger = world.hub_ledger[node]
    ledger_tuple = (
        ledger.stress_energy,
        ledger.stored_tension,
        ledger.deposited_stress,
        ledger.clean_closures,
        ledger.tension_closures,
    )
    face = world.collisions[-1].face_event if world.collisions else "none"
    return stress_out, ledger_tuple, face


def run_single(
    total_triplet: tuple[int, int, int],
) -> tuple[tuple[int, int, int], tuple[int, int, int, int, int], str]:
    world = make_world()
    set_state(world, total_triplet)
    return run_event(world)


def run_split(
    first_triplet: tuple[int, int, int],
    second_triplet: tuple[int, int, int],
) -> tuple[
    tuple[int, int, int],
    tuple[int, int, int, int, int],
    str,
    tuple[int, int, int],
    tuple[int, int, int, int, int],
    str,
]:
    world = make_world()
    set_state(world, first_triplet)
    _, _, face_a = run_event(world)

    set_state(world, second_triplet)
    final_stress, final_ledger, face_b = run_event(world)

    return (
        final_stress,
        final_ledger,
        face_a,
        final_stress,
        final_ledger,
        face_b,
    )


def fmt_ledger(x: tuple[int, int, int, int, int]) -> str:
    return (
        f"(stress_energy={x[0]}, stored_tension={x[1]}, deposited={x[2]}, "
        f"clean={x[3]}, tension={x[4]})"
    )


def compositions_for_total(total: tuple[int, int, int]) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    out: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
    ranges = [range(n + 1) for n in total]
    for a in product(*ranges):
        b = tuple(total[i] - a[i] for i in range(3))
        out.append((a, b))
    return out


def main() -> None:
    print("\n====================")
    print("COHERENT SPLIT INVARIANT SWEEP")
    print("====================")
    print("Test domain: coherent +++ triads at u1R, zero mismatch.")
    print("Compare one-event load against two-event decompositions with the same total load.")
    print("Candidate split law: delta = (-1, 0, 0, +1, 0) on the ledger.\n")

    totals = [
        (1, 1, 1),
        (2, 1, 0),
        (2, 2, 2),
        (3, 2, 1),
        (4, 2, 0),
        (3, 3, 3),
    ]

    target_delta = (-1, 0, 0, 1, 0)

    for total in totals:
        print(f"total load: {total}")
        single_stress, single_ledger, single_face = run_single(total)
        print(f"  single final S   = {single_stress}")
        print(f"  single final L   = {fmt_ledger(single_ledger)}")
        print(f"  single face      = {single_face}")

        rows = []
        for a, b in compositions_for_total(total):
            split_stress, split_ledger, face_a, _, _, face_b = run_split(a, b)
            delta = tuple(split_ledger[i] - single_ledger[i] for i in range(5))
            carrier_match = split_stress == single_stress
            ledger_match = split_ledger == single_ledger
            hits_target = delta == target_delta
            rows.append((a, b, split_stress, split_ledger, delta, carrier_match, ledger_match, hits_target, face_a, face_b))

        interesting = [r for r in rows if r[0] != (0, 0, 0) and r[1] != (0, 0, 0)]

        all_target = all(r[7] for r in interesting)
        any_carrier_match = any(r[5] for r in interesting)
        any_ledger_match = any(r[6] for r in interesting)

        print(f"  nontrivial splits checked = {len(interesting)}")
        print(f"  all delta == {target_delta}? {all_target}")
        print(f"  any carrier match?        {any_carrier_match}")
        print(f"  any ledger match?         {any_ledger_match}")

        print("  sample splits:")
        shown = 0
        for a, b, split_stress, split_ledger, delta, carrier_match, ledger_match, hits_target, face_a, face_b in interesting:
            print(f"    {a} then {b}")
            print(f"      split final S = {split_stress}")
            print(f"      split final L = {fmt_ledger(split_ledger)}")
            print(f"      delta         = {delta}")
            print(f"      faces         = {face_a}, {face_b}")
            print(f"      carrier_match={carrier_match} ledger_match={ledger_match} target_delta={hits_target}")
            shown += 1
            if shown >= 4:
                break
        print()

    print("Legend:")
    print("  ledger tuple = (stress_energy, stored_tension, deposited_stress, clean_closures, tension_closures)")
    print("  target delta = split minus single = (-1, 0, 0, +1, 0)")


if __name__ == "__main__":
    main()
