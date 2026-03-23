from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Tuple

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


def layer_index(cell, n: int) -> int:
    vals = []
    for i, j in cell.verts:
        k = n - i - j
        vals.append(min(i, j, k))
    return min(vals)


def bit_index(cell) -> int:
    return 0 if cell.orient == "up" else 1


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)

    quotient_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)
    layer_quotient_counts: DefaultDict[Tuple[int, int, int], int] = defaultdict(int)

    for c in cells:
        layer = layer_index(c, n)
        macro = layer % 3
        bit = bit_index(c)

        quotient_counts[(macro, bit)] += 1
        layer_quotient_counts[(layer, macro, bit)] += 1

    print("\nG900 CANDIDATE QUOTIENT MAP")
    print("===========================")
    print("rule: prism macro = layer mod 3, prism bit = orientation bit")
    print(f"total cells          : {len(cells)}")

    print("\nQUOTIENT CLASS TOTALS")
    print("=====================")
    for macro in range(3):
        for bit in range(2):
            print(f"({macro}, {bit})             : {quotient_counts[(macro, bit)]}")

    print("\nLAYER CONTRIBUTIONS")
    print("===================")
    for layer in range(10):
        macro = layer % 3
        row = []
        for bit in range(2):
            row.append(f"({macro},{bit})={layer_quotient_counts[(layer, macro, bit)]}")
        print(f"layer {layer} -> " + "  ".join(row))

    print("\nINTERPRETATION")
    print("==============")
    print("This is the first direct carrier-to-prism candidate map.")
    print("It uses only carrier-derived layer phase and the orientation bit.")
    print("The next question is whether this six-way collapse matches the weighted prism support in a meaningful way.")


if __name__ == "__main__":
    main()
