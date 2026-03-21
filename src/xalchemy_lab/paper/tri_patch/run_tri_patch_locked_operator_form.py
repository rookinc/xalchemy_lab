from __future__ import annotations


def vec_add(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def parity_injection(f: tuple[int, int, int]) -> tuple[int, int, int]:
    return (f[0] % 2, f[1] % 2, f[2] % 2)


def hub_hit(
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    one = (1, 1, 1)
    return vec_add(stress, one), vec_add(mismatch, one)


def return_loop(
    stress: tuple[int, int, int],
    mismatch: tuple[int, int, int],
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    two = (2, 2, 2)
    return vec_add(stress, two), vec_add(mismatch, two)


def defect_state(
    stress_offset: tuple[int, int, int],
    mismatch_offset: tuple[int, int, int],
    flip_counts: tuple[int, int, int],
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    flip_mismatch = parity_injection(flip_counts)
    total_mismatch = vec_add(mismatch_offset, flip_mismatch)
    return stress_offset, total_mismatch


def main() -> None:
    print("\n====================")
    print("LOCKED OPERATOR FORM")
    print("====================")
    print("Empirical operator summary for the signed tension-locked rail.\n")

    print("1) Native locked hub-hit operator")
    print("   (s, m) -> (s + (1,1,1), m + (1,1,1))\n")

    print("2) Native locked return-loop operator")
    print("   (s, m) -> (s + (2,2,2), m + (2,2,2))\n")

    print("3) Defect transport operator after re-lock")
    print("   (delta_s, delta_m) -> (delta_s, delta_m)\n")

    print("4) Flip-source parity injection")
    print("   f in Z^3  ->  f mod 2 in (Z2)^3  ->  injected mismatch defect\n")

    examples = [
        {
            "label": "pure stress defect on L1",
            "delta_s": (5, 0, 0),
            "delta_m": (0, 0, 0),
            "flip_counts": (0, 0, 0),
        },
        {
            "label": "pure mismatch defect on R1",
            "delta_s": (0, 0, 0),
            "delta_m": (0, 0, 3),
            "flip_counts": (0, 0, 0),
        },
        {
            "label": "one flip on L1",
            "delta_s": (0, 0, 0),
            "delta_m": (0, 0, 0),
            "flip_counts": (1, 0, 0),
        },
        {
            "label": "three flips on R1 plus stress on L2",
            "delta_s": (0, 2, 0),
            "delta_m": (0, 0, 0),
            "flip_counts": (0, 0, 3),
        },
        {
            "label": "two flips on L1 plus mismatch on L2",
            "delta_s": (0, 0, 0),
            "delta_m": (0, 4, 0),
            "flip_counts": (2, 0, 0),
        },
    ]

    for ex in examples:
        transported_ds, transported_dm = defect_state(
            ex["delta_s"],
            ex["delta_m"],
            ex["flip_counts"],
        )
        print(f"example: {ex['label']}")
        print(f"  raw stress defect      = {ex['delta_s']}")
        print(f"  raw mismatch defect    = {ex['delta_m']}")
        print(f"  flip counts            = {ex['flip_counts']}")
        print(f"  flip parity injection  = {parity_injection(ex['flip_counts'])}")
        print(f"  transported delta_s    = {transported_ds}")
        print(f"  transported delta_m    = {transported_dm}\n")

    print("5) Combined empirical operator")
    print("   Background rail:")
    print("     T_hub(s, m)  = (s + 1, m + 1)   componentwise")
    print("     T_loop(s, m) = (s + 2, m + 2)   componentwise\n")
    print("   Defect sector:")
    print("     D(delta_s, delta_m, f) = (delta_s, delta_m + (f mod 2))\n")
    print("   Evolved locked state with defects:")
    print("     state_n = background_n + transported_defect\n")


if __name__ == "__main__":
    main()
