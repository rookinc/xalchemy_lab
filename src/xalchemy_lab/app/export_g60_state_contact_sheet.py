from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path
from typing import Iterable


STATE_ORDER = ["000", "001", "010", "011", "100", "101", "110", "111"]


def png_path(state: str) -> Path:
    return Path("renders/state_cube_gallery_v1") / f"{state}.png"


def svg_path(state: str) -> Path:
    return Path("renders/state_cube_gallery_v1") / f"{state}.svg"


def detect_rasterizer() -> bool:
    try:
        import cairosvg  # type: ignore
        return True
    except Exception:
        pass
    return any(shutil.which(x) for x in ["rsvg-convert", "magick", "convert", "inkscape"])


def run_cmd(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def svg_to_png(svg: Path, png: Path, width: int, height: int) -> bool:
    try:
        import cairosvg  # type: ignore
        cairosvg.svg2png(
            url=str(svg),
            write_to=str(png),
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
            "-o", str(png),
            str(svg),
        ])

    if shutil.which("magick"):
        return run_cmd([
            "magick",
            "-background", "white",
            "-density", "200",
            str(svg),
            str(png),
        ])

    if shutil.which("convert"):
        return run_cmd([
            "convert",
            "-background", "white",
            "-density", "200",
            str(svg),
            str(png),
        ])

    if shutil.which("inkscape"):
        return run_cmd([
            "inkscape",
            str(svg),
            "--export-type=png",
            f"--export-filename={png}",
            f"--export-width={width}",
            f"--export-height={height}",
        ])

    return False


def ensure_pngs(states: Iterable[str]) -> None:
    for state in states:
        p = png_path(state)
        if p.exists():
            continue
        s = svg_path(state)
        if not s.exists():
            raise FileNotFoundError(f"missing both {p} and {s}")
        ok = svg_to_png(s, p, 1200, 900)
        if not ok:
            raise RuntimeError(f"could not rasterize {s} to {p}")


def main() -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        raise SystemExit("Pillow is required. Install with: pip install pillow")

    outdir = Path("renders/state_cube_gallery_v1")
    outdir.mkdir(parents=True, exist_ok=True)

    ensure_pngs(STATE_ORDER)

    tile_w = 1200
    tile_h = 900
    scale = 0.28
    pad = 28
    label_h = 58
    cols = 4
    rows = 2

    thumb_w = int(tile_w * scale)
    thumb_h = int(tile_h * scale)

    sheet_w = pad + cols * (thumb_w + pad)
    sheet_h = 120 + rows * (label_h + thumb_h + pad) + pad

    sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
    draw = ImageDraw.Draw(sheet)

    try:
        title_font = ImageFont.truetype("DejaVuSans.ttf", 28)
        label_font = ImageFont.truetype("DejaVuSans.ttf", 22)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 16)
    except Exception:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    title = "G60 state cube contact sheet"
    subtitle = "top row: A=0 chart   |   bottom row: A=1 chart"
    draw.text((sheet_w // 2, 26), title, fill="black", font=title_font, anchor="mm")
    draw.text((sheet_w // 2, 62), subtitle, fill="black", font=small_font, anchor="mm")

    for idx, state in enumerate(STATE_ORDER):
        row = idx // cols
        col = idx % cols

        x = pad + col * (thumb_w + pad)
        y = 96 + row * (label_h + thumb_h + pad)

        img = Image.open(png_path(state)).convert("RGB")
        thumb = img.resize((thumb_w, thumb_h), Image.LANCZOS)

        draw.rectangle(
            [x - 1, y - 1, x + thumb_w + 1, y + label_h + thumb_h + 1],
            outline="black",
            width=1,
        )
        draw.text((x + thumb_w // 2, y + 18), state, fill="black", font=label_font, anchor="mm")
        draw.text(
            (x + thumb_w // 2, y + 42),
            f"A={state[0]}  sigma={state[1]}  tau={state[2]}",
            fill="black",
            font=small_font,
            anchor="mm",
        )
        sheet.paste(thumb, (x, y + label_h))

    png_out = outdir / "contact_sheet_v1.png"
    sheet.save(png_out)
    print(f"wrote {png_out}")


if __name__ == "__main__":
    main()
