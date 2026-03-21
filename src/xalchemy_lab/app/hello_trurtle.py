from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional


Handedness = Literal["left", "right"]
Status = Literal["active", "halted"]
EdgeEventKind = Literal["trace", "reinforce", "coupling"]


@dataclass
class SideState:
    turtle_ids: list[str] = field(default_factory=list)
    turtle_classes: list[int] = field(default_factory=list)

    def classify_touch(self, turtle_id: str, turtle_class: int) -> EdgeEventKind:
        if not self.turtle_ids:
            return "trace"
        if turtle_id in self.turtle_ids:
            return "reinforce"
        return "coupling"

    def apply_touch(self, turtle_id: str, turtle_class: int) -> EdgeEventKind:
        kind = self.classify_touch(turtle_id, turtle_class)
        self.turtle_ids.append(turtle_id)
        self.turtle_classes.append(turtle_class)
        return kind

    def summary(self) -> str:
        if not self.turtle_ids:
            return "[]"
        pairs = ",".join(
            f"{tid}:{tclass}" for tid, tclass in zip(self.turtle_ids, self.turtle_classes)
        )
        return f"[{pairs}]"


@dataclass
class Cell:
    cell_id: str
    # side -> neighboring cell_id or None if boundary
    neighbors: dict[int, Optional[str]]
    # side -> richer side state
    marks: dict[int, SideState] = field(
        default_factory=lambda: {0: SideState(), 1: SideState(), 2: SideState()}
    )


@dataclass
class Turtle:
    turtle_id: str
    turtle_class: int
    cell_id: str
    entry_side: int
    handedness: Handedness
    status: Status = "active"
    steps: int = 0


@dataclass
class Event:
    tick: int
    turtle_id: str
    event_type: str
    cell_id: str
    side: Optional[int]
    note: str = ""


def build_toy_sheet() -> dict[str, Cell]:
    r"""
    A tiny 7-cell toy sheet.

             c1
           /    \
         c2--c0--c3
           \    /
            c4
          /    \
         c5    c6

    This is not a geometric renderer yet; it is just a local adjacency field.
    Side labels are abstract {0,1,2}.
    """
    return {
        "c0": Cell("c0", {0: "c1", 1: "c2", 2: "c3"}),
        "c1": Cell("c1", {0: None, 1: "c0", 2: "c2"}),
        "c2": Cell("c2", {0: "c1", 1: "c4", 2: "c0"}),
        "c3": Cell("c3", {0: "c0", 1: "c4", 2: None}),
        "c4": Cell("c4", {0: "c2", 1: "c5", 2: "c3"}),
        "c5": Cell("c5", {0: None, 1: None, 2: "c4"}),
        "c6": Cell("c6", {0: None, 1: None, 2: None}),  # spare isolated test cell
    }


def other_sides(entry_side: int) -> tuple[int, int]:
    sides = [0, 1, 2]
    sides.remove(entry_side)
    return sides[0], sides[1]


def preferred_exit(entry_side: int, handedness: Handedness) -> int:
    a, b = other_sides(entry_side)
    return a if handedness == "left" else b


def choose_exit(cell: Cell, turtle: Turtle) -> Optional[int]:
    a, b = other_sides(turtle.entry_side)
    pref = preferred_exit(turtle.entry_side, turtle.handedness)
    alt = b if pref == a else a

    # Prefer untouched side with a neighbor.
    for side in (pref, alt):
        if cell.neighbors[side] is not None and not cell.marks[side].turtle_ids:
            return side

    # Then allow previously touched side with a neighbor.
    for side in (pref, alt):
        if cell.neighbors[side] is not None:
            return side

    return None


def flip_handedness(handedness: Handedness) -> Handedness:
    return "right" if handedness == "left" else "left"


def find_back_side(cell: Cell, previous_cell_id: str) -> int:
    for side, neighbor in cell.neighbors.items():
        if neighbor == previous_cell_id:
            return side
    raise ValueError(f"{cell.cell_id} has no side back to {previous_cell_id}")


def apply_mark(
    *,
    cells: dict[str, Cell],
    old_cell_id: str,
    exit_side: int,
    turtle: Turtle,
    tick: int,
    encounter: bool = False,
) -> Event:
    side_state = cells[old_cell_id].marks[exit_side]
    mark_kind = side_state.apply_touch(turtle.turtle_id, turtle.turtle_class)
    note = f"class={turtle.turtle_class}; mark={mark_kind}"
    if encounter:
        note += "; encounter"
    return Event(
        tick=tick,
        turtle_id=turtle.turtle_id,
        event_type=mark_kind,
        cell_id=old_cell_id,
        side=exit_side,
        note=note,
    )


def tick_once(
    cells: dict[str, Cell],
    turtles: list[Turtle],
    tick: int,
) -> list[Event]:
    events: list[Event] = []
    proposals: dict[str, list[tuple[Turtle, int, str]]] = {}

    for turtle in turtles:
        if turtle.status != "active":
            continue

        cell = cells[turtle.cell_id]
        exit_side = choose_exit(cell, turtle)
        if exit_side is None:
            turtle.status = "halted"
            events.append(
                Event(
                    tick=tick,
                    turtle_id=turtle.turtle_id,
                    event_type="halt",
                    cell_id=turtle.cell_id,
                    side=None,
                    note="no legal exit",
                )
            )
            continue

        next_cell_id = cell.neighbors[exit_side]
        assert next_cell_id is not None
        proposals.setdefault(next_cell_id, []).append((turtle, exit_side, turtle.cell_id))

    for next_cell_id, arrivals in proposals.items():
        if len(arrivals) == 1:
            turtle, exit_side, old_cell_id = arrivals[0]
            events.append(
                apply_mark(
                    cells=cells,
                    old_cell_id=old_cell_id,
                    exit_side=exit_side,
                    turtle=turtle,
                    tick=tick,
                    encounter=False,
                )
            )

            next_cell = cells[next_cell_id]
            back_side = find_back_side(next_cell, old_cell_id)
            turtle.cell_id = next_cell_id
            turtle.entry_side = back_side
            turtle.steps += 1

            events.append(
                Event(
                    tick=tick,
                    turtle_id=turtle.turtle_id,
                    event_type="move",
                    cell_id=next_cell_id,
                    side=back_side,
                    note=f"from={old_cell_id}",
                )
            )
        else:
            turtle_ids = ",".join(t.turtle_id for t, _, _ in arrivals)
            for turtle, exit_side, old_cell_id in arrivals:
                events.append(
                    Event(
                        tick=tick,
                        turtle_id=turtle.turtle_id,
                        event_type="meet",
                        cell_id=next_cell_id,
                        side=None,
                        note=f"with={turtle_ids}",
                    )
                )

                events.append(
                    apply_mark(
                        cells=cells,
                        old_cell_id=old_cell_id,
                        exit_side=exit_side,
                        turtle=turtle,
                        tick=tick,
                        encounter=True,
                    )
                )

                next_cell = cells[next_cell_id]
                back_side = find_back_side(next_cell, old_cell_id)
                turtle.cell_id = next_cell_id
                turtle.entry_side = back_side
                turtle.handedness = flip_handedness(turtle.handedness)
                turtle.steps += 1

                events.append(
                    Event(
                        tick=tick,
                        turtle_id=turtle.turtle_id,
                        event_type="move",
                        cell_id=next_cell_id,
                        side=back_side,
                        note=f"from={old_cell_id}; flipped={turtle.handedness}",
                    )
                )

    return events


def print_state(cells: dict[str, Cell], turtles: list[Turtle]) -> None:
    print("\nTRURTLES")
    for t in turtles:
        print(
            f"  {t.turtle_id}: class={t.turtle_class} "
            f"cell={t.cell_id} entry={t.entry_side} hand={t.handedness} "
            f"status={t.status} steps={t.steps}"
        )

    print("\nMARKS")
    for cell_id in sorted(cells):
        cell = cells[cell_id]
        parts = []
        for side in (0, 1, 2):
            parts.append(f"{side}:{cell.marks[side].summary()}")
        print(f"  {cell_id}: " + " ".join(parts))


def main() -> None:
    cells = build_toy_sheet()
    turtles = [
        Turtle("T1", 1, "c1", 0, "left"),
        Turtle("T2", 2, "c2", 1, "right"),
        Turtle("T3", 3, "c3", 2, "left"),
    ]

    print("HELLO TRURTLE")
    print_state(cells, turtles)

    max_ticks = 6
    for tick in range(1, max_ticks + 1):
        events = tick_once(cells, turtles, tick)
        print(f"\n=== TICK {tick} ===")
        for e in events:
            print(
                f"{e.tick:02d} | {e.turtle_id:>2} | {e.event_type:<9} "
                f"| cell={e.cell_id} side={e.side} | {e.note}"
            )
        print_state(cells, turtles)

        if all(t.status == "halted" for t in turtles):
            print("\nAll trurtles halted.")
            break


if __name__ == "__main__":
    main()
