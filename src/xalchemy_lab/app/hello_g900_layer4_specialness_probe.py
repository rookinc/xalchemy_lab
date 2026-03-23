from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


Edge = Tuple[Tuple[int, int], Tuple[int, int]]


def edge_key(a: Tuple[int, int], b: Tuple[int, int]) -> Edge:
    return tuple(sorted((a, b)))


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

    layer_counts: DefaultDict[int, int] = defaultdict(int)
    layer_macro_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)
    layer_bit_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)

    edge_to_cells: DefaultDict[Edge, List[int]] = defaultdict(list)
    for idx, c in enumerate(cells):
        layer = layer_index(c, n)
        bit = bit_index(c)
        macro = layer % 3

        layer_counts[layer] += 1
        layer_macro_counts[(layer, macro)] += 1
        layer_bit_counts[(layer, bit)] += 1

        v = c.verts
        for e in [edge_key(v[0], v[1]), edge_key(v[1], v[2]), edge_key(v[2], v[0])]:
            edge_to_cells[e].append(idx)

    layer_pair_counts: DefaultDict[Tuple[int, int], int] = defaultdict(int)
    layer4_incident_counts: DefaultDict[int, int] = defaultdict(int)

    for incident in edge_to_cells.values():
        if len(incident) != 2:
            continue
        a = cells[incident[0]]
        b = cells[incident[1]]
        if tuple(sorted((bit_index(a), bit_index(b)))) != (0, 1):
            continue

        la = layer_index(a, n)
        lb = layer_index(b, n)
        pair = tuple(sorted((la, lb)))
        layer_pair_counts[pair] += 1

        if 4 in pair:
            other = pair[1] if pair[0] == 4 else pair[0]
            layer4_incident_counts[other] += 1

    print("\nG900 LAYER 4 SPECIALNESS PROBE")
    print("==============================")
    print("Testing whether barycentric layer 4 looks structurally distinguished.")
    print("Known clue: affine scale 49.5 = 99/2, and layer 4 has population 99.")

    print("\nLAYER 4 BASICS")
    print("==============")
    print(f"layer 4 population        : {layer_counts[4]}")
    print(f"layer 4 / 2              : {layer_counts[4] / 2}")

    print("\nMACRO PHASE ON LAYER 4")
    print("======================")
    for macro in range(3):
        print(f"macro {macro} count        : {layer_macro_counts[(4, macro)]}")
    dominant_macro = max(range(3), key=lambda m: layer_macro_counts[(4, m)])
    print(f"dominant macro            : {dominant_macro}")
    print(f"expected 4 mod 3          : {4 % 3}")
    print(f"phase match               : {dominant_macro == (4 % 3)}")

    print("\nBIT SPLIT ON LAYER 4")
    print("====================")
    print(f"bit 0 count               : {layer_bit_counts[(4, 0)]}")
    print(f"bit 1 count               : {layer_bit_counts[(4, 1)]}")
    print(
        f"bit difference            : "
        f"{layer_bit_counts[(4, 0)] - layer_bit_counts[(4, 1)]}"
    )

    print("\nLAYER-PAIR EDGE CONTACTS INVOLVING 4")
    print("====================================")
    for other, count in sorted(layer4_incident_counts.items()):
        print(f"layer pair (4,{other})     : {count}")

    print("\nALL LAYER-PAIR COUNTS (TOP 20)")
    print("==============================")
    for pair, count in sorted(layer_pair_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:20]:
        print(f"{pair}                    : {count}")

    print("\nINTERPRETATION")
    print("==============")
    print("Layer 4 would look especially meaningful if it is not only population-special")
    print("but also sits at a transition in phase, bit balance, or cross-layer contact.")
    print("The next question is whether layer 4 is the last fully outer shell before the")
    print("midpoint layer 5 in a way that explains why its half-population sets the affine scale.")


if __name__ == "__main__":
    main()
