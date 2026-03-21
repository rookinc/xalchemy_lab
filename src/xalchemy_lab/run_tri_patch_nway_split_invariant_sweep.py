from __future__ import annotations

from itertools import product

from xalchemy_lab.tri_patch_core import World, Turtle, apply_collision


LANES = ("L1", "L2", "R1")


def make_world(node: str = "u1R") -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=node, carry_sign="+"),
            "L2": Turtle(name="L2", chirality="L", node=node, carry_sign="+"),
            "R1": Turtle(name="R1", chirality="R", node=node, carry_sign="+"),
        }
    )


def set_state(world: World, stress_triplet: tuple[int, int, int]) -> None:
    for name, s in zip(LANES, stress_triplet):
        t = world.turtles[name]
        t.carry_sign = "+"
        t.carried_stress = s
        t.mismatch_count = 0


def run_event(world: World, node: str = "u1R") -> tuple[tuple[int, int, int], tuple[int, int, int, int, int], str]:
    world.tick += 1
    apply_collision(world, node, list(LANES))
    stress_out = tuple(world.turtles[name].carried_stress for name in LANES)
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


def run_single(total: tuple[int, int, int]) -> tuple[tuple[int, int, int], tuple[int, int, int, int, int], str]:
    world = make_world()
    set_state(world, total)
    return run_event(world)


def run_sequence(parts: list[tuple[int, int, int]]) -> tuple[tuple[int, int, int], tuple[int, int, int, int, int], list[str]]:
    world = make_world()
    faces: list[str] = []
    stress_out = (0, 0, 0)
    ledger_out = (0, 0, 0, 0, 0)
    for part in parts:
        set_state(world, part)
        stress_out, ledger_out, face = run_event(world)
        faces.append(face)
    return stress_out, ledger_out, faces


def weak_compositions(total: tuple[int, int, int], n: int) -> list[list[tuple[int, int, int]]]:
    out: list[list[tuple[int, int, int]]] = []

    def rec(remaining: tuple[int, int, int], k: int, acc: list[tuple[int, int, int]]) -> None:
        if k == 1:
            out.append(acc + [remaining])
            return
        ranges = [range(remaining[i] + 1) for i in range(3)]
        for part in product(*ranges):
            new_remaining = tuple(remaining[i] - part[i] for i in range(3))
            rec(new_remaining, k - 1, acc + [part])

    rec(total, n, [])
    return out


def is_nontrivial_sequence(parts: list[tuple[int, int, int]]) -> bool:
    return all(part != (0, 0, 0) for part in parts)


def fmt_ledger(x: tuple[int, int, int, int, int]) -> str:
    return (
        f"(stress_energy={x[0]}, stored_tension={x[1]}, deposited={x[2]}, "
        f"clean={x[3]}, tension={x[4]})"
    )


def main() -> None:
    print("\n====================")
    print("N-WAY SPLIT INVARIANT SWEEP")
    print("====================")
    print("Domain: coherent +++ triads at u1R, zero mismatch.")
    print("Compare one-shot load vs n-way coherent decompositions with same total load.\n")

    totals = [
        (1, 1, 1),
        (2, 1, 0),
        (2, 2, 2),
        (3, 2, 1),
    ]

    for total in totals:
        single_stress, single_ledger, single_face = run_single(total)
        print(f"total load: {total}")
        print(f"  single final S = {single_stress}")
        print(f"  single final L = {fmt_ledger(single_ledger)}")
        print(f"  single face    = {single_face}")

        for n in (2, 3):
            seqs = [seq for seq in weak_compositions(total, n) if is_nontrivial_sequence(seq)]
            print(f"  {n}-way nonzero splits checked = {len(seqs)}")

            expected_delta = (-(n - 1), 0, 0, +(n - 1), 0)
            all_hit = True
            any_carrier_match = False
            any_ledger_match = False
            shown = 0

            for seq in seqs:
                split_stress, split_ledger, faces = run_sequence(seq)
                delta = tuple(split_ledger[i] - single_ledger[i] for i in range(5))
                carrier_match = split_stress == single_stress
                ledger_match = split_ledger == single_ledger
                any_carrier_match = any_carrier_match or carrier_match
                any_ledger_match = any_ledger_match or ledger_match
                if delta != expected_delta:
                    all_hit = False

                if shown < 3:
                    print(f"    split: {seq}")
                    print(f"      final S      = {split_stress}")
                    print(f"      final L      = {fmt_ledger(split_ledger)}")
                    print(f"      delta        = {delta}")
                    print(f"      faces        = {faces}")
                    print(f"      carrier_match={carrier_match} ledger_match={ledger_match}")
                    shown += 1

            print(f"    expected delta = {expected_delta}")
            print(f"    all hit?       = {all_hit}")
            print(f"    any carrier match? = {any_carrier_match}")
            print(f"    any ledger match?  = {any_ledger_match}")

        print()

    print("Ledger tuple = (stress_energy, stored_tension, deposited_stress, clean_closures, tension_closures)")


if __name__ == "__main__":
    main()
