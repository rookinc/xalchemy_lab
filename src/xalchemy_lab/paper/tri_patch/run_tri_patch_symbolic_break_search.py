from __future__ import annotations

from itertools import product

from xalchemy_lab.run_tri_patch_global_bridge_table import local_holonomy_data

PRIMITIVES = [
    "hold_all",
    "advance_L1",
    "advance_L2",
    "advance_R1",
    "advance_L1_L2",
    "advance_L1_R1",
    "advance_L2_R1",
    "advance_L1_L2_R1",
]


def local_lift_bit_for_word(word: tuple[str, ...]) -> int:
    hol = local_holonomy_data(
        start_node="u1R",
        sign="+",
        stress=(0, 0, 0),
        mismatch=(0, 0, 0),
        word=word,
    )
    return int(hol["lift_bit"])


def symbolic_parity_guess(word: tuple[str, ...]) -> int:
    odd_routes = {"hold_all", "advance_L1_R1", "advance_L2_R1"}
    return sum(1 for r in word if r in odd_routes) % 2


def main() -> None:
    print("\n====================")
    print("SYSTEMATIC SYMBOLIC BREAK SEARCH")
    print("====================\n")

    checked = 0
    mismatches: list[tuple[tuple[str, ...], int, int]] = []

    for n in (1, 2, 3, 4, 5):
        print(f"WORD LENGTH {n}")
        for word in product(PRIMITIVES, repeat=n):
            local_bit = local_lift_bit_for_word(word)
            symbolic_bit = symbolic_parity_guess(word)
            checked += 1

            if local_bit != symbolic_bit:
                mismatches.append((word, local_bit, symbolic_bit))
                print(f"MISMATCH word={word} local={local_bit} symbolic={symbolic_bit}")
                break

        if mismatches:
            break

        print("  no mismatches\n")

    print(f"checked = {checked}")
    print(f"mismatches = {len(mismatches)}")

    if mismatches:
        print("\nFirst mismatch:")
        word, local_bit, symbolic_bit = mismatches[0]
        print(f"  word         = {word}")
        print(f"  local_bit    = {local_bit}")
        print(f"  symbolic_bit = {symbolic_bit}")
    else:
        print("\nNo mismatches found up to length 5.")


if __name__ == "__main__":
    main()
