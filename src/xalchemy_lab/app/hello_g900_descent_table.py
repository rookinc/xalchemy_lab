from __future__ import annotations

import json
from pathlib import Path


INVARIANT_PATH = Path("specs/paper/g60/g900_descent_invariants_v0_1.json")
WITNESS_PATH = Path("specs/paper/g60/g900_descent_witness_v0_1.json")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def expect_equal(label: str, actual, expected) -> None:
    if actual != expected:
        raise ValueError(
            f"{label} mismatch: actual={actual!r} expected={expected!r}"
        )


def bool_label(value: bool) -> str:
    return "PASS" if value else "PENDING"


def is_empty(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) == 0
    return False


def normalize_pointer(value: str) -> Path:
    if value.startswith("pending:"):
        value = value[len("pending:") :]
    return Path(value)


def pointer_exists(value) -> bool:
    if not isinstance(value, str) or is_empty(value):
        return False
    return normalize_pointer(value).exists()


def require_pointer_when_checked(
    checked: bool,
    value,
    label: str,
) -> None:
    if checked and is_empty(value):
        raise ValueError(
            f"{label} is marked checked but has no witness pointer"
        )


def require_existing_file_pointer(value: str, label: str) -> None:
    if not pointer_exists(value):
        raise FileNotFoundError(
            f"{label} pointer does not resolve to an existing file: {value!r}"
        )


def main() -> None:
    invariants = load_json(INVARIANT_PATH)
    witness = load_json(WITNESS_PATH)

    expect_equal("carrier", witness["carrier"]["type"], invariants["carrier"])
    expect_equal(
        "first_quotient",
        witness["first_quotient"]["type"],
        invariants["first_quotient"],
    )
    expect_equal(
        "second_quotient",
        witness["second_quotient"]["type"],
        invariants["second_quotient"],
    )
    expect_equal(
        "shared_center",
        witness["shared_center"]["value"],
        invariants["shared_center"],
    )
    expect_equal(
        "macro_contact",
        witness["macro_contact"]["value"],
        invariants["macro_contact"],
    )
    expect_equal(
        "macro_contact_factorization",
        witness["macro_contact"]["factorization"],
        invariants["macro_contact_factorization"],
    )

    parity_stable = witness["first_quotient"]["parity_stable"]
    parity_checked = witness["status"]["parity_checked"]
    collapse_checked = witness["status"]["collapse_checked"]
    center_checked = witness["status"]["center_checked"]
    macro_contact_checked = witness["status"]["macro_contact_checked"]

    require_pointer_when_checked(
        parity_checked,
        [
            witness["first_quotient"]["even_slice_support"],
            witness["first_quotient"]["odd_slice_support"],
            witness["first_quotient"]["parity_comparison"],
        ],
        "parity witness",
    )
    require_pointer_when_checked(
        collapse_checked,
        witness["second_quotient"]["collapse_map"],
        "collapse map",
    )
    require_pointer_when_checked(
        center_checked,
        witness["shared_center"]["witness"],
        "center witness",
    )
    require_pointer_when_checked(
        macro_contact_checked,
        witness["macro_contact"]["witness"],
        "macro witness",
    )

    even_slice_support = witness["first_quotient"]["even_slice_support"]
    odd_slice_support = witness["first_quotient"]["odd_slice_support"]
    parity_comparison = witness["first_quotient"]["parity_comparison"]
    collapse_map = witness["second_quotient"]["collapse_map"]
    center_witness = witness["shared_center"]["witness"]
    macro_witness = witness["macro_contact"]["witness"]

    require_existing_file_pointer(even_slice_support, "even slice support")
    require_existing_file_pointer(odd_slice_support, "odd slice support")
    require_existing_file_pointer(parity_comparison, "parity comparison")
    require_existing_file_pointer(collapse_map, "collapse map")
    require_existing_file_pointer(center_witness, "center witness")
    require_existing_file_pointer(macro_witness, "macro witness")

    print("\nG900 DESCENT TABLE")
    print("==================")
    print(f"carrier            : {invariants['carrier']}")
    print(f"first quotient     : {invariants['first_quotient']}")
    print(f"parity refinement  : {invariants['parity_refinement']}")
    print(f"second quotient    : {invariants['second_quotient']}")
    print(f"shared center      : {invariants['shared_center']}")
    print(
        f"macro contact      : {invariants['macro_contact']} = "
        f"{invariants['macro_contact_factorization'][0]} * "
        f"{invariants['macro_contact_factorization'][1]}"
    )

    print("\nCHECK STATUS")
    print("============")
    print(f"parity stable      : {'YES' if parity_stable else 'NO'}")
    print(f"parity checked     : {bool_label(parity_checked)}")
    print(f"collapse checked   : {bool_label(collapse_checked)}")
    print(f"center checked     : {bool_label(center_checked)}")
    print(f"macro checked      : {bool_label(macro_contact_checked)}")

    print("\nWITNESS POINTERS")
    print("================")
    print(f"even slice support : {even_slice_support}")
    print(f"odd slice support  : {odd_slice_support}")
    print(f"parity comparison  : {parity_comparison}")
    print(f"collapse map       : {collapse_map}")
    print(f"center witness     : {center_witness}")
    print(f"macro witness      : {macro_witness}")

    print("\nPOINTER STATUS")
    print("==============")
    print(f"even slice file    : {'FOUND' if pointer_exists(even_slice_support) else 'MISSING'}")
    print(f"odd slice file     : {'FOUND' if pointer_exists(odd_slice_support) else 'MISSING'}")
    print(f"parity file        : {'FOUND' if pointer_exists(parity_comparison) else 'MISSING'}")
    print(f"collapse file      : {'FOUND' if pointer_exists(collapse_map) else 'MISSING'}")
    print(f"center file        : {'FOUND' if pointer_exists(center_witness) else 'MISSING'}")
    print(f"macro file         : {'FOUND' if pointer_exists(macro_witness) else 'MISSING'}")

    print(f"\nread {INVARIANT_PATH}")
    print(f"read {WITNESS_PATH}")


if __name__ == "__main__":
    main()
