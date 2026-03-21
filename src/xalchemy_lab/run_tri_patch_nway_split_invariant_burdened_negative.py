from __future__ import annotations

from itertools import product

from xalchemy_lab.tri_patch_core import World, Turtle, apply_collision


LANES = ("L1", "L2", "R1")


def make_world(node: str, signs: tuple[str, str, str]) -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=node, carry_sign=signs[0]),
            "L2": Turtle(name="L2", chirality="L", node=node, carry_sign=signs[1]),
            "R1": Turtle(name="R1", chirality="R", node=node, carry_sign=signs[2]),
        }
    )


def set_state(
    world: World,
    stress_triplet: tuple[int, int, int],
    mismatch_triplet: tuple[int, int, int],
    signs: tuple[str, str, str],
) -> None:
    for name, s, m, sign in zip(LANES, stress_triplet, mismatch_triplet, signs):
        t = world.turtles[name]
        t.carry_sign = sign
        t.carried_stress = s
        t.mismatch_count = m


def run_event(
    world: World,
    node: str,
) -> tuple[tuple[str, str, str], tuple[int, int, int], tuple[int, int, int], tuple[int, int, int, int, int], str]:
    world.tick += 1
    apply_collision(world, node, list(LANES))
    signs_out = tuple(world.turtles[name].carry_sign for name in LANES)
    stress_out = tuple(world.turtles[name].carried_stress for name in LANES)
    mismatch_out = tuple(world.turtles[name].mismatch_count for name in LANES)
    ledger = world.hub_ledger[node]
    ledger_tuple = (
        ledger.stress_energy,
        ledger.stored_tension,
        ledger.deposited_stress,
        ledger.clean_closures,
        ledger.tension_closures,
    )
    face = world.collisions[-1].face_event if world.collisions else "none"
    return signs_out, stress_out, mismatch_out, ledger_tuple, face


def run_single(
    node: str,
    signs: tuple[str, str, str],
    total: tuple[int, int, int],
    mismatch: tuple[int, int, int],
) -> tuple[tuple[str, str, str], tuple[int, int, int], tuple[int, int, int], tuple[int, int, int, int, int], str]:
    world = make_world(node, signs)
    set_state(world, total, mismatch, signs)
    return run_event(world, node)


def run_sequence(
    node: str,
    signs: tuple[str, str, str],
    parts: list[tuple[int, int, int]],
    mismatch: tuple[int, int, int],
) -> tuple[
    tuple[str, str, str],
    tuple[int, int, int],
    tuple[int, int, int],
    tuple[int, int, int, int, int],
    list[str],
]:
    world = make_world(node, signs)
    faces: list[str] = []
    signs_out = signs
    stress_out = (0, 0, 0)
    mismatch_out = mismatch
    ledger_out = (0, 0, 0, 0, 0)

    for part in parts:
        set_state(world, part, mismatch_out, signs_out)
        signs_out, stress_out, mismatch_out, ledger_out, face = run_event(world, node)
        faces.append(face)

    return signs_out, stress_out, mismatch_out, ledger_out, faces


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


def burden(signs: tuple[str, str, str], mismatch: tuple[int, int, int], node: str) -> int:
    coherent = ("+", "+", "+") if node == "u1R" else ("-", "-", "-")
    sign_burden = sum(1 for a, b in zip(signs, coherent) if a != b)
    return sign_burden + sum(mismatch)


def main() -> None:
    print("\n====================")
    print("N-WAY SPLIT INVARIANT SWEEP (BURDENED NEGATIVE)")
    print("====================")
    print("Probe whether the burdened split law is polarity-symmetric at d1R.\n")

    cases = [
        {
            "name": "coherent_negative_positive_mismatch",
            "node": "d1R",
            "signs": ("-", "-", "-"),
            "mismatch": (1, 0, 0),
            "totals": [(1, 1, 1), (2, 2, 2)],
        },
        {
            "name": "mixed_zero_mismatch_negative_hub",
            "node": "d1R",
            "signs": ("+", "-", "+"),
            "mismatch": (0, 0, 0),
            "totals": [(1, 1, 1), (2, 2, 2)],
        },
        {
            "name": "mixed_positive_mismatch_negative_hub",
            "node": "d1R",
            "signs": ("+", "-", "+"),
            "mismatch": (1, 0, 1),
            "totals": [(1, 1, 1), (2, 2, 2)],
        },
    ]

    for case in cases:
        name = case["name"]
        node = case["node"]
        signs = case["signs"]
        mismatch = case["mismatch"]

        print(f"case family: {name}")
        print(f"  node      = {node}")
        print(f"  signs     = {signs}")
        print(f"  mismatch  = {mismatch}")
        print(f"  burden    = {burden(signs, mismatch, node)}")

        for total in case["totals"]:
            single_signs, single_stress, single_mismatch, single_ledger, single_face = run_single(
                node=node,
                signs=signs,
                total=total,
                mismatch=mismatch,
            )
            print(f"\n  total load: {total}")
            print(f"    single final signs = {single_signs}")
            print(f"    single final S     = {single_stress}")
            print(f"    single final M     = {single_mismatch}")
            print(f"    single final L     = {fmt_ledger(single_ledger)}")
            print(f"    single face        = {single_face}")

            for n in (2, 3):
                seqs = [seq for seq in weak_compositions(total, n) if is_nontrivial_sequence(seq)]
                expected_burdened_delta = ((n - 1), (n - 1), 0, 0, (n - 1))
                print(f"    {n}-way nonzero splits checked = {len(seqs)}")
                print(f"    burdened target delta          = {expected_burdened_delta}")

                all_hit_burdened_delta = True
                any_ledger_match = False
                any_state_match = False
                shown = 0

                for seq in seqs:
                    split_signs, split_stress, split_mismatch, split_ledger, faces = run_sequence(
                        node=node,
                        signs=signs,
                        parts=seq,
                        mismatch=mismatch,
                    )

                    delta = tuple(split_ledger[i] - single_ledger[i] for i in range(5))
                    ledger_match = split_ledger == single_ledger
                    state_match = (
                        split_signs == single_signs
                        and split_stress == single_stress
                        and split_mismatch == single_mismatch
                    )

                    if delta != expected_burdened_delta:
                        all_hit_burdened_delta = False
                    if ledger_match:
                        any_ledger_match = True
                    if state_match:
                        any_state_match = True

                    if shown < 3:
                        print(f"      split: {seq}")
                        print(f"        final signs   = {split_signs}")
                        print(f"        final S       = {split_stress}")
                        print(f"        final M       = {split_mismatch}")
                        print(f"        final L       = {fmt_ledger(split_ledger)}")
                        print(f"        delta         = {delta}")
                        print(f"        faces         = {faces}")
                        print(f"        state_match={state_match} ledger_match={ledger_match}")
                        shown += 1

                print(f"      all hit burdened target? {all_hit_burdened_delta}")
                print(f"      any state match?         {any_state_match}")
                print(f"      any ledger match?        {any_ledger_match}")

        print("\n" + "-" * 72 + "\n")


if __name__ == "__main__":
    main()
