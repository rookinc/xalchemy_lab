from __future__ import annotations

import csv
import json
import math
import random
import sys
from pathlib import Path
from typing import List, Tuple

Point = Tuple[float, float, float]


def load_points(path: str) -> List[Point]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text())
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of point objects or point arrays.")
        pts: List[Point] = []
        for row in data:
            if isinstance(row, dict):
                pts.append((float(row["x"]), float(row["y"]), float(row["z"])))
            elif isinstance(row, (list, tuple)) and len(row) >= 3:
                pts.append((float(row[0]), float(row[1]), float(row[2])))
            else:
                raise ValueError(f"Bad JSON row: {row!r}")
        return pts

    if p.suffix.lower() == ".csv":
        pts = []
        with p.open(newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pts.append((float(row["x"]), float(row["y"]), float(row["z"])))
        return pts

    raise ValueError("Supported input types: .json or .csv")


def mean(points: List[Point]) -> Point:
    n = len(points)
    return (
        sum(x for x, _, _ in points) / n,
        sum(y for _, y, _ in points) / n,
        sum(z for _, _, z in points) / n,
    )


def normalize_to_cube(points: List[Point]) -> List[Point]:
    cx, cy, cz = mean(points)
    centered = [(x - cx, y - cy, z - cz) for x, y, z in points]

    max_abs = max(max(abs(x), abs(y), abs(z)) for x, y, z in centered)
    if max_abs == 0:
        raise ValueError("All points are identical.")
    return [(x / max_abs, y / max_abs, z / max_abs) for x, y, z in centered]


def squared_dist(a: Point, b: Point) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def g15_sites() -> List[Tuple[str, Point]]:
    sites: List[Tuple[str, Point]] = []

    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            for sz in (-1.0, 1.0):
                sites.append((f"corner({int(sx)},{int(sy)},{int(sz)})", (sx, sy, sz)))

    sites.extend([
        ("face(+x)", (1.0, 0.0, 0.0)),
        ("face(-x)", (-1.0, 0.0, 0.0)),
        ("face(+y)", (0.0, 1.0, 0.0)),
        ("face(-y)", (0.0, -1.0, 0.0)),
        ("face(+z)", (0.0, 0.0, 1.0)),
        ("face(-z)", (0.0, 0.0, -1.0)),
    ])

    sites.append(("center", (0.0, 0.0, 0.0)))
    return sites


def assign_nearest(points: List[Point], sites: List[Tuple[str, Point]]) -> Tuple[List[int], float]:
    assignments: List[int] = []
    sse = 0.0
    site_points = [p for _, p in sites]

    for pt in points:
        best_i = min(range(len(site_points)), key=lambda i: squared_dist(pt, site_points[i]))
        assignments.append(best_i)
        sse += squared_dist(pt, site_points[best_i])

    return assignments, sse


def occupancy(assignments: List[int], k: int) -> List[int]:
    counts = [0] * k
    for a in assignments:
        counts[a] += 1
    return counts


def within_basin_stats(
    points: List[Point],
    assignments: List[int],
    sites: List[Tuple[str, Point]],
) -> List[Tuple[str, int, float]]:
    out = []
    for i, (label, site) in enumerate(sites):
        dists = [math.sqrt(squared_dist(pt, site)) for pt, a in zip(points, assignments) if a == i]
        avg = sum(dists) / len(dists) if dists else float("nan")
        out.append((label, len(dists), avg))
    return out


def random_sites_in_cube(k: int, seed: int = 0) -> List[Point]:
    rng = random.Random(seed)
    return [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(k)]


def kmeans(points: List[Point], k: int, iters: int = 40, seed: int = 0) -> Tuple[List[Point], List[int], float]:
    rng = random.Random(seed)
    centers = rng.sample(points, k)

    for _ in range(iters):
        assignments = []
        for pt in points:
            best_i = min(range(k), key=lambda i: squared_dist(pt, centers[i]))
            assignments.append(best_i)

        new_centers: List[Point] = []
        for i in range(k):
            cluster = [pt for pt, a in zip(points, assignments) if a == i]
            new_centers.append(mean(cluster) if cluster else centers[i])
        centers = new_centers

    sse = 0.0
    for pt, a in zip(points, assignments):
        sse += squared_dist(pt, centers[a])
    return centers, assignments, sse


def soft_membership_matrix(
    points: List[Point],
    sites: List[Tuple[str, Point]],
    temperature: float = 0.12,
) -> List[List[float]]:
    mat: List[List[float]] = []
    site_points = [p for _, p in sites]

    for pt in points:
        vals = []
        for sp in site_points:
            d2 = squared_dist(pt, sp)
            vals.append(math.exp(-d2 / max(temperature, 1e-9)))
        s = sum(vals)
        if s == 0:
            vals = [1.0 / len(site_points)] * len(site_points)
        else:
            vals = [v / s for v in vals]
        mat.append(vals)

    return mat


def mtm(mat: List[List[float]]) -> List[List[float]]:
    n = len(mat)
    k = len(mat[0])
    out = [[0.0 for _ in range(k)] for _ in range(k)]
    for r in range(n):
        row = mat[r]
        for i in range(k):
            ri = row[i]
            for j in range(k):
                out[i][j] += ri * row[j]
    return out


def print_matrix(mat: List[List[float]], labels: List[str], decimals: int = 2) -> None:
    print("\nM^T M coherence matrix:")
    print(" " * 18 + " ".join(f"{lbl[:8]:>8}" for lbl in labels))
    for label, row in zip(labels, mat):
        print(f"{label[:16]:>16} " + " ".join(f"{v:8.{decimals}f}" for v in row))


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python toys/test_g15_fit.py path/to/centroids.json")
        sys.exit(1)

    points = load_points(sys.argv[1])
    if len(points) < 15:
        raise ValueError("Need at least 15 points.")

    norm = normalize_to_cube(points)
    sites = g15_sites()
    labels = [label for label, _ in sites]

    g15_assign, g15_sse = assign_nearest(norm, sites)
    g15_counts = occupancy(g15_assign, len(sites))
    g15_stats = within_basin_stats(norm, g15_assign, sites)

    rnd_pts = random_sites_in_cube(15, seed=42)
    rnd_sites = [(f"rnd{i}", p) for i, p in enumerate(rnd_pts)]
    _, rnd_sse = assign_nearest(norm, rnd_sites)

    _, km_assign, km_sse = kmeans(norm, 15, iters=40, seed=42)
    km_counts = occupancy(km_assign, 15)

    print(f"\nLoaded points: {len(points)}")
    print("\n=== Fit quality ===")
    print(f"G15 scaffold SSE   : {g15_sse:.6f}")
    print(f"Random 15-site SSE : {rnd_sse:.6f}")
    print(f"K-means 15-site SSE: {km_sse:.6f}")
    if rnd_sse > 0:
        print(f"G15 vs random ratio: {g15_sse / rnd_sse:.4f}  (smaller is better)")
    if km_sse > 0:
        print(f"G15 vs kmeans ratio: {g15_sse / km_sse:.4f}  (~1 means competitive)")

    print("\n=== G15 occupancies ===")
    for label, count in zip(labels, g15_counts):
        print(f"{label:16s} {count:4d}")

    print("\n=== G15 within-basin avg distance ===")
    for label, count, avg in g15_stats:
        avg_str = "nan" if math.isnan(avg) else f"{avg:.4f}"
        print(f"{label:16s} count={count:4d} avg_dist={avg_str}")

    print("\n=== K-means occupancies ===")
    for i, count in enumerate(km_counts):
        print(f"cluster{i:02d}         {count:4d}")

    M = soft_membership_matrix(norm, sites, temperature=0.12)
    C = mtm(M)
    print_matrix(C, labels, decimals=2)


if __name__ == "__main__":
    main()
