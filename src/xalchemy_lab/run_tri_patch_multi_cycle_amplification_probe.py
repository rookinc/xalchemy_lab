from __future__ import annotations

from xalchemy_lab.tri_patch_core import World, Turtle, step


SEEDS = [
    ("s000", (0, 0, 0)),
    ("s111", (1, 1, 1)),
    ("s300", (3, 0, 0)),
    ("s421", (4, 2, 1)),
    ("s444", (4, 4, 4)),
]

N_CYCLES = 6


def make_world(stress_vec: tuple[int, int, int]) -> World:
    return World(
        turtles={
            "L1": Turtle(name="L1", chirality="L", node="u1R", carry_sign="+", carried_stress=stress_vec[0]),
            "L2": Turtle(name="L2", chirality="L", node="u1R", carry_sign="+", carried_stress=stress_vec[1]),
            "R1": Turtle(name="R1", chirality="R", node="u1R", carry_sign="+", carried_stress=stress_vec[2]),
        }
    )


def stress_vec(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[name].carried_stress for name in ("L1", "L2", "R1"))


def sign_vec(world: World) -> tuple[str | None, str | None, str | None]:
    return tuple(world.turtles[name].carry_sign for name in ("L1", "L2", "R1"))


def mismatch_vec(world: World) -> tuple[int, int, int]:
    return tuple(world.turtles[name].mismatch_count for name in ("L1", "L2", "R1"))


def ledger_summary(world: World, hub: str) -> str:
    ledger = world.hub_ledger[hub]
    return (
        f"stress_energy={ledger.stress_energy} "
        f"stored_tension={ledger.stored_tension} "
        f"deposited={ledger.deposited_stress} "
        f"clean={ledger.clean_closures} "
        f"tension={ledger.tension_closures}"
    )


def full_cycle(world: World) -> dict[str, object]:
    # 1. close at u1R
    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    u1r_first = world.collisions[-1].face_event

    # 2. export to mR
    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    export_1 = world.collisions[-1].face_event

    # 3. close at d1R
    step(world, {"L1": "d1R", "L2": "d1R", "R1": "d1R"})
    d1r = world.collisions[-1].face_event

    # 4. export back through mR
    step(world, {"L1": "mR", "L2": "mR", "R1": "mR"})
    export_2 = world.collisions[-1].face_event

    # 5. return closure at u1R
    step(world, {"L1": "u1R", "L2": "u1R", "R1": "u1R"})
    u1r_return = world.collisions[-1].face_event

    return {
        "u1r_first": u1r_first,
        "export_1": export_1,
        "d1r": d1r,
        "export_2": export_2,
        "u1r_return": u1r_return,
        "stress": stress_vec(world),
        "signs": sign_vec(world),
        "mismatch": mismatch_vec(world),
        "u1r_ledger": ledger_summary(world, "u1R"),
        "d1r_ledger": ledger_summary(world, "d1R"),
    }


def run_seed(label: str, seed: tuple[int, int, int]) -> None:
    world = make_world(seed)

    print(f"\n====================")
    print(f"SEED: {label}")
    print(f"====================")
    print(f"initial_stress   = {stress_vec(world)}")
    print(f"initial_signs    = {sign_vec(world)}")
    print(f"initial_mismatch = {mismatch_vec(world)}")
    print(f"u1R_ledger       = {ledger_summary(world, 'u1R')}")
    print(f"d1R_ledger       = {ledger_summary(world, 'd1R')}")

    for cycle in range(1, N_CYCLES + 1):
        result = full_cycle(world)
        print(f"\ncycle {cycle}")
        print(f"  u1R first       = {result['u1r_first']}")
        print(f"  export 1        = {result['export_1']}")
        print(f"  d1R             = {result['d1r']}")
        print(f"  export 2        = {result['export_2']}")
        print(f"  u1R return      = {result['u1r_return']}")
        print(f"  stress          = {result['stress']}")
        print(f"  signs           = {result['signs']}")
        print(f"  mismatch        = {result['mismatch']}")
        print(f"  u1R ledger      = {result['u1r_ledger']}")
        print(f"  d1R ledger      = {result['d1r_ledger']}")


def main() -> None:
    print("\n====================")
    print("MULTI-CYCLE AMPLIFICATION PROBE")
    print("====================")
    print("Repeated full loops:")
    print("u1R closure -> mR export -> d1R closure -> mR export -> u1R return")

    for label, seed in SEEDS:
        run_seed(label, seed)


if __name__ == "__main__":
    main()
