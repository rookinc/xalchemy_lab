from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    summary = {
        "name": "g900_descent_summary_v0_1",
        "version": "0.1",
        "carrier": {
            "type": "order_30_triangular_subdivision",
            "cell_count": 900,
            "layer_count": 10,
            "macro_count": 3,
            "bit_count": 2,
            "macro_populations": {"0": 300, "1": 300, "2": 300},
            "bit_populations": {"0": 435, "1": 465},
            "macro_bit_populations": {
                "(0,0)": 145, "(0,1)": 155,
                "(1,0)": 145, "(1,1)": 155,
                "(2,0)": 145, "(2,1)": 155
            },
            "macro_contact_counts": {
                "(0,1)": 290, "(0,2)": 290, "(1,2)": 290
            }
        },
        "layer_structure": {
            "counts": [171, 153, 135, 117, 99, 81, 63, 45, 27, 9],
            "description": "10 inward layers with arithmetic descent by 18"
        },
        "prism_quotient": {
            "support_graph": "triangular_prism",
            "exact_support_match": True,
            "weighted_edge_law": {
                "bit0_face": 140,
                "macro_rung": 145,
                "bit1_face": 150
            },
            "center": 145,
            "centered_offsets": {
                "bit0_face": -5,
                "macro_rung": 0,
                "bit1_face": 5
            },
            "weight_preserving_automorphism_count": 6
        },
        "parity_refinement": {
            "even_prism": {
                "support_graph": "triangular_prism",
                "exact_support_match": True,
                "weighted_edge_law": {
                    "bit0_face": 160,
                    "macro_rung": 240,
                    "bit1_face": 320
                }
            },
            "odd_prism": {
                "support_graph": "triangular_prism",
                "exact_support_match": True,
                "weighted_edge_law": {
                    "bit0_face": 260,
                    "macro_rung": 195,
                    "bit1_face": 130
                }
            }
        },
        "triangle_descent": {
            "coarse_triangle_edge_weight": 290,
            "even_triangle_edge_weight": 160,
            "odd_triangle_edge_weight": 130,
            "triangle_support": "3_cycle",
            "coarse_equals_even_plus_odd": True
        },
        "shared_scalar_centers": {
            "population_center": 150,
            "prism_center": 145,
            "triangle_parity_center": 145,
            "macro_contact_center": 290
        },
        "descent_chain": [
            "900_cell_sampled_carrier",
            "6_class_weighted_prism",
            "3_node_weighted_triangle"
        ]
    }

    out = Path("specs/paper/g60/g900_descent_summary_v0_1.json")
    out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out}")

    print("\nG900 DESCENT SUMMARY")
    print("====================")
    print("carrier          : 900-cell order-30 triangular subdivision")
    print("first quotient   : exact weighted triangular prism")
    print("parity refinement: prism support stable in even and odd slices")
    print("second quotient  : exact weighted triangle")
    print("shared center    : 145")
    print("macro contact    : 290 = 2 * 145")


if __name__ == "__main__":
    main()
