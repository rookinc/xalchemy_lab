from __future__ import annotations

from xalchemy_lab.tri_patch_core import triad_burden, triad_closure_class

CASES = [
    {
        "name": "coherent_zero_mismatch",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
    },
    {
        "name": "coherent_low_mismatch",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 1, "L2": 0, "R1": 0},
    },
    {
        "name": "coherent_high_mismatch",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 2, "L2": 1, "R1": 2},
    },
    {
        "name": "mixed_sign_zero_mismatch",
        "node": "u1R",
        "incoming_signs": {"L1": "-", "L2": "+", "R1": "-"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
    },
    {
        "name": "mixed_sign_with_prior_mismatch",
        "node": "u1R",
        "incoming_signs": {"L1": "-", "L2": "+", "R1": "-"},
        "incoming_mismatch": {"L1": 2, "L2": 0, "R1": 1},
    },
    {
        "name": "coherent_with_stress_but_zero_mismatch",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "note": "stress not represented in closure_class gate; expected clean",
    },
    {
        "name": "negative_hub_coherent_zero_mismatch",
        "node": "d1R",
        "incoming_signs": {"L1": "-", "L2": "-", "R1": "-"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
    },
    {
        "name": "negative_hub_mixed_zero_mismatch",
        "node": "d1R",
        "incoming_signs": {"L1": "+", "L2": "-", "R1": "+"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
    },
]


def main() -> None:
    print("\n====================")
    print("TRIADIC CLOSURE TRUTH TABLE")
    print("====================")

    for case in CASES:
        node = case["node"]
        incoming_signs = case["incoming_signs"]
        incoming_mismatch = case["incoming_mismatch"]
        burden = triad_burden(node, incoming_signs, incoming_mismatch)
        closure = triad_closure_class(node, incoming_signs, incoming_mismatch)

        print(f"\ncase: {case['name']}")
        print(f"  node              = {node}")
        print(f"  incoming_signs    = {incoming_signs}")
        print(f"  incoming_mismatch = {incoming_mismatch}")
        print(f"  burden            = {burden}")
        print(f"  closure_class     = {closure}")
        if "note" in case:
            print(f"  note              = {case['note']}")


if __name__ == "__main__":
    main()
