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


def macro_index(cell) -> int:
    xs = [v[0] for v in cell.verts]
    return min(xs) % 3


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)

    layer_macro_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)

    for c in cells:
        layer = layer_index(c, n)
        macro = macro_index(c)
        layer_macro_counts[(layer, macro)] += 1

    layers = sorted({layer for layer, _ in layer_macro_counts})

    print("\nG900 MACRO PHASE AUDIT")
    print("======================")
    print(f"carrier order n      : {n}")

    all_match = True

    print("\nLAYER DOMINANCE")
    print("===============")
    for layer in layers:
        counts = {macro: layer_macro_counts[(layer, macro)] for macro in range(3)}
        dominant_macro = max(counts, key=counts.get)
        expected_macro = layer % 3
        match = dominant_macro == expected_macro
        all_match = all_match and match

        print(f"layer {layer}")
        print(f"  macro counts       : {counts}")
        print(f"  dominant macro     : {dominant_macro}")
        print(f"  expected layer mod3: {expected_macro}")
        print(f"  match              : {match}")

    print("\nVERDICT")
    print("=======")
    print(f"dominant macro = layer mod 3 : {all_match}")

    print("\nINTERPRETATION")
    print("==============")
    if all_match:
        print("The carrier exhibits an exact mod-3 rotating macro phase across barycentric layers.")
        print("This strongly supports deriving the prism's 3-part macro structure from carrier organization.")
    else:
        print("The carrier does not exhibit an exact mod-3 dominant macro phase on every layer.")
        print("The 3-part macro structure may still be present, but not in this simplest dominance form.")


if __name__ == "__main__":
    main()
