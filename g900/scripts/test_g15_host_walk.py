#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "specs" / "examples" / "g15-host-walk-test.json"


@dataclass(frozen=True)
class State:
    vertex: str
    layer: int
    heading: int

    def as_dict(self) -> dict:
        return {
            "vertex": self.vertex,
            "layer": self.layer,
            "heading": self.heading,
        }


def load_spec(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_move_table(spec: dict) -> Dict[Tuple[int, str, int], str]:
    table: Dict[Tuple[int, str, int], str] = {}
    for row in spec.get("move_transition_subset", []):
        key = (int(row["layer"]), str(row["from_vertex"]), int(row["heading"]))
        to_vertex = str(row["to_vertex"])
        if key in table:
            raise ValueError(f"Duplicate move transition for {key}")
        table[key] = to_vertex
    return table


def op_left(state: State) -> State:
    return State(state.vertex, state.layer, (state.heading + 3) % 4)


def op_right(state: State) -> State:
    return State(state.vertex, state.layer, (state.heading + 1) % 4)


def op_lift(state: State, max_layer: int) -> State:
    if state.layer >= max_layer:
        raise ValueError(f"Lift undefined from top layer: {state}")
    return State(state.vertex, state.layer + 1, state.heading)


def op_move(state: State, move_table: Dict[Tuple[int, str, int], str]) -> State:
    key = (state.layer, state.vertex, state.heading)
    if key not in move_table:
        raise ValueError(f"Move undefined for state: {state}")
    return State(move_table[key], state.layer, state.heading)


def execute_word(
    start: State,
    word: List[str],
    move_table: Dict[Tuple[int, str, int], str],
    max_layer: int,
) -> List[State]:
    trace: List[State] = [start]
    state = start

    for step in word:
        if step == "L":
            state = op_left(state)
        elif step == "R":
            state = op_right(state)
        elif step == "U":
            state = op_lift(state, max_layer=max_layer)
        elif step == "M":
            state = op_move(state, move_table)
        else:
            raise ValueError(f"Unknown operator: {step}")
        trace.append(state)

    return trace


def format_trace(trace: List[State]) -> str:
    lines = []
    for i, state in enumerate(trace):
        lines.append(
            f"{i:02d}: vertex={state.vertex:<3} layer={state.layer} heading={state.heading}"
        )
    return "\n".join(lines)


def main() -> int:
    spec = load_spec(SPEC_PATH)
    model = spec["state_model"]

    max_layer = max(int(x) for x in model["layers"])
    start_spec = spec["start_state"]
    start = State(
        vertex=str(start_spec["vertex"]),
        layer=int(start_spec["layer"]),
        heading=int(start_spec["heading"]),
    )

    move_table = build_move_table(spec)
    word = [str(x) for x in spec["anchor_word"]]

    trace = execute_word(start, word, move_table, max_layer=max_layer)
    final_state = trace[-1]
    closes = final_state == start

    print("G15 host walk test")
    print("==================")
    print(f"Spec: {SPEC_PATH}")
    print(f"Start state: {start}")
    print(f"Final state: {final_state}")
    print(f"Closure: {'PASS' if closes else 'FAIL'}")
    print()
    print("Trace")
    print("-----")
    print(format_trace(trace))
    print()
    print("Landing trace")
    print("-------------")
    print(" -> ".join(state.vertex for state in trace))
    print()
    print("Layer trace")
    print("-----------")
    print(" -> ".join(str(state.layer) for state in trace))
    print()
    print("Heading trace")
    print("-------------")
    print(" -> ".join(str(state.heading) for state in trace))

    return 0 if closes else 1


if __name__ == "__main__":
    raise SystemExit(main())
