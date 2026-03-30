from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path
from typing import Dict, List, Tuple

Point = Tuple[float, float, float]
LabeledPoint = Tuple[str, Point]


def load_points(path: str) -> List[Point]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    raw = p.read_text().strip()
    if not raw:
        raise ValueError(f"Input file is empty: {path}")

    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("Expected a JSON list of points.")

    pts: List[Point] = []
    for row in data:
        if isinstance(row, dict):
            pts.append((float(row["x"]), float(row["y"]), float(row["z"])))
        elif isinstance(row, (list, tuple)) and len(row) >= 3:
            pts.append((float(row[0]), float(row[1]), float(row[2])))
        else:
            raise ValueError(f"Bad point row: {row!r}")
    return pts


def mean(points: List[Point]) -> Point:
    n = len(points)
    return (
        sum(x for x, _, _ in points) / n,
        sum(y for _, y, _ in points) / n,
        sum(z for _, _, z in points) / n,
    )


def normalize(points: List[Point]) -> List[Point]:
    cx, cy, cz = mean(points)
    centered = [(x - cx, y - cy, z - cz) for x, y, z in points]
    max_abs = max(max(abs(x), abs(y), abs(z)) for x, y, z in centered)
    if max_abs == 0:
        raise ValueError("All points are identical.")
    return [(x / max_abs, y / max_abs, z / max_abs) for x, y, z in centered]


def sqdist(a: Point, b: Point) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def build_polarized_g15_sites(
    pole_z: float = 1.0,
    side_r: float = 1.0,
    corner_r: float = 1.0,
    corner_z: float = 1.0,
) -> List[LabeledPoint]:
    sites: List[LabeledPoint] = [("C", (0.0, 0.0, 0.0))]

    sites.append(("Fp", (0.0, 0.0, pole_z)))
    sites.append(("Fm", (0.0, 0.0, -pole_z)))

    sites.extend([
        ("E0", ( side_r, 0.0, 0.0)),
        ("E1", (0.0,  side_r, 0.0)),
        ("E2", (-side_r, 0.0, 0.0)),
        ("E3", (0.0, -side_r, 0.0)),
    ])

    s = corner_r / math.sqrt(2.0)
    sites.extend([
        ("K0", ( s,  s,  corner_z)),
        ("K1", (-s,  s,  corner_z)),
        ("K2", (-s, -s,  corner_z)),
        ("K3", ( s, -s,  corner_z)),
        ("K4", ( s,  s, -corner_z)),
        ("K5", (-s,  s, -corner_z)),
        ("K6", (-s, -s, -corner_z)),
        ("K7", ( s, -s, -corner_z)),
    ])

    return sites


def assign_nearest(points: List[Point], sites: List[LabeledPoint]) -> Tuple[List[int], float]:
    site_points = [p for _, p in sites]
    assignments: List[int] = []
    sse = 0.0

    for pt in points:
        best_i = min(range(len(site_points)), key=lambda i: sqdist(pt, site_points[i]))
        assignments.append(best_i)
        sse += sqdist(pt, site_points[best_i])

    return assignments, sse


def occupancy(assignments: List[int], k: int) -> List[int]:
    counts = [0] * k
    for a in assignments:
        counts[a] += 1
    return counts


def optimize_template(points: List[Point]) -> Tuple[List[LabeledPoint], List[int], float, Dict[str, float]]:
    pole_vals = [0.5, 0.75, 1.0, 1.25]
    side_vals = [0.5, 0.75, 1.0, 1.25]
    corner_r_vals = [0.5, 0.75, 1.0, 1.25]
    corner_z_vals = [0.5, 0.75, 1.0, 1.25]

    best_sites: List[LabeledPoint] | None = None
    best_assign: List[int] | None = None
    best_sse = float("inf")
    best_params: Dict[str, float] = {}

    for pole_z in pole_vals:
        for side_r in side_vals:
            for corner_r in corner_r_vals:
                for corner_z in corner_z_vals:
                    sites = build_polarized_g15_sites(
                        pole_z=pole_z,
                        side_r=side_r,
                        corner_r=corner_r,
                        corner_z=corner_z,
                    )
                    assign, sse = assign_nearest(points, sites)
                    if sse < best_sse:
                        best_sse = sse
                        best_sites = sites
                        best_assign = assign
                        best_params = {
                            "pole_z": pole_z,
                            "side_r": side_r,
                            "corner_r": corner_r,
                            "corner_z": corner_z,
                        }

    assert best_sites is not None
    assert best_assign is not None
    return best_sites, best_assign, best_sse, best_params


def random_sites(k: int, seed: int = 42) -> List[Point]:
    rng = random.Random(seed)
    return [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(k)]


def kmeans(points: List[Point], k: int, iters: int = 40, seed: int = 42) -> Tuple[List[Point], List[int], float]:
    rng = random.Random(seed)
    centers = rng.sample(points, k)

    for _ in range(iters):
        assignments = []
        for pt in points:
            best_i = min(range(k), key=lambda i: sqdist(pt, centers[i]))
            assignments.append(best_i)

        new_centers: List[Point] = []
        for i in range(k):
            cluster = [pt for pt, a in zip(points, assignments) if a == i]
            new_centers.append(mean(cluster) if cluster else centers[i])
        centers = new_centers

    sse = 0.0
    for pt, a in zip(points, assignments):
        sse += sqdist(pt, centers[a])

    return centers, assignments, sse


def avg_dist(points: List[Point], assignments: List[int], sites: List[LabeledPoint]) -> List[Tuple[str, int, float]]:
    out = []
    for i, (label, site) in enumerate(sites):
        ds = [math.sqrt(sqdist(pt, site)) for pt, a in zip(points, assignments) if a == i]
        avg = sum(ds) / len(ds) if ds else float("nan")
        out.append((label, len(ds), avg))
    return out


def summarize_role_groups(labels: List[str], counts: List[int]) -> Dict[str, int]:
    out = {"C": 0, "poles": 0, "equator": 0, "corners": 0}
    for label, count in zip(labels, counts):
        if label == "C":
            out["C"] += count
        elif label in {"Fp", "Fm"}:
            out["poles"] += count
        elif label.startswith("E"):
            out["equator"] += count
        elif label.startswith("K"):
            out["corners"] += count
    return out


def format_report(
    input_path: str,
    points: List[Point],
    base_sse: float,
    opt_sse: float,
    rnd_sse: float,
    km_sse: float,
    opt_params: Dict[str, float],
    labels: List[str],
    counts: List[int],
    grouped: Dict[str, int],
    avg_rows: List[Tuple[str, int, float]],
    km_counts: List[int],
) -> str:
    lines: List[str] = []

    def add(line: str = "") -> None:
        lines.append(line)

    add(f"Polarized G15 report")
    add(f"Input: {input_path}")
    add(f"Loaded points: {len(points)}")
    add()

    add("=== Fit quality ===")
    add(f"Base polarized G15 SSE : {base_sse:.6f}")
    add(f"Optimized polarized SSE: {opt_sse:.6f}")
    add(f"Random 15-site SSE     : {rnd_sse:.6f}")
    add(f"K-means 15-site SSE    : {km_sse:.6f}")
    if rnd_sse > 0:
        add(f"Base / random ratio    : {base_sse / rnd_sse:.4f}")
        add(f"Opt  / random ratio    : {opt_sse / rnd_sse:.4f}")
    if km_sse > 0:
        add(f"Base / kmeans ratio    : {base_sse / km_sse:.4f}")
        add(f"Opt  / kmeans ratio    : {opt_sse / km_sse:.4f}")
    add()

    add("=== Optimized parameters ===")
    for k, v in opt_params.items():
        add(f"{k:10s} {v:.4f}")
    add()

    add("=== Optimized polarized occupancies ===")
    for label, count in zip(labels, counts):
        add(f"{label:4s} {count:4d}")
    add()

    add("=== Role group totals ===")
    for key, value in grouped.items():
        add(f"{key:8s} {value:4d}")
    add()

    add("=== Optimized within-basin average distance ===")
    for label, count, avg in avg_rows:
        avg_str = "nan" if math.isnan(avg) else f"{avg:.4f}"
        add(f"{label:4s} count={count:4d} avg_dist={avg_str}")
    add()

    add("=== K-means occupancies ===")
    for i, count in enumerate(km_counts):
        add(f"cluster{i:02d} {count:4d}")

    return "\n".join(lines) + "\n"


def default_output_path(input_path: str) -> Path:
    p = Path(input_path)
    stem = p.stem
    return p.with_name(f"{stem}__polarized_g15_report.txt")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python toys/test_polarized_g15.py path/to/centroids.json [output_report.txt]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else default_output_path(input_path)

    points = load_points(input_path)
    points = normalize(points)

    base_sites = build_polarized_g15_sites()
    base_assign, base_sse = assign_nearest(points, base_sites)

    opt_sites, opt_assign, opt_sse, opt_params = optimize_template(points)

    rnd_pts = random_sites(15, seed=42)
    rnd_sites = [(f"R{i}", p) for i, p in enumerate(rnd_pts)]
    _, rnd_sse = assign_nearest(points, rnd_sites)

    _, km_assign, km_sse = kmeans(points, 15, iters=50, seed=42)

    labels = [label for label, _ in opt_sites]
    counts = occupancy(opt_assign, len(opt_sites))
    grouped = summarize_role_groups(labels, counts)
    avg_rows = avg_dist(points, opt_assign, opt_sites)
    km_counts = occupancy(km_assign, 15)

    report = format_report(
        input_path=input_path,
        points=points,
        base_sse=base_sse,
        opt_sse=opt_sse,
        rnd_sse=rnd_sse,
        km_sse=km_sse,
        opt_params=opt_params,
        labels=labels,
        counts=counts,
        grouped=grouped,
        avg_rows=avg_rows,
        km_counts=km_counts,
    )

    print(report, end="")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    print(f"\nWrote report to: {output_path}")


if __name__ == "__main__":
    main()
