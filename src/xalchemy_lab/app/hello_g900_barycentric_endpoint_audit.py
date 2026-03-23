from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Dict, List, Tuple

from xalchemy_lab.app.hello_g900_subdivision import generate_order_n_triangular_cells


def centroid(cell) -> Tuple[float, float]:
    xs = [v[0] for v in cell.verts]
    ys = [v[1] for v in cell.verts]
    return (sum(xs) / 3.0, sum(ys) / 3.0)


def layer_index(cell, n: int) -> int:
    vals = []
    for i, j in cell.verts:
        k = n - i - j
        vals.append(min(i, j, k))
    return min(vals)


def summarize_cells(cells) -> Dict[str, object]:
    cents = [centroid(c) for c in cells]
    xs = [p[0] for p in cents]
    ys = [p[1] for p in cents]
    orients: Dict[str, int] = defaultdict(int)
    for c in cells:
        orients[c.orient] += 1
    return {
        "count": len(cells),
        "x_min": min(xs),
        "x_max": max(xs),
        "x_mean": mean(xs),
        "y_min": min(ys),
        "y_max": max(ys),
        "y_mean": mean(ys),
        "orient_counts": dict(orients),
    }


def main() -> None:
    n = 30
    cells = generate_order_n_triangular_cells(n)

    by_layer: Dict[int, List[object]] = defaultdict(list)
    for c in cells:
        by_layer[layer_index(c, n)].append(c)

    layers = sorted(by_layer)
    low = layers[0]
    high = layers[-1]
    mid = layers[len(layers) // 2]

    low_summary = summarize_cells(by_layer[low])
    high_summary = summarize_cells(by_layer[high])
    mid_summary = summarize_cells(by_layer[mid])

    print("\nG900 BARYCENTRIC ENDPOINT AUDIT")
    print("================================")
    print(f"carrier order n          : {n}")
    print(f"available layers         : {layers}")
    print(f"endpoint layers          : {low}, {high}")
    print(f"chosen midpoint layer    : {mid}")

    print("\nENDPOINT STRATUM SUMMARY")
    print("========================")
    print(f"layer {low} count         : {low_summary['count']}")
    print(f"layer {high} count        : {high_summary['count']}")
    print(f"layer {mid} count         : {mid_summary['count']}")

    print("\nLAYER 0 GEOMETRY")
    print("================")
    print(f"x range                  : [{low_summary['x_min']}, {low_summary['x_max']}]")
    print(f"y range                  : [{low_summary['y_min']}, {low_summary['y_max']}]")
    print(f"centroid mean            : ({low_summary['x_mean']}, {low_summary['y_mean']})")
    print(f"orient counts            : {low_summary['orient_counts']}")

    print("\nLAYER 9 GEOMETRY")
    print("================")
    print(f"x range                  : [{high_summary['x_min']}, {high_summary['x_max']}]")
    print(f"y range                  : [{high_summary['y_min']}, {high_summary['y_max']}]")
    print(f"centroid mean            : ({high_summary['x_mean']}, {high_summary['y_mean']})")
    print(f"orient counts            : {high_summary['orient_counts']}")

    print("\nMID LAYER GEOMETRY")
    print("==================")
    print(f"x range                  : [{mid_summary['x_min']}, {mid_summary['x_max']}]")
    print(f"y range                  : [{mid_summary['y_min']}, {mid_summary['y_max']}]")
    print(f"centroid mean            : ({mid_summary['x_mean']}, {mid_summary['y_mean']})")
    print(f"orient counts            : {mid_summary['orient_counts']}")

    print("\nINTERPRETATION")
    print("==============")
    print("This audit checks whether the carrier has genuine endpoint strata and an interior mediating layer.")
    print("It does not yet prove that prism top/rung/bottom are literal quotient images of these layers.")
    print("A positive result here would support that next identification step.")

