from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Set, Tuple

FACES = ("U", "D", "F", "B", "L", "R")
ALPHABET = ("F", "L", "R", "X")

FORWARD_TABLE: Dict[Tuple[str, int], str] = {
    ("U", 0): "B", ("U", 1): "R", ("U", 2): "F", ("U", 3): "L",
    ("D", 0): "F", ("D", 1): "R", ("D", 2): "B", ("D", 3): "L",
    ("F", 0): "U", ("F", 1): "R", ("F", 2): "D", ("F", 3): "L",
    ("B", 0): "U", ("B", 1): "L", ("B", 2): "D", ("B", 3): "R",
    ("L", 0): "U", ("L", 1): "F", ("L", 2): "D", ("L", 3): "B",
    ("R", 0): "U", ("R", 1): "B", ("R", 2): "D", ("R", 3): "F",
}

OPPOSITE_FACE: Dict[str, str] = {
    "U": "D", "D": "U",
    "F": "B", "B": "F",
    "L": "R", "R": "L",
}

EDGE_CLASS_MAP: Dict[Tuple[str, int], str] = {
    ("U", 0): "UB", ("U", 1): "UR", ("U", 2): "UF", ("U", 3): "UL",
    ("D", 0): "DF", ("D", 1): "DR", ("D", 2): "DB", ("D", 3): "DL",
    ("F", 0): "UF", ("F", 1): "FR", ("F", 2): "DF", ("F", 3): "FL",
    ("B", 0): "UB", ("B", 1): "BL", ("B", 2): "DB", ("B", 3): "BR",
    ("L", 0): "UL", ("L", 1): "FL", ("L", 2): "DL", ("L", 3): "BL",
    ("R", 0): "UR", ("R", 1): "BR", ("R", 2): "DR", ("R", 3): "FR",
}


@dataclass(frozen=True)
class State:
    face: str
    heading: int
    sheet: int


@dataclass
class EvalResult:
    word: str
    initial_state: State
    final_state: State
    base_closed: bool
    full_closed: bool
    parity: int
    raw_trace: List[str]
    reduced_edges: List[Tuple[str, str]]
    support_type: str
    refined_nodes: List[str]
    refined_edges: List[Tuple[str, str]]


@dataclass
class SearchHit:
    word: str
    final_state: State
    parity: int
    raw_trace: List[str]
    reduced_edges: List[Tuple[str, str]]
    support_type: str
    refined_nodes: List[str]
    refined_edges: List[Tuple[str, str]]


@dataclass
class SearchResult:
    initial_state: State
    max_length: int
    shortest_length: Optional[int]
    hits: List[SearchHit]
    support_histogram: Dict[str, int]


def heading_involution(h: int) -> int:
    return (-h) % 4


def move_L(s: State) -> State:
    return State(s.face, (s.heading + 1) % 4, s.sheet)


def move_R(s: State) -> State:
    return State(s.face, (s.heading - 1) % 4, s.sheet)


def move_F(s: State) -> State:
    return State(FORWARD_TABLE[(s.face, s.heading)], s.heading, s.sheet)


def move_X(s: State) -> State:
    return State(OPPOSITE_FACE[s.face], heading_involution(s.heading), 1 - s.sheet)


MOVE_FUNCS = {
    "L": move_L,
    "R": move_R,
    "F": move_F,
    "X": move_X,
}


def step(s: State, a: str) -> State:
    return MOVE_FUNCS[a](s)


def project_state(s: State) -> str:
    return EDGE_CLASS_MAP[(s.face, s.heading)]


def trace_to_edge_walk(trace: List[str]) -> List[Tuple[str, str]]:
    walk: List[Tuple[str, str]] = []
    for u, v in zip(trace, trace[1:]):
        if u == v:
            continue
        walk.append(tuple(sorted((u, v))))
    return walk


def cancel_immediate_backtracks(edge_walk: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    stack: List[Tuple[str, str]] = []
    for e in edge_walk:
        if stack and stack[-1] == e:
            stack.pop()
        else:
            stack.append(e)
    return stack


def reduce_trace_to_support(trace: List[str]) -> Set[Tuple[str, str]]:
    walk = trace_to_edge_walk(trace)
    reduced_walk = cancel_immediate_backtracks(walk)
    return set(reduced_walk)


def build_graph_from_edges(edges: Set[Tuple[str, str]]) -> Dict[str, Set[str]]:
    g: Dict[str, Set[str]] = defaultdict(set)
    for u, v in edges:
        g[u].add(v)
        g[v].add(u)
    return g


def connected_components(graph: Dict[str, Set[str]]) -> List[Set[str]]:
    seen: Set[str] = set()
    comps: List[Set[str]] = []
    for node in graph:
        if node in seen:
            continue
        comp: Set[str] = set()
        stack = [node]
        seen.add(node)
        while stack:
            x = stack.pop()
            comp.add(x)
            for y in graph[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(comp)
    return comps


def classify_support(edges: Set[Tuple[str, str]]) -> str:
    if not edges:
        return "empty"

    g = build_graph_from_edges(edges)
    comps = connected_components(g)

    if len(comps) > 1:
        return "disconnected"

    degrees = sorted(len(g[v]) for v in g)
    edge_count = len(edges)
    vertex_count = len(g)

    if all(d == 2 for d in degrees):
        if edge_count == 6 and vertex_count == 6:
            return "C6"
        return "cycle"

    deg1 = sum(1 for d in degrees if d == 1)
    deg2 = sum(1 for d in degrees if d == 2)
    if deg1 == 2 and deg1 + deg2 == vertex_count:
        if edge_count == 6 and vertex_count == 7:
            return "P7"
        return "path"

    return "other"


def axis_class_for_transition(face_a: str, face_b: str) -> str:
    pair = {face_a, face_b}
    if "U" in pair or "D" in pair:
        return "A_V"
    if "F" in pair or "B" in pair:
        return "A_FB"
    return "A_LR"


def enhanced_support_labels(state_trace: List[State]) -> Set[str]:
    counts = {"A_V": 0, "A_FB": 0, "A_LR": 0}
    for s1, s2 in zip(state_trace, state_trace[1:]):
        if s1.face == s2.face:
            continue
        ax = axis_class_for_transition(s1.face, s2.face)
        counts[ax] += 1
    return {ax for ax, c in counts.items() if c >= 2}


def refined_support_from_state_trace(
    state_trace: List[State],
    raw_trace: List[str],
) -> Tuple[Set[str], Set[Tuple[str, str]]]:
    local_support_edges = reduce_trace_to_support(raw_trace)
    active_axial = enhanced_support_labels(state_trace)

    active_nodes: Set[str] = set()
    refined_edges: Set[Tuple[str, str]] = set()

    for u, v in local_support_edges:
        active_nodes.add(u)
        active_nodes.add(v)
        refined_edges.add(tuple(sorted((u, v))))

    for ax in active_axial:
        active_nodes.add(ax)

    for s1, s2 in zip(state_trace, state_trace[1:]):
        if s1.face == s2.face:
            continue
        ax = axis_class_for_transition(s1.face, s2.face)
        if ax not in active_axial:
            continue
        q1 = project_state(s1)
        q2 = project_state(s2)
        active_nodes.add(q1)
        active_nodes.add(q2)
        refined_edges.add(tuple(sorted((ax, q1))))
        refined_edges.add(tuple(sorted((ax, q2))))

    return active_nodes, refined_edges


def evaluate_word(initial: State, word: str) -> EvalResult:
    state = initial
    state_trace = [state]
    raw_trace = [project_state(state)]
    parity = 0

    for a in word:
        state = step(state, a)
        state_trace.append(state)
        raw_trace.append(project_state(state))
        if a == "X":
            parity ^= 1

    reduced_edges = reduce_trace_to_support(raw_trace)
    support_type = classify_support(reduced_edges)
    refined_nodes, refined_edges = refined_support_from_state_trace(state_trace, raw_trace)

    return EvalResult(
        word=word,
        initial_state=initial,
        final_state=state,
        base_closed=(state.face == initial.face and state.heading == initial.heading),
        full_closed=(state == initial),
        parity=parity,
        raw_trace=raw_trace,
        reduced_edges=sorted(reduced_edges),
        support_type=support_type,
        refined_nodes=sorted(refined_nodes),
        refined_edges=sorted(refined_edges),
    )


def bfs_shortest_nontrivial_base_closed(initial: State, max_length: int) -> SearchResult:
    queue = deque()
    queue.append((initial, "", [initial], [project_state(initial)], 0))

    hits: List[SearchHit] = []
    shortest_length: Optional[int] = None

    while queue:
        state, word, state_trace, raw_trace, parity = queue.popleft()

        if shortest_length is not None and len(word) >= shortest_length:
            continue

        for a in ALPHABET:
            next_state = step(state, a)
            next_word = word + a
            if len(next_word) > max_length:
                continue

            next_state_trace = state_trace + [next_state]
            next_raw_trace = raw_trace + [project_state(next_state)]
            next_parity = parity ^ (1 if a == "X" else 0)

            base_closed = (
                next_state.face == initial.face and
                next_state.heading == initial.heading
            )

            if base_closed and next_parity == 1:
                reduced_edges = reduce_trace_to_support(next_raw_trace)
                support_type = classify_support(reduced_edges)
                refined_nodes, refined_edges = refined_support_from_state_trace(next_state_trace, next_raw_trace)

                if shortest_length is None:
                    shortest_length = len(next_word)

                if len(next_word) == shortest_length:
                    hits.append(SearchHit(
                        word=next_word,
                        final_state=next_state,
                        parity=next_parity,
                        raw_trace=next_raw_trace,
                        reduced_edges=sorted(reduced_edges),
                        support_type=support_type,
                        refined_nodes=sorted(refined_nodes),
                        refined_edges=sorted(refined_edges),
                    ))
            else:
                queue.append((next_state, next_word, next_state_trace, next_raw_trace, next_parity))

    histogram = Counter(hit.support_type for hit in hits)
    return SearchResult(
        initial_state=initial,
        max_length=max_length,
        shortest_length=shortest_length,
        hits=hits,
        support_histogram=dict(histogram),
    )


def state_to_dict(s: State) -> Dict[str, object]:
    return {"face": s.face, "heading": s.heading, "sheet": s.sheet}


def eval_to_dict(res: EvalResult) -> Dict[str, object]:
    return {
        "word": res.word,
        "initial_state": state_to_dict(res.initial_state),
        "final_state": state_to_dict(res.final_state),
        "base_closed": res.base_closed,
        "full_closed": res.full_closed,
        "parity": res.parity,
        "raw_trace": res.raw_trace,
        "reduced_edges": [list(e) for e in res.reduced_edges],
        "support_type": res.support_type,
        "refined_nodes": res.refined_nodes,
        "refined_edges": [list(e) for e in res.refined_edges],
    }


def search_to_dict(res: SearchResult) -> Dict[str, object]:
    return {
        "initial_state": state_to_dict(res.initial_state),
        "max_length": res.max_length,
        "shortest_length": res.shortest_length,
        "support_histogram": res.support_histogram,
        "hits": [
            {
                "word": h.word,
                "final_state": state_to_dict(h.final_state),
                "parity": h.parity,
                "raw_trace": h.raw_trace,
                "reduced_edges": [list(e) for e in h.reduced_edges],
                "support_type": h.support_type,
                "refined_nodes": h.refined_nodes,
                "refined_edges": [list(e) for e in h.refined_edges],
            }
            for h in res.hits
        ],
    }


def print_seed_report(res: EvalResult) -> None:
    print(f"word:          {res.word}")
    print(f"initial_state: {res.initial_state}")
    print(f"final_state:   {res.final_state}")
    print(f"base_closed:   {'yes' if res.base_closed else 'no'}")
    print(f"full_closed:   {'yes' if res.full_closed else 'no'}")
    print(f"parity:        {res.parity}")
    print(f"raw_trace:     {res.raw_trace}")
    print(f"reduced_edges: {res.reduced_edges}")
    print(f"support_type:  {res.support_type}")
    print(f"refined_nodes: {res.refined_nodes}")
    print(f"refined_edges: {res.refined_edges}")


def print_search_report(res: SearchResult) -> None:
    print("=" * 72)
    print(f"initial_state:   {res.initial_state}")
    print(f"max_length:      {res.max_length}")
    print(f"shortest_length: {res.shortest_length}")
    print(f"hit_count:       {len(res.hits)}")
    print(f"support_hist:    {res.support_histogram}")
    print("-" * 72)
    for h in res.hits:
        print(f"word={h.word} parity={h.parity} type={h.support_type} final={h.final_state}")
        print(f"  raw_trace={h.raw_trace}")
        print(f"  reduced_edges={h.reduced_edges}")
        print(f"  refined_nodes={h.refined_nodes}")
        print(f"  refined_edges={h.refined_edges}")
    print("=" * 72)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prototype cube-host passage transducer search for shortest nontrivial base-closed words."
    )
    parser.add_argument("--face", default="U", choices=FACES)
    parser.add_argument("--heading", default=0, type=int, choices=(0, 1, 2, 3))
    parser.add_argument("--sheet", default=0, type=int, choices=(0, 1))
    parser.add_argument("--max-length", default=8, type=int)
    parser.add_argument(
        "--seed",
        action="append",
        dest="seeds",
        default=[],
        help="Seed word to evaluate. May be passed multiple times.",
    )
    parser.add_argument(
        "--json-out",
        default="",
        help="Optional path to write JSON report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    initial = State(args.face, args.heading, args.sheet)

    seeds = args.seeds or ["FXFXFX", "FRXFLXFX"]

    print("Seed diagnostics")
    print("-" * 72)
    seed_results: List[EvalResult] = []
    for word in seeds:
        res = evaluate_word(initial, word)
        seed_results.append(res)
        print_seed_report(res)
        print("-" * 72)

    print("\nBFS search")
    search_result = bfs_shortest_nontrivial_base_closed(initial, args.max_length)
    print_search_report(search_result)

    if args.json_out:
        payload = {
            "prototype_version": "cube_host_v0",
            "seed_results": [eval_to_dict(r) for r in seed_results],
            "search_result": search_to_dict(search_result),
        }
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        print(f"\nJSON report written to: {args.json_out}")


if __name__ == "__main__":
    main()
