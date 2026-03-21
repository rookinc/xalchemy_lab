from __future__ import annotations

import json
import math
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


Point2 = Tuple[float, float]
Point3 = Tuple[float, float, float]


@dataclass
class ViewSpec:
    yaw_deg: float
    pitch_deg: float
    distance: float
    cube_size_px: int


TRACE_ORDER = [
    ("A", "O", "O", "O"),
    ("A", "E1", "E1", "E1"),
    ("A", "E2", "E2", "E2"),
    ("E1", "E1", "E1", "O"),
    ("E1", "E1", "E1", "E2"),
    ("D", "E1", "E1", "E2"),
    ("D", "E1", "E1", "M+"),
    ("D", "E1", "E2", "E2"),
    ("E2", "E2", "E2", "E2"),
    ("D", "E1", "O", "M+"),
    ("E1", "E1", "M+", "M+"),
    ("E1", "E2", "E2", "E2"),
    ("E1", "E2", "M+", "M+"),
    ("E1", "M+", "M+", "O"),
    ("E2", "E2", "E2", "O"),
]


def load_kernel(path: str) -> dict:
    return json.loads(Path(path).read_text())


def cube_vertices() -> Dict[str, Point3]:
    return {
        "LBF": (-1.0, -1.0,  1.0),
        "RBF": ( 1.0, -1.0,  1.0),
        "RTF": ( 1.0,  1.0,  1.0),
        "LTF": (-1.0,  1.0,  1.0),
        "LBB": (-1.0, -1.0, -1.0),
        "RBB": ( 1.0, -1.0, -1.0),
        "RTB": ( 1.0,  1.0, -1.0),
        "LTB": (-1.0,  1.0, -1.0),
    }


def cube_faces() -> Dict[str, List[str]]:
    return {
        "front":  ["LBF", "RBF", "RTF", "LTF"],
        "right":  ["RBF", "RBB", "RTB", "RTF"],
        "top":    ["LTF", "RTF", "RTB", "LTB"],
        "left":   ["LBB", "LBF", "LTF", "LTB"],
        "bottom": ["LBB", "RBB", "RBF", "LBF"],
        "back":   ["RBB", "LBB", "LTB", "RTB"],
    }


def rotate_point(p: Point3, yaw_deg: float, pitch_deg: float) -> Point3:
    x, y, z = p
    yaw = math.radians(yaw_deg)
    pitch = math.radians(pitch_deg)

    cy = math.cos(yaw)
    sy = math.sin(yaw)
    cp = math.cos(pitch)
    sp = math.sin(pitch)

    x1 = cy * x + sy * z
    y1 = y
    z1 = -sy * x + cy * z

    x2 = x1
    y2 = cp * y1 - sp * z1
    z2 = sp * y1 + cp * z1
    return (x2, y2, z2)


def project_point(p: Point3, width: int, height: int, view: ViewSpec) -> Point2:
    x, y, z = rotate_point(p, view.yaw_deg, view.pitch_deg)
    denom = view.distance - z
    if abs(denom) < 1e-6:
        denom = 1e-6
    f = view.cube_size_px / denom
    return (width / 2 + x * f, height / 2 - y * f)


def polygon_depth(points3: List[Point3], view: ViewSpec) -> float:
    zs = [rotate_point(p, view.yaw_deg, view.pitch_deg)[2] for p in points3]
    return sum(zs) / len(zs)


def polygon_center(points2: List[Point2]) -> Point2:
    return (
        sum(p[0] for p in points2) / len(points2),
        sum(p[1] for p in points2) / len(points2),
    )


def lerp2(a: Point2, b: Point2, t: float) -> Point2:
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def face_uv_to_canvas(face_poly: List[Point2], u: float, v: float) -> Point2:
    p00, p10, p11, p01 = face_poly
    top = lerp2(p00, p10, u)
    bottom = lerp2(p01, p11, u)
    return lerp2(top, bottom, v)


def svg_poly(points: List[Point2], stroke: str = "black", stroke_width: float = 1.0, fill: str = "none") -> str:
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'


def svg_line(a: Point2, b: Point2, stroke: str = "black", stroke_width: float = 1.0) -> str:
    return f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{stroke}" stroke-width="{stroke_width}"/>'


def svg_circle(c: Point2, r: float, fill: str = "none", stroke: str = "black", stroke_width: float = 1.0) -> str:
    return f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{r:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'


def svg_text(p: Point2, text: str, size: int = 12, anchor: str = "middle", weight: str = "normal") -> str:
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<text x="{p[0]:.2f}" y="{p[1]:.2f}" font-family="Helvetica,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="black">{safe}</text>'
    )


def trace_map(A: int, sigma: int, tau: int) -> Dict[Tuple[str, ...], int]:
    out: Dict[Tuple[str, ...], int] = {}
    if A == 0:
        out[("A", "O", "O", "O")] = tau
        out[("A", "E1", "E1", "E1")] = sigma
        out[("A", "E2", "E2", "E2")] = 0
    else:
        out[("A", "E2", "E2", "E2")] = 1
        out[("A", "E1", "E1", "E1")] = 1 if (sigma, tau) in {(0, 0), (0, 1)} else 0
        out[("A", "O", "O", "O")] = 1 if (sigma, tau) in {(0, 0), (1, 0)} else 0

    out[("E1", "E1", "E1", "O")] = 1 if (sigma, tau) in {(0, 0), (1, 1)} else 0
    out[("E1", "E1", "E1", "E2")] = sigma

    out[("D", "E1", "E1", "E2")] = 1
    out[("D", "E1", "E1", "M+")] = 1
    out[("D", "E1", "E2", "E2")] = 1
    out[("E2", "E2", "E2", "E2")] = 1

    out[("D", "E1", "O", "M+")] = 0
    out[("E1", "E1", "M+", "M+")] = 0
    out[("E1", "E2", "E2", "E2")] = 0
    out[("E1", "E2", "M+", "M+")] = 0
    out[("E1", "M+", "M+", "O")] = 0
    out[("E2", "E2", "E2", "O")] = 0
    return out


def face_weight(face_name: str, traces: Dict[Tuple[str, ...], int]) -> float:
    if face_name == "front":
        return 0.55 + 0.25 * traces[("A", "O", "O", "O")]
    if face_name == "top":
        return 0.45 + 0.35 * traces[("A", "E1", "E1", "E1")]
    if face_name == "right":
        return 0.45 + 0.35 * traces[("A", "E2", "E2", "E2")]
    if face_name == "left":
        return 0.35 + 0.15 * traces[("D", "E1", "E1", "E2")]
    if face_name == "bottom":
        return 0.35 + 0.15 * (1 - traces[("D", "E1", "O", "M+")])
    if face_name == "back":
        return 0.20 + 0.20 * traces[("E1", "E1", "E1", "O")]
    return 0.25


def visible_face_anchors(face_name: str, traces: Dict[Tuple[str, ...], int]) -> List[Tuple[float, float]]:
    if face_name == "front":
        return [(0.2, 0.2), (0.8, 0.2), (0.5, 0.5), (0.2, 0.8), (0.8, 0.8)]
    if face_name == "top":
        if traces[("A", "E1", "E1", "E1")] == 1:
            return [(0.18, 0.22), (0.82, 0.22), (0.5, 0.45), (0.22, 0.78), (0.78, 0.78)]
        return [(0.28, 0.28), (0.72, 0.28), (0.5, 0.72)]
    if face_name == "right":
        if traces[("A", "E2", "E2", "E2")] == 1:
            return [(0.2, 0.2), (0.8, 0.25), (0.35, 0.75), (0.8, 0.8), (0.5, 0.5)]
        return [(0.3, 0.3), (0.7, 0.7)]
    return []


def visible_face_edges(face_name: str, traces: Dict[Tuple[str, ...], int]) -> List[Tuple[int, int]]:
    if face_name == "front":
        edges = [(0, 2), (1, 2), (3, 2), (4, 2), (0, 1), (3, 4)]
        if traces[("A", "O", "O", "O")] == 1:
            edges += [(0, 4), (1, 3)]
        return edges
    if face_name == "top":
        if traces[("A", "E1", "E1", "E1")] == 1:
            return [(0, 2), (1, 2), (3, 2), (4, 2), (0, 1), (3, 4), (0, 4), (1, 3)]
        return [(0, 2), (1, 2)]
    if face_name == "right":
        if traces[("A", "E2", "E2", "E2")] == 1:
            return [(0, 1), (1, 3), (3, 2), (2, 0), (0, 4), (1, 4), (2, 4), (3, 4)]
        return [(0, 1)]
    return []


def role_tag(face_name: str) -> str:
    return {
        "front": "H/O",
        "top": "E1",
        "right": "E2",
        "left": "Do",
        "bottom": "De",
        "back": "C",
    }[face_name]


def run_cmd(cmd: List[str]) -> bool:
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def export_png(svg_path: Path, png_path: Path, width: int = 1200, height: int = 900) -> bool:
    png_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import cairosvg  # type: ignore

        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(png_path),
            output_width=width,
            output_height=height,
        )
        return True
    except Exception:
        pass

    if shutil.which("rsvg-convert"):
        return run_cmd([
            "rsvg-convert",
            "-w", str(width),
            "-h", str(height),
            "-o", str(png_path),
            str(svg_path),
        ])

    if shutil.which("magick"):
        return run_cmd([
            "magick",
            "-background", "white",
            "-density", "200",
            str(svg_path),
            str(png_path),
        ])

    if shutil.which("convert"):
        return run_cmd([
            "convert",
            "-background", "white",
            "-density", "200",
            str(svg_path),
            str(png_path),
        ])

    if shutil.which("inkscape"):
        return run_cmd([
            "inkscape",
            str(svg_path),
            "--export-type=png",
            f"--export-filename={png_path}",
            f"--export-width={width}",
            f"--export-height={height}",
        ])

    return False


def render_state(kernel: dict, state_name: str, state: dict, output_path: Path) -> None:
    width, height = 1200, 900
    view_data = kernel["view"]
    view = ViewSpec(
        yaw_deg=float(view_data["yaw_deg"]),
        pitch_deg=float(view_data["pitch_deg"]),
        distance=float(view_data["distance"]),
        cube_size_px=int(view_data["cube_size_px"]),
    )

    A = int(state["A"])
    sigma = int(state["sigma"])
    tau = int(state["tau"])
    traces = trace_map(A, sigma, tau)

    verts = cube_vertices()
    faces = cube_faces()
    face_records = []
    for face_name, vertex_names in faces.items():
        pts3 = [verts[name] for name in vertex_names]
        pts2 = [project_point(p, width, height, view) for p in pts3]
        depth = polygon_depth(pts3, view)
        face_records.append((depth, face_name, pts2))
    face_records.sort(key=lambda item: item[0])

    svg: List[str] = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="white"/>')
    svg.append(svg_text((width / 2, 36), f"{kernel['name']} :: state {state_name}", size=22, weight="bold"))
    svg.append(svg_text((width / 2, 62), f"(A,sigma,tau)=({A},{sigma},{tau})", size=14))

    visible = {"front", "top", "right"}
    for _depth, face_name, pts2 in face_records:
        svg.append(svg_poly(pts2, stroke="black", stroke_width=2.4 if face_name in visible else 1.0, fill="none"))
        if face_name not in visible:
            continue

        cx, cy = polygon_center(pts2)
        anchors_uv = visible_face_anchors(face_name, traces)
        anchors = [face_uv_to_canvas(pts2, u, v) for u, v in anchors_uv]
        edges = visible_face_edges(face_name, traces)
        w = face_weight(face_name, traces)
        radius = 14 + 8 * w

        svg.append(svg_circle((cx, cy), radius, fill="none", stroke="black", stroke_width=1.2))
        svg.append(svg_circle((cx, cy), radius * 0.35, fill="none", stroke="black", stroke_width=1.0))

        for corner in pts2:
            svg.append(svg_line(corner, (cx, cy), stroke="black", stroke_width=0.8))

        for i, j in edges:
            if i < len(anchors) and j < len(anchors):
                svg.append(svg_line(anchors[i], anchors[j], stroke="black", stroke_width=1.0))

        for pt in anchors:
            svg.append(svg_circle(pt, 3.0 + 3.0 * w, fill="black", stroke="black", stroke_width=1.0))

        svg.append(svg_text((cx, cy + 50), role_tag(face_name), size=14, weight="bold"))
        svg.append(svg_text((cx, cy + 68), f"w={w:.2f}", size=11))

    legend_x = 950
    legend_y = 130
    svg.append(svg_text((legend_x, legend_y), "trace receipts", size=16, weight="bold", anchor="start"))
    y = legend_y + 26
    for trace in TRACE_ORDER:
        bit = traces[trace]
        svg.append(svg_text((legend_x, y), f"{''.join(trace)} = {'ODD' if bit else 'EVEN'}", size=11, anchor="start"))
        y += 18

    svg.append("</svg>")
    output_path.write_text("\n".join(svg), encoding="utf-8")


def main() -> None:
    kernel = load_kernel("specs/app/g60_cube_state_kernel_v1.json")
    outdir = Path("renders/state_cube_gallery_v1")
    outdir.mkdir(parents=True, exist_ok=True)

    png_ok = None
    for state_name, state in kernel["states"].items():
        svg_path = outdir / f"{state_name}.svg"
        png_path = outdir / f"{state_name}.png"

        render_state(kernel, state_name, state, svg_path)
        print(f"wrote {svg_path}")

        ok = export_png(svg_path, png_path)
        if ok:
            print(f"wrote {png_path}")
        else:
            print(f"skipped png for {state_name} (no rasterizer found)")
        png_ok = ok if png_ok is None else (png_ok or ok)

    if not png_ok:
        print("tip: install cairosvg, librsvg, imagemagick, or inkscape for PNG export")


if __name__ == "__main__":
    main()
