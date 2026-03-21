from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

Point2 = Tuple[float, float]
Triangle = Tuple[Point2, Point2, Point2]


TRACE_KEYS = {
    "front": ("A", "O", "O", "O"),
    "top": ("A", "E1", "E1", "E1"),
    "right": ("A", "E2", "E2", "E2"),
    "left": ("D", "E1", "E1", "E2"),
    "bottom": ("D", "E1", "O", "M+"),
    "back": ("E1", "E1", "E1", "O"),
}


def load_kernel(path: str) -> dict:
    return json.loads(Path(path).read_text())


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


def net_face_origins(face_size: float, gap: float) -> Dict[str, Point2]:
    s = face_size
    g = gap
    # classic cross net
    return {
        "top": (s + g, 0),
        "left": (0, s + g),
        "front": (s + g, s + g),
        "right": (2 * (s + g), s + g),
        "back": (3 * (s + g), s + g),
        "bottom": (s + g, 2 * (s + g)),
    }


def square_triangles(origin: Point2, size: float, n: int) -> List[Triangle]:
    ox, oy = origin
    step = size / n
    tris: List[Triangle] = []
    for r in range(n):
        for c in range(n):
            x0 = ox + c * step
            y0 = oy + r * step
            x1 = x0 + step
            y1 = y0 + step
            # split each square into two triangles
            tris.append(((x0, y0), (x1, y0), (x1, y1)))
            tris.append(((x0, y0), (x1, y1), (x0, y1)))
    return tris


def triangle_centroid(tri: Triangle) -> Point2:
    return (
        (tri[0][0] + tri[1][0] + tri[2][0]) / 3.0,
        (tri[0][1] + tri[1][1] + tri[2][1]) / 3.0,
    )


def role_tag(face: str) -> str:
    return {
        "front": "H/O",
        "top": "E1",
        "right": "E2",
        "left": "Do",
        "bottom": "De",
        "back": "C",
    }[face]


def face_triangle_fill(face: str, idx: int, traces: Dict[Tuple[str, ...], int]) -> str:
    bit = traces[TRACE_KEYS[face]]

    # more visually distinct than the cube view:
    # active faces get alternating black bands, inactive mostly white.
    if face == "front":
        return "black" if bit == 1 and idx % 2 == 0 else "white"
    if face == "top":
        return "black" if bit == 1 and idx % 3 != 1 else "white"
    if face == "right":
        return "black" if bit == 1 and idx % 3 == 0 else "white"
    if face == "left":
        return "black" if idx % 4 == 0 else "white"
    if face == "bottom":
        return "black" if bit == 1 and idx % 4 != 0 else "white"
    if face == "back":
        return "black" if bit == 1 and idx % 2 == 1 else "white"
    return "white"


def svg_polygon(points: List[Point2], fill: str = "white", stroke: str = "black", stroke_width: float = 1.0) -> str:
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'


def svg_text(x: float, y: float, text: str, size: int = 14, weight: str = "normal", anchor: str = "middle") -> str:
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Helvetica,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="black">{safe}</text>'
    )


def export_png(svg_path: Path, png_path: Path, width: int, height: int) -> bool:
    try:
        import cairosvg  # type: ignore
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=width, output_height=height)
        return True
    except Exception:
        pass

    def run(cmd: List[str]) -> bool:
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False

    if shutil.which("rsvg-convert"):
        return run(["rsvg-convert", "-w", str(width), "-h", str(height), "-o", str(png_path), str(svg_path)])
    if shutil.which("magick"):
        return run(["magick", "-background", "white", "-density", "200", str(svg_path), str(png_path)])
    if shutil.which("convert"):
        return run(["convert", "-background", "white", "-density", "200", str(svg_path), str(png_path)])
    if shutil.which("inkscape"):
        return run([
            "inkscape", str(svg_path),
            "--export-type=png",
            f"--export-filename={png_path}",
            f"--export-width={width}",
            f"--export-height={height}",
        ])
    return False


def render_state(state_name: str, state: dict, output_svg: Path) -> None:
    A = int(state["A"])
    sigma = int(state["sigma"])
    tau = int(state["tau"])
    traces = trace_map(A, sigma, tau)

    face_size = 180.0
    gap = 18.0
    n = 4
    origins = net_face_origins(face_size, gap)

    width = int(4 * (face_size + gap) + gap)
    height = int(3 * (face_size + gap) + 120)

    parts: List[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="white"/>')
    parts.append(svg_text(width / 2, 28, f"state sheet {state_name}", size=22, weight="bold"))
    parts.append(svg_text(width / 2, 52, f"(A,sigma,tau)=({A},{sigma},{tau})", size=14))

    for face, origin in origins.items():
        tris = square_triangles((origin[0], origin[1] + 20), face_size, n)
        for idx, tri in enumerate(tris):
            fill = face_triangle_fill(face, idx, traces)
            parts.append(svg_polygon(list(tri), fill=fill, stroke="black", stroke_width=0.8))

        ox, oy = origin
        oy += 20
        square = [(ox, oy), (ox + face_size, oy), (ox + face_size, oy + face_size), (ox, oy + face_size)]
        parts.append(svg_polygon(square, fill="none", stroke="black", stroke_width=2.0))
        parts.append(svg_text(ox + face_size / 2, oy - 6, role_tag(face), size=13, weight="bold"))

        bit = traces[TRACE_KEYS[face]]
        parts.append(svg_text(ox + face_size / 2, oy + face_size + 16, f"{''.join(TRACE_KEYS[face])}={'1' if bit else '0'}", size=10))

    parts.append("</svg>")
    output_svg.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    kernel = load_kernel("specs/app/g60_cube_state_kernel_v1.json")
    outdir = Path("renders/state_sheet_gallery_v1")
    outdir.mkdir(parents=True, exist_ok=True)

    png_any = False
    for state_name, state in kernel["states"].items():
        svg_path = outdir / f"{state_name}.svg"
        png_path = outdir / f"{state_name}.png"
        render_state(state_name, state, svg_path)
        print(f"wrote {svg_path}")
        if export_png(svg_path, png_path, 900, 720):
            print(f"wrote {png_path}")
            png_any = True
        else:
            print(f"skipped png for {state_name}")

    if not png_any:
        print("tip: install cairosvg, librsvg, imagemagick, or inkscape for PNG export")


if __name__ == "__main__":
    main()
