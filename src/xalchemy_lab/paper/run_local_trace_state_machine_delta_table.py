from __future__ import annotations

import json
from collections import defaultdict
from copy import deepcopy
from pathlib import Path


SECTOR_BY_EDGE = {
    "e00": "A",
    "e01": "O", "e04": "O", "e07": "O",
    "e02": "E1", "e05": "E1", "e08": "E1", "e10": "E1", "e11": "E1", "e12": "E1", "e15": "E1",
    "e03": "E2", "e06": "E2", "e09": "E2", "e13": "E2", "e14": "E2", "e17": "E2", "e20": "E2", "e23": "E2", "e24": "E2", "e25": "E2",
    "e16": "M+", "e18": "M+", "e19": "M+", "e21": "M+", "e26": "M+",
    "e22": "D", "e27": "D",
    "e28": "X", "e29": "X",
}

STATE_SPECS = [
    ("001_baseline", []),
    ("000_tau_off", ["e01"]),
    ("011_sigma_on", ["e02"]),
    ("010_sigma_on_tau_off", ["e01", "e02"]),
    ("110_alt_preimage", ["e00", "e01", "e02"]),
]


def load_json(path: str):
    return json.loads(Path(path).read_text())


def sheet(v: str) -> str:
    if v.endswith("+"):
        return "+"
    if v.endswith("-"):
        return "-"
    raise ValueError(v)


def flip_lift_pair(rows, edge_label: str):
    out = []
    seen = 0
    for label, u, v in rows:
        if label != edge_label:
            out.append([label, u, v])
            continue
        new_v = v[:-1] + ("-" if v.endswith("+") else "+")
        out.append([label, u, new_v])
        seen += 1
    if seen != 2:
        raise ValueError(f"{edge_label} appears {seen} times")
    return out


def derive_edge_cocycle(data):
    lift_edges = defaultdict(list)
    for label, u, v in data["lift_edges"]:
        lift_edges[label].append((u, v))

    result = {}
    for label, _u, _v in data["base_edges"]:
        pairs = lift_edges[label]
        crossed0 = sheet(pairs[0][0]) != sheet(pairs[0][1])
        crossed1 = sheet(pairs[1][0]) != sheet(pairs[1][1])
        if crossed0 != crossed1:
            raise ValueError(f"inconsistent lift type for {label}")
        result[label] = 1 if crossed0 else 0
    return result


def invariants(edge_cocycle):
    A = edge_cocycle["e00"] % 2
    sigma = (edge_cocycle["e02"] + edge_cocycle["e05"] + edge_cocycle["e10"]) % 2
    tau = (edge_cocycle["e01"] + edge_cocycle["e04"] + edge_cocycle["e07"]) % 2
    return A, sigma, tau


def bridge_signature(inv):
    A, sigma, tau = inv
    return 0, (A + sigma) % 2, (A + tau) % 2


def canonical_cycle(edges):
    n = len(edges)
    rots = [tuple(edges[i:] + edges[:i]) for i in range(n)]
    rev = list(reversed(edges))
    rots += [tuple(rev[i:] + rev[:i]) for i in range(n)]
    return min(rots)


def canonical_trace(trace):
    n = len(trace)
    rots = [tuple(trace[i:] + trace[:i]) for i in range(n)]
    rev = list(reversed(trace))
    rots += [tuple(rev[i:] + rev[:i]) for i in range(n)]
    return min(rots)


def state_catalog(base_source: dict, flips: list[str]):
    trial = deepcopy(base_source)
    for edge in flips:
        trial["lift_edges"] = flip_lift_pair(trial["lift_edges"], edge)

    edge_cocycle = derive_edge_cocycle(trial)
    inv = invariants(edge_cocycle)
    sig = bridge_signature(inv)

    nbrs = defaultdict(list)
    edge_between = {}
    for label, u, v in trial["base_edges"]:
        nbrs[u].append((v, label))
        nbrs[v].append((u, label))
        edge_between[frozenset((u, v))] = label

    seen = set()
    by_trace = {}

    for q0 in sorted(nbrs):
        for q1, e01 in nbrs[q0]:
            if q1 == q0:
                continue
            for q2, e12 in nbrs[q1]:
                if q2 in {q0, q1}:
                    continue
                for q3, e23 in nbrs[q2]:
                    if q3 in {q0, q1, q2}:
                        continue
                    if frozenset((q3, q0)) not in edge_between:
                        continue
                    e30 = edge_between[frozenset((q3, q0))]
                    cycle_edges = [e01, e12, e23, e30]
                    key = canonical_cycle(cycle_edges)
                    if key in seen:
                        continue
                    seen.add(key)
                    parity = sum(edge_cocycle[e] for e in cycle_edges) % 2
                    trace = canonical_trace([SECTOR_BY_EDGE.get(e, "?") for e in cycle_edges])
                    by_trace[trace] = parity

    return {
        "invariants": inv,
        "bridge_signature": sig,
        "trace_parity": by_trace,
    }


def parity_tag(v: int | None) -> str:
    if v is None:
        return "-"
    return "ODD" if v == 1 else "EVEN"


def main() -> None:
    source = load_json("specs/paper/bridge/signed_lift_source_v1.json")

    states = {}
    all_traces = set()

    for name, flips in STATE_SPECS:
        catalog = state_catalog(source, flips)
        states[name] = {"flips": flips, **catalog}
        all_traces.update(catalog["trace_parity"].keys())

    state_names = [name for name, _ in STATE_SPECS]

    print("\n====================")
    print("LOCAL TRACE STATE MACHINE DELTA TABLE")
    print("====================\n")

    print("state summaries\n")
    for name in state_names:
        st = states[name]
        print(f"{name}")
        print(f"  flips            = {st['flips']}")
        print(f"  invariants       = {st['invariants']}")
        print(f"  bridge_signature = {st['bridge_signature']}")
        print()

    print("====================")
    print("TRACE PARITY TABLE")
    print("====================\n")

    header = "trace".ljust(26) + "  " + "  ".join(name.ljust(22) for name in state_names)
    print(header)
    print("-" * len(header))

    for trace in sorted(all_traces):
        row = [str(trace).ljust(26)]
        for name in state_names:
            p = states[name]["trace_parity"].get(trace)
            row.append(parity_tag(p).ljust(22))
        print("  ".join(row))

    print("\n====================")
    print("PAIRWISE DELTAS")
    print("====================\n")

    for i in range(len(state_names) - 1):
        left = state_names[i]
        right = state_names[i + 1]
        print(f"{left}  ->  {right}")
        flips = []
        for trace in sorted(all_traces):
            lp = states[left]["trace_parity"].get(trace)
            rp = states[right]["trace_parity"].get(trace)
            if lp != rp:
                flips.append((trace, lp, rp))

        if not flips:
            print("  no trace parity changes")
        else:
            for trace, lp, rp in flips:
                print(f"  {trace}: {parity_tag(lp)} -> {parity_tag(rp)}")
        print()

    out = {
        "name": "local_trace_state_machine_delta_table_v1",
        "states": {
            name: {
                "flips": states[name]["flips"],
                "invariants": list(states[name]["invariants"]),
                "bridge_signature": list(states[name]["bridge_signature"]),
                "trace_parity": {str(k): v for k, v in states[name]["trace_parity"].items()},
            }
            for name in state_names
        }
    }
    Path("specs/paper/g60/local_trace_state_machine_delta_table_v1.json").write_text(json.dumps(out, indent=2) + "\n")
    print("Wrote specs/paper/g60/local_trace_state_machine_delta_table_v1.json")


if __name__ == "__main__":
    main()
