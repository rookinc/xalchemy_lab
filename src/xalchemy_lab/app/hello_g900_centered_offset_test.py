from __future__ import annotations

CANDIDATES = [
    {"top": 140, "rung": 145, "bottom": 150},
    {"top": 140, "rung": 144, "bottom": 150},
    {"top": 140, "rung": 146, "bottom": 150},
    {"top": 135, "rung": 145, "bottom": 155},
    {"top": 130, "rung": 145, "bottom": 160},
]


def main() -> None:
    print("\nG900 CENTERED OFFSET TEST")
    print("========================")
    print("Testing the structural rule that the rung is the true center class.\n")

    survivors = []

    for cand in CANDIDATES:
        top = cand["top"]
        rung = cand["rung"]
        bottom = cand["bottom"]

        base_ok = (top + bottom == 290)
        centered_offset = ((top - rung) + (bottom - rung) == 0)

        print(f"candidate top={top}, rung={rung}, bottom={bottom}")
        print(f"  base sum 290         : {base_ok}")
        print(f"  centered offset law  : {centered_offset}")

        if base_ok and centered_offset:
            survivors.append(cand)
            print("  status               : survives structural test")
        else:
            print("  status               : rejected")
        print()

    print("SUMMARY")
    print("=======")
    print(f"survivors under centered-offset structural rule: {len(survivors)}")
    for cand in survivors:
        print(f"  survivor: {cand}")

    print("\nINTERPRETATION")
    print("==============")
    if survivors:
        print("Centered-offset structure eliminates noncentered arithmetic survivors.")
        print("Midpoint balance is forced once the rung is treated as the true center class.")
    else:
        print("No candidates survived; check the candidate set or assumptions.")


if __name__ == "__main__":
    main()
