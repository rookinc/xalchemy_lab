from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import math


Point = Tuple[int, int]


@dataclass(frozen=True)
class TriCell:
    cell_id: int
    orient: str
    verts: Tuple[Point, Point, Point]


def generate_order_n_triangular_cells(n: int) -> List[TriCell]:
    cells: List[TriCell] = []
    cell_id = 0

    for i in range(n):
        for j in range(n - i):
            up = ((i, j), (i + 1, j), (i, j + 1))
            cells.append(TriCell(cell_id, "up", up))
            cell_id += 1

    for i in range(n - 1):
        for j in range(n - 1 - i):
            down = ((i + 1, j), (i + 1, j + 1), (i, j + 1))
            cells.append(TriCell(cell_id, "down", down))
            cell_id += 1

    return cells


def cell_layer(cell: TriCell, n: int) -> int:
    vals = []
    for i, j in cell.verts:
        k = n - i - j
        vals.append(min(i, j, k))
    return min(vals)


def centroid_times_3(cell: TriCell) -> Tuple[int, int]:
    xs = sum(v[0] for v in cell.verts)
    ys = sum(v[1] for v in cell.verts)
    return xs, ys


def macro_sector(cell: TriCell) -> int:
    cx3, cy3 = centroid_times_3(cell)
    return ((cx3 + 2 * cy3) // 3) % 3


def live_bit(cell: TriCell) -> int:
    cx3, cy3 = centroid_times_3(cell)
    return (cx3 + 2 * cy3 + (0 if cell.orient == "up" else 1)) % 2


def bary_to_xy(i: int, j: int, scale: float, ox: float, oy: float) -> Tuple[float, float]:
    # Triangle lattice coordinates:
    # e1 = (1, 0)
    # e2 = (1/2, sqrt(3)/2)
    x = ox + scale * (i + 0.5 * j)
    y = oy - scale * (math.sqrt(3) / 2.0) * j
    return x, y


def cell_polygon_xy(cell: TriCell, scale: float, ox: float, oy: float) -> List[Tuple[float, float]]:
    return [bary_to_xy(i, j, scale, ox, oy) for (i, j) in cell.verts]


def rgb(hex_color: str) -> Tuple[int, int, int]:
    s = hex_color.lstrip("#")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def blend(c1: str, c2: str, t: float) -> str:
    r1, g1, b1 = rgb(c1)
    r2, g2, b2 = rgb(c2)
    r = round(r1 + (r2 - r1) * t)
    g = round(g1 + (g2 - g1) * t)
    b = round(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def color_for_cell(layer: int, macro: int, bit: int, max_layer: int) -> str:
    macro_base = {
        0: "#58b8ff",  # blue
        1: "#84c98a",  # green
        2: "#e8a0a0",  # red
    }[macro]
    light = "#f2cc5c" if bit == 1 else "#0f1115"
    t = 0.18 + 0.62 * (layer / max_layer)
    return blend(macro_base, light, t)


def build_svg(n: int = 30) -> str:
    cells = generate_order_n_triangular_cells(n)
    max_layer = max(cell_layer(c, n) for c in cells)

    scale = 24.0
    pad = 80.0
    width = scale * n + scale * n * 0.6 + 2 * pad
    height = scale * n * 0.95 + 2 * pad

    ox = pad
    oy = height - pad

    parts: List[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height:.1f}" '
        f'width="{width:.1f}" height="{height:.1f}">'
    )
    parts.append('<rect width="100%" height="100%" fill="#050505"/>')

    # cells
    for cell in cells:
        layer = cell_layer(cell, n)
        macro = macro_sector(cell)
        bit = live_bit(cell)
        pts = cell_polygon_xy(cell, scale, ox, oy)
        points_attr = " ".join(f"{x:.3f},{y:.3f}" for x, y in pts)
        fill = color_for_cell(layer, macro, bit, max_layer)
        parts.append(
            f'<polygon points="{points_attr}" fill="{fill}" stroke="#111111" stroke-width="0.45" />'
        )

    # outer frame triangle
    A = bary_to_xy(0, 0, scale, ox, oy)
    B = bary_to_xy(n, 0, scale, ox, oy)
    C = bary_to_xy(0, n, scale, ox, oy)
    abc = " ".join(f"{x:.3f},{y:.3f}" for x, y in [A, B, C])
    parts.append(f'<polygon points="{abc}" fill="none" stroke="#eaeaea" stroke-width="2"/>')

    # title
    parts.append(
        '<text x="36" y="42" fill="#eaeaea" font-size="28" font-family="Arial, Helvetica, sans-serif" '
        'font-weight="700">G900 layer / macro / bit probe</text>'
    )

    # subtitle
    parts.append(
        '<text x="36" y="68" fill="#bfc6cf" font-size="16" font-family="Arial, Helvetica, sans-serif">'
        'order-30 triangular subdivision colored by 10-layer depth, 3 macro sectors, and 2 live-bit classes'
        '</text>'
    )

    # legend
    lx = width - 260
    ly = 90
    parts.append(f'<rect x="{lx}" y="{ly}" width="200" height="138" fill="#0d0d0d" stroke="#333"/>')
    parts.append(
        f'<text x="{lx+14}" y="{ly+24}" fill="#eaeaea" font-size="16" font-family="Arial" font-weight="700">Legend</text>'
    )
    legend_rows = [
        ("macro 0", "#58b8ff"),
        ("macro 1", "#84c98a"),
        ("macro 2", "#e8a0a0"),
    ]
    for idx, (label, color) in enumerate(legend_rows):
        y = ly + 48 + idx * 22
        parts.append(f'<rect x="{lx+14}" y="{y-11}" width="12" height="12" fill="{color}" stroke="#111"/>')
        parts.append(f'<text x="{lx+34}" y="{y}" fill="#d8dde7" font-size="14" font-family="Arial">{label}</text>')

    parts.append(
        f'<text x="{lx+14}" y="{ly+118}" fill="#d8dde7" font-size="14" font-family="Arial">bit 0 = darker</text>'
    )
    parts.append(
        f'<text x="{lx+14}" y="{ly+136}" fill="#d8dde7" font-size="14" font-family="Arial">bit 1 = lighter/gold blend</text>'
    )

    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    out_dir = Path("renders")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "g900_layer_macrobit_probe.svg"
    svg = build_svg(n=30)
    out_path.write_text(svg, encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
