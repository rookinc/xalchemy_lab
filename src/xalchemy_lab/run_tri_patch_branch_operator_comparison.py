from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


def make_world(
    node: str,
    signs: tuple[str, str, str],
    mismatch: tuple[int, int, int],
    stress: tuple[int, int, int],
) -> World:
    return World(
        turtles={
            "L1": Turtle(
                name="L1",
                chirality="L",
                node=node,
                carry_sign=signs[0],  # type: ignore[arg-type]
                mismatch_count=mismatch[0],
                carried_stress=stress[0],
            ),
            "L2": Turtle(
                name="L2",
                chirality="L",
                node=node,
                carry_sign=signs[1],  # type: ignore[arg-type]
                mismatch_count=mismatch[1],
                carried_stress=stress[1],
            ),
            "R1": Turtle(
                name="R1",
                chirality="R",
                node=node,
                carry_sign=signs[2],  # type: ignore[arg-type]
                mismatch_count=mismatch[2],
                carried_stress=stress[2],
            ),
        }
    )


def run_case(
    label: str,
    node: str,
    signs: tuple[str, str, str],
    mismatch: tuple[int, int, int],
    stress: tuple[int, int, int],
    export_node: str,
) -> None:
    world = make_world(node=node, signs=signs, mismatch=mismatch, stress=stress)

    incoming_signs = {name: world.turtles[name].carry_sign for name in ("L1", "L2", "R1")}
    incoming_mismatch = {name: world.turtles[name].mismatch_count for name in ("L1", "L2", "R1")}
    incoming_stress = {name: world.turtles[name].carried_stress for name in ("L1", "L2", "R1")}

    step(world, {"L1": node, "L2": node, "R1": node})
    closure = world.collisions[-1]

    after_closure_signs = {name: world.turtles[name].carry_sign for name in ("L1", "L2", "R1")}
    after_closure_mismatch = {name: world.turtles[name].mismatch_count for name in ("L1", "L2", "R1")}
    after_closure_stress = {name: world.turtles[name].carried_stress for name in ("L1", "L2", "R1")}

    step(world, {"L1": export_node, "L2": export_node, "R1": export_node})
    export = world.collisions[-1]

    after_export_stress = {name: world.turtles[name].carried_stress for name in ("L1", "L2", "R1")}
    ledger = world.hub_ledger[node]  # type: ignore[index]

    delta_stress = {
        name: after_closure_stress[name] - incoming_stress[name]
        for name in ("L1", "L2", "R1")
    }
    delta_mismatch = {
        name: after_closure_mismatch[name] - incoming_mismatch[name]
        for name in ("L1", "L2", "R1")
    }

    print(f"\ncase: {label}")
    print(f"  node                 = {node}")
    print(f"  incoming_signs       = {incoming_signs}")
    print(f"  incoming_mismatch    = {incoming_mismatch}")
    print(f"  incoming_stress      = {incoming_stress}")
    print(f"  closure_class        = {closure.face_event}")
    print(f"  closure_out_signs    = {after_closure_signs}")
    print(f"  closure_out_mismatch = {after_closure_mismatch}")
    print(f"  closure_out_stress   = {after_closure_stress}")
    print(f"  delta_mismatch       = {delta_mismatch}")
    print(f"  delta_stress         = {delta_stress}")
    print(f"  export_face          = {export.face_event}")
    print(f"  export_out_stress    = {after_export_stress}")
    print(f"  deposited_stress     = {ledger.deposited_stress}")
    print(f"  stress_energy        = {ledger.stress_energy}")
    print(f"  stored_tension       = {ledger.stored_tension}")
    print(f"  tension_closures     = {ledger.tension_closures}")
    print(f"  clean_closures       = {ledger.clean_closures}")


def main() -> None:
    print("\n====================")
    print("BRANCH OPERATOR COMPARISON")
    print("====================")

    # Clean coherent closure: same sign, zero burden, nontrivial stress profile.
    run_case(
        label="clean_closed_coherent",
        node="u1R",
        signs=("+", "+", "+"),
        mismatch=(0, 0, 0),
        stress=(4, 2, 1),
        export_node="mR",
    )

    # Tension by coherent prior burden: same sign, nonzero burden.
    run_case(
        label="tension_coherent_prior_burden",
        node="u1R",
        signs=("+", "+", "+"),
        mismatch=(1, 0, 0),
        stress=(4, 2, 1),
        export_node="mR",
    )

    # Tension by mixed-sign burden with zero prior mismatch.
    run_case(
        label="tension_mixed_sign_zero_prior_mismatch",
        node="u1R",
        signs=("-", "+", "-"),
        mismatch=(0, 0, 0),
        stress=(4, 2, 1),
        export_node="mR",
    )

    # Negative-hub comparison.
    run_case(
        label="negative_hub_tension_mixed_sign",
        node="d1R",
        signs=("+", "-", "+"),
        mismatch=(0, 0, 0),
        stress=(4, 2, 1),
        export_node="mR",
    )


if __name__ == "__main__":
    main()
