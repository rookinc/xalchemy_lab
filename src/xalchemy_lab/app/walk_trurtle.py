from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from xalchemy_lab.app.hello_trurtle import (
    Turtle,
    build_toy_sheet,
    print_state,
    tick_once,
)


def main() -> None:
    cells = build_toy_sheet()
    trurtles = [
        Turtle("T1", 1, "c1", 0, "left"),
        Turtle("T2", 2, "c2", 1, "right"),
        Turtle("T3", 3, "c3", 2, "left"),
    ]

    max_ticks = 20
    all_events = []

    print("TRURTLE WALK")
    print_state(cells, trurtles)

    for tick in range(1, max_ticks + 1):
        events = tick_once(cells, trurtles, tick)
        all_events.extend(asdict(e) for e in events)

        print(f"\n=== TICK {tick} ===")
        for e in events:
            print(
                f"{e.tick:02d} | {e.turtle_id:>2} | {e.event_type:<9} "
                f"| cell={e.cell_id} side={e.side} | {e.note}"
            )

        if all(t.status == "halted" for t in trurtles):
            print("\nAll trurtles halted.")
            break

    outdir = Path("export")
    outdir.mkdir(exist_ok=True)

    summary = {
        "name": "trurtle_walk",
        "max_ticks": max_ticks,
        "final_trurtles": [
            {
                "id": t.turtle_id,
                "class": t.turtle_class,
                "cell": t.cell_id,
                "entry_side": t.entry_side,
                "handedness": t.handedness,
                "status": t.status,
                "steps": t.steps,
            }
            for t in trurtles
        ],
        "events": all_events,
        "final_marks": {
            cell_id: {
                str(side): {
                    "touch_count": len(cell.marks[side].turtle_ids),
                    "trurtle_ids": cell.marks[side].turtle_ids,
                    "classes_present": cell.marks[side].turtle_classes,
                }
                for side in (0, 1, 2)
            }
            for cell_id, cell in cells.items()
        },
    }

    outpath = outdir / "trurtle_walk.json"
    outpath.write_text(json.dumps(summary, indent=2))
    print(f"\nWrote {outpath}")


if __name__ == "__main__":
    main()
