from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, Tuple

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


def layer_index(cell, n: int) -> int:
    vals = []
    for i, j in cell.verts:
        k = n - i - j
        vals.append(min(i, j, k))
    return min(vals)


def macro_index(cell) -> int:
    xs = [v[0] for v in cell.verts]
    return min(xs) % 3


def bit_index(cell) -> int:
    return 0 if cell.orient == "up" else 1


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)

    bucket_counts: DefaultDict[Tuple[int, int, int], int] = defaultdict(int)
    macro_bit_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)
    layer_macro_bit_counts: DefaultDict[Tuple[int, int, int], int] = defaultdict(int)

    for c in cells:
        layer = layer_index(c, n)
        macro = macro_index(c)
        bit = bit_index(c)

        bucket_counts[(layer, macro, bit)] += 1
        macro_bit_counts[(macro, bit)] += 1
        layer_macro_bit_counts[(layer, macro, bit)] += 1

    print("\nG900 CARRIER BUCKET SCAN")
    print("========================")
    print(f"total cells          : {len(cells)}")

    print("\nMACRO x BIT TOTALS")
    print("==================")
    for macro in range(3):
        for bit in range(2):
            print(f"({macro}, {bit})             : {macro_bit_counts[(macro, bit)]}")

    print("\nLAYER x MACRO x BIT")
    print("===================")
    for layer in sorted({k[0] for k in layer_macro_bit_counts}):
        print(f"\nlayer {layer}")
        for macro in range(3):
            row = []
            for bit in range(2):
                row.append(f"({macro},{bit})={layer_macro_bit_counts[(layer, macro, bit)]}")
            print("  " + "  ".join(row))

    print("\nINTERPRETATION")
    print("==============")
    print("This scan exposes the carrier bucket structure before any quotient claim.")
    print("The next question is whether these buckets collapse naturally to the 3x2 prism classes.")
