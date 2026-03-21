#!/usr/bin/env python3
"""
BRIDGE-READY HARNESS FOR ACTUAL SIGNED LOOPS

Current purpose:
- reuse the exact local bridge words already established in
  run_tri_patch_global_bridge_table.py
- compute local lift_bit honestly from the current local rule
- keep a clean seam where actual signed-lift loop representatives
  and actual global Z2 values can later be inserted

This script is intentionally narrow.
It does not fake the missing signed-lift layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from xalchemy_lab.run_tri_patch_global_bridge_table import (
    LOCAL_WORDS,
    BRIDGE_PAIRS,
)


@dataclass
class LiftState:
    lift_bit: int = 0


def maybe_toggle_lift_bit(state: LiftState, route_name: str) -> None:
    """
    Current invariant local rule:

        lift_bit = 1 on:
            - hold_all
            - advance_L1_R1
            - advance_L2_R1

        lift_bit = 0 on all other currently named primitive routes
    """
    if route_name in {"hold_all", "advance_L1_R1", "advance_L2_R1"}:
        state.lift_bit ^= 1


def compute_local_lift_bit(word_routes: Iterable[str]) -> int:
    state = LiftState()
    for route_name in word_routes:
        maybe_toggle_lift_bit(state, route_name)
    return state.lift_bit


def load_actual_global_loops():
    """
    TODO:
    Replace this with actual signed-lift loop representatives
    from the Thalean / signed-lift side.

    Expected eventual shape:
        {
            "global_square": {...},
            "global_twist":  {...},
            "global_return": {...},
        }
    """
    return {
        "global_square": None,
        "global_twist": None,
        "global_return": None,
    }


def compute_global_loop_parity(loop_repr) -> int | None:
    """
    TODO:
    Given an actual signed-lift loop representative, return its true Z2 parity.

    Returning None for now keeps the boundary honest.
    """
    if loop_repr is None:
        return None
    raise NotImplementedError("Actual signed-lift loop parity not yet wired.")


def main() -> None:
    loops = load_actual_global_loops()

    print("\n====================")
    print("BRIDGE-READY ACTUAL SIGNED LOOP HARNESS")
    print("====================")
    print("Status: local side wired, global signed-lift side still pending.\n")

    for local_name, global_name in BRIDGE_PAIRS:
        word_routes = LOCAL_WORDS[local_name]
        local_lift_bit = compute_local_lift_bit(word_routes)
        global_loop = loops.get(global_name)
        global_parity = compute_global_loop_parity(global_loop)

        print(f"local={local_name:12s} <-> global={global_name}")
        print(f"  routes         = {word_routes}")
        print(f"  local_lift_bit = {local_lift_bit}")
        print(f"  global_loop    = {global_loop}")
        print(f"  global_parity  = {global_parity}")
        if global_parity is None:
            print(f"  match          = PENDING_ACTUAL_SIGNED_LIFT")
        else:
            print(f"  match          = {local_lift_bit == global_parity}")
        print()

    print("Next required ingredient:")
    print("  actual signed-lift loop representatives + actual Z2 parity evaluator")
    print()


if __name__ == "__main__":
    main()
