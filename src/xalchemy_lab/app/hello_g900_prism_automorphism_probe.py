from __future__ import annotations

from itertools import permutations


NODES = [
    (0, 0),
    (1, 0),
    (2, 0),
    (0, 1),
    (1, 1),
    (2, 1),
]

WEIGHTS = {
    frozenset(((0, 0), (1, 0))): 140,
    frozenset(((0, 0), (2, 0))): 140,
    frozenset(((1, 0), (2, 0))): 140,

    frozenset(((0, 1), (1, 1))): 150,
    frozenset(((0, 1), (2, 1))): 150,
    frozenset(((1, 1), (2, 1))): 150,

    frozenset(((0, 0), (0, 1))): 145,
    frozenset(((1, 0), (1, 1))): 145,
    frozenset(((2, 0), (2, 1))): 145,
}


def edge_weight(a, b):
    return WEIGHTS.get(frozenset((a, b)), 0)


def is_weight_preserving(perm):
    mapping = {NODES[i]: NODES[perm[i]] for i in range(6)}
    for a in NODES:
        for b in NODES:
            if edge_weight(a, b) != edge_weight(mapping[a], mapping[b]):
                return False
    return True


def main():
    autos = []
    for perm in permutations(range(6)):
        if is_weight_preserving(perm):
            autos.append(perm)

    print("G900 WEIGHTED PRISM AUTOMORPHISM PROBE")
    print("======================================")
    print(f"node order = {NODES}")
    print(f"weight-preserving automorphism count = {len(autos)}")
    print("\nfirst 12 automorphisms")
    for perm in autos[:12]:
        print(f"  {perm}")


if __name__ == "__main__":
    main()
