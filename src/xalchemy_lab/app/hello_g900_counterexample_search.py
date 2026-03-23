from __future__ import annotations

CANDIDATES = [
    {"top": 130, "rung": 145, "bottom": 160},
    {"top": 135, "rung": 145, "bottom": 155},
    {"top": 140, "rung": 144, "bottom": 150},
    {"top": 140, "rung": 146, "bottom": 150},
    {"top": 138, "rung": 145, "bottom": 152},
    {"top": 142, "rung": 145, "bottom": 148},
]


def midpoint(top: int, bottom: int) -> float:
    return (top + bottom) / 2


def main() -> None:
    print("\nG900 NONCENTERED COUNTEREXAMPLE SEARCH")
    print("======================================")
    print("Testing whether noncentered prism weights can preserve")
    print("the base edge law top + bottom = 290 while breaking midpoint balance.\n")

    survivors = []

    for cand in CANDIDATES:
        top = cand["top"]
        rung = cand["rung"]
        bottom = cand["bottom"]

        sum_ok = (top + bottom == 290)
        centered = (rung == midpoint(top, bottom))
        macro_match = (top + bottom == 290)

        print(f"candidate top={top}, rung={rung}, bottom={bottom}")
        print(f"  top + bottom = 290   : {sum_ok}")
        print(f"  macro match          : {macro_match}")
        print(f"  midpoint centered    : {centered}")

        if sum_ok and macro_match and not centered:
            survivors.append(cand)
            print("  status               : SURVIVES arithmetic constraints")
        else:
            print("  status               : rejected")
        print()

    print("SUMMARY")
    print("=======")
    print(f"noncentered survivors under arithmetic-only constraints: {len(survivors)}")
    for cand in survivors:
        print(f"  survivor: {cand}")

    print("\nINTERPRETATION")
    print("==============")
    if survivors:
        print("Arithmetic constraints alone do not force midpoint balance.")
        print("Any forcing theorem must use stronger structural assumptions.")
    else:
        print("Even arithmetic constraints eliminate all tested noncentered candidates.")
        print("Midpoint balance looks closer to forced.")


if __name__ == "__main__":
    main()
