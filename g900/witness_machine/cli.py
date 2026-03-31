from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import (
    action_dict,
    apply_word,
    batch_classify_cycles,
    classify_cycle,
    export_machine,
    list_states,
    mu,
    normalize_word,
    output_signature,
    phase_label,
    species_of_action,
    species_of_state,
    state_code,
    state_dict,
    tau,
    tau_inv,
    validate_state,
)
from .render import (
    action_summary,
    render_actions_list,
    render_ascii_graph,
    render_compare,
    render_info,
    render_observer_view,
    render_orbit,
    render_states_list,
    render_table,
    state_summary,
)


def _state_label(state: tuple[int, int]) -> str:
    return f"({state[0]},{state[1]})"


def parse_state(text: str) -> tuple[int, int]:
    try:
        a, b = text.split(",", 1)
        return (int(a), int(b))
    except Exception as exc:
        raise argparse.ArgumentTypeError(
            "state must look like frame,phase  e.g. 0,1"
        ) from exc


def parse_word(text: str) -> list[str]:
    ops = [x.strip() for x in text.split(",") if x.strip()]
    valid = {"tau", "tau_inv", "mu"}
    bad = [x for x in ops if x not in valid]
    if bad:
        raise argparse.ArgumentTypeError(
            f"invalid ops in word: {', '.join(bad)}"
        )
    return ops


def parse_cycle(text: str) -> list[str]:
    parts = [x.strip() for x in text.split(",") if x.strip()]
    if len(parts) < 3:
        raise argparse.ArgumentTypeError("cycle must have at least 3 comma-separated vertices")
    return parts


def apply_op(state: tuple[int, int], op: str, r: int) -> tuple[int, int]:
    if op == "tau":
        return tau(state, r)
    if op == "tau_inv":
        return tau_inv(state, r)
    if op == "mu":
        return mu(state, r)
    raise ValueError(f"unknown op: {op}")


def load_batch_items(path: str):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        items = payload.get("items")
        if items is None:
            raise SystemExit("batch input JSON must contain an 'items' field")
    elif isinstance(payload, list):
        items = payload
    else:
        raise SystemExit("batch input JSON must be a list or an object with an 'items' field")
    return items


def cmd_show(args: argparse.Namespace) -> int:
    st = validate_state(args.state, args.r)
    print(state_summary(st, args.r))
    return 0


def cmd_step(args: argparse.Namespace) -> int:
    st = validate_state(args.state, args.r)
    nxt = apply_op(st, args.op, args.r)
    print(_state_label(nxt))
    print(state_summary(nxt, args.r))
    return 0


def cmd_classify(args: argparse.Namespace) -> int:
    if args.input:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        cycle = payload.get("cycle")
        if not cycle:
            raise SystemExit("input JSON must contain a 'cycle' field")
    elif args.cycle:
        cycle = args.cycle
    else:
        raise SystemExit("provide either --cycle or --input")

    result = classify_cycle(cycle, args.r)
    text = json.dumps(result, indent=2)

    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


def cmd_batch_classify(args: argparse.Namespace) -> int:
    items = load_batch_items(args.input)
    result = batch_classify_cycles(items, args.r)
    text = json.dumps(result, indent=2)

    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


def cmd_report_batch(args: argparse.Namespace) -> int:
    items = load_batch_items(args.input)
    result = batch_classify_cycles(items, args.r)
    rows = result["results"]

    confidence_counts = {"exact": 0, "nearest": 0, "ambiguous": 0}
    for row in rows:
        conf = row.get("confidence")
        if conf in confidence_counts:
            confidence_counts[conf] += 1

    print(f"scale: {result['scale']}")
    print(f"count: {result['count']}")
    print("classification_counts:")
    for k, v in result["classification_counts"].items():
        print(f"  {k}: {v}")

    print("confidence_counts:")
    for k, v in confidence_counts.items():
        print(f"  {k}: {v}")

    ambiguous = [r for r in rows if r.get("confidence") == "ambiguous"]
    near_action = [
        r for r in rows
        if r.get("classification") == "action-cell" and r.get("confidence") == "nearest"
    ]
    exact_states = [
        r for r in rows
        if r.get("classification") in {"subjective-state", "objective-state"}
        and r.get("confidence") == "exact"
    ]

    print()
    print("ambiguous_cases:")
    if ambiguous:
        for r in ambiguous:
            ds = r.get("distance_summary", {})
            print(
                f"  {r.get('label')}: "
                f"S={ds.get('best_subjective_distance')} "
                f"O={ds.get('best_objective_distance')} "
                f"A={ds.get('best_action_distance')}"
            )
    else:
        print("  none")

    print()
    print("near_action_cases:")
    if near_action:
        for r in near_action:
            ds = r.get("distance_summary", {})
            print(
                f"  {r.get('label')}: "
                f"A={ds.get('best_action_distance')} "
                f"O={ds.get('best_objective_distance')} "
                f"S={ds.get('best_subjective_distance')}"
            )
    else:
        print("  none")

    print()
    print("exact_state_hits:")
    if exact_states:
        for r in exact_states:
            print(f"  {r.get('label')}: {r.get('classification')}")
    else:
        print("  none")

    return 0


def cmd_list_states(args: argparse.Namespace) -> int:
    print(render_states_list(args.r))
    return 0


def cmd_list_actions(args: argparse.Namespace) -> int:
    print(render_actions_list(args.r))
    return 0


def cmd_action(args: argparse.Namespace) -> int:
    print(action_summary(args.frame, args.r))
    return 0


def cmd_table(args: argparse.Namespace) -> int:
    print(render_table(args.r))
    return 0


def cmd_ascii(args: argparse.Namespace) -> int:
    print(render_ascii_graph(args.r))
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    print(render_info(args.r))
    return 0


def cmd_observe(args: argparse.Namespace) -> int:
    st = validate_state(args.state, args.r)
    print(render_observer_view(st, args.view, args.r))
    return 0


def _pow_tau(state: tuple[int, int], steps: int, r: int) -> tuple[int, int]:
    out = state
    for _ in range(steps):
        out = tau(out, r)
    return out


def cmd_check(args: argparse.Namespace) -> int:
    r = args.r
    states = list_states(r)
    ok = True

    expected_states = 10 * r
    if len(states) != expected_states:
        print(f"states: fail ({len(states)} != {expected_states})")
        ok = False
    else:
        print(f"states: ok ({len(states)})")

    tau_ok = all(_pow_tau(st, 5 * r, r) == st for st in states)
    print(f"tau^(5r): {'ok' if tau_ok else 'fail'}")
    ok &= tau_ok

    mu_ok = all(mu(mu(st, r), r) == st for st in states)
    print(f"mu^2: {'ok' if mu_ok else 'fail'}")
    ok &= mu_ok

    commute_ok = all(tau(mu(st, r), r) == mu(tau(st, r), r) for st in states)
    print(f"tau*mu = mu*tau: {'ok' if commute_ok else 'fail'}")
    ok &= commute_ok

    state_species_ok = all(species_of_state(st) == "O-O-O-S-T-S" for st in states)
    print(f"state species: {'ok' if state_species_ok else 'fail'}")
    ok &= state_species_ok

    action_species_ok = all(
        species_of_action(i, r) == "O-S-T-S-T-S" for i in range(5 * r)
    )
    print(f"action species: {'ok' if action_species_ok else 'fail'}")
    ok &= action_species_ok

    output_ok = all(
        output_signature(st, r) in {
            ("return", 4, 26),
            ("forward", 5, 18),
        }
        for st in states
    )
    print(f"output partition: {'ok' if output_ok else 'fail'}")
    ok &= output_ok

    return 0 if ok else 1


def cmd_export(args: argparse.Namespace) -> int:
    if args.kind == "machine":
        payload = export_machine(args.r)
    elif args.kind == "state":
        if args.state is None:
            raise SystemExit("--state is required for --kind state")
        payload = state_dict(validate_state(args.state, args.r), args.r)
    elif args.kind == "action":
        if args.frame is None:
            raise SystemExit("--frame is required for --kind action")
        payload = action_dict(args.frame, args.r)
    else:
        raise SystemExit("unknown export kind")

    text = json.dumps(payload, indent=2)

    if args.out:
        path = Path(args.out)
        path.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {path}")
    else:
        print(text)
    return 0


def orbit_trace_from_op(state: tuple[int, int], op: str, r: int) -> list[dict]:
    st = validate_state(state, r)
    trace = [
        {
            "step": 0,
            "op": "start",
            "code": state_code(st, r),
            "state": _state_label(st),
            "phase": phase_label(st, r),
        }
    ]
    seen = {st}
    cur = st
    step = 0
    while True:
        step += 1
        cur = apply_op(cur, op, r)
        trace.append(
            {
                "step": step,
                "op": op,
                "code": state_code(cur, r),
                "state": _state_label(cur),
                "phase": phase_label(cur, r),
            }
        )
        if cur in seen:
            break
        seen.add(cur)
    return trace


def orbit_trace_from_word(state: tuple[int, int], word: list[str], r: int) -> list[dict]:
    st = validate_state(state, r)
    if not word:
        return [
            {
                "step": 0,
                "op": "start",
                "code": state_code(st, r),
                "state": _state_label(st),
                "phase": phase_label(st, r),
            }
        ]

    trace = [
        {
            "step": 0,
            "op": "start",
            "code": state_code(st, r),
            "state": _state_label(st),
            "phase": phase_label(st, r),
        }
    ]
    seen = {st}
    cur = st
    step = 0
    word_label = ",".join(word)
    while True:
        cur = apply_word(cur, word, r)
        step += 1
        trace.append(
            {
                "step": step,
                "op": word_label,
                "code": state_code(cur, r),
                "state": _state_label(cur),
                "phase": phase_label(cur, r),
            }
        )
        if cur in seen:
            break
        seen.add(cur)
    return trace


def cmd_orbit(args: argparse.Namespace) -> int:
    st = validate_state(args.state, args.r)
    if args.word:
        trace = orbit_trace_from_word(st, args.word, args.r)
        title = f"orbit from {_state_label(st)} under word {','.join(args.word)}"
    else:
        trace = orbit_trace_from_op(st, args.op, args.r)
        title = f"orbit from {_state_label(st)} under {args.op}"
    print(render_orbit(trace, title))
    return 0


def cmd_compose(args: argparse.Namespace) -> int:
    info = normalize_word(args.word, args.r)
    print(f"word: {','.join(info['word'])}")
    print(f"frame_delta: {info['frame_delta']} mod {info['frame_modulus']}")
    print(f"phase_delta: {info['phase_delta']} mod {info['phase_modulus']}")
    print(f"affine_form: {info['affine_form']}")
    print(f"frame_component_order: {info['frame_component_order']}")
    print(f"phase_component_order: {info['phase_component_order']}")
    print(f"orbit_formula: {info['orbit_formula']}")
    print(f"orbit_length: {info['orbit_length']}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    words = args.word if args.word else [["tau"], ["mu"], ["tau", "mu"]]
    print(render_compare(args.r1, args.r2, words))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 -m witness_machine.cli")
    p.add_argument("--r", type=int, default=1, help="scale parameter, default 1")
    sub = p.add_subparsers(dest="command", required=True)

    info = sub.add_parser("info")
    info.set_defaults(func=cmd_info)

    show = sub.add_parser("show")
    show.add_argument("--state", type=parse_state, required=True)
    show.set_defaults(func=cmd_show)

    step = sub.add_parser("step")
    step.add_argument("--state", type=parse_state, required=True)
    step.add_argument("--op", choices=["tau", "tau_inv", "mu"], required=True)
    step.set_defaults(func=cmd_step)

    classify = sub.add_parser("classify")
    classify.add_argument("--cycle", type=parse_cycle)
    classify.add_argument("--input")
    classify.add_argument("--out")
    classify.set_defaults(func=cmd_classify)

    batch = sub.add_parser("batch-classify")
    batch.add_argument("--input", required=True)
    batch.add_argument("--out")
    batch.set_defaults(func=cmd_batch_classify)

    report = sub.add_parser("report-batch")
    report.add_argument("--input", required=True)
    report.set_defaults(func=cmd_report_batch)

    orbit = sub.add_parser("orbit")
    orbit.add_argument("--state", type=parse_state, required=True)
    orbit.add_argument("--op", choices=["tau", "tau_inv", "mu"], default="tau")
    orbit.add_argument("--word", type=parse_word)
    orbit.set_defaults(func=cmd_orbit)

    compose = sub.add_parser("compose")
    compose.add_argument("--word", type=parse_word, required=True)
    compose.set_defaults(func=cmd_compose)

    compare = sub.add_parser("compare")
    compare.add_argument("--r1", type=int, required=True)
    compare.add_argument("--r2", type=int, required=True)
    compare.add_argument("--word", type=parse_word, action="append")
    compare.set_defaults(func=cmd_compare)

    ls = sub.add_parser("list-states")
    ls.set_defaults(func=cmd_list_states)

    la = sub.add_parser("list-actions")
    la.set_defaults(func=cmd_list_actions)

    action = sub.add_parser("action")
    action.add_argument("--frame", type=int, required=True)
    action.set_defaults(func=cmd_action)

    table = sub.add_parser("table")
    table.set_defaults(func=cmd_table)

    ascii_p = sub.add_parser("ascii")
    ascii_p.set_defaults(func=cmd_ascii)

    obs = sub.add_parser("observe")
    obs.add_argument("--state", type=parse_state, required=True)
    obs.add_argument("--view", choices=["frame", "phase", "output"], required=True)
    obs.set_defaults(func=cmd_observe)

    chk = sub.add_parser("check")
    chk.set_defaults(func=cmd_check)

    export = sub.add_parser("export")
    export.add_argument("--kind", choices=["machine", "state", "action"], default="machine")
    export.add_argument("--state", type=parse_state)
    export.add_argument("--frame", type=int)
    export.add_argument("--out")
    export.set_defaults(func=cmd_export)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
