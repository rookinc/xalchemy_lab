from __future__ import annotations

import json
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path


CORE = ["e00", "e01", "e02", "e04", "e05", "e07", "e10"]
BOUNDARY = ["e03", "e06", "e11", "e12", "e14", "e15"]
SPECTATORS = ["e13", "e16", "e22", "e25"]
TRIPLE_SETS = [
    ("twist_cluster", ["e01", "e04", "e07"]),
    ("square_cluster", ["e02", "e05", "e10"]),
]


def load_json(path: str):
    return json.loads(Path(path).read_text())


def sheet(v: str) -> str:
    if v.endswith("+"):
        return "+"
    if v.endswith("-"):
        return "-"
    raise ValueError(f"bad lift vertex: {v}")


def flip_lift_pair(rows, edge_label: str):
    out = []
    seen = 0
    for row in rows:
        label, u, v = row
        if label != edge_label:
            out.append(row)
            continue
        new_v = v[:-1] + ("-" if v.endswith("+") else "+")
        out.append([label, u, new_v])
        seen += 1
    if seen != 2:
        raise ValueError(f"edge {edge_label} appears {seen} times, expected 2")
    return out


def derive_edge_cocycle(data):
    lift_edges = {}
    for label, u, v in data["lift_edges"]:
        if "TBD" in u or "TBD" in v:
            continue
        lift_edges.setdefault(label, []).append((u, v))

    result = {}
    for label, _u0, _v0 in data["base_edges"]:
        pairs = lift_edges.get(label, [])
        if len(pairs) != 2:
            continue
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


def signature_from_invariants(inv):
    A, sigma, tau = inv
    return 0, (A + sigma) % 2, (A + tau) % 2


def run_trial(source, flips):
    trial = deepcopy(source)
    for edge in flips:
        trial["lift_edges"] = flip_lift_pair(trial["lift_edges"], edge)
    cocycle = derive_edge_cocycle(trial)
    return invariants(cocycle)


def main() -> None:
    source = load_json("specs/paper/bridge/signed_lift_source_v1.json")

    trials = [("baseline", [])]
    for e in CORE:
        trials.append((f"single_core_{e}", [e]))
    for e in BOUNDARY:
        trials.append((f"single_boundary_{e}", [e]))
    for e in SPECTATORS:
        trials.append((f"single_spectator_{e}", [e]))
    for e1, e2 in combinations(CORE, 2):
        trials.append((f"double_core_{e1}_{e2}", [e1, e2]))
    for label, edges in TRIPLE_SETS:
        trials.append((label, edges))

    seen = {}
    for label, flips in trials:
        inv = run_trial(source, flips)
        seen.setdefault(inv, []).append((label, flips))

    print("\n====================")
    print("BRIDGE INVARIANT PHASE PORTRAIT")
    print("====================\n")

    for inv in product([0, 1], repeat=3):
        sig = signature_from_invariants(inv)
        realized = inv in seen
        print(f"invariants {inv} -> signature {sig}  realized={'YES' if realized else 'NO'}")
        if realized:
            for label, flips in seen[inv]:
                print(f"  {label:28s} flips={flips}")
        print()

    out = {
        "name": "bridge_invariant_phase_portrait_v1",
        "version": "0.1",
        "quotient_map": "(A,sigma,tau) -> (0,A+sigma,A+tau)",
        "states": []
    }

    for inv in product([0, 1], repeat=3):
        sig = signature_from_invariants(inv)
        out["states"].append({
            "invariants": {"A": inv[0], "sigma": inv[1], "tau": inv[2]},
            "signature": {"return": sig[0], "square": sig[1], "twist": sig[2]},
            "realized": inv in seen,
            "realizations": [
                {"label": label, "flips": flips}
                for label, flips in seen.get(inv, [])
            ],
        })

    Path("specs/paper/g60/bridge_invariant_phase_portrait_v1.json").write_text(json.dumps(out, indent=2) + "\n")
    print("Wrote specs/paper/g60/bridge_invariant_phase_portrait_v1.json")


if __name__ == "__main__":
    main()
