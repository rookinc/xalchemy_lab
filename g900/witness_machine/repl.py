from __future__ import annotations

import argparse

from .core import state_code, validate_state, tau, tau_inv, mu
from .render import (
    render_ascii_graph,
    render_info,
    render_observer_view,
    action_summary,
    state_summary,
)

HELP = """
Commands:
  show                 show current state
  tau                  apply tau
  back                 apply tau inverse
  mu                   apply mu
  goto i,p             jump to state
  frame                observer: frame
  phase                observer: phase
  output               observer: output
  action               show current action cell
  ascii                show machine graph
  info                 show machine info
  help                 show this help
  quit / exit          leave repl
""".strip()


def parse_state(text: str) -> tuple[int, int]:
    a, b = text.split(",", 1)
    return (int(a.strip()), int(b.strip()))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 -m witness_machine.repl")
    p.add_argument("--r", type=int, default=1, help="scale parameter, default 1")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    r = args.r
    state = (0, 0)

    print("Witness machine REPL")
    print(f"scale: {r}")
    print("start:", state, "code:", state_code(state, r))
    print(HELP)

    while True:
        try:
            raw = input("wm> ").strip()
        except EOFError:
            print()
            return 0

        if not raw:
            continue

        if raw in {"quit", "exit"}:
            return 0

        if raw == "help":
            print(HELP)
            continue

        if raw == "show":
            print(state_summary(state, r))
            continue

        if raw == "tau":
            state = tau(state, r)
            print(state, "code:", state_code(state, r))
            continue

        if raw == "back":
            state = tau_inv(state, r)
            print(state, "code:", state_code(state, r))
            continue

        if raw == "mu":
            state = mu(state, r)
            print(state, "code:", state_code(state, r))
            continue

        if raw.startswith("goto "):
            try:
                nxt = parse_state(raw[5:])
                state = validate_state(nxt, r)
                print(state, "code:", state_code(state, r))
            except Exception as exc:
                print(f"error: {exc}")
            continue

        if raw == "frame":
            print(render_observer_view(state, "frame", r))
            continue

        if raw == "phase":
            print(render_observer_view(state, "phase", r))
            continue

        if raw == "output":
            print(render_observer_view(state, "output", r))
            continue

        if raw == "action":
            print(action_summary(state[0], r))
            continue

        if raw == "ascii":
            print(render_ascii_graph(r))
            continue

        if raw == "info":
            print(render_info(r))
            continue

        print("unknown command; type 'help'")

if __name__ == "__main__":
    raise SystemExit(main())
