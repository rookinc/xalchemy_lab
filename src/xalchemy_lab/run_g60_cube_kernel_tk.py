from __future__ import annotations

import json
import math
import tkinter as tk
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
    # unit cube centered at origin
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
        "back":   ["RBB", "LBB", "LTB", "RTB"]
    }


def rotate_point(p: Point3, yaw_deg: float, pitch_deg: float) -> Point3:
    x, y, z = p
    yaw = math.radians(yaw_deg)
    pitch = math.radians(pitch_deg)

    cy = math.cos(yaw)
    sy = math.sin(yaw)
    cp = math.cos(pitch)
    sp = math.sin(pitch)

    # yaw around y axis
    x1 = cy * x + sy * z
    y1 = y
    z1 = -sy * x + cy * z

    # pitch around x axis
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
    x = sum(p[0] for p in points2) / len(points2)
    y = sum(p[1] for p in points2) / len(points2)
    return (x, y)


def lerp2(a: Point2, b: Point2, t: float) -> Point2:
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def face_uv_to_canvas(face_poly: List[Point2], u: float, v: float) -> Point2:
    # bilinear map using polygon order p00, p10, p11, p01
    p00, p10, p11, p01 = face_poly
    top = lerp2(p00, p10, u)
    bottom = lerp2(p01, p11, u)
    return lerp2(top, bottom, v)


def draw_rosette(canvas: tk.Canvas, center: Point2, radius: float) -> None:
    cx, cy = center
    canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, width=1)
    inner = radius * 0.35
    canvas.create_oval(cx - inner, cy - inner, cx + inner, cy + inner, width=1)
    for k in range(8):
        ang = 2 * math.pi * k / 8.0
        x = cx + math.cos(ang) * radius
        y = cy + math.sin(ang) * radius
        canvas.create_line(cx, cy, x, y, width=1)


def draw_face_overlay(
    canvas: tk.Canvas,
    face_name: str,
    face_poly: List[Point2],
    face_data: dict,
) -> None:
    role = face_data.get("role", face_name)
    weight = face_data.get("weight", 0.0)
    anchors_uv = face_data.get("anchors", [])
    edges = face_data.get("edges", [])
    center_rosette = face_data.get("center_rosette", False)

    # label
    cx, cy = polygon_center(face_poly)
    canvas.create_text(cx, cy + 44, text=f"{face_name}: {role}", font=("Helvetica", 10))
    canvas.create_text(cx, cy + 60, text=f"w={weight:.2f}", font=("Helvetica", 9))

    # rosette
    if center_rosette:
        draw_rosette(canvas, (cx, cy), 18)

    # anchors
    anchor_pts: List[Point2] = []
    for u, v in anchors_uv:
        pt = face_uv_to_canvas(face_poly, float(u), float(v))
        anchor_pts.append(pt)
        r = 2.5 + 3.5 * float(weight)
        canvas.create_oval(pt[0]-r, pt[1]-r, pt[0]+r, pt[1]+r, fill="black", outline="black")

    # edges
    for i, j in edges:
        if 0 <= i < len(anchor_pts) and 0 <= j < len(anchor_pts):
            a = anchor_pts[i]
            b = anchor_pts[j]
            canvas.create_line(a[0], a[1], b[0], b[1], width=1)

    # light cross braces from corners to center for visible structure
    for corner in face_poly:
        canvas.create_line(corner[0], corner[1], cx, cy, width=1)


def main() -> None:
    kernel = load_kernel("specs/g60_cube_kernel_v1.json")
    view_data = kernel["view"]
    view = ViewSpec(
        yaw_deg=float(view_data["yaw_deg"]),
        pitch_deg=float(view_data["pitch_deg"]),
        distance=float(view_data["distance"]),
        cube_size_px=int(view_data["cube_size_px"]),
    )

    root = tk.Tk()
    root.title("G60 Cube Kernel Hello World")
    width, height = 1000, 760
    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack(fill="both", expand=True)

    verts = cube_vertices()
    faces = cube_faces()

    face_records = []
    for face_name, vertex_names in faces.items():
        pts3 = [verts[name] for name in vertex_names]
        pts2 = [project_point(p, width, height, view) for p in pts3]
        depth = polygon_depth(pts3, view)
        face_records.append((depth, face_name, pts2))

    # paint far to near
    face_records.sort(key=lambda item: item[0])

    visible_faces = {"front", "right", "top"}
    for _depth, face_name, pts2 in face_records:
        fill = ""
        outline_width = 2 if face_name in visible_faces else 1
        flat_pts = [coord for pt in pts2 for coord in pt]
        canvas.create_polygon(*flat_pts, fill=fill, outline="black", width=outline_width)

        face_data = kernel["faces"].get(face_name, {})
        if face_name in visible_faces:
            draw_face_overlay(canvas, face_name, pts2, face_data)

    title = kernel.get("name", "kernel")
    canvas.create_text(width / 2, 28, text=title, font=("Helvetica", 16, "bold"))
    canvas.create_text(
        width / 2,
        52,
        text="hello-world semantic cube: G15 -> G30 -> Faces(G60)",
        font=("Helvetica", 11),
    )

    root.mainloop()


if __name__ == "__main__":
    main()
