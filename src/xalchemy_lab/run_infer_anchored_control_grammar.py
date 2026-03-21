from __future__ import annotations

import json
from collections import defaultdict
from copy import deepcopy
from pathlib import Path


STATE_FLIPS = [
    ("000", ["e01"]),
    ("001", []),
    ("010", ["e01", "e02"]),
    ("011", ["e02"]),
    ("100", ["e00", "e01"]),
    ("101", ["e00"]),
    ("110", ["e00", "e01", "e02"]),
    ("111", ["e00", "e02"]),
]

TARGET_TRACES = [
    ("A", "O", "O", "O"),
    ("A", "E1", "E1", "E1"),
    ("A", "E2", "E2", "E2"),
    ("E1", "E1", "E1", "O"),
    ("E1", "E1", "E1", "E2"),
]

SECTOR_BY_EDGE = {
    "e00": "A",
    "e01": "O", "e04": "O", "e07": "O",
    "e02": "E1", "e05": "E1", "e08": "E1", "e10": "E1", "e11": "E1", "e12": "E1", "e15": "E1",
    "e03": "E2", "e06": "E2", "e09": "E2", "e13": "E2", "e14": "E2", "e17": "E2", "e20": "E2", "e23": "E2", "e24": "E2", "e25": "E2",
    "e16": "M+", "e18": "M+", "e19": "M+", "e21": "M+", "e26": "M+",
    "e22": "D", "e27": "D",
    "e28": "X", "e29": "X",
}


def load_json(path: str):
    return json.loads(Path(path).read_text())


def sheet(v: str) -> str:
    return "+" if v.endswith("+") else "-"


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


def catalog_for_flips(source, flips):
    trial = deepcopy(source)
    for edge in flips:
        trial["lift_edges"] = flip_lift_pair(trial["lift_edges"], edge)

    edge_cocycle = derive_edge_cocycle(trial)
    inv = invariants(edge_cocycle)

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

    return inv, by_trace


def tag(x: int) -> str:
    return "ODD" if x else "EVEN"


def main() -> None:
    source = load_json("specs/signed_lift_source_v1.json")

    observed = {}
    for name, flips in STATE_FLIPS:
        inv, by_trace = catalog_for_flips(source, flips)
        observed[name] = {
            "invariants": inv,
            "trace_parity": {trace: by_trace.get(trace) for trace in TARGET_TRACES},
        }

    print("\n====================")
    print("INFER ANCHORED CONTROL GRAMMAR")
    print("====================\n")

    header = "state".ljust(8) + "  " + "  ".join(str(t).ljust(22) for t in TARGET_TRACES)
    print(header)
    print("-" * len(header))
    for name, _flips in STATE_FLIPS:
        row = [name.ljust(8)]
        for trace in TARGET_TRACES:
            row.append(tag(observed[name]["trace_parity"][trace]).ljust(22))
        print("  ".join(row))

    print("\n====================")
    print("CHART SPLIT")
    print("====================\n")
    for A_val in (0, 1):
        print(f"A = {A_val}")
        for name, _flips in STATE_FLIPS:
            inv = observed[name]["invariants"]
            if inv[0] != A_val:
                continue
            sigma, tau = inv[1], inv[2]
            vals = ", ".join(f"{trace}={tag(observed[name]['trace_parity'][trace])}" for trace in TARGET_TRACES)
            print(f"  state={name}  (sigma,tau)=({sigma},{tau})  {vals}")
        print()

    print("====================")
    print("WORKING READ")
    print("====================\n")
    print("A=0 chart:")
    print("  (A,O,O,O) tracks tau")
    print("  (A,E1,E1,E1) tracks sigma")
    print("  (A,E2,E2,E2) stays EVEN")
    print("  shuttle traces depend on interaction of sigma and tau")
    print()
    print("A=1 chart:")
    print("  anchored behavior is different and must be treated as a separate local chart")
    print("  (A,E2,E2,E2) is always ODD in observed states")
    print("  (A,E1,E1,E1) is ODD except when (sigma,tau)=(1,0)")
    print("  (A,O,O,O) is ODD except when (sigma,tau)=(0,1)")
    print()

    out = {
        "name": "anchored_control_grammar_v1",
        "target_traces": [list(t) for t in TARGET_TRACES],
        "states": {
            name: {
                "invariants": list(observed[name]["invariants"]),
                "trace_parity": {str(trace): observed[name]["trace_parity"][trace] for trace in TARGET_TRACES},
            }
            for name, _ in STATE_FLIPS
        },
    }
    Path("specs/anchored_control_grammar_v1.json").write_text(json.dumps(out, indent=2) + "\n")
    print("Wrote specs/anchored_control_grammar_v1.json")


if __name__ == "__main__":
    main()
