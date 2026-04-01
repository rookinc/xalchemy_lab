#!/usr/bin/env python3
from __future__ import annotations

from g15_cocycle_decode import VERTICES, EDGES

ADJ = {v: set() for v in VERTICES}
for a, b in EDGES:
    ADJ[a].add(b)
    ADJ[b].add(a)

START = "o0"
N = len(VERTICES)

def canon_cycle(cycle: list[str]) -> tuple[str, ...]:
    cyc = cycle[:-1] if cycle[0] == cycle[-1] else cycle[:]
    rots = [tuple(cyc[i:] + cyc[:i]) for i in range(len(cyc))]
    rev = list(reversed(cyc))
    rots += [tuple(rev[i:] + rev[:i]) for i in range(len(rev))]
    return min(rots)

seen = set()
solutions = []

def dfs(path: list[str], used: set[str]) -> None:
    cur = path[-1]
    if len(path) == N:
        if START in ADJ[cur]:
            cyc = path + [START]
            key = canon_cycle(cyc)
            if key not in seen:
                seen.add(key)
                solutions.append(cyc)
        return

    for nxt in sorted(ADJ[cur]):
        if nxt in used:
            continue
        used.add(nxt)
        path.append(nxt)
        dfs(path, used)
        path.pop()
        used.remove(nxt)

dfs([START], {START})

print(f"hamiltonian_cycle_count={len(solutions)}")
for i, cyc in enumerate(solutions[:20]):
    print(f"{i}: {'-'.join(cyc)}")
