from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
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


def layer_color(layer: int, max_layer: int) -> str:
    return blend("#1f2937", "#f2cc5c", layer / max_layer)


def macro_color(macro: int) -> str:
    return {
        0: "#58b8ff",
        1: "#84c98a",
        2: "#e8a0a0",
    }[macro]


def bit_color(bit: int) -> str:
    return {
        0: "#334155",
        1: "#f2cc5c",
    }[bit]


def macro_bit_color(macro: int, bit: int) -> str:
    return blend(macro_color(macro), "#f2cc5c" if bit == 1 else "#0f1115", 0.42)


def color_for(mode: str, layer: int, macro: int, bit: int, max_layer: int) -> str:
    if mode == "layer":
        return layer_color(layer, max_layer)
    if mode == "macro":
        return macro_color(macro)
    if mode == "bit":
        return bit_color(bit)
    if mode == "macrobit":
        return macro_bit_color(macro, bit)
    raise ValueError(mode)


def build_svg(n: int, mode: str, title: str, subtitle: str) -> str:
    cells = generate_order_n_triangular_cells(n)
    max_layer = max(cell_layer(c, n) for c in cells)

    scale = 24.0
    pad = 80.0
    width = scale * n + scale * n * 0.7 + 2 * pad
    height = scale * n * 0.95 + 2 * pad

    ox = pad
    oy = height - pad

    parts: List[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height:.1f}" '
        f'width="{width:.1f}" height="{height:.1f}">'
    )
    parts.append('<rect width="100%" height="100%" fill="#050505"/>')

    for cell in cells:
        layer = cell_layer(cell, n)
        macro = macro_sector(cell)
        bit = live_bit(cell)
        pts = cell_polygon_xy(cell, scale, ox, oy)
        points_attr = " ".join(f"{x:.3f},{y:.3f}" for x, y in pts)
        fill = color_for(mode, layer, macro, bit, max_layer)
        parts.append(
            f'<polygon points="{points_attr}" fill="{fill}" stroke="#111111" stroke-width="0.45" />'
        )

    A = bary_to_xy(0, 0, scale, ox, oy)
    B = bary_to_xy(n, 0, scale, ox, oy)
    C = bary_to_xy(0, n, scale, ox, oy)
    abc = " ".join(f"{x:.3f},{y:.3f}" for x, y in [A, B, C])
    parts.append(f'<polygon points="{abc}" fill="none" stroke="#eaeaea" stroke-width="2"/>')

    parts.append(
        '<text x="36" y="42" fill="#eaeaea" font-size="28" font-family="Arial, Helvetica, sans-serif" font-weight="700">'
        f'{title}</text>'
    )
    parts.append(
        '<text x="36" y="68" fill="#bfc6cf" font-size="16" font-family="Arial, Helvetica, sans-serif">'
        f'{subtitle}</text>'
    )

    lx = width - 280
    ly = 90
    parts.append(f'<rect x="{lx}" y="{ly}" width="220" height="150" fill="#0d0d0d" stroke="#333"/>')
    parts.append(
        f'<text x="{lx+14}" y="{ly+24}" fill="#eaeaea" font-size="16" font-family="Arial" font-weight="700">Legend</text>'
    )

    if mode == "layer":
        legend = [("outer", layer_color(0, max_layer)), ("inner", layer_color(max_layer, max_layer))]
    elif mode == "macro":
        legend = [("macro 0", macro_color(0)), ("macro 1", macro_color(1)), ("macro 2", macro_color(2))]
    elif mode == "bit":
        legend = [("bit 0", bit_color(0)), ("bit 1", bit_color(1))]
    else:
        legend = [
            ("macro 0 / bit blend", macro_bit_color(0, 1)),
            ("macro 1 / bit blend", macro_bit_color(1, 1)),
            ("macro 2 / bit blend", macro_bit_color(2, 1)),
        ]

    for idx, (label, color) in enumerate(legend):
        y = ly + 48 + idx * 22
        parts.append(f'<rect x="{lx+14}" y="{y-11}" width="12" height="12" fill="{color}" stroke="#111"/>')
        parts.append(f'<text x="{lx+34}" y="{y}" fill="#d8dde7" font-size="14" font-family="Arial">{label}</text>')

    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    out_dir = Path("renders")
    out_dir.mkdir(exist_ok=True)

    specs = [
        ("layer", "g900_layer_only", "G900 layer-only probe", "order-30 triangular subdivision colored by inward layer depth"),
        ("macro", "g900_macro_only", "G900 macro-only probe", "order-30 triangular subdivision colored by 3 macro sectors"),
        ("bit", "g900_bit_only", "G900 bit-only probe", "order-30 triangular subdivision colored by 2 live-bit classes"),
        ("macrobit", "g900_layer_macrobit_probe", "G900 macro/bit probe", "order-30 triangular subdivision colored by 3 macro sectors and 2 live-bit classes"),
    ]

    for mode, stem, title, subtitle in specs:
        svg = build_svg(30, mode, title, subtitle)
        path = out_dir / f"{stem}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
