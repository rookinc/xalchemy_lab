from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    data = {
        "name": "g900_descent_invariants",
        "version": "0.1",
        "carrier": "900-cell order-30 triangular subdivision",
        "first_quotient": "exact weighted triangular prism",
        "parity_refinement": "prism support stable in even and odd slices",
        "second_quotient": "exact weighted triangle",
        "shared_center": 145,
        "macro_contact": 290,
        "macro_contact_factorization": [2, 145],
    }

    out_path = Path("specs/paper/g60/g900_descent_invariants_v0_1.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    print("\nG900 DESCENT TABLE")
    print("==================")
    print(f"carrier            : {data['carrier']}")
    print(f"first quotient     : {data['first_quotient']}")
    print(f"parity refinement  : {data['parity_refinement']}")
    print(f"second quotient    : {data['second_quotient']}")
    print(f"shared center      : {data['shared_center']}")
    print(
        f"macro contact      : {data['macro_contact']} = "
        f"{data['macro_contact_factorization'][0]} * "
        f"{data['macro_contact_factorization'][1]}"
    )
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
