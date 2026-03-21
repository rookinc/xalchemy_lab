from __future__ import annotations

import json
import math
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
    sx = width / 2 + x * f
    sy = height / 2 - y * f
    return (sx, sy)


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
    return (
        f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" '
        f'x2="{b[0]:.2f}" y2="{b[1]:.2f}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def svg_circle(c: Point2, r: float, fill: str = "none", stroke: str = "black", stroke_width: float = 1.0) -> str:
    return (
        f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{r:.2f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def svg_text(p: Point2, text: str, size: int = 12, anchor: str = "middle") -> str:
    safe = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return (
        f'<text x="{p[0]:.2f}" y="{p[1]:.2f}" '
        f'font-family="Helvetica,Arial,sans-serif" font-size="{size}" '
        f'text-anchor="{anchor}" fill="black">{safe}</text>'
    )


def rosette_svg(center: Point2, radius: float) -> List[str]:
    cx, cy = center
    out = [
        svg_circle((cx, cy), radius, fill="none", stroke="black", stroke_width=1.0),
        svg_circle((cx, cy), radius * 0.35, fill="none", stroke="black", stroke_width=1.0),
    ]
    for k in range(8):
        ang = 2 * math.pi * k / 8.0
        x = cx + math.cos(ang) * radius
        y = cy + math.sin(ang) * radius
        out.append(svg_line((cx, cy), (x, y), stroke="black", stroke_width=1.0))
    return out


def render_svg(kernel_path: str, output_path: str, width: int = 1200, height: int = 900) -> None:
    kernel = load_kernel(kernel_path)
    view_data = kernel["view"]
    view = ViewSpec(
        yaw_deg=float(view_data["yaw_deg"]),
        pitch_deg=float(view_data["pitch_deg"]),
        distance=float(view_data["distance"]),
        cube_size_px=int(view_data["cube_size_px"]),
    )

    verts = cube_vertices()
    faces = cube_faces()

    face_records = []
    for face_name, vertex_names in faces.items():
        pts3 = [verts[name] for name in vertex_names]
        pts2 = [project_point(p, width, height, view) for p in pts3]
        depth = polygon_depth(pts3, view)
        face_records.append((depth, face_name, pts2))

    face_records.sort(key=lambda item: item[0])

    visible_faces = {"front", "right", "top"}

    svg_parts: List[str] = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg_parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="white"/>')

    title = kernel.get("name", "g60 cube kernel")
    svg_parts.append(svg_text((width / 2, 34), title, size=22))
    svg_parts.append(svg_text((width / 2, 58), "hello-world semantic cube: G15 -> G30 -> Faces(G60)", size=13))

    for _depth, face_name, pts2 in face_records:
        outline_width = 2.2 if face_name in visible_faces else 1.0
        svg_parts.append(svg_poly(pts2, stroke="black", stroke_width=outline_width, fill="none"))

        face_data = kernel["faces"].get(face_name, {})
        if face_name not in visible_faces:
            continue

        role = face_data.get("role", face_name)
        weight = float(face_data.get("weight", 0.0))
        anchors_uv = face_data.get("anchors", [])
        edges = face_data.get("edges", [])
        center_rosette = bool(face_data.get("center_rosette", False))

        cx, cy = polygon_center(pts2)

        if center_rosette:
            svg_parts.extend(rosette_svg((cx, cy), 18.0))

        anchor_pts: List[Point2] = []
        for u, v in anchors_uv:
            pt = face_uv_to_canvas(pts2, float(u), float(v))
            anchor_pts.append(pt)
            r = 2.5 + 3.5 * weight
            svg_parts.append(svg_circle(pt, r, fill="black", stroke="black", stroke_width=1.0))

        for i, j in edges:
            if 0 <= i < len(anchor_pts) and 0 <= j < len(anchor_pts):
                svg_parts.append(svg_line(anchor_pts[i], anchor_pts[j], stroke="black", stroke_width=1.0))

        for corner in pts2:
            svg_parts.append(svg_line(corner, (cx, cy), stroke="black", stroke_width=0.8))

        svg_parts.append(svg_text((cx, cy + 44), f"{face_name}: {role}", size=12))
        svg_parts.append(svg_text((cx, cy + 60), f"w={weight:.2f}", size=11))

    svg_parts.append("</svg>")
    Path(output_path).write_text("\n".join(svg_parts), encoding="utf-8")


def main() -> None:
    kernel_path = "specs/app/g60_cube_kernel_v1.json"
    output_path = "renders/g60_cube_kernel_v1.svg"
    Path("renders").mkdir(exist_ok=True)
    render_svg(kernel_path, output_path)
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
