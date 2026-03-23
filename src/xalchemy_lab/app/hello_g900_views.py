from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


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


def bary_to_xy(i: int, j: int, scale: float) -> Tuple[float, float]:
    x = scale * (i + 0.5 * j)
    y = scale * (math.sqrt(3) / 2.0) * j
    return x, y


def cell_polygon_xy(cell: TriCell, scale: float) -> List[Tuple[float, float]]:
    pts = [bary_to_xy(i, j, scale) for (i, j) in cell.verts]
    return [(x, -y) for x, y in pts]


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
    base = "#1f2937"
    top = "#f2cc5c"
    t = layer / max_layer
    return blend(base, top, t)


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
    base = macro_color(macro)
    mix = "#f2cc5c" if bit == 1 else "#0f1115"
    return blend(base, mix, 0.42)


def draw_view(
    n: int,
    mode: str,
    out_stem: str,
    title: str,
    subtitle: str,
) -> None:
    cells = generate_order_n_triangular_cells(n)
    max_layer = max(cell_layer(c, n) for c in cells)

    scale = 1.0
    fig, ax = plt.subplots(figsize=(14, 9), dpi=160)
    fig.patch.set_facecolor("#050505")
    ax.set_facecolor("#050505")

    for cell in cells:
        pts = cell_polygon_xy(cell, scale)
        layer = cell_layer(cell, n)
        macro = macro_sector(cell)
        bit = live_bit(cell)

        if mode == "layer":
            face = layer_color(layer, max_layer)
        elif mode == "macro":
            face = macro_color(macro)
        elif mode == "bit":
            face = bit_color(bit)
        elif mode == "macrobit":
            face = macro_bit_color(macro, bit)
        else:
            raise ValueError(mode)

        poly = Polygon(
            pts,
            closed=True,
            facecolor=face,
            edgecolor="#111111",
            linewidth=0.25,
        )
        ax.add_patch(poly)

    # outer frame triangle
    A = bary_to_xy(0, 0, scale)
    B = bary_to_xy(n, 0, scale)
    C = bary_to_xy(0, n, scale)
    A = (A[0], -A[1])
    B = (B[0], -B[1])
    C = (C[0], -C[1])
    ax.add_patch(
        Polygon([A, B, C], closed=True, fill=False, edgecolor="#eaeaea", linewidth=1.8)
    )

    xs = [A[0], B[0], C[0]]
    ys = [A[1], B[1], C[1]]
    pad_x = 2.0
    pad_y = 2.0
    ax.set_xlim(min(xs) - pad_x, max(xs) + pad_x * 12)
    ax.set_ylim(min(ys) - pad_y * 2, max(ys) + pad_y * 5)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.text(0.03, 0.95, title, color="#eaeaea", fontsize=20, fontweight="bold", ha="left")
    fig.text(0.03, 0.915, subtitle, color="#bfc6cf", fontsize=11, ha="left")

    # legend
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

    lx, ly = 0.80, 0.80
    fig.text(lx, ly + 0.07, "Legend", color="#eaeaea", fontsize=12, fontweight="bold", ha="left")
    for idx, (label, color) in enumerate(legend):
        y = ly + 0.045 - idx * 0.028
        fig.text(lx, y, "■", color=color, fontsize=12, ha="left", va="center")
        fig.text(lx + 0.02, y, label, color="#d8dde7", fontsize=11, ha="left", va="center")

    out_dir = Path("renders")
    out_dir.mkdir(exist_ok=True)

    svg_path = out_dir / f"{out_stem}.svg"
    png_path = out_dir / f"{out_stem}.png"

    fig.savefig(svg_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    fig.savefig(png_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)

    print(f"wrote {svg_path}")
    print(f"wrote {png_path}")


def main() -> None:
    n = 30
    draw_view(
        n=n,
        mode="layer",
        out_stem="g900_layer_only",
        title="G900 layer-only probe",
        subtitle="order-30 triangular subdivision colored by inward layer depth",
    )
    draw_view(
        n=n,
        mode="macro",
        out_stem="g900_macro_only",
        title="G900 macro-only probe",
        subtitle="order-30 triangular subdivision colored by 3 macro sectors",
    )
    draw_view(
        n=n,
        mode="bit",
        out_stem="g900_bit_only",
        title="G900 bit-only probe",
        subtitle="order-30 triangular subdivision colored by 2 live-bit classes",
    )
    draw_view(
        n=n,
        mode="macrobit",
        out_stem="g900_layer_macrobit_probe",
        title="G900 macro/bit probe",
        subtitle="order-30 triangular subdivision colored by 3 macro sectors and 2 live-bit classes",
    )


if __name__ == "__main__":
    main()
