#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def cumulative(values: list[int]) -> list[int]:
    total = 0
    out: list[int] = []
    for value in values:
        total += value
        out.append(total)
    return out


def build_rows(
    occupancies: list[int],
    shell_caps: list[int],
    bulk_caps: list[int],
) -> list[dict]:
    rows: list[dict] = []

    for index, (occupancy, shell_capacity, bulk_capacity) in enumerate(
        zip(occupancies, shell_caps, bulk_caps)
    ):
        shell_density = (occupancy / shell_capacity) if shell_capacity else 0.0
        bulk_density = (occupancy / bulk_capacity) if bulk_capacity else 0.0
        density_difference = shell_density - bulk_density
        density_ratio = (shell_density / bulk_density) if bulk_density else None

        rows.append(
            {
                "index": index,
                "occupancy": occupancy,
                "shell_capacity": shell_capacity,
                "bulk_capacity": bulk_capacity,
                "shell_density": shell_density,
                "bulk_density": bulk_density,
                "density_difference": density_difference,
                "density_ratio": density_ratio,
                "notes": "",
            }
        )

    return rows


def main() -> None:
    model_id = "G900"
    run_id = "RUN_001"
    root_id = "ROOT_001"

    # First-light placeholder shell vector.
    # Replace this with a real shell vector from the sim when ready.
    occupancies = [1, 4, 8, 16, 24, 6, 1]

    # Basecamp first-pass choice:
    # empirical shell envelope = current shell occupancy for this run.
    shell_caps = occupancies[:]

    # cumulative observed occupancy through shell k
    bulk_caps = cumulative(occupancies)

    payload = {
        "experiment_id": "g900-shell-bulk-v1",
        "model_id": model_id,
        "run_id": run_id,
        "root_id": root_id,
        "index_mode": "shell",
        "shell_scale_definition": (
            "S_k = empirical shell envelope, currently set equal to observed "
            "shell occupancy for this first-light run"
        ),
        "bulk_scale_definition": "C_k = cumulative observed occupancy through shell k",
        "rows": build_rows(occupancies, shell_caps, bulk_caps),
    }

    out_dir = Path("specs/examples")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "g900-first-real-shell-bulk-payload.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
