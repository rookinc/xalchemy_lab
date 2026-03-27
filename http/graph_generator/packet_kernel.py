from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Literal

# Lazy universe:
# prefer one completed packet, reject stale branching, and stabilize into the
# smallest repeating chamber regime available.
#
# Current policy:
# - vertices lock pre-sheet
# - face chirality is assigned afterward
# - one-center packet uses structured phase-sensitive routing
# - shared packet supports collapsed / semistructured / structured+x-echo
# - canonical class labels expose local attractor behavior

Operator = Literal["x", "y", "z"]
Polarity = Literal["top", "bottom"]
Phase = Literal["t1", "t2", "t3"]
SharedMode = Literal["collapsed", "semistructured", "structured"]


@dataclass
class LockedCenter:
    key: str
    chamber_class: str
    shell: int
    bias: str = "paired"


@dataclass
class CandidateClass:
    key: tuple
    ops: set[Operator] = field(default_factory=set)
    sources: set[str] = field(default_factory=set)
    phases: set[Phase] = field(default_factory=set)
    visits: int = 0
    sheet_memory: Counter = field(default_factory=Counter)
    locked: bool = False

    def register(
        self,
        op: Operator,
        source: str,
        phase: Phase,
        polarity: Polarity,
    ) -> None:
        self.ops.add(op)
        self.sources.add(source)
        self.phases.add(phase)
        self.visits = len(self.phases)
        self.sheet_memory[polarity] += 1

    def packet_complete(self) -> bool:
        return self.ops == {"x", "y", "z"}

    def bias_label(self) -> str:
        top = self.sheet_memory["top"]
        bottom = self.sheet_memory["bottom"]
        if top > bottom:
            return "top"
        if bottom > top:
            return "bottom"
        return "paired"


@dataclass
class Face:
    key: str
    verts: tuple[str, str, str]
    order: tuple[Operator, Operator, Operator]
    polarity: Polarity

    def sign(self) -> str:
        positive = {
            ("x", "y", "z"),
            ("y", "z", "x"),
            ("z", "x", "y"),
        }
        orientation = 1 if self.order in positive else -1
        closure = 1 if self.polarity == "top" else -1
        return "+" if orientation * closure > 0 else "-"


def operator_polarity(op: Operator) -> Polarity:
    return "bottom" if op == "z" else "top"


def routed_direction(op: Operator, phase: Phase, inherited_direction: str) -> str:
    if phase == "t1":
        return {
            "x": "L",
            "y": "C",
            "z": "R",
        }[op]

    if phase == "t2":
        return {
            "x": inherited_direction,
            "y": inherited_direction,
            "z": "C",
        }[op]

    return {
        "x": inherited_direction,
        "y": inherited_direction,
        "z": inherited_direction,
    }[op]


def candidate_key(
    center: LockedCenter,
    phase: Phase,
    op: Operator,
    inherited_direction: str,
) -> tuple:
    direction = routed_direction(op, phase, inherited_direction)
    shell = center.shell + {"t1": 1, "t2": 2, "t3": 2}[phase]
    return (center.key, shell, direction)


def shared_candidate_key(
    centers: list[LockedCenter],
    phase: Phase,
    op: Operator,
    inherited_direction: str,
    mode: SharedMode = "collapsed",
) -> tuple:
    source_class = tuple(sorted(c.chamber_class for c in centers))

    if mode == "collapsed":
        shell = min(c.shell for c in centers) + 2
        direction = inherited_direction
        return (shell, direction, source_class)

    if mode == "semistructured":
        shell = min(c.shell for c in centers) + 2
        direction = inherited_direction
        return (shell, direction, source_class)

    shell = min(c.shell for c in centers) + {"t1": 1, "t2": 2, "t3": 2}[phase]
    direction = routed_direction(op, phase, inherited_direction)
    return (shell, direction, source_class)


def should_reject(c: CandidateClass, decision_window: int = 3) -> bool:
    return (not c.locked) and c.visits >= decision_window and not c.packet_complete()


def promote_class(c: CandidateClass) -> str:
    key = c.key
    bias = c.bias_label()

    if len(key) == 3 and isinstance(key[0], str):
        _, shell, direction = key
        return f"K_{direction}_{shell}_{bias}"

    shell, direction, _family = key
    return f"K_{direction}_{shell}_{bias}"


def local_face_fan(center: LockedCenter) -> list[Face]:
    if center.chamber_class.startswith("K_C"):
        return [
            Face("F0", ("A", center.key, "B"), ("x", "y", "z"), "top"),
            Face("F1", ("B", center.key, "C"), ("y", "z", "x"), "top"),
            Face("F2", ("C", center.key, "D"), ("z", "x", "y"), "top"),
        ]
    return [
        Face("F0", ("A", center.key, "B"), ("x", "y", "z"), "top"),
        Face("F1", ("B", center.key, "C"), ("y", "x", "z"), "top"),
        Face("F2", ("C", center.key, "D"), ("z", "x", "y"), "bottom"),
    ]


def class_census(centers: list[LockedCenter]) -> tuple:
    return tuple(sorted(Counter(c.chamber_class for c in centers).items()))


def sign_census(centers: list[LockedCenter]) -> tuple:
    counts = Counter()
    for c in centers:
        if not c.chamber_class.startswith("K_"):
            continue
        for face in local_face_fan(c):
            counts[face.sign()] += 1
    return tuple(sorted(counts.items()))


def run_local_packet(
    center: LockedCenter,
    inherited_direction: str = "R",
) -> tuple[list[LockedCenter], dict[tuple, CandidateClass], list[str]]:
    candidates: dict[tuple, CandidateClass] = {}
    log: list[str] = []
    locked_key: tuple | None = None

    phase_order: dict[Phase, list[Operator]] = {
        "t1": ["x", "y", "z"],
        "t2": ["y", "x", "z"],
        "t3": ["x", "z", "y"],
    }

    for phase in ("t1", "t2", "t3"):
        log.append(f"{center.key} {phase}")
        for op in phase_order[phase]:
            if locked_key is not None:
                log.append(f"  skip {center.key}:{op} (winner already locked at {locked_key})")
                continue

            key = candidate_key(center, phase, op, inherited_direction)
            cand = candidates.setdefault(key, CandidateClass(key=key))
            cand.register(
                op=op,
                source=center.key,
                phase=phase,
                polarity=operator_polarity(op),
            )
            log.append(
                f"  {center.key}:{op} -> {key} | ops={sorted(cand.ops)} visits={cand.visits}"
            )

            if not cand.locked and cand.packet_complete():
                cand.locked = True
                locked_key = key
                log.append(f"  LOCK {key} bias={cand.bias_label()}")

    promoted: list[LockedCenter] = []
    if locked_key is not None:
        cand = candidates[locked_key]
        _, shell, direction = locked_key
        promoted.append(
            LockedCenter(
                key=f"{center.key}_{direction}_{shell}",
                chamber_class=promote_class(cand),
                shell=shell,
                bias=cand.bias_label(),
            )
        )

    return promoted, candidates, log


def run_shared_packet(
    centers: list[LockedCenter],
    inherited_direction: str = "R",
    mode: SharedMode = "collapsed",
) -> tuple[list[LockedCenter], dict[tuple, CandidateClass], list[str]]:
    candidates: dict[tuple, CandidateClass] = {}
    log: list[str] = []
    locked_key: tuple | None = None
    x_echo_enabled = mode == "structured"
    x_seen_sources: set[str] = set()

    phase_order: dict[Phase, list[Operator]] = {
        "t1": ["x"],
        "t2": ["y"],
        "t3": ["z"],
    }

    for phase in ("t1", "t2", "t3"):
        log.append(f"shared {phase} mode={mode}")
        ops = phase_order[phase]
        for source_center in centers:
            for op in ops:
                if locked_key is not None:
                    log.append(
                        f"  skip {source_center.key}:{op} "
                        f"(winner already locked at {locked_key})"
                    )
                    continue

                key = shared_candidate_key(
                    centers,
                    phase,
                    op,
                    inherited_direction,
                    mode=mode,
                )
                cand = candidates.setdefault(key, CandidateClass(key=key))
                cand.register(
                    op=op,
                    source=source_center.key,
                    phase=phase,
                    polarity=operator_polarity(op),
                )
                log.append(
                    f"  {source_center.key}:{op} -> {key} | ops={sorted(cand.ops)} "
                    f"sources={sorted(cand.sources)} visits={cand.visits}"
                )

                if phase == "t1" and op == "x":
                    x_seen_sources.add(source_center.key)

                if not cand.locked and cand.packet_complete():
                    cand.locked = True
                    locked_key = key
                    log.append(
                        f"  LOCK {key} bias={cand.bias_label()} "
                        f"sources={sorted(cand.sources)}"
                    )

        if x_echo_enabled and locked_key is None and phase == "t2" and x_seen_sources:
            echo_key = (
                min(c.shell for c in centers) + 2,
                inherited_direction,
                tuple(sorted(c.chamber_class for c in centers)),
            )
            echo_cand = candidates.setdefault(echo_key, CandidateClass(key=echo_key))
            for source in sorted(x_seen_sources):
                echo_cand.register(
                    op="x",
                    source=source,
                    phase=phase,
                    polarity=operator_polarity("x"),
                )
            log.append(
                f"  echo x-forward -> {echo_key} | ops={sorted(echo_cand.ops)} "
                f"sources={sorted(echo_cand.sources)} visits={echo_cand.visits}"
            )
            if not echo_cand.locked and echo_cand.packet_complete():
                echo_cand.locked = True
                locked_key = echo_key
                log.append(
                    f"  LOCK {echo_key} bias={echo_cand.bias_label()} "
                    f"sources={sorted(echo_cand.sources)}"
                )

    promoted: list[LockedCenter] = []
    if locked_key is not None:
        cand = candidates[locked_key]
        shell, direction, _ = locked_key
        promoted.append(
            LockedCenter(
                key=f"S0_{direction}_{shell}",
                chamber_class=promote_class(cand),
                shell=shell,
                bias=cand.bias_label(),
            )
        )

    return promoted, candidates, log


def sweep_shared_modes(
    rounds: int = 6,
    inherited_direction: str = "R",
) -> None:
    modes: list[SharedMode] = ["collapsed", "semistructured", "structured"]

    print("== lazy-universe shared mode sweep ==")
    for mode in modes:
        centers = [
            LockedCenter("I0", "seedL", 0),
            LockedCenter("I1", "seedM", 0),
            LockedCenter("I2", "seedR", 0),
        ]
        history: list[tuple[tuple, tuple]] = []

        print(f"-- mode={mode} --")
        for rnd in range(rounds):
            promoted, _, _ = run_shared_packet(
                centers,
                inherited_direction=inherited_direction,
                mode=mode,
            )

            cc = class_census(promoted)
            sc = sign_census(promoted)
            history.append((cc, sc))
            print(f"round {rnd}: classes={cc} | signs={sc}")

            if promoted:
                centers = [
                    LockedCenter(f"B{rnd}L", centers[0].chamber_class, centers[0].shell),
                    *promoted,
                    LockedCenter(f"B{rnd}R", centers[-1].chamber_class, centers[-1].shell),
                ]
            else:
                break

        seen: dict[tuple[tuple, tuple], int] = {}
        repeat_found = False
        for idx, pair in enumerate(history):
            if pair in seen:
                first = seen[pair]
                print(
                    f"repeat detected: rounds {first} and {idx} "
                    f"share classes={pair[0]} signs={pair[1]}"
                )
                repeat_found = True
                break
            seen[pair] = idx

        if not repeat_found:
            print("repeat detected: none in sweep window")
        print()


def demo() -> None:
    print("== one-center packet ==")
    center = LockedCenter("I0", "seed", 0)
    promoted, _, log = run_local_packet(center)
    for line in log:
        print(line)
    print("promoted:", [p.chamber_class for p in promoted])
    print("class census:", class_census(promoted))
    print("sign census :", sign_census(promoted))
    print()

    centers = [
        LockedCenter("I0", "seedL", 0),
        LockedCenter("I1", "seedM", 0),
        LockedCenter("I2", "seedR", 0),
    ]

    print("== shared packet (collapsed) ==")
    promoted, _, log = run_shared_packet(centers, mode="collapsed")
    for line in log:
        print(line)
    print("promoted:", [p.chamber_class for p in promoted])
    print("class census:", class_census(promoted))
    print("sign census :", sign_census(promoted))
    print()

    print("== shared packet (semistructured) ==")
    promoted, _, log = run_shared_packet(centers, mode="semistructured")
    for line in log:
        print(line)
    print("promoted:", [p.chamber_class for p in promoted])
    print("class census:", class_census(promoted))
    print("sign census :", sign_census(promoted))
    print()

    print("== shared packet (structured, x-echo) ==")
    promoted, _, log = run_shared_packet(centers, mode="structured")
    for line in log:
        print(line)
    print("promoted:", [p.chamber_class for p in promoted])
    print("class census:", class_census(promoted))
    print("sign census :", sign_census(promoted))
    print()

    sweep_shared_modes()


if __name__ == "__main__":
    demo()
