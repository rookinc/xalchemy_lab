from __future__ import annotations

from collections import deque
from typing import Dict, List, Tuple

Vertex = str
Edge = Tuple[Vertex, Vertex]

OUTERS = [f"o{i}" for i in range(5)]
SPOKES = [f"s{i}" for i in range(5)]
INNERS = [f"t{i}" for i in range(5)]
VERTICES: List[Vertex] = OUTERS + SPOKES + INNERS
VERTEX_INDEX: Dict[Vertex, int] = {v: i for i, v in enumerate(VERTICES)}

# Original Petersen graph edge labels underlying the line graph G15.
# We use:
#   o_i = outer edge U_i-U_{i+1}
#   s_i = spoke edge U_i-V_i
#   t_i = inner edge V_i-V_{i+2}
#
# With this convention:
#   o_i-o_{i+1}-o_{i+2}-s_{i+3}-t_{i+3}-s_i-o_i
# and
#   o_i-o_{i+1}-o_{i+2}-s_{i+2}-t_i-s_i-o_i
# are both valid 6-cycles in L(Petersen).

def mod5(i: int) -> int:
    return i % 5

def original_endpoints(label: Vertex) -> Tuple[str, str]:
    kind = label[0]
    i = int(label[1:])
    if kind == "o":
        return (f"U{i}", f"U{mod5(i+1)}")
    if kind == "s":
        return (f"U{i}", f"V{i}")
    if kind == "t":
        return (f"V{i}", f"V{mod5(i+2)}")
    raise ValueError(f"Unknown vertex label: {label}")

def shares_endpoint(a: Vertex, b: Vertex) -> bool:
    ea = set(original_endpoints(a))
    eb = set(original_endpoints(b))
    return len(ea & eb) > 0

def build_edge_list() -> List[Edge]:
    edges: List[Edge] = []
    for i, u in enumerate(VERTICES):
        for v in VERTICES[i + 1 :]:
            if shares_endpoint(u, v):
                edges.append((u, v))
    return edges

EDGES: List[Edge] = build_edge_list()
EDGE_INDEX: Dict[Edge, int] = {e: i for i, e in enumerate(EDGES)}

def edge_index(u: Vertex, v: Vertex) -> int:
    e = (u, v) if VERTEX_INDEX[u] < VERTEX_INDEX[v] else (v, u)
    return EDGE_INDEX[e]

def build_neighbors() -> Dict[Vertex, List[Vertex]]:
    nbrs: Dict[Vertex, List[Vertex]] = {v: [] for v in VERTICES}
    for u, v in EDGES:
        nbrs[u].append(v)
        nbrs[v].append(u)
    for v in VERTICES:
        nbrs[v].sort(key=lambda x: VERTEX_INDEX[x])
    return nbrs

NEIGHBORS = build_neighbors()

def vertex_type(v: Vertex) -> str:
    return v[0].upper()

def canonical_cycle_word(word: List[str]) -> List[str]:
    rots = [tuple(word[i:] + word[:i]) for i in range(len(word))]
    rev = list(reversed(word))
    rots += [tuple(rev[i:] + rev[:i]) for i in range(len(word))]
    return list(min(rots))

def edge_vector_from_support(support: Tuple[int, ...] | List[int]) -> List[int]:
    x = [0] * len(EDGES)
    for idx in support:
        x[idx] = 1
    return x

def support_edge_indices_from_x(x: List[int]) -> List[int]:
    return [i for i, bit in enumerate(x) if bit]

def support_vertex_degrees(edge_indices: List[int]) -> Dict[Vertex, int]:
    deg = {v: 0 for v in VERTICES}
    for idx in edge_indices:
        u, v = EDGES[idx]
        deg[u] += 1
        deg[v] += 1
    return deg

def support_neighbors(edge_indices: List[int]) -> Dict[Vertex, List[Vertex]]:
    nbrs: Dict[Vertex, List[Vertex]] = {v: [] for v in VERTICES}
    for idx in edge_indices:
        u, v = EDGES[idx]
        nbrs[u].append(v)
        nbrs[v].append(u)
    for v in VERTICES:
        nbrs[v].sort(key=lambda x: VERTEX_INDEX[x])
    return nbrs

def support_components(edge_indices: List[int]) -> List[Dict[str, object]]:
    nbrs = support_neighbors(edge_indices)
    used = set()
    comps = []

    active_vertices = [v for v in VERTICES if nbrs[v]]
    for start in active_vertices:
        if start in used:
            continue
        q = deque([start])
        used.add(start)
        verts = []
        e_set = set()
        while q:
            u = q.popleft()
            verts.append(u)
            for w in nbrs[u]:
                e = (u, w) if VERTEX_INDEX[u] < VERTEX_INDEX[w] else (w, u)
                e_set.add(e)
                if w not in used:
                    used.add(w)
                    q.append(w)
        comps.append(
            {
                "vertices": sorted(verts, key=lambda x: VERTEX_INDEX[x]),
                "edges": sorted(e_set, key=lambda e: EDGE_INDEX[e]),
            }
        )
    return comps

def classify_support_graph(edge_indices: List[int]) -> Tuple[bool, bool, str, List[Vertex]]:
    deg = support_vertex_degrees(edge_indices)
    comps = support_components(edge_indices)
    active = [v for v, d in deg.items() if d > 0]
    boundary = sorted([v for v, d in deg.items() if d == 1], key=lambda x: VERTEX_INDEX[x])
    closed = all((deg[v] % 2 == 0) for v in active)
    connected = (len(comps) == 1 and len(active) > 0)

    m = len(edge_indices)
    if m == 0:
        return closed, connected, "empty", boundary

    support_type = "other"

    if m == 6:
        if connected:
            if len(active) == 6 and all(deg[v] == 2 for v in active):
                support_type = "C6"
            elif len(active) == 7 and sorted(deg[v] for v in active) == [1, 1, 2, 2, 2, 2, 2]:
                support_type = "P7"
        else:
            if len(comps) == 2:
                comp_sizes = sorted(len(c["edges"]) for c in comps)
                if comp_sizes == [3, 3]:
                    tri = True
                    for c in comps:
                        verts = c["vertices"]
                        if len(verts) != 3:
                            tri = False
                            break
                        cdeg = {v: 0 for v in verts}
                        for u, v in c["edges"]:
                            cdeg[u] += 1
                            cdeg[v] += 1
                        if sorted(cdeg.values()) != [2, 2, 2]:
                            tri = False
                            break
                    if tri:
                        support_type = "C3+C3"

    return closed, connected, support_type, boundary

def recover_cycle_order(edge_indices: Tuple[int, ...] | List[int]) -> List[Vertex]:
    edge_indices = list(edge_indices)
    closed, connected, support_type, boundary = classify_support_graph(edge_indices)
    if support_type != "C6":
        raise ValueError("recover_cycle_order requires a C6 support")

    nbrs = support_neighbors(edge_indices)
    cycle_vertices = [v for v in VERTICES if len(nbrs[v]) == 2]
    start = min(cycle_vertices, key=lambda x: VERTEX_INDEX[x])

    a, b = nbrs[start]
    # deterministic direction choice
    prev = start
    curr = a if VERTEX_INDEX[a] < VERTEX_INDEX[b] else b
    order = [start]

    while curr != start:
        order.append(curr)
        nxts = nbrs[curr]
        nxt = nxts[0] if nxts[1] == prev else nxts[1]
        prev, curr = curr, nxt
        if len(order) > 6:
            raise RuntimeError("Cycle recovery failed")

    if len(order) != 6:
        raise RuntimeError("Recovered cycle is not length 6")

    return order

def bfs_tree_edges(root: Vertex = "o0") -> List[int]:
    used = {root}
    q = deque([root])
    tree: List[int] = []
    while q:
        u = q.popleft()
        for v in NEIGHBORS[u]:
            if v in used:
                continue
            used.add(v)
            q.append(v)
            tree.append(edge_index(u, v))
    if len(tree) != len(VERTICES) - 1:
        raise RuntimeError("Spanning tree did not have 14 edges")
    return tree

def tree_path_edges(tree_edge_indices: List[int], src: Vertex, dst: Vertex) -> List[int]:
    tree_nbrs: Dict[Vertex, List[Tuple[Vertex, int]]] = {v: [] for v in VERTICES}
    for idx in tree_edge_indices:
        u, v = EDGES[idx]
        tree_nbrs[u].append((v, idx))
        tree_nbrs[v].append((u, idx))

    q = deque([src])
    parent: Dict[Vertex, Tuple[Vertex, int] | None] = {src: None}
    while q:
        u = q.popleft()
        if u == dst:
            break
        for v, idx in tree_nbrs[u]:
            if v in parent:
                continue
            parent[v] = (u, idx)
            q.append(v)

    if dst not in parent:
        raise RuntimeError("No tree path found")

    path_edges: List[int] = []
    cur = dst
    while parent[cur] is not None:
        p, idx = parent[cur]
        path_edges.append(idx)
        cur = p
    path_edges.reverse()
    return path_edges

def build_fundamental_cycle_basis() -> List[List[int]]:
    tree = bfs_tree_edges("o0")
    tree_set = set(tree)
    chords = [idx for idx in range(len(EDGES)) if idx not in tree_set]
    if len(chords) != 16:
        raise RuntimeError("Expected 16 non-tree edges")

    rows: List[List[int]] = []
    for chord in chords:
        u, v = EDGES[chord]
        row = [0] * len(EDGES)
        row[chord] = 1
        for idx in tree_path_edges(tree, u, v):
            row[idx] ^= 1
        rows.append(row)
    return rows
