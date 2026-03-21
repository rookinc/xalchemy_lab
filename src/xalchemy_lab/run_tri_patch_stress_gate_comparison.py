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
        "name": "coherent_m0_s111",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 1, "L2": 1, "R1": 1},
    },
    {
        "name": "coherent_m0_s333",
        "node": "u1R",
        "incoming_signs": {"L1": "+", "L2": "+", "R1": "+"},
        "incoming_mismatch": {"L1": 0, "L2": 0, "R1": 0},
        "incoming_stress": {"L1": 3, "L2": 3, "R1": 3},
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


def hub_flavor(node: str) -> str:
    if node.startswith("u1"):
        return "ABC+"
    if node.startswith("d1"):
        return "ABC-"
    return "bundle"


def closure_class_with_stress_gate(
    node: str,
    incoming_signs: dict[str, str | None],
    incoming_mismatch: dict[str, int],
    incoming_stress: dict[str, int],
    stress_threshold: int,
) -> str:
    base_burden = triad_burden(node, incoming_signs, incoming_mismatch)
    total_stress = sum(incoming_stress.values())
    extended_burden = base_burden + (1 if total_stress >= stress_threshold else 0)

    if extended_burden == 0:
        return f"{hub_flavor(node)}_closed"
    return f"{hub_flavor(node)}_tension"


def main() -> None:
    print("\n====================")
    print("STRESS GATE COMPARISON")
    print("====================")

    thresholds = [1, 3, 6]

    for case in CASES:
        node = case["node"]
        incoming_signs = case["incoming_signs"]
        incoming_mismatch = case["incoming_mismatch"]
        incoming_stress = case["incoming_stress"]

        base_burden = triad_burden(node, incoming_signs, incoming_mismatch)
        base_class = triad_closure_class(node, incoming_signs, incoming_mismatch)
        total_stress = sum(incoming_stress.values())

        print(f"\ncase: {case['name']}")
        print(f"  node              = {node}")
        print(f"  incoming_signs    = {incoming_signs}")
        print(f"  incoming_mismatch = {incoming_mismatch}")
        print(f"  incoming_stress   = {incoming_stress}")
        print(f"  total_stress      = {total_stress}")
        print(f"  base_burden       = {base_burden}")
        print(f"  current_law       = {base_class}")

        for k in thresholds:
            alt = closure_class_with_stress_gate(
                node=node,
                incoming_signs=incoming_signs,
                incoming_mismatch=incoming_mismatch,
                incoming_stress=incoming_stress,
                stress_threshold=k,
            )
            print(f"  stress_gate(k={k}) = {alt}")


if __name__ == "__main__":
    main()
