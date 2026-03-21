from __future__ import annotations

from xalchemy_lab.tri_patch_core import triad_burden, triad_closure_class

CASES = [
    {
        "name": "coherent_m0_s000",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 0, "L2": 0, "R1": 0},
    },
    {
        "name": "coherent_m0_s100",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 1, "L2": 0, "R1": 0},
    },
    {
        "name": "coherent_m0_s110",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 1, "L2": 1, "R1": 0},
    },
    {
        "name": "coherent_m0_s111",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 1, "L2": 1, "R1": 1},
    },
    {
        "name": "coherent_m0_s222",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 2, "L2": 2, "R1": 2},
    },
    {
        "name": "coherent_m1_s000",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 1, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 0, "L2": 0, "R1": 0},
    },
    {
        "name": "coherent_m1_s111",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 1, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 1, "L2": 1, "R1": 1},
    },
    {
        "name": "coherent_m1_s333",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 1, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 3, "L2": 3, "R1": 3},
    },
    {
        "name": "mixed_m0_s000",
        "node": "u1R",
        "incoming_signs": {"L1": "-", "L2": "+", "R1": "-"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 0, "L2": 0, "R1": 0},
    },
    {
        "name": "mixed_m0_s111",
        "node": "u1R",
        "incoming_signs": {"L1": "-", "L2": "+", "R1": "-"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 1, "L2": 1, "R1": 1},
    },
    {
        "name": "mixed_m0_s333",
        "node": "u1R",
        "incoming_signs": {"L1": "-", "L2": "+", "R1": "-"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 3, "L2": 3, "R1": 3},
    },
]


def main() -> None:
    print("\n====================")
    print("STRESS GATE PROBE")
    print("====================")

    for case in CASES:
        node = case["node"]
        incoming_signs = case["incoming_signs"]
        incoming_mismatch = case["incoming_mismatch"]
        incoming_stress = case["incoming_stress"]

        burden = triad_burden(node, incoming_signs, incoming_mismatch)
        closure = triad_closure_class(node, incoming_signs, incoming_mismatch)
        total_stress = sum(incoming_stress.values())

        print(f"\ncase: {case['name']}")
        print(f"  node              = {node}")
        print(f"  incoming_signs    = {incoming_signs}")
        print(f"  incoming_mismatch = {incoming_mismatch}")
        print(f"  incoming_stress   = {incoming_stress}")
        print(f"  total_stress      = {total_stress}")
        print(f"  burden            = {burden}")
        print(f"  closure_class     = {closure}")


if __name__ == "__main__":
    main()
