from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import (
    action_cell,
    action_dict,
    apply_word,
    batch_classify_cycles,
    classify_cycle,
    cycle_key,
    export_machine,
    frame2_exact_prototype,
    frame2_socket_cycle,
    list_states,
    nearest_action_frames,
    normalize_cycle,
    normalized_diff,
    normalize_word,
    output_signature,
    phase_label,
    socket_payload,
    species_of_action,
    species_of_state,
    so_orbit_summary,
    state_dict,
    state_code,
    subjective_objective_family,
    target_cycle_for_spec,
    tau,
    tau_inv,
    mu,
    validate_state,
    witness_assembly,
)
from .render import (
    render_actions_list,
    render_ascii_graph,
    render_audit_neighborhood,
    render_compare,
    render_explain_cycle,
    render_info,
    render_observer_view,
    render_orbit,
    render_states_list,
    render_table,
    state_label as _state_label,
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


def parse_t_value(text: str) -> str:
    value = text.strip()
    if not value:
        raise argparse.ArgumentTypeError("T payload must be non-empty")
    return value


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


def _one_edit_variants(seed: list[str], r: int) -> list[dict]:
    n = 5 * r
    vocab = []
    for i in range(n):
        vocab.extend([f"o{i}", f"s{i}", f"t{i}"])

    out = []
    seen = set()
    for pos in range(len(seed)):
        original = seed[pos]
        for candidate in vocab:
            if candidate == original:
                continue
            mutated = seed.copy()
            mutated[pos] = candidate
            key = tuple(mutated)
            if key in seen:
                continue
            seen.add(key)
            out.append(
                {
                    "label": f"edit_pos{pos}_{original}_to_{candidate}",
                    "cycle": mutated,
                }
            )
    return out


def cmd_explain_cycle(args: argparse.Namespace) -> int:
    c = classify_cycle(args.cycle, args.r)

    diff_payload = None
    if args.show_diff:
        target = target_cycle_for_spec(args.show_diff, args.r)
        diff = normalized_diff(args.cycle, target)
        diff_payload = {
            "target_spec": args.show_diff,
            "target_normalized_cycle": normalize_cycle(target),
            "diff": diff,
            "hamming": len(diff),
        }

    print(render_explain_cycle(args.cycle, c, diff_payload))
    return 0




def cmd_assembly(args: argparse.Namespace) -> int:
    if args.t:
        cycle = frame2_socket_cycle(args.t, args.r)
    elif args.input:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        cycle = payload.get("cycle")
        if not cycle:
            raise SystemExit("input JSON must contain a 'cycle' field")
    elif args.cycle:
        cycle = args.cycle
    else:
        cycle = frame2_exact_prototype(args.r)

    c = classify_cycle(cycle, args.r)
    asm = witness_assembly(c["normalized_cycle"], args.r)

    result = {
        "input_cycle": cycle,
        "normalized_cycle": c["normalized_cycle"],
        "classification": c["classification"],
        "confidence": c["confidence"],
        "distance_summary": c["distance_summary"],
        "nearest_action_frames": nearest_action_frames(c),
        "frame2_exact_prototype": frame2_exact_prototype(args.r),
        "socket_payload": socket_payload(c["normalized_cycle"]),
        "assembly": asm,
    }

    text = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        if getattr(args, "pretty", False):
            print(_render_pretty_assembly(result))
        else:
            print(text)
    return 0



def cmd_socket_neighborhood(args: argparse.Namespace) -> int:
    if args.t:
        cycle = frame2_socket_cycle(args.t, args.r)
    elif args.input:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        cycle = payload.get("cycle")
        if not cycle:
            raise SystemExit("input JSON must contain a 'cycle' field")
    elif args.cycle:
        cycle = args.cycle
    else:
        cycle = frame2_exact_prototype(args.r)

    parent = classify_cycle(cycle, args.r)
    parent_norm = parent["normalized_cycle"]
    parent_payload = socket_payload(parent_norm)

    kids = _one_edit_variants(parent_norm, args.r)

    seam_children = []
    payload_hist = {}
    mismatch_hist = {}
    exact_children = []
    t2_children = []
    off_scaffold = []

    for item in kids:
        c = classify_cycle(item["cycle"], args.r)
        child_norm = c["normalized_cycle"]

        if not (
            c["classification"] == "action-cell"
            and c["distance_summary"]["best_action_distance"] == 1
            and 2 in nearest_action_frames(c)
        ):
            continue

        payload = socket_payload(child_norm)
        payload_hist[payload] = payload_hist.get(payload, 0) + 1

        diff = normalized_diff(child_norm, frame2_exact_prototype(args.r))
        mism = [row["position"] for row in diff]
        mismatch_hist[str(mism)] = mismatch_hist.get(str(mism), 0) + 1

        row = {
            "label": item["label"],
            "normalized_cycle": child_norm,
            "socket_payload": payload,
            "mismatch_positions_vs_E2": mism,
            "classification": c["classification"],
            "confidence": c["confidence"],
            "nearest_action_frames": nearest_action_frames(c),
        }
        seam_children.append(row)

        if payload == "t2":
            t2_children.append(row)
        if mism != [4]:
            off_scaffold.append(row)
        if c["confidence"] == "exact":
            exact_children.append(row)

    result = {
        "parent_cycle": parent_norm,
        "parent_payload": parent_payload,
        "frame2_exact_prototype": frame2_exact_prototype(args.r),
        "assembly": witness_assembly(parent_norm, args.r),
        "summary": {
            "seam_child_count": len(seam_children),
            "payload_histogram": dict(sorted(payload_hist.items())),
            "mismatch_histogram_vs_E2": dict(sorted(mismatch_hist.items())),
            "t2_child_count": len(t2_children),
            "off_scaffold_child_count": len(off_scaffold),
            "exact_child_count": len(exact_children),
        },
        "seam_children": seam_children,
        "t2_child_examples": t2_children[:20],
        "off_scaffold_child_examples": off_scaffold[:20],
        "exact_child_examples": exact_children[:20],
    }

    text = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        if getattr(args, "pretty", False):
            print(_render_pretty_socket_neighborhood(result))
        else:
            print(text)
    return 0



def cmd_socket_family(args: argparse.Namespace) -> int:
    if args.r != 1:
        raise SystemExit("socket-family is currently defined only for r=1")

    full_payloads = ["t2", "o4", "s0", "s1", "s2", "s3", "s4", "t0", "t1", "t3", "t4"]
    bounded_payloads = ["o4", "s0", "s2", "s3", "s4", "t0", "t3", "t4"]

    if args.bounded:
        payloads = bounded_payloads
    else:
        payloads = full_payloads

    rows = []

    for payload in payloads:
        cycle = frame2_socket_cycle(payload, args.r)
        c = classify_cycle(cycle, args.r)
        asm = witness_assembly(c["normalized_cycle"], args.r)
        is_exact = payload == "t2"
        row = {
            "payload": payload,
            "normalized_cycle": c["normalized_cycle"],
            "classification": c["classification"],
            "confidence": c["confidence"],
            "best_action_distance": c["distance_summary"]["best_action_distance"],
            "nearest_action_frames": nearest_action_frames(c),
            "branch": "exact junction" if is_exact else "punctured socket branch",
            "assembly": asm,
        }
        rows.append(row)

    result = {
        "frame2_exact_prototype": frame2_exact_prototype(args.r),
        "mode": "bounded" if args.bounded else "full",
        "rows": rows,
        "summary": {
            "exact_junction_count": sum(1 for r in rows if r["branch"] == "exact junction"),
            "punctured_branch_count": sum(1 for r in rows if r["branch"] == "punctured socket branch"),
            "payloads": [r["payload"] for r in rows],
        },
    }

    text = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        if getattr(args, "pretty", False):
            print(_render_pretty_socket_family(result))
        else:
            print(text)
    return 0


def cmd_audit_neighborhood(args: argparse.Namespace) -> int:
    kids = _one_edit_variants(args.cycle, args.r)

    classification_hist = {}
    confidence_hist = {}
    best_action_hist = {}
    nearest_frame_hist = {}
    slot4_trans = {}

    examples = {
        "exact": [],
        "action_nearest": [],
        "ambiguous": [],
    }

    parent_norm = normalize_cycle(args.cycle)
    parent_slot4 = parent_norm[4] if len(parent_norm) > 4 else None

    for item in kids:
        c = classify_cycle(item["cycle"], args.r)

        classification_hist[c["classification"]] = classification_hist.get(c["classification"], 0) + 1
        confidence_hist[c["confidence"]] = confidence_hist.get(c["confidence"], 0) + 1

        a = c["distance_summary"].get("best_action_distance")
        best_action_hist[a] = best_action_hist.get(a, 0) + 1

        frames = nearest_action_frames(c)
        for f in frames:
            nearest_frame_hist[f] = nearest_frame_hist.get(f, 0) + 1

        child_norm = c["normalized_cycle"]
        child_slot4 = child_norm[4] if len(child_norm) > 4 else None
        if parent_slot4 is not None and child_slot4 is not None:
            key = (parent_slot4, child_slot4)
            slot4_trans[key] = slot4_trans.get(key, 0) + 1

        row = {
            "label": item["label"],
            "classification": c["classification"],
            "confidence": c["confidence"],
            "best_action_distance": a,
            "normalized_cycle": child_norm,
        }

        if c["classification"] == "action-cell" and c["confidence"] == "exact":
            if len(examples["exact"]) < 10:
                examples["exact"].append(row)
        elif c["classification"] == "action-cell" and c["confidence"] == "nearest":
            if len(examples["action_nearest"]) < 10:
                examples["action_nearest"].append(row)
        elif c["confidence"] == "ambiguous":
            if len(examples["ambiguous"]) < 10:
                examples["ambiguous"].append(row)

    summary = {
        "cycle": args.cycle,
        "normalized_cycle": normalize_cycle(args.cycle),
        "child_count": len(kids),
        "classification_histogram": dict(sorted(classification_hist.items())),
        "confidence_histogram": dict(sorted(confidence_hist.items())),
        "best_action_distance_histogram": dict(
            sorted(best_action_hist.items(), key=lambda kv: (kv[0] is None, kv[0]))
        ),
        "nearest_action_frame_histogram": dict(sorted(nearest_frame_hist.items())),
        "slot4_transition_histogram": [
            {"from": a, "to": b, "count": n}
            for (a, b), n in sorted(slot4_trans.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        "examples": examples,
    }

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(render_audit_neighborhood(summary))
    return 0


def _render_pretty_assembly(result: dict[str, Any]) -> str:
    asm = result["assembly"]
    a = asm["assembly"]
    s = asm["scaffold_register"]
    frames = result.get("nearest_action_frames", [])
    frame_text = ",".join(str(x) for x in frames) if frames else "none"

    lines = []
    lines.append(f"assembly   : [W,X,Y,Z,T,I] = [{a['W']},{a['X']},{a['Y']},{a['Z']},{a['T']},{a['I']}]")
    lines.append(f"witness    : {'-'.join(asm['closed_witness_word'])}")
    lines.append(f"scaffold   : [{s['W']},{s['X']},{s['Y']},{s['Z']},{s['I']}]")
    lines.append(f"socket     : {asm['socket']}")
    lines.append(f"payload    : {asm['payload']}")
    lines.append(f"exact      : {asm['exact_frame2_payload']}")
    lines.append(f"installed  : {'yes' if asm['is_exact_payload'] else 'no'}")
    lines.append(
        f"branch     : {'exact junction' if asm['is_exact_payload'] else 'punctured socket branch'}"
    )
    lines.append(
        f"status     : {result['classification']} / {result['confidence']} / "
        f"A={result['distance_summary']['best_action_distance']} / frame={frame_text}"
    )
    lines.append(f"rigid edges: {', '.join(asm['rigid_edges'])}")
    lines.append(f"var edges  : {', '.join(asm['variable_edges'])}")
    lines.append(f"diads      : {', '.join(asm['diads'])}")
    lines.append(f"couplers   : {', '.join(asm['couplers'])}")
    return "\n".join(lines)


def _render_pretty_socket_neighborhood(result: dict[str, Any]) -> str:
    summary = result["summary"]
    asm = result["assembly"]["assembly"]
    payload_hist = summary.get("payload_histogram", {})
    payloads = ", ".join(payload_hist.keys()) if payload_hist else "none"
    mismatch_hist = summary.get("mismatch_histogram_vs_E2", {})
    mismatch_text = ", ".join(f"{k}:{v}" for k, v in mismatch_hist.items()) if mismatch_hist else "none"

    lines = []
    lines.append(f"assembly      : [W,X,Y,Z,T,I] = [{asm['W']},{asm['X']},{asm['Y']},{asm['Z']},{asm['T']},{asm['I']}]")
    lines.append(f"parent payload: {result['parent_payload']}")
    lines.append(f"seam children : {summary['seam_child_count']}")
    lines.append(f"payloads      : {payloads}")
    lines.append(f"mismatch hist : {mismatch_text}")
    lines.append(f"t2 children   : {summary['t2_child_count']}")
    lines.append(f"off scaffold  : {summary['off_scaffold_child_count']}")
    lines.append(f"exact children: {summary['exact_child_count']}")
    closure_ok = (
        summary.get("t2_child_count", 0) == 0
        and summary.get("off_scaffold_child_count", 0) == 0
        and summary.get("mismatch_histogram_vs_E2", {}) == {"[4]": summary.get("seam_child_count", 0)}
    )
    lines.append(f"closure       : {'yes' if closure_ok else 'no'}")
    if result.get("seam_children"):
        lines.append("")
        lines.append("children:")
        for row in result["seam_children"][:12]:
            lines.append(
                f"  {row['socket_payload']:<3} :: "
                f"{row['label']} :: "
                f"mism={row['mismatch_positions_vs_E2']}"
            )
        if len(result["seam_children"]) > 12:
            lines.append(f"  ... ({len(result['seam_children']) - 12} more)")
    return "\n".join(lines)



def _render_pretty_socket_family(result: dict[str, Any]) -> str:
    lines = []
    lines.append(f"frame2 socket family ({result.get('mode', 'full')})")
    lines.append(f"exact prototype: {result['frame2_exact_prototype']}")
    lines.append("")
    for row in result["rows"]:
        a = row["assembly"]["assembly"]
        lines.append(
            f"{row['payload']:<3} :: "
            f"[{a['W']},{a['X']},{a['Y']},{a['Z']},{a['T']},{a['I']}] :: "
            f"{row['classification']}/{row['confidence']} :: "
            f"A={row['best_action_distance']} :: "
            f"frame={','.join(str(x) for x in row['nearest_action_frames']) if row['nearest_action_frames'] else 'none'} :: "
            f"{row['branch']}"
        )
    lines.append("")
    lines.append("summary:")
    lines.append(f"  exact junctions : {result['summary']['exact_junction_count']}")
    lines.append(f"  punctured branch: {result['summary']['punctured_branch_count']}")
    lines.append(f"  payloads        : {', '.join(result['summary']['payloads'])}")
    return "\n".join(lines)



def _render_pretty_so_family(result: dict[str, Any]) -> str:
    lines = []
    lines.append("subjective/objective family")
    lines.append("rule: subjective = return / 4 / 26 ; objective = forward / 5 / 18")
    lines.append("")
    for row in result["rows"]:
        s = row["subjective"]
        o = row["objective"]
        sa = s["assembly"]["assembly"]
        oa = o["assembly"]["assembly"]
        lines.append(f"i={row['i']}")
        lines.append(
            f"  S :: [{sa['W']},{sa['X']},{sa['Y']},{sa['Z']},{sa['T']},{sa['I']}] :: "
            f"{s['alignment']} / spread={s['spread']} / fiber={s['fiber']}"
        )
        lines.append(
            f"  O :: [{oa['W']},{oa['X']},{oa['Y']},{oa['Z']},{oa['T']},{oa['I']}] :: "
            f"{o['alignment']} / spread={o['spread']} / fiber={o['fiber']}"
        )
    return "\n".join(lines)


def cmd_so_family(args: argparse.Namespace) -> int:
    result = subjective_objective_family(args.r)
    text = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        if getattr(args, "pretty", False):
            print(_render_pretty_so_family(result))
        else:
            print(text)
    return 0



def _render_pretty_so_orbit(result: dict[str, Any]) -> str:
    s0 = result["subjective_start"]
    o0 = result["objective_start"]
    g15 = result["after_g15"]
    g30 = result["after_g30"]

    lines = []
    lines.append(f"subjective/objective orbit at i={result['i']}")
    lines.append(f"G15 length : {result['g15_length']}")
    lines.append(f"G30 length : {result['g30_length']}")
    lines.append("")
    lines.append(
        f"S0         : {s0['sheet_state']} :: {'-'.join(s0['cycle'] + [s0['cycle'][0]])} :: "
        f"{s0['alignment']} / spread={s0['spread']} / fiber={s0['fiber']}"
    )
    lines.append(
        f"O0         : {o0['sheet_state']} :: {'-'.join(o0['cycle'] + [o0['cycle'][0]])} :: "
        f"{o0['alignment']} / spread={o0['spread']} / fiber={o0['fiber']}"
    )
    lines.append("")
    lines.append(
        f"after G15  : S->{g15['subjective_sheet_state']} / O->{g15['objective_sheet_state']} :: "
        f"{g15['sign_closing_rule']}"
    )
    lines.append(
        f"after G30  : S->{g30['subjective_sheet_state']} / O->{g30['objective_sheet_state']} :: "
        f"{g30['identity_restoring_rule']}"
    )
    lines.append("")
    lines.append("sheet rule : one full G15 walk flips sheet; two full passes restore it")
    lines.append("readout    : one full G15 walk is sign-closing; two passes restore identity")
    return "\n".join(lines)


def cmd_so_orbit(args: argparse.Namespace) -> int:
    result = so_orbit_summary(args.i, args.r)
    text = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        if getattr(args, "pretty", False):
            print(_render_pretty_so_orbit(result))
        else:
            print(text)
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

    assembly = sub.add_parser("assembly")
    assembly.add_argument("--cycle", type=parse_cycle)
    assembly.add_argument("--input")
    assembly.add_argument("--t", type=parse_t_value)
    assembly.add_argument("--out")
    assembly.add_argument("--pretty", action="store_true")
    assembly.set_defaults(func=cmd_assembly)

    socket_nb = sub.add_parser("socket-neighborhood")
    socket_nb.add_argument("--cycle", type=parse_cycle)
    socket_nb.add_argument("--input")
    socket_nb.add_argument("--t", type=parse_t_value)
    socket_nb.add_argument("--out")
    socket_nb.add_argument("--pretty", action="store_true")
    socket_nb.set_defaults(func=cmd_socket_neighborhood)

    socket_family = sub.add_parser("socket-family")
    socket_family.add_argument("--out")
    socket_family.add_argument("--pretty", action="store_true")
    socket_family.add_argument("--bounded", action="store_true")
    socket_family.set_defaults(func=cmd_socket_family)

    so_family = sub.add_parser("so-family")
    so_family.add_argument("--out")
    so_family.add_argument("--pretty", action="store_true")
    so_family.set_defaults(func=cmd_so_family)

    so_orbit = sub.add_parser("so-orbit")
    so_orbit.add_argument("--i", type=int, default=0)
    so_orbit.add_argument("--out")
    so_orbit.add_argument("--pretty", action="store_true")
    so_orbit.set_defaults(func=cmd_so_orbit)


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

    explain = sub.add_parser("explain-cycle")
    explain.add_argument("--cycle", type=parse_cycle, required=True)
    explain.add_argument("--show-diff")
    explain.set_defaults(func=cmd_explain_cycle)

    audit = sub.add_parser("audit-neighborhood")
    audit.add_argument("--cycle", type=parse_cycle, required=True)
    audit.add_argument("--json", action="store_true")
    audit.set_defaults(func=cmd_audit_neighborhood)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
