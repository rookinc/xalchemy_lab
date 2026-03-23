from __future__ import annotations

from typing import Dict, List, Tuple

ClassNode = Tuple[int, int]
MacroNode = int


CLASS_NODES: List[ClassNode] = [
    (0, 0), (1, 0), (2, 0),
    (0, 1), (1, 1), (2, 1),
]

COARSE = [
    [0, 140, 140, 145, 0,   0],
    [140, 0, 140, 0,   145, 0],
    [140, 140, 0, 0,   0,   145],
    [145, 0,   0, 0,   150, 150],
    [0,   145, 0, 150, 0,   150],
    [0,   0,   145, 150, 150, 0],
]

EVEN = [
    [0, 55, 55, 80, 0, 0],
    [55, 0, 50, 0, 80, 0],
    [55, 50, 0, 0, 0, 80],
    [80, 0, 0, 0, 105, 105],
    [0, 80, 0, 105, 0, 110],
    [0, 0, 80, 105, 110, 0],
]

ODD = [
    [0, 85, 85, 65, 0, 0],
    [85, 0, 90, 0, 65, 0],
    [85, 90, 0, 0, 0, 65],
    [65, 0, 0, 0, 45, 45],
    [0, 65, 0, 45, 0, 40],
    [0, 0, 65, 45, 40, 0],
]


def collapse_rungs(weights: List[List[int]]) -> Dict[Tuple[MacroNode, MacroNode], int]:
    macro_edge_weights: Dict[Tuple[MacroNode, MacroNode], int] = {}

    for a in range(3):
        for b in range(a + 1, 3):
            total = 0
            # sum all class-to-class edges whose endpoints live in macro a and macro b
            for i, na in enumerate(CLASS_NODES):
                for j, nb in enumerate(CLASS_NODES):
                    if i < j and na[0] == a and nb[0] == b:
                        total += weights[i][j]
            macro_edge_weights[(a, b)] = total

    return macro_edge_weights


def print_triangle(name: str, weights: List[List[int]]) -> None:
    tri = collapse_rungs(weights)
    print(f"\n{name}")
    print("-" * len(name))
    for edge in sorted(tri):
        print(f"  {edge}: {tri[edge]}")

    vals = list(tri.values())
    print("  support = triangle")
    print(f"  min/max = {min(vals)} / {max(vals)}")


def main() -> None:
    print("G900 PRISM TO TRIANGLE DESCENT")
    print("=============================")
    print_triangle("COARSE", COARSE)
    print_triangle("EVEN", EVEN)
    print_triangle("ODD", ODD)


if __name__ == "__main__":
    main()
