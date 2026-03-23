from __future__ import annotations

import math
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None
    ImageDraw = None


OUT_DIR = Path("specs/paper/g60")
SVG_PATH = OUT_DIR / "g900_symbolic_prism.svg"
PNG_PATH = OUT_DIR / "g900_symbolic_prism.png"


def triangle_points(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    pts = []
    for k in range(3):
        ang = -math.pi / 2 + k * 2 * math.pi / 3
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def line_svg(x1: float, y1: float, x2: float, y2: float, stroke: str = "#222", width: int = 2) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width}" />'
    )


def circle_svg(x: float, y: float, r: float = 6, fill: str = "#fff", stroke: str = "#222") -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2" />'


def text_svg(x: float, y: float, s: str, size: int = 16, anchor: str = "middle", weight: str = "normal") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'
    )


def build_svg(width: int, height: int) -> str:
    top = triangle_points(300, 220, 90)
    bot = triangle_points(300, 430, 90)
    tgt = triangle_points(760, 320, 110)

    labels_top = ["top_a", "top_b", "top_c"]
    labels_bot = ["bottom_a", "bottom_b", "bottom_c"]

    triangle_vertex_targets = {
        "top_a": "A",
        "top_b": "B",
        "top_c": "C",
        "bottom_a": "A",
        "bottom_b": "B",
        "bottom_c": "C",
    }

    svg_parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white" />',
        text_svg(500, 40, "G900 Symbolic Prism -> Triangle Collapse", size=28, weight="bold"),
        text_svg(300, 90, "Shared symbolic prism carrier", size=20, weight="bold"),
        text_svg(760, 90, "Weighted triangle target", size=20, weight="bold"),
    ]

    for i in range(3):
        x1, y1 = top[i]
        x2, y2 = top[(i + 1) % 3]
        svg_parts.append(line_svg(x1, y1, x2, y2))
    for i in range(3):
        x1, y1 = bot[i]
        x2, y2 = bot[(i + 1) % 3]
        svg_parts.append(line_svg(x1, y1, x2, y2))
    for i in range(3):
        x1, y1 = top[i]
        x2, y2 = bot[i]
        svg_parts.append(line_svg(x1, y1, x2, y2))

    for (x, y), label in zip(top, labels_top):
        svg_parts.append(circle_svg(x, y))
        svg_parts.append(text_svg(x, y - 14, label, size=14))
    for (x, y), label in zip(bot, labels_bot):
        svg_parts.append(circle_svg(x, y))
        svg_parts.append(text_svg(x, y + 24, label, size=14))

    numeric_labels = [
        ((top[0][0] + top[1][0]) / 2, (top[0][1] + top[1][1]) / 2 - 10, "140"),
        ((top[1][0] + top[2][0]) / 2 + 18, (top[1][1] + top[2][1]) / 2 + 2, "140"),
        ((top[2][0] + top[0][0]) / 2 - 18, (top[2][1] + top[0][1]) / 2 + 2, "140"),
        ((bot[0][0] + bot[1][0]) / 2, (bot[0][1] + bot[1][1]) / 2 - 10, "150"),
        ((bot[1][0] + bot[2][0]) / 2 + 18, (bot[1][1] + bot[2][1]) / 2 + 2, "150"),
        ((bot[2][0] + bot[0][0]) / 2 - 18, (bot[2][1] + bot[0][1]) / 2 + 2, "150"),
        ((top[0][0] + bot[0][0]) / 2 - 18, (top[0][1] + bot[0][1]) / 2, "145"),
        ((top[1][0] + bot[1][0]) / 2 + 18, (top[1][1] + bot[1][1]) / 2, "145"),
        ((top[2][0] + bot[2][0]) / 2 - 18, (top[2][1] + bot[2][1]) / 2, "145"),
    ]
    for x, y, s in numeric_labels:
        svg_parts.append(text_svg(x, y, s, size=16, weight="bold"))

    for i in range(3):
        x1, y1 = tgt[i]
        x2, y2 = tgt[(i + 1) % 3]
        svg_parts.append(line_svg(x1, y1, x2, y2))
    for (x, y), label in zip(tgt, ["A", "B", "C"]):
        svg_parts.append(circle_svg(x, y))
        svg_parts.append(text_svg(x, y - 14, label, size=18, weight="bold"))

    tgt_edge_labels = [
        ((tgt[0][0] + tgt[1][0]) / 2, (tgt[0][1] + tgt[1][1]) / 2 - 10, "AB"),
        ((tgt[1][0] + tgt[2][0]) / 2 + 20, (tgt[1][1] + tgt[2][1]) / 2 + 6, "BC"),
        ((tgt[2][0] + tgt[0][0]) / 2 - 20, (tgt[2][1] + tgt[0][1]) / 2 + 6, "CA"),
    ]
    for x, y, s in tgt_edge_labels:
        svg_parts.append(text_svg(x, y, s, size=14))

    svg_parts.append(text_svg(760, 515, "triangle_face", size=14))

    arrow_targets = {
        "top_a": tgt[0],
        "top_b": tgt[1],
        "top_c": tgt[2],
        "bottom_a": tgt[0],
        "bottom_b": tgt[1],
        "bottom_c": tgt[2],
    }
    for (x, y), label in list(zip(top, labels_top)) + list(zip(bot, labels_bot)):
        tx, ty = arrow_targets[label]
        svg_parts.append(
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" '
            f'stroke="#666" stroke-width="1.5" stroke-dasharray="6,6" />'
        )

    legend_x = 560
    legend_y = 560
    legend = [
        "Extracted prism law:",
        "top face = 140",
        "vertical = 145",
        "bottom face = 150",
        "",
        "offset form around center 145:",
        "top = -5",
        "vertical = 0",
        "bottom = +5",
    ]
    for i, s in enumerate(legend):
        svg_parts.append(
            text_svg(
                legend_x,
                legend_y + i * 22,
                s,
                size=15 if i not in (0, 5) else 16,
                anchor="start",
                weight="bold" if i in (0, 5) else "normal",
            )
        )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def build_png(width: int, height: int) -> bool:
    if Image is None or ImageDraw is None:
        return False

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    top = triangle_points(300, 220, 90)
    bot = triangle_points(300, 430, 90)
    tgt = triangle_points(760, 320, 110)

    labels_top = ["top_a", "top_b", "top_c"]
    labels_bot = ["bottom_a", "bottom_b", "bottom_c"]

    def draw_poly_edges(pts):
        for i in range(3):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % 3]
            draw.line((x1, y1, x2, y2), fill="black", width=2)

    def draw_nodes(pts, labels, bottom=False):
        for (x, y), label in zip(pts, labels):
            draw.ellipse((x - 6, y - 6, x + 6, y + 6), outline="black", fill="white", width=2)
            ty = y + 12 if bottom else y - 22
            draw.text((x - 22, ty), label, fill="black")

    draw.text((240, 20), "G900 Symbolic Prism -> Triangle Collapse", fill="black")
    draw.text((215, 80), "Shared symbolic prism carrier", fill="black")
    draw.text((700, 80), "Weighted triangle target", fill="black")

    draw_poly_edges(top)
    draw_poly_edges(bot)
    for i in range(3):
        draw.line((top[i][0], top[i][1], bot[i][0], bot[i][1]), fill="black", width=2)

    draw_nodes(top, labels_top, bottom=False)
    draw_nodes(bot, labels_bot, bottom=True)

    numeric_labels = [
        ((top[0][0] + top[1][0]) / 2, (top[0][1] + top[1][1]) / 2 - 10, "140"),
        ((top[1][0] + top[2][0]) / 2 + 18, (top[1][1] + top[2][1]) / 2 + 2, "140"),
        ((top[2][0] + top[0][0]) / 2 - 18, (top[2][1] + top[0][1]) / 2 + 2, "140"),
        ((bot[0][0] + bot[1][0]) / 2, (bot[0][1] + bot[1][1]) / 2 - 10, "150"),
        ((bot[1][0] + bot[2][0]) / 2 + 18, (bot[1][1] + bot[2][1]) / 2 + 2, "150"),
        ((bot[2][0] + bot[0][0]) / 2 - 18, (bot[2][1] + bot[0][1]) / 2 + 2, "150"),
        ((top[0][0] + bot[0][0]) / 2 - 18, (top[0][1] + bot[0][1]) / 2, "145"),
        ((top[1][0] + bot[1][0]) / 2 + 18, (top[1][1] + bot[1][1]) / 2, "145"),
        ((top[2][0] + bot[2][0]) / 2 - 18, (top[2][1] + bot[2][1]) / 2, "145"),
    ]
    for x, y, s in numeric_labels:
        draw.text((x - 10, y - 8), s, fill="black")

    draw_poly_edges(tgt)
    for (x, y), label in zip(tgt, ["A", "B", "C"]):
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), outline="black", fill="white", width=2)
        draw.text((x - 6, y - 24), label, fill="black")

    for (x, y), label in list(zip(top, labels_top)) + list(zip(bot, labels_bot)):
        tx, ty = {"top_a": tgt[0], "top_b": tgt[1], "top_c": tgt[2],
                  "bottom_a": tgt[0], "bottom_b": tgt[1], "bottom_c": tgt[2]}[label]
        draw.line((x, y, tx, ty), fill="gray", width=1)

    legend = [
        "Extracted prism law:",
        "top face = 140",
        "vertical = 145",
        "bottom face = 150",
        "offsets around 145: -5, 0, +5",
    ]
    for i, s in enumerate(legend):
        draw.text((560, 560 + i * 22), s, fill="black")

    img.save(PNG_PATH)
    return True


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    width = 1000
    height = 760

    svg = build_svg(width, height)
    SVG_PATH.write_text(svg, encoding="utf-8")
    print(f"wrote {SVG_PATH}")

    png_ok = build_png(width, height)
    if png_ok:
        print(f"wrote {PNG_PATH}")
    else:
        print("png skipped: Pillow not installed")


if __name__ == "__main__":
    main()
