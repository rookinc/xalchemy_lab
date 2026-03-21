from __future__ import annotations


def clean(s: int) -> int:
    return max(s - 1, 0)


def tension(s: int) -> int:
    return s + 1


def apply_clean_triplet(stress: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(clean(x) for x in stress)


def apply_tension_triplet(stress: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(tension(x) for x in stress)


def fmt_triplet(x: tuple[int, int, int]) -> str:
    return f"({x[0]},{x[1]},{x[2]})"


def main() -> None:
    cases = [
        ("s000", (0, 0, 0)),
        ("s100", (1, 0, 0)),
        ("s010", (0, 1, 0)),
        ("s001", (0, 0, 1)),
        ("s110", (1, 1, 0)),
        ("s101", (1, 0, 1)),
        ("s011", (0, 1, 1)),
        ("s210", (2, 1, 0)),
        ("s200", (2, 0, 0)),
        ("s321", (3, 2, 1)),
    ]

    print("\n====================")
    print("OPERATOR ORDER PROBE")
    print("====================")
    print("C(s) = max(s-1, 0)")
    print("T(s) = s+1")
    print("Compare T(C(s)) against C(T(s)) componentwise on triplets.")

    for label, stress in cases:
        clean_then_tension = apply_tension_triplet(apply_clean_triplet(stress))
        tension_then_clean = apply_clean_triplet(apply_tension_triplet(stress))
        commutes = clean_then_tension == tension_then_clean
        delta = tuple(a - b for a, b in zip(clean_then_tension, tension_then_clean))

        print("")
        print(f"case: {label}")
        print(f"  in              = {fmt_triplet(stress)}")
        print(f"  C then T        = {fmt_triplet(clean_then_tension)}")
        print(f"  T then C        = {fmt_triplet(tension_then_clean)}")
        print(f"  commute         = {commutes}")
        print(f"  delta           = {fmt_triplet(delta)}")

    print("")
    print("Interpretation:")
    print("- Noncommutation should appear exactly on lanes that begin at zero.")
    print("- Positive lanes should commute under the pair (clean, tension).")


if __name__ == "__main__":
    main()
