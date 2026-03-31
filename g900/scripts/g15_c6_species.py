from __future__ import annotations

from g15_graph import (
    edge_vector_from_support,
    recover_cycle_order,
    vertex_type,
    canonical_cycle_word,
    build_fundamental_cycle_basis,
)

def syndrome_from_x(A, x):
    bits = []
    for row in A:
        s = 0
        for a, b in zip(row, x):
            s ^= (a & b)
        bits.append(str(s))
    return "".join(bits)

if __name__ == "__main__":
    A = build_fundamental_cycle_basis()
    print(f"cycle_basis_rows={len(A)}")
