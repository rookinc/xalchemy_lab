from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from g15_graph import edge_index, edge_vector_from_support, build_fundamental_cycle_basis
from g15_cocycle_decode import build_B, classify_support

A = build_fundamental_cycle_basis()
B = build_B()

def syndrome_from_x(A, x):
    bits = []
    for row in A:
        s = 0
        for a, b in zip(row, x):
            s ^= (a & b)
        bits.append(str(s))
    return "".join(bits)

def parse_vertex(v: str):
    return v[0], int(v[1:])

def cyc_dist(a: int, b: int, n: int = 5) -> int:
    d = abs(a - b) % n
    return min(d, n - d)

def cycle_to_support_indices(cyc):
    out = []
    for i in range(len(cyc)):
        u = cyc[i]
        v = cyc[(i + 1) % len(cyc)]
        out.append(edge_index(u, v))
    return sorted(out)

def subjective_cycle(i: int):
    return [
        f"o{i%5}",
        f"o{(i+1)%5}",
        f"o{(i+2)%5}",
        f"s{(i+2)%5}",
        f"t{i%5}",
        f"s{i%5}",
    ]

def objective_cycle(i: int):
    return [
        f"o{i%5}",
        f"o{(i+1)%5}",
        f"o{(i+2)%5}",
        f"s{(i+3)%5}",
        f"t{(i+3)%5}",
        f"s{i%5}",
    ]

def alignment_and_spread(cyc):
    W, X, Y, Z, T, I = cyc
    _, y_idx = parse_vertex(Y)
    _, z_idx = parse_vertex(Z)
    _, t_idx = parse_vertex(T)
    _, i_idx = parse_vertex(I)

    if t_idx == z_idx:
        alignment = "forward_aligned"
    elif t_idx == i_idx:
        alignment = "return_aligned"
    else:
        alignment = "split_aligned"

    d_yz = cyc_dist(y_idx, z_idx)
    d_zt = cyc_dist(z_idx, t_idx)
    d_ti = cyc_dist(t_idx, i_idx)
    d_iy = cyc_dist(i_idx, y_idx)
    spread_score = d_yz + d_zt + d_ti + d_iy

    return alignment, spread_score

supports = list(itertools.combinations(range(30), 6))
fiber_cache = {}

def fiber_stats_for_syndrome(syndrome: str):
    if syndrome in fiber_cache:
        return fiber_cache[syndrome]

    fiber_rows = []
    for support in supports:
        x = edge_vector_from_support(support)
        syn = syndrome_from_x(A, x)
        if syn != syndrome:
            continue
        closed, connected, support_type, boundary_vertices = classify_support(x, B)
        fiber_rows.append({
            "closed": closed,
            "connected": connected,
            "support_type": support_type,
            "support": list(support),
        })

    others = [r for r in fiber_rows if r["support_type"] != "C6"]
    out = {
        "fiber_size": len(fiber_rows),
        "other_count": len(others),
        "other_connected_count": sum(1 for r in others if r["connected"]),
        "other_closed_count": sum(1 for r in others if r["closed"]),
    }
    out["score"] = [
        out["other_closed_count"],
        out["other_connected_count"],
        out["other_count"],
    ]
    out["top_class"] = (out["score"] == [0, 0, 17])
    fiber_cache[syndrome] = out
    return out

def collect(name: str, family_fn):
    rows = []
    for i in range(5):
        cyc = family_fn(i)
        support = cycle_to_support_indices(cyc)
        x = edge_vector_from_support(support)
        syndrome = syndrome_from_x(A, x)
        closed, connected, support_type, boundary_vertices = classify_support(x, B)

        alignment, spread_score = alignment_and_spread(cyc)
        fiber = fiber_stats_for_syndrome(syndrome)

        rows.append({
            "i": i,
            "cycle_vertices": cyc,
            "support_indices": support,
            "syndrome": syndrome,
            "support_type": support_type,
            "alignment": alignment,
            "spread_score": spread_score,
            **fiber,
        })

    out = {
        "family": name,
        "count_found": len(rows),
        "fiber_size_histogram": {},
        "alignment_histogram": {},
        "spread_histogram": {},
        "top_class_count": 0,
        "rows": rows,
    }

    for r in rows:
        out["fiber_size_histogram"][str(r["fiber_size"])] = out["fiber_size_histogram"].get(str(r["fiber_size"]), 0) + 1
        out["alignment_histogram"][r["alignment"]] = out["alignment_histogram"].get(r["alignment"], 0) + 1
        out["spread_histogram"][str(r["spread_score"])] = out["spread_histogram"].get(str(r["spread_score"]), 0) + 1
        if r["top_class"]:
            out["top_class_count"] += 1

    return out

payload = {
    "subjective_family": collect("subjective_family", subjective_cycle),
    "objective_family": collect("objective_family", objective_cycle),
}

print(json.dumps(payload, indent=2))
Path("artifacts/g15_subjective_objective_test.json").write_text(json.dumps(payload, indent=2))
print("\nWrote artifacts/g15_subjective_objective_test.json")
