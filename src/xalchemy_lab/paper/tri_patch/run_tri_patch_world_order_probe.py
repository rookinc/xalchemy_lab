from __future__ import annotations

from copy import deepcopy

from xalchemy_lab.tri_patch_core import World, Turtle, apply_collision


def make_world(hub: str, sign: str, stress_triplet: tuple[int, int, int]) -> World:
    world = World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node=hub, carry_sign=sign),
            "L2": Turtle(name="L2", chirality="L", node=hub, carry_sign=sign),
            "R1": Turtle(name="R1", chirality="R", node=hub, carry_sign=sign),
        }
    )
    for name, stress in zip(["L1", "L2", "R1"], stress_triplet):
        t = world.turtles[name]
        t.carried_stress = stress
        t.mismatch_count = 0
        t.seen_nodes = [hub]
    return world


def snapshot(world: World, hub: str) -> dict:
    ledger = world.hub_ledger[hub]
    return {
        "stress": tuple(world.turtles[n].carried_stress for n in ["L1", "L2", "R1"]),
        "signs": tuple(world.turtles[n].carry_sign for n in ["L1", "L2", "R1"]),
        "mismatch": tuple(world.turtles[n].mismatch_count for n in ["L1", "L2", "R1"]),
        "ledger": (
            ledger.stress_energy,
            ledger.stored_tension,
            ledger.deposited_stress,
            ledger.clean_closures,
            ledger.tension_closures,
        ),
        "face": world.collisions[-1].face_event if world.collisions else None,
    }


def force_clean(world: World, hub: str) -> None:
    for t in world.turtles.values():
        t.carry_sign = "+" if hub.startswith("u1") else "-"
        t.mismatch_count = 0
    apply_collision(world, hub, ["L1", "L2", "R1"])


def force_tension(world: World, hub: str) -> None:
    hub_sign = "+" if hub.startswith("u1") else "-"
    off_sign = "-" if hub_sign == "+" else "+"
    world.turtles["L1"].carry_sign = off_sign
    world.turtles["L2"].carry_sign = hub_sign
    world.turtles["R1"].carry_sign = off_sign
    world.turtles["L1"].mismatch_count = 0
    world.turtles["L2"].mismatch_count = 0
    world.turtles["R1"].mismatch_count = 0
    apply_collision(world, hub, ["L1", "L2", "R1"])


def run_case(label: str, stress_triplet: tuple[int, int, int], hub: str = "u1R") -> None:
    sign = "+" if hub.startswith("u1") else "-"

    world_ct = make_world(hub, sign, stress_triplet)
    force_clean(world_ct, hub)
    after_clean = snapshot(world_ct, hub)
    force_tension(world_ct, hub)
    after_ct = snapshot(world_ct, hub)

    world_tc = make_world(hub, sign, stress_triplet)
    force_tension(world_tc, hub)
    after_tension = snapshot(world_tc, hub)
    force_clean(world_tc, hub)
    after_tc = snapshot(world_tc, hub)

    print("")
    print(f"case: {label}")
    print(f"  start stress        = {stress_triplet}")
    print(f"  clean -> tension    = {after_ct['stress']}")
    print(f"  tension -> clean    = {after_tc['stress']}")
    print(f"  same final stress   = {after_ct['stress'] == after_tc['stress']}")
    print(f"  after clean         = {after_clean['stress']}  face={after_clean['face']}")
    print(f"  after tension       = {after_tension['stress']}  face={after_tension['face']}")
    print(f"  ledger C->T         = {after_ct['ledger']}")
    print(f"  ledger T->C         = {after_tc['ledger']}")
    print(f"  same final ledger   = {after_ct['ledger'] == after_tc['ledger']}")


def main() -> None:
    print("\n====================")
    print("WORLD ORDER PROBE")
    print("====================")
    print("Compare two actual triadic hub event orders on the same starting stress.")
    print("Order A: clean then tension")
    print("Order B: tension then clean")

    cases = [
        ("s000", (0, 0, 0)),
        ("s100", (1, 0, 0)),
        ("s210", (2, 1, 0)),
        ("s321", (3, 2, 1)),
    ]

    for label, stress_triplet in cases:
        run_case(label, stress_triplet, hub="u1R")


if __name__ == "__main__":
    main()
